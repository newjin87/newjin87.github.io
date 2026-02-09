
import os
from pathlib import Path

# Base Directories
# Assuming settings.py is in automation/config/
AUTOMATION_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = AUTOMATION_DIR.parent
POSTS_DIR = PROJECT_ROOT / "_posts"

# Ensure _posts exists (it should in a Jekyll blog)
if not POSTS_DIR.exists():
    print(f"⚠️ Warning: _posts directory not found at {POSTS_DIR}")

# --- 1. Macro Analysis Configuration ---
MACRO_SEED_QUERIES = [
    "Global Market News",
    "US Economy Outlook",
    "Federal Reserve Interest Rates",
    "Inflation Report US",
    "Geopolitical Risk Economy",
    "Tech Sector Trends",
    "Oil Prices Energy Market",
    "China Economy Update"
]

MACRO_KEYWORD_COUNT = 5  # Number of hot topics to extract
MACRO_DEEP_NEWS_COUNT = 5 # Number of articles to analyze per topic

# --- 2. Corporate Analysis Configuration ---
NEWS_SEARCH_COUNT = 10    # Number of news items to search per company
NEWS_SCRAP_COUNT = 5      # Number of items to fully scrape content for
