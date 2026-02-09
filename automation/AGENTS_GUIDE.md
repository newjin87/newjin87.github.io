# 📘 AI Automation System Developer Guide (Vibe Coding Standard)

This document serves as the **primary reference** for AI coding assistants (GitHub Copilot, Gemini, etc.) when adding new features or agents to the `automation/` system.

---

## 🏗️ System Architecture

The project follows a **Modular Agent Architecture**. Independent "Agents" (generators) utilize shared "Libraries" (libs) and "Configurations" (config) to perform tasks.

### Directory Structure
```text
automation/
├── config/                  # Shared Settings & Environment Variables
│   ├── settings.py          # Global constants
│   └── .env                 # API Keys (GitIgnored)
│
├── libs/                    # Shared Tools (Do NOT duplicate code!)
│   ├── scraper.py           # Web scraping tools (News, HTML)
│   ├── analyzer.py          # LLM Analyzers (Gemini, OpenAI)
│   ├── advisor.py           # Investment Strategy Logic
│   └── utils.py             # File I/O, Logging, State Management
│
├── generators/              # 🤖 Agents live here
│   ├── daily_briefing/      # [Agent 1] Market Briefing
│   │   ├── run.py           # Entry point for this agent
│   │   ├── _path_setup.py   # Path helper (Crucial!)
│   │   └── ... (Agent specific scripts)
│   │
│   └── youtube_summary/     # [Agent 2] Example Future Agent
│       └── ...
│
├── logs/                    # Execution logs
└── data/                    # Shared storage (DB, JSON, Markdown outputs)
```

---

## 🚀 How to Create a New Agent

When you ask an AI to "Create a new agent for X", it should follow these steps:

### 1. Create Folder
Create a new folder in `generators/<agent_name>/`.

### 2. Add Path Setup (`_path_setup.py`)
**MANDATORY:** Every agent must have this file to access `libs` and `config`.

```python
import sys
from pathlib import Path

# Add automation root to sys.path
current_dir = Path(__file__).resolve().parent
automation_root = current_dir.parent.parent

if str(automation_root) not in sys.path:
    sys.path.append(str(automation_root))
```

### 3. Create Entry Point (`run.py`)
The main script should be named `run.py`. It must import `_path_setup` first.

```python
import _path_setup
from libs.utils import ReportGenerator
import config.settings as config

def main():
    print("Agent Started...")
    # Logic here
```

### 4. Create Root Launcher (Optional but Recommended)
To make execution easy, create a named launcher in the `automation/` root.
Example: `automation/run_<agent_name>.py`

```python
# automation/run_my_agent.py
import os
import sys
import subprocess
from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    target_script = base_dir / "generators" / "my_agent" / "run.py"
    
    # Run in subprocess to preserve paths
    subprocess.run([sys.executable, str(target_script)], cwd=target_script.parent)

if __name__ == "__main__":
    main()
```

---

## ⚠️ Coding Canons (Rules)

1.  **Don't Re-invent the Wheel:**
    *   Need to scrape a webpage? Use `libs.scraper.NewsScraper`.
    *   Need to call Gemini? Use `libs.analyzer`.
    *   Need to save a file? Use `libs.utils.ReportGenerator`.
2.  **Encapsulation:**
    *   Agent-specific logic stays inside `generators/<agent>/`.
    *   Generic logic goes to `libs/`.
3.  **Environment Variables:**
    *   Never hardcode API Keys. Use `os.getenv("KEY")` and add entry to `config/.env`.
4.  **Relative Paths:**
    *   Always use `Path(__file__).parent` to locate files relative to the script.
    *   Output data should go to `../../data` (relative to the generator).

---

## 📝 GitHub Actions Integration (Pending)

*Sections regarding CI/CD and automated execution will be added here.*
