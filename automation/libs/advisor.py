import os
import yfinance as yf
import google.generativeai as genai
from typing import Dict, List, Any

class InvestmentAdvisor:
    def __init__(self):
        # API Key Setup
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY environment variable is not set.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def get_financial_info(self, ticker_symbol: str) -> Dict[str, Any]:
        """
        yfinance를 사용하여 기업의 주요 재무 및 주가 정보를 가져옵니다.
        """
        print(f"💰 Fetching financial data for {ticker_symbol}...")
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            
            # Extract key metrics
            financials = {
                "current_price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
                "target_high": info.get("targetHighPrice", "N/A"),
                "target_mean": info.get("targetMeanPrice", "N/A"),
                "recommendation": info.get("recommendationKey", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "forward_pe": info.get("forwardPE", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": info.get("fiftyTwoWeekLow", "N/A")
            }
            
            # Format numbers for readability
            for k, v in financials.items():
                if isinstance(v, (int, float)) and k == "market_cap":
                     financials[k] = f"{v:,}"
            
            return financials
        except Exception as e:
            print(f"⚠️ Failed to fetch financial info: {e}")
            return {}

    def generate_investment_report(self, ticker: str, financial_info: Dict, news_data: List[Dict], macro_report: str = "", language: str = 'ko') -> str:
        """
        재무 정보, 뉴스 분석 데이터, 그리고 거시 경제 리포트를 종합하여 투자 조언을 생성합니다.
        language: 'ko' or 'en'
        """
        print(f"🤖 Generating AI Investment Advice... ({language})")
        
        # Prepare News Context
        news_context = ""
        for item in news_data:
            title = item.get('title', 'No Title')
            content = item.get('content', '')[:2000] 
            news_context += f"Title: {title}\nContent: {content}\n---\n"
            
        financial_context = "\n".join([f"{k}: {v}" for k, v in financial_info.items()])
        
        # Add Macro Context Section if available
        macro_section = ""
        if macro_report:
            macro_section = f"""
        ## Input 3: Macro Economic Backdrop (Recent Analysis)
        {macro_report[:5000]} # Limit to relevant summary part
        
        **Macro Integration Instruction**:
        - Use this macro info to assess systemic risks or tailwinds for {ticker}.
        - Does the current macro environment (Rates, GDP, Sentiment) support a Buy or Sell for this specific sector?
            """

        if language == 'en':
            role_desc = "You are a highly experienced Senior Research Analyst at a top-tier investment bank. Write in English."
            lang_instruction = "Language: English (Professional Financial Tone)."
            report_title = f"# 📑 [{ticker}] Deep-Dive Investment Analysis"
            section_1_title = "## 1. 📊 Valuation & Fundamental Analysis"
            section_1_desc = f"""
        - **Price Analysis**: Analyze upsides based on Target Mean ({financial_info.get('target_mean', 'N/A')}).
        - **Multiples**: Interpret PE/PBR vs Peers.
        - **Financial Health**: Assess balance sheet strength and dividend appeal.
            """
            section_2_title = "## 2. 📰 Key Drivers & Deep News Analysis"
            section_2_desc = """
        ### (1) [Issue Name]
        - **Fact Check**: Detailed summary of the news.
        - **Implication**: Impact on Revenue/Earnings/Moat.
        - **Sentiment**: Market reaction vs Priced-in status.
            """
            section_3_title = "## 3. ⚖️ Scenario Analysis (Bull vs Bear)"
            section_3_desc = """
        - **📈 Bull Case**: Best case price target & conditions.
        - **📉 Bear Case**: Downside risks & support levels.
            """
            section_4_title = "## 4. 🧠 Final Verdict"
            verdict_lines = """
        ### 🚀 Rating: [Strong Buy / Buy / Hold / Sell]
        
        **Investment Thesis**:
        *(2-3 detailed paragraphs explaining exactly WHY you chose this verdict. Connect the fundamentals with the news analysis.)*

        **Action Plan**:
        - **Entry Timing**: (Buy Now vs Wait for Dip)
        - **Risk Management**: (Stop-loss or Macro red flags)
            """
        else:
            role_desc = "You are a highly experienced Senior Research Analyst at a top-tier investment bank. Write in Korean (한국어 business professional style)."
            lang_instruction = "Language: Korean (한국어 business professional style)."
            report_title = f"# 📑 [{ticker}] 심층 투자 분석 리포트"
            section_1_title = "## 1. 📊 Valuation & Fundamental Analysis"
            section_1_desc = f"""
        - **주가 분석**: 현재 주가 대비 목표가({financial_info.get('target_mean', 'N/A')}) 괴리율 및 상승 여력 분석.
        - **지표 해석**: PER/PBR 수치가 경쟁사나 과거 평균 대비 어떤 의미를 갖는지 상세 서술.
        - **재무 건전성**: 제공된 지표를 바탕으로 회사의 기초 체력 및 배당 매력도 평가.
            """
            section_2_title = "## 2. 📰 Key Drivers & Deep News Analysis"
            section_2_desc = """
        ### (1) [Issue Name]
        - **Fact Check**: 뉴스 내용 상세 요약 (육하원칙에 의거하여 구체적으로)
        - **Implication**: 이 이슈가 회사의 매출, 이익, 또는 시장 지배력에 미칠 구체적 영향 (단기 vs 장기)
        - **Sentiment**: 시장의 반응(우려/기대)과 이것이 주가에 선반영되었는지 여부
            """
            section_3_title = "## 3. ⚖️ Scenario Analysis (Bull vs Bear)"
            section_3_desc = """
        - **📈 Bull Case (낙관 시나리오)**: 
            - 최상의 경우 주가가 어디까지 갈 수 있는지.
            - 핵심 전제 조건 (예: 신제품 성공, 환율 안정 등).
        - **📉 Bear Case (비관 시나리오)**: 
            - 리스크가 현실화될 경우의 하방 지지선.
            - 최악의 악재 시나리오와 대응책.
            """
            section_4_title = "## 4. 🧠 Final Verdict (종합 투자의견)"
            verdict_lines = """
        ### 🚀 등급: [Strong Buy / Buy / Hold / Sell]
        
        **상세 투자 논거**:
        *(Write 2-3 detailed paragraphs explaining exactly WHY you chose this verdict. Connect the fundamentals with the news analysis.)*

        **실행 전략 (Action Plan)**:
        - **진입 타이밍**: (지금 당장 매수해야 하는지, 조정 시 매수해야 하는지)
        - **리스크 관리**: (손절가 혹은 주의해야 할 거시경제 지표)
            """
        
        prompt = f"""
        {role_desc}
        Your task is to write a **Deep-Dive Investment Analysis Report** for '{ticker}'.
        
        **CRITICAL INSTRUCTION**: Do NOT summarize briefly. Provide detailed, actionable, and in-depth analysis. 
        Your goal is to provide enough depth for a portfolio manager to make a high-stakes decision.

        ## Input 1: Financial Fundamentals
        {financial_context}

        ## Input 2: Scraped News Reports (Raw Data)
        {news_context}
        {macro_section}

        ## Analytic Guidelines
        1. **Time-Weighted Analysis (CRITICAL)**:
            - Input data covers various dates. You MUST prioritize recent news (last 3-7 days) for the "Action Plan" and "Verdict".
            - Treat older news (>1 week) as context/background trends. 
            - If recent news contradicts older news, follow the recent trend (e.g., "Earnings shock" yesterday overrides "Expectation" from last week).
        2. **Deep Correlation**: Don't just list news. Explain HOW specific news items (e.g., new tech, earnings shock) directly impact specific financial metrics (e.g., Forward PE, Revenue Growth).
        3. **Macro Sensitivity**: Explicitly discuss how the provided Macro Economic Backdrop impacts this specific company.
        4. **Quantitative reasoning**: Use the provided financial numbers to back up your qualitative news analysis.
        5. **Language**: {lang_instruction}

        ## Report Structure (Markdown)

        {report_title}

        {section_1_title}
        *(Write a detailed paragraph analyzing the valuation. Do not just list numbers.)*
        {section_1_desc}

        {section_2_title}
        *(Select the top 3-5 most critical issues. Analyze each in depth.)*
        {section_2_desc}

        {section_3_title}
        {section_3_desc}

        {section_4_title}
        {verdict_lines}

        ---
        *Disclaimer: 본 리포트는 AI 분석 결과이며 투자 권유가 아닙니다. (English: AI Analysis, not investment advice.)*
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Analysis Failed: {e}"

    def analyze_macro_trends(self, market_data: Dict[str, Any], news_content: str, language: str = 'ko') -> str:
        """
        거시 경제 지표와 수집된 뉴스를 종합하여 시장 전망 리포트를 생성합니다.
        language: 'ko' or 'en'
        """
        print(f"🤖 Generating AI Macro Economic Report... ({language})")
        
        market_context = "\n".join([f"{k}: {v}" for k, v in market_data.items()])
        
        if language == 'en':
            lang_instruction = "Tone: Professional, insightful, and decisive. Language: English."
            title_text = "# 🌍 [Daily Macro Strategy] Global Market Deep Dive"
        else:
            lang_instruction = "Tone: Professional, insightful, and decisive. Language: Korean (한국어)."
            title_text = "# 🌍 [Daily Macro Strategy] 글로벌 시장 심층 분석"

        
        prompt = f"""
        You are a Chief Global Strategist at a major hedge fund.
        Your task is to write a **Daily Macro Economic Strategy Brief**.
        
        ## Input 1: Key Market Indicators (Real-time)
        {market_context}

        ## Input 2: Global News & Trends (Consolidated)
        {news_content[:20000]}  # Limit context window if necessary

        ## Analytic Guidelines
        1. **Time-Weighted Analysis (CRITICAL)**:
            - Focus heavily on "What just happened" (Last 24-72 hours) for the "Market Atmosphere" summary.
            - Use older news only to explain the cause of the current situation.
        2. **Connect the Dots**: Don't just list news. Explain the relationship between the news events and the market indicators.
        3. **Forward-Looking**: Focus on "What comes next?" rather than "What happened?".
        4. **Tone**: {lang_instruction}

        ## Report Structure (Markdown)

        {title_text}

        ## 1. 🚨 Executive Summary (3-Minute Read)
        - **오늘의 핵심 테마 (Key Theme)**: 시장을 관통하는 하나의 키워드나 테마 정의.
        - **시장 분위기 (Market Sentiment)**: (Risk-On / Risk-Off / Neutral) 판단 및 이유.
        - **주요 변동 사항 (Key Moves)**: 위 Market Indicators 중 유의미한 변화가 있는 지표 해석.

        ## 2. 🔑 Key Drivers & Deep Analysis
        *(Identify 3 major themes from the news loop)*
        
        ### Theme 1: [Title]
        - **Situation**: 뉴스 팩트 및 배경 설명.
        - **Market Impact**: 주식, 채권, 환율에 미치는 파급 효과 분석.
        - **Forecast**: 향후 전개 방향 예측.

        (Repeat for Theme 2, 3...)

        ## 3. 📈 Regional & Asset Class Outlook
        - **US Market**: 미 증시(S&P, Nasdaq) 전망 및 관전 포인트.
        - **Korea Market**: 한국 증시(KOSPI, KOSDAQ)에 미칠 영향 (환율, 수출 관점).
        - **Crypto/Assets**: 비트코인, 금, 유가 등 대체 자산 흐름 분석.

        ## 4. 🧭 Actionable Investment Strategy
        - **Top Picks / Sectors**: 현재 국면에서 유망한 섹터나 자산군 추천.
        - **Cautionary Notes**: 투자자가 반드시 주의해야 할 리스크(함정).
        - **Closing Advice**: 투자자들에게 전하는 한 문장 조언.

        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Macro Analysis Failed: {e}")
            return f"❌ Macro Analysis Failed: {e}"
