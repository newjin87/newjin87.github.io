
# Configuration settings for Daily Briefing Automation

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
