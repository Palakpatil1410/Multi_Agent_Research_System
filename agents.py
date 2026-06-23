import time
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Model Setup — Groq free tier
# Get your free API key → https://console.groq.com
# Add to .env file: GROQ_API_KEY=your_key_here
# ─────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)


# ─────────────────────────────────────────────
# Rate limit helper — waits between API calls
# ─────────────────────────────────────────────
def safe_invoke(chain_or_agent, inputs: dict, delay: float = 2.0):
    """Invoke a chain or agent with a small delay to avoid Groq rate limits."""
    time.sleep(delay)
    return chain_or_agent.invoke(inputs)


# ─────────────────────────────────────────────
# Agent 1 — Web Search Agent
# ─────────────────────────────────────────────
def build_search_agent():
    return create_react_agent(
        model=llm,
        tools=[web_search],
        prompt=(
            "You are a research assistant specialized in finding high-quality "
            "information on the web. Use the web_search tool ONCE to find relevant "
            "sources, facts, and data about the given topic. Return a list of "
            "useful URLs and brief summaries of what each page contains."
        ),
    )


# ─────────────────────────────────────────────
# Agent 2 — Scraper / Reader Agent
# ─────────────────────────────────────────────
def build_reader_agent():
    return create_react_agent(
        model=llm,
        tools=[scrape_url],
        prompt=(
            "You are a web content extractor. Pick ONLY the single most relevant "
            "URL from the search results and use the scrape_url tool ONCE to extract "
            "the most important information. Focus on facts, data, and key insights. "
            "Do NOT scrape more than one URL. Return well-organized notes."
        ),
    )


# ─────────────────────────────────────────────
# Chain 3 — Writer Chain
# ─────────────────────────────────────────────
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured, and "
        "insightful reports that are factual, professional, and easy to read.",
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual, and professional.""",
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# ─────────────────────────────────────────────
# Chain 4 — Critic Chain
# ─────────────────────────────────────────────
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. Be honest, "
        "specific, and fair in your evaluation.",
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...""",
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()


# ─────────────────────────────────────────────
# Chain 5 — Q&A Chain
# Answers user questions based on research context
# ─────────────────────────────────────────────
qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful research assistant. Answer the user's question "
        "based ONLY on the research report and context provided below. "
        "Be concise, clear, and accurate. "
        "If the answer is not found in the research, say so clearly.",
    ),
    (
        "human",
        """Research Report:
{report}

Research Context:
{research}

User Question:
{question}

Answer the question clearly and concisely based on the research above.""",
    ),
])

qa_chain = qa_prompt | llm | StrOutputParser()