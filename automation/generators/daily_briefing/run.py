import os
import sys
import time
import csv
import subprocess
from pathlib import Path
from datetime import datetime

# -----------------------------------------------------------
# Virtual Environment Auto-Switching Logic (Must be at top)
# -----------------------------------------------------------
def ensure_venv():
    # Check if running in a virtual environment
    is_venv = sys.prefix != sys.base_prefix
    if is_venv:
        return

    # Try to locate .venv in common locations
    script_dir = Path(__file__).parent.resolve()
    # venv is at automation/.venv, but script is at automation/generators/daily_briefing/
    # So we need to go up 2 levels
    automation_root = script_dir.parent.parent
    venv_python = automation_root / ".venv" / "bin" / "python"
    
    if venv_python.exists():
        print(f"🔄 Auto-switching to Virtual Environment: {venv_python}")
        try:
            # Re-execute the script with the venv python
            os.execv(str(venv_python), [str(venv_python)] + sys.argv)
        except OSError as e:
            print(f"⚠️ Failed to switch virtual environment: {e}")
            pass

# Run venv check immediately
ensure_venv()

# Setup Path for imports
import _path_setup

# Now import valid packages
try:
    from dotenv import load_dotenv
except ImportError:
    # Fallback if dotenv is missing in system python and venv switch failed
    def load_dotenv(): pass
    print("⚠️ 'python-dotenv' not found. Environment variables might not load.")

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
        print(f"✅ [Completed] {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ [Error] {description}: {e}")
        return False

def main():
    # Change working directory to the script's directory to ensure relative paths work
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)
    print(f"📂 Changed working directory to: {script_dir}")

    load_dotenv()
    print("=========================================================")
    print("   🤖 AI Investment Daily Briefing Automation System")
    print("   Date: " + datetime.now().strftime("%Y-%m-%d"))
    print("=========================================================\n")

    # Analysis result path (adjusted for new structure)
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Reports are now saved in ../../data/analysis_result/ (relative to script dir)
    base_output_dir = Path("../../data/analysis_result")
    
    macro_report_path = base_output_dir / today_str / f"{today_str}_analysis_macro_Economy_KR.md"
    
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
    
    korea_report_path = base_output_dir / today_str / f"{today_str}_Korea_Market_Strategy_KR.md"
    
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
    
    # Data is now in automation/data (../../data relative to script)
    csv_path = Path("../../data/favorite_tickers.csv")
    if not csv_path.exists():
        print(f"❌ 즐겨찾기 파일이 없습니다: {csv_path.resolve()}")
        return

    favorites = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # csv 헤더 공백 제거 및 필드명 정리
            if reader.fieldnames:
                reader.fieldnames = [name.strip() for name in reader.fieldnames]
            for row in reader:
                favorites.append(row)
    except Exception as e:
        print(f"❌ CSV 읽기 실패: {e}")
        return

    total_companies = len(favorites)
    print(f"📋 총 {total_companies}개 기업의 분석을 시작합니다.\n")
    
    success_count = 0

    for idx, row in enumerate(favorites):
        # 컬럼명에 공백이 있을 수 있으므로 strip() 처리
        ticker = row.get('ticker', '').strip()
        company_name = row.get('company_name', '').strip()
        
        if not ticker or not company_name:
            continue
        
        print(f"---------------------------------------------------------")
        print(f"🏭 [{idx+1}/{total_companies}] Target Processing: {company_name} ({ticker})")
        print(f"---------------------------------------------------------")

        # Check if analysis already exists for today
        # today_str is already defined above
        
        # We can implement a simple check: if the main report file exists, skip.
        # But since filenames can vary based on content, let's check if "02_market_analyzer.py" would generate it.
        # A simpler approach: check if we successfully completed this ticker in this run? No, across runs.
        
        # Reports are in ../../data/analysis_result/
        output_dir = base_output_dir / today_str
        
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
        else:
            print(f"   ✅ Done: {company_name}")
            success_count += 1
            
        time.sleep(5) # Cool-down between companies

    print("\n=========================================================")
    print(f"🎉 Process Completed. Successfully generated {success_count}/{total_companies} reports.")
    print("📂 Check 'analysis_result/' folder.")
    print("=========================================================")
    
    if success_count == 0 and total_companies > 0:
        print("❌ Error: No reports were generated. Check API Keys (GOOGLE_API_KEY) or logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
