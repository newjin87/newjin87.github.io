import os
import sys
import time
import pandas as pd
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

def run_command(command, description, env=None):
    """
    쉘 명령어를 실행하고 결과를 출력합니다.
    """
    print(f"\n🚀 [Starting] {description}...")
    try:
        # sys.executable을 사용하여 현재 활성화된 가상환경의 python을 사용
        # Quote the executable path to handle spaces in path
        full_command = f'"{sys.executable}" {command}' # Added quotes around sys.executable
        
        # Pass env if provided, otherwise use current environment
        proc_env = env if env else os.environ.copy()

        result = subprocess.run(full_command, shell=True, check=True, text=True, env=proc_env)
        if result.returncode == 0:
            print(f"✅ [Completed] {description}")
            return True
        else:
            print(f"❌ [Failed] {description}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ [Error] {description}: {e}")
        return False

def main():
    load_dotenv()
    print("=========================================================")
    print("   🤖 AI Investment Daily Briefing Automation System")
    print("   Date: " + datetime.now().strftime("%Y-%m-%d"))
    print("=========================================================\n")

    # -----------------------------------------------------------
    # 1. Macro Economy Analysis (Top-Down Approach)
    # -----------------------------------------------------------
    print(">>> STEP 1: Macro Economy Analysis")
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    # Check for KR version as primary indicator
    macro_report_path = Path(f"analysis_result/{today_str}/{today_str}_analysis_macro_Economy_KR.md")
    
    if macro_report_path.exists():
        print(f"   ✨ Macro Report already exists. Skipping...")
    else:
        if not run_command("03_macro_daily_brief.py", "Macro Economic Scraping & Analysis"):
            print("⚠️ 거시 경제 분석 실패. 기업 분석은 거시 리포트 없이 진행됩니다.")
    
    time.sleep(2) # Stabilize

    # -----------------------------------------------------------
    # 1.5 Korea Market Analysis (Global Context Driven)
    # -----------------------------------------------------------
    print("\n>>> STEP 1.5: Korea Market Strategy Analysis")
    
    korea_report_path = Path(f"analysis_result/{today_str}/{today_str}_Korea_Market_Strategy_KR.md")
    
    if korea_report_path.exists():
        print(f"   ✨ Korea Strategy Report already exists. Skipping...")
    else:
        if not run_command("04_korea_strategy_brief.py", "Korea Market Scraping & Analysis"):
             print("⚠️ 한국 시장 분석 실패.")

    time.sleep(2)

    # -----------------------------------------------------------
    # 2. Daily Corporate Analysis (Bottom-Up)
    # -----------------------------------------------------------
    print("\n>>> STEP 2: Corporate Analysis (Favorites)")
    
    csv_path = Path("data/favorite_tickers.csv")
    if not csv_path.exists():
        print(f"❌ 즐겨찾기 파일이 없습니다: {csv_path}")
        return

    try:
        favorites = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ CSV 읽기 실패: {e}")
        return

    total_companies = len(favorites)
    print(f"📋 총 {total_companies}개 기업의 분석을 시작합니다.\n")

    for idx, row in favorites.iterrows():
        ticker = row['ticker']
        company_name = row['company_name']
        
        print(f"---------------------------------------------------------")
        print(f"🏭 [{idx+1}/{total_companies}] Target Processing: {company_name} ({ticker})")
        print(f"---------------------------------------------------------")

        # Check if analysis already exists for today
        today_str = datetime.now().strftime("%Y-%m-%d")
        # Expected analysis file pattern: analysis_result/{date}/{date}_{company_name_cleaned}_{ticker}_Report.md 
        # (Note: Exact filename depends on 02_market_analyzer.py logic, but we can check if folder has files for this ticker)
        
        # We can implement a simple check: if the main report file exists, skip.
        # But since filenames can vary based on content, let's check if "02_market_analyzer.py" would generate it.
        # A simpler approach: check if we successfully completed this ticker in this run? No, across runs.
        
        # Let's assume the standard output directory
        output_dir = Path(f"analysis_result/{today_str}")
        
        # Check if any report for this ticker exists in today's folder
        # Files are usually named like: {date}_{company_name}.md or similar. 
        # From 02_market_analyzer.py, it saves using TARGET_COMPANY_NAME if available.
        # Format: {today}_analysis_{safe_name}.md
        
        # Safe name logic to match 02_market_analyzer.py
        safe_name = company_name.replace(" ", "_").replace("/", "-").replace(":", "")
        expected_report = output_dir / f"{today_str}_analysis_{safe_name}.md"

        if expected_report.exists():
            print(f"   ✨ Report already exists for {company_name}. Skipping...")
            continue

        # Set target for the subprocess
        env = os.environ.copy()
        env["TARGET_TICKER"] = ticker
        env["TARGET_COMPANY_NAME"] = company_name
        
        # 2-1. News Collection
        if not run_command("01_news_collector.py", f"Collecting News for {company_name}", env=env):
            print(f"   ⚠️ 뉴스 수집 실패: {company_name}. Skip.")
            continue
            
        time.sleep(3) # API Rate Limit Cool-down

        # 2-2. Investment Analysis
        if not run_command("02_market_analyzer.py", f"Analyzing Investment Report for {company_name}", env=env):
             print(f"   ⚠️ 분석 리포트 생성 실패: {company_name}")
        
        print(f"   ✅ Done: {company_name}")
        time.sleep(5) # Cool-down between companies

    print("\n=========================================================")
    print("🎉 All Daily Briefings Completed Successfully!")
    print("📂 Check 'analysis_result/' folder.")
    print("=========================================================")

if __name__ == "__main__":
    main()
