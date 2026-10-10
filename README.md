# 🔬 ResearchMind — Multi-Agent AI Research System

🌐 **Live Demo:** [ResearchMind](https://researchmind-ai-research-system.streamlit.app/)  
💻 **GitHub:** [Multi-Agent Research System](https://github.com/Palakpatil1410/Multi_Agent_Research_System)

## 🧠 What is ResearchMind?

ResearchMind is a multi-agent AI research system that turns a topic into a structured research report using web search, content extraction, AI writing, and critical review.

You enter a topic, and the system runs through these stages:

1. **Search Agent** — Searches the web for relevant and recent information.
2. **Reader Agent** — Extracts useful content from relevant webpages.
3. **Writer Chain** — Creates a structured research report.
4. **Critic Chain** — Reviews the report, scores it, and suggests improvements.
5. **Q&A Chain** — Answers follow-up questions based on the research context.

Reports can be downloaded in Markdown or Word (`.docx`) format.

## ✨ Features

- 🔍 Real-time web search using Tavily API
- 📄 Webpage content extraction using BeautifulSoup and Requests
- ✍️ Structured research reports with introduction, findings, conclusion, and sources
- 🧐 AI critic with a score, strengths, and improvement suggestions
- 💬 Follow-up Q&A based on the generated research
- ⬇️ Export reports as `.md` or `.docx`
- ⚡ Groq-powered language model
- 🎨 Custom dark-themed Streamlit interface

## 🗂️ Project Structure

```text
Multi_Agent_Research_System/
├── app.py              # Streamlit UI and research workflow
├── agents.py           # Agents, LLM chains, and safe_invoke
├── tools.py            # Web search and webpage scraping
├── pipeline.py         # Optional CLI runner, if included
├── requirements.txt    # Python dependencies
├── .env                # API keys; never commit this file
├── .gitignore
└── README.md
```

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — `openai/gpt-oss-20b` |
| Agent Framework | LangChain and LangGraph |
| Web Search | Tavily API |
| Web Scraping | BeautifulSoup4 and Requests |
| UI | Streamlit |
| Report Export | python-docx and Markdown |
| Q&A | LangChain |

## 🛠️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Palakpatil1410/Multi_Agent_Research_System.git
cd Multi_Agent_Research_System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get API keys from:

- **Groq:** https://console.groq.com/
- **Tavily:** https://app.tavily.com/

Never commit your real API keys to GitHub.

### 5. Run the application

```bash
python -m streamlit run app.py
```

If your repository includes `pipeline.py` and supports CLI execution, you can also run:

```bash
python pipeline.py
```

## 🌐 Deploy on Streamlit Community Cloud

1. Push your project to GitHub.
2. Open https://share.streamlit.io/
3. Connect your GitHub repository.
4. Select `app.py` as the main file.
5. Open the app's settings and configure the secrets:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
TAVILY_API_KEY = "your_tavily_api_key_here"
```

6. Deploy the application and check the deployment logs if an error occurs.

**Security:** Add `.env` to `.gitignore`. Do not put real API keys in your README or source code.

## 📦 Requirements

Install dependencies from the repository's `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 🤖 Agent Details

### 🔍 Agent 1 — Search Agent

Uses Tavily to find relevant web sources and return search information such as titles, URLs, and snippets.

### 📄 Agent 2 — Reader Agent

Extracts readable text from relevant webpages to provide additional context for the research.

### ✍️ Agent 3 — Writer Chain

Combines the available research context into a structured report with key findings, a conclusion, and sources.

### 🧐 Agent 4 — Critic Chain

Evaluates the generated report, provides a score, identifies strengths, and suggests areas for improvement.

### 💬 Q&A Chain

Answers follow-up questions using the research context available to the application.

## 🐛 Common Errors & Fixes

| Error | Possible cause | What to check |
|---|---|---|
| `404 model_not_found` | Unsupported, deprecated, or inaccessible model | Check the model ID configured in `agents.py` and any `GROQ_MODEL` secret. |
| `401 Unauthorized` | Missing or invalid API key | Check `GROQ_API_KEY` in your environment or Streamlit secrets. |
| `429 Too Many Requests` | Rate limit or quota reached | Check your Groq account's current limits and usage. |
| `ModuleNotFoundError` | Dependency not installed | Run `pip install -r requirements.txt`. |
| `ImportError` | Code files or dependencies are out of sync | Check imports and push the latest compatible files. |
| App deployment failure | Dependency, configuration, or runtime error | Review the Streamlit Cloud logs. |

**Model configuration:** This project documentation uses `openai/gpt-oss-20b`. Make sure it matches the model configured in your actual application and that the model is available to your Groq account.

## 💡 Research Topics to Try

- Recent developments in AI agents
- CRISPR gene-editing research
- Advances in quantum computing
- Fusion energy developments
- India's startup ecosystem
- Applications of multi-agent AI systems

## 👩‍💻 Author

**Palak Patil**

- 🐙 GitHub: [@Palakpatil1410](https://github.com/Palakpatil1410)
- 💼 LinkedIn: [Palak Patil](https://www.linkedin.com/in/palak-patil1410/)
