# 🤖 AI Investment Automation System

This directory contains the automated system for gathering financial news, performing AI analysis (Macro, Market Strategy, Company Analysis), and publishing reports to the Jekyll blog.

## 📂 Directory Structure

```text
automation/
├── 📄 custom_guide.md       # (Pending) User guide or custom notes
├── 📄 AGENTS_GUIDE.md       # Developer guide for adding new AI agents
├── 📄 agents.py             # CLI tool to manage/create/run agents
├── 📄 run_daily_briefing.py # One-click launcher for the daily briefing
├── 📄 requirements.txt      # Python dependencies
│
├── 📁 config/               # Configuration & Prompts
│   ├── .env                 # API Keys (Google Gemini, etc.) - Keep secret!
│   ├── .env.template        # Template for .env
│   ├── settings.py          # Global settings (Seed queries, counts)
│   └── prompts.py           # Centralized AI prompts (Titles, Analysis)
│
├── 📁 generators/           # Independent AI Agents (Features)
│   └── daily_briefing/      # [Main Feature] Daily Market Briefing
│       ├── run.py           # Agent entry point
│       ├── 01_news_collector.py
│       ├── 02_market_analyzer.py
│       ├── 03_macro_daily_brief.py
│       └── 04_korea_strategy_brief.py
│
├── 📁 libs/                 # Shared Libraries (Tools)
│   ├── analyzer.py          # AI Analysis (Gemini)
│   ├── scraper.py           # Web Scraper (DuckDuckGo, Naver)
│   ├── advisor.py           # Investment Strategy Logic
│   └── utils.py             # File I/O, Blog Publishing, State Management
│
├── 📁 data/                 # Data Storage (GitIgnore recommended)
│   ├── raw_news/            # Scraped JSON data
│   ├── analysis_result/     # Intermediate Markdown reports
│   └── scraping_state.json  # History to prevent duplicate scraping
│
└── 📁 logs/                 # Execution logs
```

## 🚀 How to Run

### 1. Manual Execution (Daily Briefing)
To run the full daily briefing process (Macro -> Korea Strategy -> Company Analysis -> Blog Post):

```bash
# Option A: Root Launcher
python automation/run_daily_briefing.py

# Option B: Agent CLI
python automation/agents.py run daily_briefing
```

### 2. Automatic Execution (GitHub Actions)
The system is configured to run automatically every day at **07:00 AM KST** via GitHub Actions.
- Workflow File: `.github/workflows/daily_briefing.yml`

## 🛠️ Configuration

1.  **API Keys**: Copy `config/.env.template` to `config/.env` and add your `GOOGLE_API_KEY`.
2.  **Settings**: Adjust scraping counts or keywords in `config/settings.py`.
3.  **Prompts**: Modify AI persona or title styles in `config/prompts.py`.

## 🧩 Adding New Features (Agents)

To create a new automation bot (e.g., for YouTube summaries):

```bash
python automation/agents.py new youtube_summary
```

Refer to `AGENTS_GUIDE.md` for coding standards.
