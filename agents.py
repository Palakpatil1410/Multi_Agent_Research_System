import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url

load_dotenv()

# ── Load all keys from .env ───────────────────────────────────────────────────
# Supports GEMINI_KEY_1, GEMINI_KEY_2, GEMINI_KEY_3 ... or plain GOOGLE_API_KEY
def _load_keys():
    keys = []

    # Accept numbered keys: GEMINI_KEY_1, GEMINI_KEY_2, ...
    i = 1
    while True:
        k = os.getenv(f"GEMINI_KEY_{i}")
        if not k:
            break
        keys.append(k.strip())
        i += 1

    # Accept any of these common single-key names as fallback
    for name in ("GOOGLE_API_KEY", "GEMINI_API_KEY", "GOOGLE_GENAI_API_KEY"):
        val = os.getenv(name)
        if val and val.strip() not in keys:
            keys.append(val.strip())

    if not keys:
        raise ValueError(
            "No Gemini API key found in .env!\n"
            "Add one of these to your .env file:\n"
            "  GEMINI_KEY_1=AIza...\n"
            "  GOOGLE_API_KEY=AIza...\n"
            "  GEMINI_API_KEY=AIza..."
        )
    print(f"[KeyManager] Loaded {len(keys)} API key(s)")
    return keys

_keys = _load_keys()
_key_index = 0

def _get_llm():
    """Return LLM using the current active key."""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=_keys[_key_index],
    )

def _rotate_key():
    """Switch to the next key. Raises if all keys exhausted."""
    global _key_index
    _key_index += 1
    if _key_index >= len(_keys):
        _key_index = 0
        raise RuntimeError(
            f"All {len(_keys)} API key(s) have hit their daily quota.\n"
            "Please wait until midnight (PT) or add more keys to .env as GEMINI_KEY_2, GEMINI_KEY_3 ..."
        )
    print(f"[KeyRotation] Switched to key #{_key_index + 1} of {len(_keys)}")

def _is_quota_error(e):
    s = str(e)
    return "429" in s or "RESOURCE_EXHAUSTED" in s or "quota" in s.lower()

def _invoke_with_retry(fn, *args, max_attempts=None, **kwargs):
    """Call fn(*args, **kwargs), rotating keys on quota errors."""
    global _key_index
    max_attempts = max_attempts or len(_keys)
    last_err = None
    for attempt in range(max_attempts):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if _is_quota_error(e):
                last_err = e
                try:
                    _rotate_key()
                    # rebuild agents/chains use fresh llm after rotation
                except RuntimeError:
                    raise
            else:
                raise
    raise last_err

# ── Agent 1 — Search ──────────────────────────────────────────────────────────
def build_search_agent():
    llm = _get_llm()
    return create_react_agent(
        model=llm,
        tools=[web_search],
        prompt=(
            "You are a research search agent. "
            "When given a topic, call the web_search tool and return the FULL raw output exactly as received. "
            "Do NOT summarize, paraphrase, or rewrite anything. "
            "Your response MUST include every URL from the search results in this exact format: URL: https://... "
            "Never drop or hide any URLs."
        ),
    )

# ── Agent 2 — Reader ──────────────────────────────────────────────────────────
def build_reader_agent():
    llm = _get_llm()
    return create_react_agent(
        model=llm,
        tools=[scrape_url],
        prompt=(
            "You are a web scraping agent. "
            "You will receive text containing URLs in the format 'URL: https://...'. "
            "Extract ALL URLs from the input and call scrape_url on each one. "
            "Return the full scraped content from every URL. "
            "If a URL fails, note the error and continue to the next one. "
            "Never skip URLs."
        ),
    )

# ── Writer chain ──────────────────────────────────────────────────────────────
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that writes concise and informative summaries based on the information provided."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well explained points)
- Methodology (explain how you gathered and analyzed the information)
- Analysis
- Results (what does the information suggest about the topic?)
- Limitations 
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

# ── Critic chain ──────────────────────────────────────────────────────────────
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that critiques research reports."),
    ("human", """Critique the research report based on the information provided.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas of Improvement:
- ...
- ...

One line verdict: ..."""),
])

def _make_chains():
    llm = _get_llm()
    return (
        writer_prompt | llm | StrOutputParser(),
        critic_prompt | llm | StrOutputParser(),
    )

writer_chain, critic_chain = _make_chains()

# ── Public invoke helpers (with key rotation) ─────────────────────────────────
def invoke_search_agent(topic: str):
    global writer_chain, critic_chain
    for attempt in range(len(_keys)):
        try:
            agent = build_search_agent()
            return agent.invoke({"messages": [("user",
                f"Find recent, reliable and detailed information about: {topic}")]})
        except Exception as e:
            if _is_quota_error(e):
                _rotate_key()
                writer_chain, critic_chain = _make_chains()
            else:
                raise
    raise RuntimeError("All keys exhausted during search.")

def invoke_reader_agent(topic: str, search_results: str):
    for attempt in range(len(_keys)):
        try:
            agent = build_reader_agent()
            return agent.invoke({"messages": [("user",
                f"Here are search results about '{topic}'. "
                f"Extract every URL that appears in the format 'URL: https://...' and scrape each one.\n\n"
                f"Search Results:\n{search_results}")]})
        except Exception as e:
            if _is_quota_error(e):
                _rotate_key()
            else:
                raise
    raise RuntimeError("All keys exhausted during scraping.")

def invoke_writer(topic: str, research: str):
    global writer_chain, critic_chain
    for attempt in range(len(_keys)):
        try:
            return writer_chain.invoke({"topic": topic, "research": research})
        except Exception as e:
            if _is_quota_error(e):
                _rotate_key()
                writer_chain, critic_chain = _make_chains()
            else:
                raise
    raise RuntimeError("All keys exhausted during writing.")

def invoke_critic(report: str):
    global writer_chain, critic_chain
    for attempt in range(len(_keys)):
        try:
            return critic_chain.invoke({"report": report})
        except Exception as e:
            if _is_quota_error(e):
                _rotate_key()
                writer_chain, critic_chain = _make_chains()
            else:
                raise
    raise RuntimeError("All keys exhausted during critique.")