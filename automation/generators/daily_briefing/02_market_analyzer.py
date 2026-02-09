
import os
import sys
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

import _path_setup
from libs.analyzer import NewsAnalyzer
from libs.advisor import InvestmentAdvisor
from libs.utils import ReportGenerator
import config.settings as config

def main():
    """
    시장 분석기 (Market Analyzer) & 리포트 생성기
    """
    load_dotenv()
    
    target_ticker = os.getenv("TARGET_TICKER")
    company_name = os.getenv("TARGET_COMPANY_NAME")
    
    if not company_name:
        print("❌ Error: TARGET_COMPANY_NAME is not set.")
        sys.exit(1)
        
    print(f"\n🧠 [Market Analyzer] Analyzing data for: {company_name}")
    
    # 1. Load News Data
    safe_name = company_name.replace(" ", "_").replace("/", "-")
    # Path relative to automation/generators/daily_briefing/
    news_file = Path(f"../../data/raw_news/{safe_name}_news.json")
    
    if not news_file.exists():
        print(f"   ❌ News file not found: {news_file}")
        news_data = []
    else:
        with open(news_file, "r", encoding="utf-8") as f:
            news_data = json.load(f)

    # 2. Check for Macro Context (Optional)
    today_str = datetime.now().strftime("%Y-%m-%d")
    macro_report_path = Path(f"analysis_result/{today_str}/{today_str}_analysis_macro_Economy_KR.md")
    macro_context = ""
    if macro_report_path.exists():
        try:
            macro_context = macro_report_path.read_text(encoding="utf-8")
        except:
            pass
            
    # 3. Initialize Agents
    analyzer = NewsAnalyzer()
    advisor = InvestmentAdvisor()
    generator = ReportGenerator()
    
    # 4. Get Financial Data (Shared)
    financial_info = advisor.get_financial_info(target_ticker)

    # 5. Loop for Multi-Language Generation
    languages = ['ko', 'en']
    
    for lang in languages:
        print(f"\n   🌐 Processing Language: {lang.upper()}")
        
        # 5-1. Analyze News
        print("      🤖 Analyzing news content...")
        analysis_result = analyzer.analyze_company_news(company_name, news_data, macro_context=macro_context, language=lang)
        
        # 5-2. Generate Investment Advice
        print("      ⚖️ Generating investment advice...")
        advice = advisor.generate_investment_report(
            ticker=target_ticker,
            financial_info=financial_info,
            news_data=news_data,
            macro_report=macro_context,
            language=lang
        )
        
        # 5-3. Create Final Report
        print("      📝 Generating final report...")
        final_report = generator.create_company_report(
            company_name=company_name,
            ticker=target_ticker,
            analysis=analysis_result,
            advice=advice,
            news_items=news_data,
            language=lang
        )
        
        # 5-4. Save to File
        output_dir = Path(f"analysis_result/{today_str}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        suffix = "_KR" if lang == 'ko' else "_EN"
        report_file = output_dir / f"{today_str}_analysis_{safe_name}{suffix}.md"
        report_file.write_text(final_report, encoding="utf-8")
        print(f"      ✅ File generated: {report_file}")
        
        # 5-5. Publish to Blog
        # Title Generation
        summary_text = analysis_result.get("executive_summary", "")[:500]
        
        if lang == 'ko':
             viral_subtitle = analyzer.generate_viral_title(summary_text)
             blog_title = f"[{today_str}] {company_name} ({target_ticker}): {viral_subtitle}"
             tags = ["Stock", "Investment", company_name, target_ticker]
        else:
             # For English, we append a clear indicator or use a different title format
             blog_title = f"[{today_str}] {company_name} ({target_ticker}) - Deep Dive Analysis (English)"
             tags = ["Stock", "Investment", company_name, target_ticker, "English"]

        generator.save_to_blog(
            title=blog_title,
            category="Stock-Analysis",
            content=final_report,
            tags=tags
        )

if __name__ == "__main__":
    main()
