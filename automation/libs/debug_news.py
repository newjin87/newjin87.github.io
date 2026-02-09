import yfinance as yf
from duckduckgo_search import DDGS
import json

def test_yfinance(ticker_symbol):
    print(f"\n--- Testing yfinance for {ticker_symbol} ---")
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        print(f"Raw news count: {len(news) if news else 0}")
        if news:
            print("First item sample:", json.dumps(news[0], indent=2))
        else:
            print("❌ No news returned from yfinance.")
    except Exception as e:
        print(f"❌ yfinance Error: {e}")

def test_ddg(query):
    print(f"\n--- Testing DuckDuckGo for '{query}' ---")
    try:
        results = DDGS().news(keywords=query, max_results=5)
        print(f"Raw news count: {len(results) if results else 0}")
        if results:
            print("First item sample:", json.dumps(results[0], indent=2))
    except Exception as e:
        print(f"❌ DDG Error: {e}")

if __name__ == "__main__":
    test_yfinance("NVDA")
    test_ddg("NVDA stock news")
