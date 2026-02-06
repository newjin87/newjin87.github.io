import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from src.korea_news_scraper import KoreaNewsScraper
from src.korea_market_analyzer import KoreaMarketAnalyzer
from src.utils import ReportGenerator # Assuming this exists and is reusable

def main():
    load_dotenv()
    print("--- 🇰🇷 Korea Market Strategy Briefing Started ---")

    # 1. Load Global Context
    global_macro_path = Path("data/latest_global_macro_summary.txt")
    if not global_macro_path.exists():
        print("❌ Global Macro Summary not found. Please run Step 1 (Macro Analysis) first.")
        return

    with open(global_macro_path, "r", encoding="utf-8") as f:
        global_summary = f.read()

    print("✅ Global Macro Context Loaded.")

    # 2. Scrape Korean News
    scraper = KoreaNewsScraper()
    
    # Fetch Finance News
    finance_news = scraper.fetch_naver_finance_news(limit=7)
    
    # Fetch Real Estate News
    land_news = scraper.fetch_naver_land_news(limit=7)
    
    all_news = finance_news + land_news
    
    if not all_news:
        print("❌ No Korean news found.")
        return

    # Fetch content for the articles (Incremental scraping to save time/bandwidth)
    print("\n📥 Fetching article contents for deep analysis...")
    enriched_news = []
    for item in all_news:
        try:
            content = scraper.fetch_article_content(item['url'])
            if content:
                item['content'] = content
                enriched_news.append(item)
                print(f"   - Scraped: {item['title'][:30]}...")
            else:
                print(f"   ⚠️ Content empty: {item['title'][:30]}...")
        except Exception as e:
            print(f"   ❌ Error scraping {item['url']}: {e}")
    
    # 3. Analyze (Dual Language)
    analyzer = KoreaMarketAnalyzer()
    
    # 3-1. Korean Analysis
    print("\n🇰🇷 Generating Korean Report...")
    strategy_report_kr = analyzer.analyze_market_impact(global_summary, enriched_news, language='ko')
    
    # 3-2. English Analysis
    print("\n🇺🇸 Generating English Report...")
    strategy_report_en = analyzer.analyze_market_impact(global_summary, enriched_news, language='en')

    # 4. Save Reports
    today_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(f"analysis_result/{today_str}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save Korean
    output_file_kr = output_dir / f"{today_str}_Korea_Market_Strategy_KR.md"
    with open(output_file_kr, "w", encoding="utf-8") as f:
        f.write("# 🇰🇷 Korea Market Strategy Report (Global/Macro Driven)\n")
        f.write(f"Date: {today_str}\n\n")
        f.write(strategy_report_kr)
        f.write("\n\n---\n")
        f.write("## 🔗 Referenced Korean News Sources\n")
        for news in enriched_news:
            f.write(f"- [{news['title']}]({news['url']})\n")
    print(f"\n🎉 Korea Strategy Report (KR) Saved: {output_file_kr}")

    # Save English
    output_file_en = output_dir / f"{today_str}_Korea_Market_Strategy_EN.md"
    with open(output_file_en, "w", encoding="utf-8") as f:
        f.write("# 🇰🇷 Korea Market Strategy Report (Global/Macro Driven) [EN]\n")
        f.write(f"Date: {today_str}\n\n")
        f.write(strategy_report_en)
        f.write("\n\n---\n")
        f.write("## 🔗 Referenced Korean News Sources\n")
        for news in enriched_news:
            f.write(f"- [{news['title']}]({news['url']})\n")
    print(f"🎉 Korea Strategy Report (EN) Saved: {output_file_en}")


if __name__ == "__main__":
    main()
