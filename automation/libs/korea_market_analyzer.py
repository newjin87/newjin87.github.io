import os
import google.generativeai as genai
from typing import List, Dict

class KoreaMarketAnalyzer:
    def __init__(self):
        # API Key Setup
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY environment variable is not set.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def analyze_market_impact(self, global_macro_summary: str, korea_news_list: List[Dict], language: str = 'ko') -> str:
        """
        Analyzes the impact of Global Macro trends on the Korean Market based on scraped news.
        language: 'ko' or 'en'
        """
        print(f"🧠 analyzing Korea Market Impact... ({language})")
        
        # 1. Format Korean News
        news_context = ""
        for news in korea_news_list:
            title = news.get('title', 'No Title')
            category = news.get('category', 'General')
            content = news.get('content', '')[:500] # Limit content length for context window
            news_context += f"- [{category}] {title}\n  Summary/Excerpt: {content}...\n\n"

        if not news_context:
            news_context = "No specific Korean news articles were provided."

        # Define Output Language instructions
        if language == 'en':
            lang_instruction = "Language: English. Write for an international investor audience interested in the Korean market."
            section_headers = 'Use sections: "Global Context Overview", "Impact on Korean Stocks", "Impact on Real Estate", "FX Outlook", "Strategic Conclusion".'
        else:
            lang_instruction = "Language: Korean (한국어)."
            section_headers = 'Use sections: "Global Context Overview", "Impact on Korean Stocks", "Impact on Real Estate", "FX Outlook", "Strategic Conclusion".'


        # 2. Construct Prompt
        prompt = f"""
        You are an elite Chief Economist specializing in the correlation between Global Markets and the South Korean Economy.

        # GLOBAL MARKET CONTEXT (Macro Analysis)
        {global_macro_summary}

        # KOREAN MARKET NEWS (Recent Headlines & Content)
        {news_context}

        # TASK
        Analyze how the global market trends described above will impact the South Korean economy, specifically focusing on:
        
        1. **Stock Market (KOSPI/KORDAQ)**:
           - Focus on Export-driven sectors (Semiconductors, Auto, Batteries).
           - How global risk sentiment (from the macro summary) affects foreign capital flow into Korea.
        
        2. **Real Estate Market**:
           - Analyze the impact of US Treasury yields and Fed policy (from macro summary) on Korean Bank of Korea (BOK) interest rate decisions.
           - Impact on mortgage rates and housing sentiment in Korea.
        
        3. **Currency (USD/KRW)**:
           - Directional forecast based on Dollar Index (DXY) and global liquidity trends.

        # OUTPUT FORMAT
        - Provide a professional Markdown report.
        - {section_headers}
        - Be specific about causality (e.g., "Because US 10Y Yields are rising, Korean lending rates may...").
        - {lang_instruction}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Analysis Generation Failed: {e}")
            return "Analysis could not be generated due to an error."
