
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
            
    # 3. AI Analysis
    analyzer = NewsAnalyzer()
    
    # Summarize News
    print("   🤖 Analyzing news content...")
    analysis_result = analyzer.analyze_company_news(company_name, news_data, macro_context=macro_context)
    
    # 4. Generate Investment Advice
    print("   ⚖️ Generating investment advice...")
    advisor = InvestmentAdvisor()
    advice = advisor.generate_advice(company_name, target_ticker, analysis_result)
    
    # 5. Generate Report
    print("   📝 Generating final report...")
    generator = ReportGenerator()
    
    # Merge analysis and advice
    report_content = generator.create_company_report(
        company_name=company_name,
        ticker=target_ticker,
        analysis=analysis_result,
        advice=advice,
        news_items=news_data
    )
    
    # Save Report
    output_dir = Path(f"analysis_result/{today_str}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = output_dir / f"{today_str}_analysis_{safe_name}.md"
    report_file.write_text(report_content, encoding="utf-8")
    
    print(f"   ✅ Report generated: {report_file}")

if __name__ == "__main__":
    main()
