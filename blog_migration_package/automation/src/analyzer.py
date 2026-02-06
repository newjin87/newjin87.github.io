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
