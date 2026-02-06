import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict

class KoreaNewsScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def _get_soup(self, url: str) -> BeautifulSoup:
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            # Naver uses cp949 or euc-kr often, but requests usually auto-detects.
            # However, sometimes we need to enforce encoding if it detects wrong.
            # Usually utf-8 or euc-kr.
            return BeautifulSoup(res.content, "html.parser")
        except Exception as e:
            print(f"❌ Connection error to {url}: {e}")
            return None

    def fetch_naver_finance_news(self, limit: int = 10) -> List[Dict]:
        """
        Naver Finance Main News
        URL: https://finance.naver.com/news/mainnews.naver
        """
        print("   🇰🇷 Fetching Naver Finance Main News...")
        url = "https://finance.naver.com/news/mainnews.naver"
        soup = self._get_soup(url)
        if not soup:
            return []

        news_list = []
        # Structure: usually inside div.mainNewsList or ul.newsList
        # Let's target the list items.
        # Structure is roughly: dl > dd > a (title)
        
        articles = soup.select(".mainNewsList li dl") 
        # If .mainNewsList li doesn't exist, try generic .newsList
        if not articles:
             articles = soup.select(".newsList li dl")

        for item in articles:
            if len(news_list) >= limit:
                break
            
            # Title is usually in <dd class="articleSubject"> <a ...>
            title_tag = item.select_one(".articleSubject a")
            summary_tag = item.select_one(".articleSummary")
            
            if title_tag:
                title = title_tag.text.strip()
                link = "https://finance.naver.com" + title_tag["href"]
                
                # Extract simple summary if available
                summary = summary_tag.text.strip() if summary_tag else ""
                
                news_list.append({
                    "title": title,
                    "url": link,
                    "category": "Stock/Economy",
                    "summary": summary
                })
        
        print(f"   ✅ Collected {len(news_list)} Finance articles.")
        return news_list

    def fetch_naver_land_news(self, limit: int = 10) -> List[Dict]:
        """
        Naver Real Estate News (Trend/Policy)
        URL: https://land.naver.com/news/
        """
        print("   🏠 Fetching Naver Real Estate News...")
        # 'trend' section: https://land.naver.com/news/trendReport.naver
        # 'breaking' section: https://land.naver.com/news/headline.naver
        url = "https://land.naver.com/news/headline.naver"
        
        soup = self._get_soup(url)
        if not soup:
            return []

        news_list = []
        # Structure: div.headline_list > ul > li
        articles = soup.select(".headline_list ul li")

        for item in articles:
            if len(news_list) >= limit:
                break
            
            # Title is in <dt><a>...</a></dt>
            title_tag = item.select_one("dt a")
            if not title_tag:
                continue
                
            title = title_tag.text.strip()
            # Link is usually relative or absolute?
            link = title_tag["href"]
            if not link.startswith("http"):
                link = "https://land.naver.com" + link

            news_list.append({
                "title": title,
                "url": link,
                "category": "Real Estate",
                "summary": "" 
            })

        print(f"   ✅ Collected {len(news_list)} Real Estate articles.")
        return news_list

    def fetch_article_content(self, url: str) -> str:
        """
        Fetches the body text of a Naver News article.
        Handles both Finance and Land news formats.
        """
        time.sleep(random.uniform(0.3, 0.8)) # Respectful delay
        soup = self._get_soup(url)
        if not soup:
            return ""

        # Common Content IDs
        # Finance: #content > .article_cont
        # Land: #articleBody
        # Generic Naver News: #dic_area or #articleBodyContents
        
        content = ""
        
        # Try generic selectors
        selectors = [
            "#dic_area", 
            "#articleBodyContents", 
            "#news_read", 
            ".article_cont",  # Finance specific often
            "#articleBody"    # Land specific
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # Remove scripts and styles
                for script in element(["script", "style", "a", "iframe", "span.end_photo_org"]):
                    script.extract()
                content = element.get_text(strip=True)
                break
        
        return content
