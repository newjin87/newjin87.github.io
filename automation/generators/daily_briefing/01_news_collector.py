
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

import _path_setup
from libs.scraper import NewsScraper
from libs.utils import StateManager
import config.settings as config

def main():
    """
    뉴스 수집기 (News Collector)
    - 특정 기업(TARGET_COMPANY_NAME)에 대한 최신 뉴스를 수집합니다.
    - 수집된 뉴스는 JSON 파일로 저장되어 다음 단계(Analyzer)에서 사용됩니다.
    """
    load_dotenv()
    
    # Environment Variables Check
    target_ticker = os.getenv("TARGET_TICKER")
    company_name = os.getenv("TARGET_COMPANY_NAME")
    
    if not company_name:
        print("❌ Error: TARGET_COMPANY_NAME is not set in environment.")
        sys.exit(1)
        
    print(f"\n📰 [News Collector] Starting news collection for: {company_name} ({target_ticker})")
    
    scraper = NewsScraper()
    state_manager = StateManager(state_file="../../data/scraping_state.json")

    # Determine time limit (Incremental Crawl)
    time_limit = state_manager.get_last_search_time_limit(company_name)
    print(f"   🕒 Search Time Limit: {time_limit}")
    
    # 1. Search Headlines
    print(f"   🔍 Searching for headlines...")
    # Using simple search query logic appropriate for the company
    query = f"{company_name} 주가 전망 실적 이슈"
    
    # Search count from config
    search_count = getattr(config, 'NEWS_SEARCH_COUNT', 10)
    
    news_items = scraper.search_by_keyword(query, count=search_count, time_limit=time_limit)
    
    valid_news = []
    
    if news_items:
        print(f"   ✅ Found {len(news_items)} headline candidates. Scraping details...")
        
        target_scrap_count = getattr(config, 'NEWS_SCRAP_COUNT', 5)
        
        for item in news_items:
            if len(valid_news) >= target_scrap_count:
                break
                
            content = scraper.fetch_article_content(item['url'])
            if content:
                item['content'] = content 
                valid_news.append(item)
                print(f"      - Scraped: {item['title'][:30]}...")
            time.sleep(1) # Polite scraping
    else:
        print("   ⚠️ No news found.")
        
    # Save Results
    output_dir = Path("../../data/raw_news")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    safe_name = company_name.replace(" ", "_").replace("/", "-")
    output_file = output_dir / f"{safe_name}_news.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(valid_news, f, ensure_ascii=False, indent=4)
        
    print(f"   💾 Saved {len(valid_news)} news items to {output_file}")
    
    # Update State (Mark this run time)
    state_manager.update_last_run(company_name)

if __name__ == "__main__":
    main()
