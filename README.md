# 🔍 Multi-Agent AI Research System

An AI-powered research assistant that automates the process of researching a topic, collecting information from the web, generating a structured report, and evaluating the report's quality. It also allows users to ask follow-up questions about the generated research.

## 🚀 Overview

The Multi-Agent AI Research System uses multiple AI agents to perform different research tasks. Each agent has a specific responsibility, making the research workflow more organized and efficient.

The system takes a user query, searches for relevant information, extracts useful content, generates a report, and reviews the report before presenting it to the user.

## ✨ Features

- **Web Search:** Finds relevant information from online sources.
- **Web Scraping:** Extracts useful content from web pages.
- **AI Report Generation:** Creates structured research reports based on collected information.
- **Report Critic:** Reviews the generated report for quality, clarity, and completeness.
- **Follow-up Q&A:** Answers additional questions related to the research report.
- **Interactive UI:** Provides a user-friendly interface built with Streamlit.
- **Document Export:** Supports downloading research reports as Word documents.

## 🧠 AI Agents

The system consists of the following agents:

1. **Search Agent:** Finds relevant web sources for the given topic.
2. **Scraping Agent:** Extracts information from selected web pages.
3. **Writer Agent:** Organizes the collected information into a research report.
4. **Critic Agent:** Evaluates the report and suggests improvements.
5. **Question Answering:** Helps users explore the generated report through follow-up questions.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | User interface |
| LangChain | LLM integration and agent tools |
| LangGraph | Workflow and agent orchestration |
| Groq API | Language model inference |
| Llama / supported Groq models | Research and text generation |
| Tavily | Web search |
| BeautifulSoup4 | Web scraping |
| Requests | HTTP requests |
| python-docx | Word document generation |

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Palakpatil1410/Multi_Agent_Research_System.git
```

### 2. Navigate to the project folder

```bash
cd Multi_Agent_Research_System
```

### 3. Create
