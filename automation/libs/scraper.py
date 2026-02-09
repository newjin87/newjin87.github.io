import yfinance as yf
from curl_cffi import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import time
import random

class NewsScraper:
    def __init__(self):
        # API 차단 대비 주요 기업 하드코딩
        self.known_tickers = {
            "samsung": "005930.KS", "삼성전자": "005930.KS",
            "nvidia": "NVDA", "엔비디아": "NVDA",
            "tesla": "TSLA", "테슬라": "TSLA",
            "apple": "AAPL", "애플": "AAPL",
            "microsoft": "MSFT", "마이크로소프트": "MSFT",
            "google": "GOOGL", "구글": "GOOGL",
            "skhynix": "000660.KS", "sk하이닉스": "000660.KS"
        }

    def fetch_article_content(self, url: str) -> Optional[str]:
        """
        URL에서 기사 본문을 스크래핑합니다. (news_scrap_merge.py 로직 이식)
        """
        try:
            # User Agent for bypassing basic protections
            response = requests.get(
                url, 
                impersonate="chrome110", 
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.google.com/"}
            )
            if response.status_code != 200: 
                return None
            
            # Domain filtering
            skip_domains = ["namu.wiki", "samsung.com", "sec.co.kr", "ko.wikipedia.org", "youtube.com"]
            if any(d in url for d in skip_domains):
                return None

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove distracting tags
            for tag in soup(["script", "style", "nav", "footer", "header", "iframe", "aside"]):
                tag.decompose()
                
            # Heuristic to find article body (Compatible with Investing.com & General sites)
            article_body = soup.find('div', class_='WYSIWYG articlePage') or \
                           soup.find('div', class_='article_container') or \
                           soup.find('div', id='article-content')
            
            target = article_body if article_body else soup
            paragraphs = target.find_all('p')
            
            # Join paragraphs usually containing text
            content = "\n\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text()) > 30])
            
            return content if len(content) > 100 else None
            
        except Exception as e:
            print(f"      ❌ Scraping failed: {e}")
            return None

    def search_deep_news(self, ticker: str, keyword: str, count: int = 5) -> List[Dict[str, str]]:
        """
        DuckDuckGo를 사용하여 특정 키워드에 대한 심층 뉴스를 검색합니다.
        """
        import config
        query = f"{ticker} {keyword} news"
        print(f"🔎 Deep Searching: '{query}'...")
        
        try:
            region = getattr(config, 'NEWS_SEARCH_REGION', 'wt-wt')
            results = DDGS().news(keywords=query, max_results=count, region=region)
            news_list = []
            if results:
                for res in results:
                    news_list.append({
                        "title": res.get("title", "No Title"),
                        "url": res.get("url", "#"),
                        "source": res.get("source", "Unknown"),
                        "date": res.get("date", "")
                    })
            print(f"   ✅ Found {len(news_list)} articles for '{keyword}'")
            return news_list
        except Exception as e:
            print(f"   ⚠️ Search failed for '{keyword}': {e}")
            return []

    def search_by_keyword(self, keyword: str, count: int = 5, time_limit: str = None, region_key: str = 'MACRO_SEARCH_REGION') -> List[Dict[str, str]]:
        """
        특정 키워드로 뉴스 검색 (Macro용). region_key 설정값('MACRO' or 'NEWS') 사용.
        """
        import config # Lazy import to avoid circular dependency if any
        print(f"🔎 Keyword Searching: '{keyword}'...")
        try:
            region = getattr(config, region_key, 'wt-wt')
            results = DDGS().news(keywords=keyword, max_results=count, region=region, timelimit=time_limit)
            
            news_list = []
            if results:
                for res in results:
                     news_list.append({
                        "title": res.get("title", "No Title"),
                        "url": res.get("url", "#"),
                        "source": res.get("source", "Unknown"),
                        "date": res.get("date", "")
                    })
            print(f"   ✅ Found {len(news_list)} articles for '{keyword}'")
            return news_list
        except Exception as e:
            print(f"   ⚠️ Search failed for '{keyword}': {e}")
            return []

    def get_ticker(self, query: str) -> Optional[str]:
        """
        기업명을 입력받아 Ticker Symbol을 반환합니다.
        1. 하드코딩된 리스트 확인
        2. Yahoo Finance Search API 사용
        """
        query_lower = query.lower().strip()
        
        # 1. 하드코딩 매핑 확인
        if query_lower in self.known_tickers:
            print(f"✅ Known ticker found: {query} -> {self.known_tickers[query_lower]}")
            return self.known_tickers[query_lower]

        # 2. 티커 형식이면 바로 반환 (간단한 체크)
        if query.upper() in ["NVDA", "AAPL", "TSLA", "MSFT", "GOOG", "AMZN"]:
            return query.upper()
        if query.endswith(".KS") or query.endswith(".KQ"):
            return query.upper()

        # 3. Yahoo Finance API 검색
        print(f"🔍 Searching ticker for: {query}...")
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        params = {"q": query, "quotesCount": 1, "newsCount": 0}

        try:
            res = requests.get(url, params=params, headers=headers)
            data = res.json()
            if 'quotes' in data and len(data['quotes']) > 0:
                symbol = data['quotes'][0]['symbol']
                print(f"✅ Found via API: {symbol}")
                return symbol
        except Exception as e:
            print(f"⚠️ Ticker search failed: {e}")
        
        return None

    def get_headlines(self, ticker_symbol: str, count: int = 20) -> List[str]:
        """
        해당 티커의 최신 뉴스 헤드라인을 가져옵니다.
        """
        print(f"📡 Fetching headlines for: {ticker_symbol}")
        try:
            ticker = yf.Ticker(ticker_symbol)
            news = ticker.news
            
            headlines = []
            if news:
                for item in news[:count]:
                    # Handle varying yfinance news structure
                    title = item.get('title')
                    if not title and 'content' in item:
                        title = item['content'].get('title')
                    
                    if title:
                        headlines.append(title)
            
            print(f"✅ Retrieved {len(headlines)} headlines.")
            return headlines
        except Exception as e:
            print(f"❌ Error fetching headlines: {e}")
            return []

    def _fetch_google_rss(self, query: str) -> List[str]:
        """Google News RSS Fallback"""
        try:
            import urllib.parse
            encoded_query = urllib.parse.quote(query)
            # Google News RSS (Korean edition)
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, features='xml')
                items = soup.find_all('item')
                return [item.title.text for item in items[:10] if item.title]
        except Exception as e:
            print(f"      ❌ RSS Error for '{query}': {e}")
        return []

    def get_macro_headlines(self, seed_queries: List[str], time_limit: str = 'w') -> List[str]:
        """
        주어진 시드 쿼리로 헤드라인을 수집합니다. time_limit('d', 'w', 'm') 반영.
        """
        import config # Lazy import to avoid circular dependency
        print(f"🌍 Fetching Macro Headlines ({time_limit}) Region: {getattr(config, 'MACRO_SEARCH_REGION', 'wt-wt')}...")
        headlines = set()
        
        try:
            for query in seed_queries:
                print(f"   🔎 Scanning: {query}...")
                try:
                    # Apply time_limit to DuckDuckGo search
                    # config.MACRO_SEARCH_REGION 사용 (기본값: 'wt-wt')
                    region = getattr(config, 'MACRO_SEARCH_REGION', 'wt-wt')
                    results = DDGS().news(keywords=query, max_results=10, region=region, timelimit=time_limit)
                    if results:
                        for item in results:
                            headlines.add(item.get('title'))
                    time.sleep(3) 
                except Exception as inner_e:
                    print(f"      ⚠️ Failed to fetch for '{query}': {inner_e}")
                    time.sleep(5) 
 
                
            # Fallback Check
            if len(headlines) < 5:
                print("\n   ⚠️ DDGS yielded few results. Activating Google RSS Fallback...")
                for query in seed_queries:
                    print(f"   📡 RSS Scanning: {query}...")
                    rss_titles = self._fetch_google_rss(query)
                    headlines.update(rss_titles)
                    time.sleep(1)

            headline_list = list(headlines)
            print(f"✅ Collected {len(headline_list)} unique macro headlines.")
            return headline_list
        except Exception as e:
            print(f"❌ Error fetching macro headlines: {e}")
            return []
