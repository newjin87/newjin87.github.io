import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class StateManager:
    """
    뉴스 수집 상태(마지막 실행일, 수집된 URL)를 관리하여 중복 수집을 방지합니다.
    """
    def __init__(self, state_file="data/scraping_state.json"):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_state(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4)

    def get_last_search_time_limit(self, keyword: str) -> str:
        """
        마지막 수집일을 기준으로 검색 기간 옵션('d', 'w', 'm')을 반환합니다.
        """
        last_date_str = self.state.get("last_run", {}).get(keyword)
        if not last_date_str:
            return 'm' # 처음이면 한 달 치 검색
        
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
        delta = (datetime.now() - last_date).days
        
        if delta <= 1:
            return 'd' # 어제 이후면 1일 치
        elif delta <= 7:
            return 'w' # 1주일 이내면 1주 치
        else:
            return 'm'

    def update_last_run(self, keyword: str):
        if "last_run" not in self.state:
            self.state["last_run"] = {}
        self.state["last_run"][keyword] = datetime.now().strftime("%Y-%m-%d")
        self.save_state()

class ReportGenerator:
    def __init__(self, base_dir="scraped_news"):
        self.base_dir = Path(base_dir)
        
    def sanitize_filename(self, text: str) -> str:
        # Replace forbidden characters with underscore
        return re.sub(r'[\\/*?:"<>| ]', '_', text)

    def save_analysis_report(self, report_name: str, content: str):
        """
        AI 분석 리포트를 'analysis_result/YYYY-MM-DD/' 폴더에 저장합니다.
        """
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # 분석 결과 저장 경로: analysis_result/YYYY-MM-DD/
        save_dir = Path("analysis_result") / today_str
        save_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{today_str}_{report_name}.md"
        file_path = save_dir / filename
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Analysis Report Saved: {file_path}")
            return str(file_path)
        except Exception as e:
            print(f"❌ Failed to save analysis report: {e}")
            return None

    def save_consolidated_report(self, title: str, news_data: Dict[str, List[Dict[str, str]]]):
        """
        여러 키워드의 뉴스 데이터를 하나의 파일로 통합 저장합니다. (거시 경제용)
        news_data 구조: { "키워드": [뉴스항목1, 뉴스항목2...] }
        """
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # 디렉토리 생성 (예: scraped_news/MACRO_ECONOMY/)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # 파일명 생성
        filename = f"{today_str}_{title}.md"
        file_path = self.base_dir / filename
        
        content = [
            f"# 🌍 {title.replace('_', ' ')}",
            f"**Date**: {today_str}",
            "---"
        ]
        
        for topic, items in news_data.items():
            content.append(f"## 📌 Topic: {topic}")
            content.append(f"*(Found {len(items)} articles)*")
            content.append("")
            
            for idx, item in enumerate(items, 1):
                raw_content = item.get('content', 'No Content Available.')
                # Format content with blockquotes for better readability
                formatted_content = "\n".join([f"> {line}" for line in raw_content.split('\n') if line.strip()])
                
                content.append(f"### {idx}. [{item['title']}]({item['url']})")
                content.append(f"**Source**: {item.get('source', 'Unknown')} | **Date**: {item.get('date', '-')}")
                content.append("")
                content.append(formatted_content)
                content.append("")
                content.append("---")
                content.append("")
            
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(content))
            print(f"   💾 Consolidated Report Saved: {file_path}")
        except Exception as e:
            print(f"   ❌ Failed to save consolidated report: {e}")

    def save_report(self, ticker: str, keyword: str, news_items: List[Dict[str, str]]):
        """
        뉴스 검색 결과를 Markdown 파일로 저장합니다.
        파일명 형식: 날짜_티커_키워드.md (예: 2026-02-02_NVDA_AI_Chip.md)
        """
        if not news_items:
            return

        # 1. Directory Setup
        today_str = datetime.now().strftime("%Y-%m-%d")
        ticker_dir = self.base_dir / ticker
        ticker_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Filename Construction
        safe_keyword = self.sanitize_filename(keyword)
        filename = f"{today_str}_{ticker}_{safe_keyword}.md"
        file_path = ticker_dir / filename
        
        # 3. Content Generation
        content = [
            f"# 📊 Deep Dive Report: {keyword}",
            f"**Target**: {ticker}",
            f"**Date**: {today_str}",
            f"**Source**: DuckDuckGo News Search",
            "",
            "## 📰 Key News Articles",
            ""
        ]
        
        for idx, item in enumerate(news_items, 1):
            content.append(f"### {idx}. [{item['title']}]({item['url']})")
            content.append(f"**Source**: {item['source']} | **Date**: {item['date']}")
            content.append("")
            content.append(item.get('content', '*Content could not be scraped.*'))
            content.append("")
            content.append("---")
            content.append("")
        
        content.append("Generated by Smart News Analyzer 🤖")

        # 4. Save File
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(content))
            print(f"   💾 Report Saved: {file_path}")
        except Exception as e:
            print(f"   ❌ Failed to save report: {e}")

    def save_final_report(self, ticker: str, report_content: str):
        """
        최종 투자 브리핑 리포트를 저장합니다.
        """
        today_str = datetime.now().strftime("%Y-%m-%d")
        ticker_dir = self.base_dir / ticker
        ticker_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{today_str}_{ticker}_Daily_Investment_Briefing.md"
        file_path = ticker_dir / filename
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report_content)
            print(f"📝 Final Investment Briefing saved to: {file_path}")
        except Exception as e:
            print(f"❌ Failed to save final report: {e}")
