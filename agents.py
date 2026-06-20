from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Model Setup
# Get your free API key → https://aistudio.google.com/app/apikey
# Add to .env file:  GOOGLE_API_KEY=your_key_here
# ─────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)


# ─────────────────────────────────────────────
# Agent 1 — Web Search Agent
# Searches the web for relevant URLs and summaries
# ─────────────────────────────────────────────
def build_search_agent():
    return create_react_agent(
        model=llm,
        tools=[web_search],
        prompt=(
            "You are a research assistant specialized in finding high-quality "
            "information on the web. Use the web_search tool to find relevant "
            "sources, facts, and data about the given topic. Return a list of "
            "useful URLs and brief summaries of what each page contains."
        ),
    )


# ─────────────────────────────────────────────
# Agent 2 — Scraper / Reader Agent
# Visits URLs and extracts detailed content
# ─────────────────────────────────────────────
def build_reader_agent():
    return create_react_agent(
        model=llm,
        tools=[scrape_url],
        prompt=(
            "You are a web content extractor. Given a list of URLs, use the "
            "scrape_url tool to visit each page and extract the most important "
            "and relevant information. Focus on facts, data, quotes, and key "
            "insights. Return well-organized notes from each source."
        ),
    )


# ─────────────────────────────────────────────
# Chain 3 — Writer Chain
# Turns raw research into a structured report
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
- Recommendations (if applicable)
- Limitations (if applicable)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual, and professional.""",
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# ─────────────────────────────────────────────
# Chain 4 — Critic Chain
# Reviews and scores the written report
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