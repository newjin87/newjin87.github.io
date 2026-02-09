import os
import google.generativeai as genai
import ast
import re
from typing import List

class NewsAnalyzer:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY environment variable is not set. Please check your .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def extract_keywords(self, ticker: str, headlines: List[str], count: int = 5) -> List[str]:
        """
        뉴스 헤드라인 리스트에서 주요 트렌드 키워드를 추출합니다.
        """
        if not headlines:
            print("⚠️ No headlines to analyze.")
            return []

        print(f"🧠 Analyzing {len(headlines)} headlines with Gemini...")
        
        headlines_text = "\n".join(f"- {h}" for h in headlines)
        
        prompt = f"""
        You are a financial news analyst. 
        Analyze the following recent news headlines for the company '{ticker}' (Stock).
        Identify the top {count} most important specific topics or keywords that investors should pay attention to right now.
        
        Headlines:
        {headlines_text}
        
        Output format:
        Provide ONLY the keywords as a python list of strings.
        Example: ["AI Chip Demand", "Earnings Surprise", "Cloud Growth"]
        
        IMPORTANT: Output ONLY the list. No markdown formatting, no explanations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean up potential markdown code blocks
            text = re.sub(r'```python|```', '', text).strip()
            
            try:
                keywords = ast.literal_eval(text)
                if isinstance(keywords, list):
                    print(f"✅ Extracted keywords: {keywords}")
                    return keywords
            except:
                pass
                
            # Fallback if ast fails
            print(f"⚠️ Raw parsing failed, returning raw text: {text}")
            return [text]
                
        except Exception as e:
            print(f"❌ AI Analysis failed: {e}")
            return []

    def extract_macro_keywords(self, headlines: List[str], count: int = 5) -> List[str]:
        """
        일반 경제 뉴스 헤드라인에서 '거시 경제 핫토픽' 키워드를 추출합니다.
        """
        print(f"🧠 Finding Top {count} Macro Trends from {len(headlines)} headlines...")
        head_text = "\n".join(f"- {h}" for h in headlines)
        
        prompt = f"""
        You are a Global Macroeconomic Analyst.
        Here are the latest headlines from the financial markets:
        
        {head_text}
        
        Task: Identify the Top {count} most critical macroeconomic themes or risks currently impacting the market.
        (e.g., "Fed Interest Rates", "Oil Price Surge", "Bitcoin Rally", "Middle East Conflict")
        
        Output format: Python list of strings ONLY.
        Example: ["US Inflation Data", "China Stimulus", "AI Bubble Concerns"]
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.replace("```python", "").replace("```", "").strip()
            return ast.literal_eval(text)
        except Exception:
            return []

    def analyze_company_news(self, company_name: str, news_items: list, macro_context: str = "") -> dict:
        """
        기업 뉴스 데이터를 분석하여 요약, 주요 이슈, 투자 포인트를 추출합니다.
        사용자 요청: 키워드별 뉴스 요약 포함.
        """
        import json
        
        if not news_items:
            return {"summary": "No news data available.", "keywords": []}

        print(f"🧠 Analyzing detailed news for {company_name}...")
        
        # Prepare context (Max ~20 items to avoid token limits)
        news_text = ""
        for idx, item in enumerate(news_items[:20], 1): 
            content_preview = item.get('content', '')[:1000] 
            news_text += f"[{idx}] Title: {item.get('title', 'No Title')}\nContent: {content_preview}\n\n"

        prompt = f"""
        You are a Professional Equity Research Analyst.
        Analyze the provided news articles for the company **{company_name}**.
        
        Context (Macro Economy):
        {macro_context[:500] if macro_context else "No specific macro context provided."}
        
        News Data:
        {news_text}
        
        Task:
        1. **Executive Summary**: A concise summary of the current situation (3-5 sentences).
        2. **Topic Analysis**: Group the news by key themes/keywords. For each keyword, provide a bullet-point summary of the relevant facts.
        3. **Bullish Factors (Good News)**: List positive indicators.
        4. **Bearish Factors (Risk Factors)**: List negative indicators or risks.
        5. **Sentiment Score**: A score from 0 (Extremely Negative) to 100 (Extremely Positive).
        
        Output Format (JSON):
        {{
            "executive_summary": "...",
            "topic_analysis": [
                {{
                    "keyword": "Topic Name",
                    "summary": "- Fact 1...\\n- Fact 2..."
                }}
            ],
            "bullish_factors": ["Point 1", "Point 2"],
            "bearish_factors": ["Point 1", "Point 2"],
            "sentiment_score": 75
        }}
        
        IMPORTANT: Return ONLY valid JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            # Clean up potential leading/trailing non-json chars
            if "{" in text:
                text = text[text.find("{"):text.rfind("}")+1]
            return json.loads(text)
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return {
                "executive_summary": "Analysis failed due to an error.",
                "topic_analysis": [],
                "bullish_factors": [],
                "bearish_factors": [],
                "sentiment_score": 50
            }
