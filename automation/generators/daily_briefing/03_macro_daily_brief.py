import os
import sys
import time
import random
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dotenv import load_dotenv

import _path_setup
import yfinance as yf
from libs.scraper import NewsScraper
from libs.analyzer import NewsAnalyzer
from libs.advisor import InvestmentAdvisor
from libs.utils import ReportGenerator, StateManager
import config.settings as config

def get_market_indicators_summary():
    """
    yfinance를 통해 세계 주요 거시 경제 지표를 수집합니다.
    (S&P, Nasdaq, VIX, Oil, Gold, Exchange Rates, Treasury Yields)
    """
    tickers = {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "KOSPI": "^KS11",
        "VIX (Volatility)": "^VIX",
        "USD/KRW": "KRW=X",
        "Crude Oil": "CL=F",
        "Gold": "GC=F",
        "US 10Y Bond": "^TNX",
        "Bitcoin": "BTC-USD"
    }
    
    print("\n📊 Fetching Real-time Market Indicators...")
    data = {}
    for name, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            # Fetch latest data (fastest way)
            hist = ticker.history(period="1d")
            if not hist.empty:
                last_price = hist['Close'].iloc[-1]
                prev_close = ticker.info.get('previousClose', last_price)
                if prev_close and prev_close != 0:
                    change = ((last_price - prev_close) / prev_close) * 100
                else:
                    change = 0.0
                
                change_emoji = "🔺" if change > 0 else "🔻"
                data[name] = f"{last_price:,.2f} ({change_emoji} {change:+.2f}%)"
            else:
                data[name] = "N/A"
        except Exception as e:
            data[name] = "Error"
    
    return data

def collect_macro_news(scraper: NewsScraper, analyzer: NewsAnalyzer, state_manager: StateManager) -> Dict[str, List[Dict]]:
    """
    거시 경제 뉴스를 수집합니다. (Incremental Search)
    """
    # Determine search time limit based on last run
    time_limit = state_manager.get_last_search_time_limit("MACRO")
    print(f"🕒 Incremental Search Limit: '{time_limit}'")

    # 1. Collect Seed Headlines
    seed_queries = config.MACRO_SEED_QUERIES
    headlines = scraper.get_macro_headlines(seed_queries, time_limit=time_limit)
    
    if not headlines:
        print("❌ No macro headlines found.")
        return {}

    # 2. Extract Hot Topics
    keywords = analyzer.extract_macro_keywords(headlines, count=config.MACRO_KEYWORD_COUNT)
    print(f"\n✅ Top Macro Topics: {keywords}")
    
    # 3. Deep Search & Consolidated Data Building
    consolidated_data = {}
    
    for topic in keywords:
        print(f"\n🔍 Keyword Deep Search: {topic}")
        # Use multiplier for robust scraping (Skip mechanism)
        target_count = getattr(config, 'MACRO_DEEP_NEWS_COUNT', 10)
        candidates_count = target_count * 3
        
        deep_news = scraper.search_by_keyword(topic, count=candidates_count, time_limit=time_limit)
        
        enriched_news = []
        if deep_news:
            print(f"   📥 Scraping content for topic: {topic} (Target: {target_count})...")
            for item in deep_news:
                # Stop if we have enough
                if len(enriched_news) >= target_count:
                    print(f"      ✅ Reached target count of {target_count}. Stopping.")
                    break
                    
                content = scraper.fetch_article_content(item['url'])
                if content:
                    item['content'] = content
                    enriched_news.append(item)
                    print(f"      - Scraped: {item['title'][:30]}...")
                else:
                    print(f"      ⚠️ Skipped: {item['title'][:30]}...")
                time.sleep(random.uniform(1.0, 1.5))
        
        if enriched_news:
             consolidated_data[topic] = enriched_news
        else:
            print(f"   ⚠️ No content found for topic: {topic}")

    return consolidated_data

def main():
    load_dotenv()
    print("--- 🌍 Macro Economy Daily Briefing System Started ---")
    
    scraper = NewsScraper()
    analyzer = NewsAnalyzer()
    advisor = InvestmentAdvisor()
    state_manager = StateManager(state_file_path="../../data/scraping_state.json") # Initialize local state manager
    reporter = ReportGenerator(base_dir="../../data/scraped_news") 
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    news_file_path = reporter.base_dir / "MACRO_ECONOMY" / f"{today_str}_Macro_Economy_Briefing.md"
    
    # ---------------------------------------------------------
    # Step 1: Check Existing News Data (Smart Integration)
    # ---------------------------------------------------------
    news_content = ""
    
    if news_file_path.exists():
        print(f"\n✅ Found existing news report for today: {news_file_path}")
        print("   👉 Skipping collection phase and proceeding to analysis.")
        with open(news_file_path, "r", encoding="utf-8") as f:
            news_content = f.read()
            
    else:
        print("\n🚀 No news report found for today. Starting fresh collection...")
        # Run Collection Phase
        news_data = collect_macro_news(scraper, analyzer, state_manager)
        
        if news_data:
            # Save Raw News Report (Consolidated)
            print("\n--- 💾 Saving Consolidated Macro Report ---")
            reporter.save_consolidated_report("Macro_Economy_Briefing", news_data)
            
            # Update Last Run Date on Success
            state_manager.update_last_run("MACRO")
            
            # Read back the saved content for analysis context
            if news_file_path.exists():
                 with open(news_file_path, "r", encoding="utf-8") as f:
                    news_content = f.read()
        else:
            print("❌ Macro news collection failed. Aborting.")
            # Even if collection failed, if we have NO previous report, we can't proceed.
            return

    # ---------------------------------------------------------
    # Step 2: Fetch Market Indicators
    # ---------------------------------------------------------
    market_metrics = get_market_indicators_summary()
    print(f"✅ Market Metrics: {market_metrics}")

    # ---------------------------------------------------------
    # Step 3: AI Deep Analysis (Dual Language)
    # ---------------------------------------------------------
    if news_content and market_metrics:
        print("\n--- 🧠 Running AI Investment Strategist (Dual Language) ---")
        
        # 1. Korean Analysis
        print("   🇰🇷 Generating Korean Report...")
        analysis_report_kr = advisor.analyze_macro_trends(market_metrics, news_content, language='ko')
        
        if analysis_report_kr:
            saved_path_kr = reporter.save_analysis_report("analysis_macro_Economy_KR", analysis_report_kr)
            
            # Save a copy to a fixed path for "Korea Market Analysis" to consume
            # We use the Korean version as context for the Korean market analysis
            fixed_summary_path = Path("../../data/latest_global_macro_summary.txt")
            fixed_summary_path.parent.mkdir(parents=True, exist_ok=True)
            with open(fixed_summary_path, "w", encoding="utf-8") as f:
                f.write(analysis_report_kr)
            print(f"      also saved context to fixed path: {fixed_summary_path}")
            print(f"      Saved KR Report: {saved_path_kr}")
            
        # 2. English Analysis
        print("   🇺🇸 Generating English Report...")
        analysis_report_en = advisor.analyze_macro_trends(market_metrics, news_content, language='en')
        
        if analysis_report_en:
             saved_path_en = reporter.save_analysis_report("analysis_macro_Economy_EN", analysis_report_en)
             print(f"      Saved EN Report: {saved_path_en}")

        if analysis_report_kr or analysis_report_en:
            print(f"\n🎉 Process Completed!")
        else:
             print("❌ AI Analysis failed.")

    else:
        print("⚠️ Not enough data to generate analysis.")

if __name__ == "__main__":
    main()
