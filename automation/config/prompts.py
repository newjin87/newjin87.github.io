# prompts.py
# AI Prompts used across the automation system
# This centralization allows for easy tuning and A/B testing of prompts.

class Prompts:
    
    # --- Title Generation ---
    TITLE_GENERATION = """
    Analyze the following investment report content and generate a catchy, click-worthy title for a blog post.
    The title should be professional yet intriguing to investors.
    
    Content Summary:
    {content_summary}
    
    Requirements:
    1. Language: Korean
    2. Format: Just the title text (no quotes, no prefixes)
    3. Style: Financial News / YouTube Thumbnail Style (e.g., "Crisis or Opportunity?", "Why is XXX surging?")
    4. Max Length: 40 characters
    5. Do NOT include the date or company ticker (those are added automatically).
    """

    # --- Market Analysis ---
    MARKET_ANALYSIS_KR = """
    You are a professional investment strategist for the Korean market.
    Analyze the following market data and news to provide a strategic outlook.

    Global Macro Context:
    {macro_context}

    Latest News (Korea):
    {news_data}

    Task:
    1. Analyze the impact of global macro trends on the Korean market (KOSPI/KOSDAQ).
    2. Identify key sectors to watch.
    3. Provide actionable investment strategies.

    Output Language: Korean
    Format: Markdown
    """
    
    MARKET_ANALYSIS_EN = """
    You are a global investment strategist.
    Analyze the following market data and news to provide a strategic outlook for global investors interested in Korea.

    Global Macro Context:
    {macro_context}

    Latest News (Korea):
    {news_data}

    Task:
    1. Analyze the impact of global macro trends on the Korean market.
    2. Identify key sectors to watch.
    3. Provide actionable investment strategies.

    Output Language: English
    Format: Markdown
    """

    # --- Company Analysis ---
    COMPANY_ANALYSIS = """
    You are an expert stock analyst. Analyze the following news and data for {company_name}.
    
    Macro Context:
    {macro_context}
    
    News Articles:
    {news_data}
    
    Task:
    1. Executive Summary: What is happening with this company right now?
    2. Sentiment Score: Rate from 0 (Bearish) to 100 (Bullish).
    3. Topic Analysis: Group news into key topics.
    4. Bull vs Bear: List positive and negative factors.
    
    Output Format: JSON
    """

    # --- Investment Advice ---
    INVESTMENT_ADVICE = """
    Based on the analysis below, provide clear investment advice for {company_name} ({ticker}).
    
    Analysis:
    {analysis_result}
    
    Task:
    1. Recommendation: Buy / Hold / Sell (with confidence level).
    2. Short-term Strategy (Next 1-2 weeks).
    3. Long-term Strategy (Next 6-12 months).
    4. Key Risks to Monitor.
    
    Output Language: Korean
    Format: Markdown
    """
