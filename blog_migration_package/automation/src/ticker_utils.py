from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
from typing import List, Dict, Optional

def search_ticker(query: str) -> List[Dict[str, str]]:
    """
    Searches for a ticker.
    1. Checks hardcoded common mappings.
    2. Searches Naver General Search (for "Name (Ticker)" pattern).
    3. Searches Naver Finance (for domestic codes).
    4. Searches Yahoo Finance (fallback).
    """
    
    # 1. Hardcoded Common Mappings (Korean -> Ticker)
    common_map = {
        "팔랑티어": "PLTR", "팔란티어": "PLTR",
        "애플": "AAPL",
        "테슬라": "TSLA",
        "엔비디아": "NVDA", "앤비디아": "NVDA",
        "마이크로소프트": "MSFT", "마소": "MSFT",
        "구글": "GOOGL", "알파벳": "GOOGL",
        "아마존": "AMZN",
        "메타": "META", "페이스북": "META",
        "넷플릭스": "NFLX",
        "티에스엠씨": "TSM", "tsmc": "TSM",
        "브로드컴": "AVGO",
        "amd": "AMD", "에이엠디": "AMD",
        "인텔": "INTC",
        "퀄컴": "QCOM",
        "쿠팡": "CPNG",
        "아이온큐": "IONQ",
        "리비안": "RIVN",
        "루시드": "LCID",
        "니콜라": "NKLA",
        "로블록스": "RBLX",
        "유니티": "U",
        "코카콜라": "KO",
        "펩시": "PEP",
        "스타벅스": "SBUX",
        "나이키": "NKE",
        "디즈니": "DIS",
        "보잉": "BA",
        "델타항공": "DAL",
        "아메리칸항공": "AAL",
        "카니발": "CCL",
        "로얄캐리비안": "RCL",
        "노르웨이지안": "NCLH",
        "엑슨모빌": "XOM",
        "쉐브론": "CVX",
        "옥시덴탈": "OXY",
        "버크셔": "BRK-B", "버크셔해서웨이": "BRK-B",
        "제이피모건": "JPM",
        "뱅크오브아메리카": "BAC",
        "웰스파고": "WFC",
        "시티그룹": "C",
        "골드만삭스": "GS",
        "모건스탠리": "MS",
        "비자": "V",
        "마스터카드": "MA",
        "페이팔": "PYPL",
        "블록": "SQ", "스퀘어": "SQ",
        "쇼피파이": "SHOP",
        "우버": "UBER",
        "에어비앤비": "ABNB",
        "도어대시": "DASH",
        "팔로알토": "PANW",
        "크라우드스트라이크": "CRWD",
        "스노우플레이크": "SNOW",
        "데이터독": "DDOG",
        "몽고디비": "MDB",
        "아틀라시안": "TEAM",
        "서비스나우": "NOW",
        "오라클": "ORCL",
        "어도비": "ADBE",
        "세일즈포스": "CRM",
        "인튜이트": "INTU",
        "ibm": "IBM",
        "hp": "HPQ",
        "델": "DELL",
        "웨스턴디지털": "WDC",
        "시게이트": "STX",
        "마이크론": "MU",
        "램리서치": "LRCX",
        "어플라이드머티리얼즈": "AMAT",
        "asml": "ASML",
        "klac": "KLAC",
        "테라다인": "TER",
        "엔페이즈": "ENPH",
        "솔라엣지": "SEDG",
        "퍼스트솔라": "FSLR",
        "플러그파워": "PLUG",
        "퓨얼셀에너지": "FCEL",
        "블룸에너지": "BE",
        "선런": "RUN",
        "선파워": "SPWR",
        "넥스트에라": "NEE",
        "듀크에너지": "DUK",
        "서던컴퍼니": "SO",
        "도미니언": "D",
        "아메리칸타워": "AMT",
        "에퀴닉스": "EQIX",
        "프로로지스": "PLD",
        "리얼티인컴": "O",
        "사이먼프로퍼티": "SPG",
        "웰타워": "WELL",
        "벤타스": "VTR",
        "보스턴프로퍼티": "BXP",
        "알렉산드리아": "ARE",
        "메디컬프로퍼티": "MPW",
        "오메가헬스케어": "OHI",
        "서브라": "SBRA",
        "내셔널헬스": "NHI",
        "케어트러스트": "CTRE",
        "ltc": "LTC",
        "stag": "STAG",
        "agree": "ADC",
        "epr": "EPR",
        "glpi": "GLPI",
        "vici": "VICI",
        "gaming": "GLPI",
        "kimco": "KIM",
        "regency": "REG",
        "federal": "FRT",
        "brixmor": "BRX",
        "spirit": "SRC",
        "essential": "EPRT",
        "four": "FCPT",
        "getty": "GTY",
        "safe": "SAFE",
        "istart": "STAR",
        "sl": "SLG",
        "vornado": "VNO",
        "empire": "ESRT",
        "hudson": "HPP",
        "kilroy": "KRC",
        "douglas": "DEI",
        "piedmont": "PDM",
        "highwoods": "HIW",
        "cousins": "CUZ",
        "brandywine": "BDN",
        "paramount": "PGRE",
        "city": "CIO",
        "office": "OPI",
        "franklin": "FSP",
        "easterly": "DEA",
        "corporate": "OFC",
        "jbg": "JBGS",
        "service": "SVC",
        "pebble": "PEB",
        "host": "HST",
        "park": "PK",
        "sunstone": "SHO",
        "diamond": "DRH",
        "xenia": "XHR",
        "rlj": "RLJ",
        "chatham": "CLDT",
        "hersha": "HT",
        "summit": "INN",
        "apple": "APLE",
        "braemar": "BHR",
        "ashford": "AHT",
        "corepoint": "CPLG",
        "condor": "CDOR",
        "sotherly": "SOHO",
        "ryman": "RHP",
        "gaming": "GLPI",
        "vici": "VICI",
        "mgm": "MGP",
        "iron": "IRM",
        "lamar": "LAMR",
        "outfront": "OUT",
        "geo": "GEO",
        "corecivic": "CXW",
        "potlatch": "PCH",
        "rayonier": "RYN",
        "weyerhaeuser": "WY",
        "catchmark": "CTT",
        "gladstone": "LAND",
        "farmland": "FPI",
        "innovative": "IIPR",
        "postal": "PSTL",
        "safestore": "SAFE",
        "big": "BIG",
        "cube": "CUBE",
        "extra": "EXR",
        "life": "LSI",
        "national": "NSA",
        "public": "PSA",
        "global": "SELF",
        "jernigan": "JCAP"
    }
    
    clean_query = query.replace(" ", "").lower()
    if clean_query in common_map:
        ticker = common_map[clean_query]
        # Return immediately if found in map, pretending it's a valid search result
        return [{
            "symbol": ticker,
            "name": query.capitalize(), # Best guess display name
            "exchange": "US (Mapped)",
            "type": "EQUITY"
        }]

    # 2. General Naver Search (Good for "Name -> Ticker" discovery)
    # Checks for "팔랑티어 주가" -> "팔란티어 테크놀로지스 (PLTR)"
    candidates = []
    if re.search("[가-힣]", query):
        candidates = search_naver_general(query)
        if candidates:
            return candidates
        
        # 3. Naver Finance Search (Best for Korean codes 005930)
        candidates = search_naver_finance(query)
        if candidates:
            return candidates
            
    # 4. Yahoo Finance (Best for English)
    return search_yahoo_finance(query)

def search_naver_general(query: str) -> List[Dict[str, str]]:
    """
    Searches 'query + 주가' on Naver and looks for 'Company (Ticker)' pattern.
    """
    try:
        url = f"https://search.naver.com/search.naver?query={urllib.parse.quote(query + ' 주가')}"
        response = requests.get(
            url, 
            impersonate="chrome110",
            headers={"Referer": "https://www.naver.com/"}
        )
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        candidates = []
        # Pattern: Korean Name (Ticker) e.g., "팔란티어 테크놀로지스 (PLTR)"
        # This usually appears in 'span' or 'div' with specific classes, 
        # but regex on text is more robust against class changes.
        
        # Limit the search scope to plausible containers to avoid random text
        # The finance box usually has classes like 'spt_con', 'cs_stock', 'api_subject_bx'
        
        # Let's search all text nodes for the pattern "Name (TICKER)" 
        # where TICKER is 1-5 uppercase letters.
        
        text = soup.get_text(" ", strip=True)
        
        # Regex to find: Korean chars, space, (TICKER)
        # Note: simplistic, but works for "팔란티어 테크놀로지스 (PLTR)"
        matches = re.findall(r"([가-힣\s]+)\(([A-Z]{1,5})\)", text)
        
        seen = set()
        for name, ticker in matches:
            name = name.strip()
            if len(name) < 2: continue # Too short
            if ticker in seen: continue
            
            # Filter out common false positives if any (e.g. (KOSPI)) -> KOSPI is > 5 chars? No, 5.
            if ticker in ["KOSPI", "KOSDAQ", "KRX", "ETF", "ETN"]: continue
            
            seen.add(ticker)
            candidates.append({
                "symbol": ticker,
                "name": name,
                "exchange": "US (Detected)",
                "type": "EQUITY"
            })
            
            if len(candidates) >= 3: break
            
        return candidates

    except Exception as e:
        print(f"Naver General search failed: {e}")
        return []

def search_naver_finance(query: str) -> List[Dict[str, str]]:
    candidates = []
    try:
        # Naver requires EUC-KR encoding for the query
        encoded_query = urllib.parse.quote(query.encode('euc-kr'))
        url = f"https://finance.naver.com/search/searchList.naver?query={encoded_query}"
        
        # Do not manually set User-Agent if impersonating, but Naver might check Referer specifically
        # Let's try minimal headers with impersonate
        
        response = requests.get(
            url, 
            impersonate="chrome110",
            headers={"Referer": "https://finance.naver.com/"}
        )
        
        # Naver returns EUC-KR usually, but let's check content encoding
        # curl_cffi might decode utf-8 automatically but Naver is euc-kr.
        # We need to access .content and decode manually
        
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='euc-kr')
        
        # Select result rows
        rows = soup.select("td.tit")
        
        for row in rows[:5]: # Top 5
            link = row.find('a')
            if not link: continue
            
            name = link.get_text().strip()
            href = link['href']
            
            # Extract code from href (e.g., /item/main.naver?code=005930)
            match = re.search(r"code=(\d+)", href)
            if match:
                code = match.group(1)
                
                # Determine KOSPI (.KS) or KOSDAQ (.KQ)
                # We can check the next column or sidebar, but for now let's guess.
                # Usually checking Yahoo is best, but let's assume .KS effectively or search yahoo with code.
                
                # Naver search results table structure:
                # <tr> <td class="tit">...</td> <td class="sale">...</td> ... </tr>
                # It doesn't explicitly say Market in this table easily.
                
                # Robust way: Check Yahoo for code.KS and code.KQ
                # Optimized way: Assume .KS (KOSPI) is most common for major stocks users search.
                # However, many tech stocks are KOSDAQ.
                
                # Let's try to verify with Yahoo Search using the code
                yh_candidates = search_yahoo_finance(code)
                if yh_candidates:
                     candidates.extend(yh_candidates)
                else:
                    # Fallback to .KS and .KQ blind addition if detailed search fails
                    candidates.append({
                        "symbol": f"{code}.KS",
                        "name": name,
                        "exchange": "KOSPI (Guessed)",
                        "type": "EQUITY"
                    })
        
        # Remove duplicates based on symbol
        unique_candidates = []
        seen = set()
        for c in candidates:
            if c['symbol'] not in seen:
                seen.add(c['symbol'])
                unique_candidates.append(c)
                
        return unique_candidates

    except Exception as e:
        print(f"Naver search failed: {e}")
        return []

def search_yahoo_finance(query: str) -> List[Dict[str, str]]:
    url = "https://query1.finance.yahoo.com/v1/finance/search"
    
    # Minimal headers relying on impersonation
    headers = {
        "Referer": "https://finance.yahoo.com/",
    }
    
    params = {
        "q": query,
        "quotesCount": 10,
        "newsCount": 0,
        "enableFuzzyQuery": "false",
        "quotesQueryId": "tss_match_phrase_query"
    }

    try:
        response = requests.get(url, params=params, headers=headers, impersonate="chrome110", timeout=10)
        
        if response.status_code != 200:
            return []
            
        data = response.json()
        candidates = []
        if "quotes" in data:
            for quote in data["quotes"]:
                # We prioritize EQUITY and ETF
                quote_type = quote.get("quoteType", "")
                if quote_type not in ["EQUITY", "ETF"]:
                    continue
                
                symbol = quote.get("symbol")
                # Filter out garbage symbols if needed
                
                shortname = quote.get("shortname", "")
                longname = quote.get("longname", "")
                exchange = quote.get("exchDisp", "")
                name = longname if longname else shortname
                
                candidates.append({
                    "symbol": symbol,
                    "name": name,
                    "exchange": exchange,
                    "type": quote_type
                })
        return candidates

    except Exception as e:
        print(f"Yahoo search failed: {e}")
        return []

if __name__ == "__main__":
    # Test
    q = "삼성전자"
    print(f"Searching for {q}...")
    results = search_ticker(q)
    for r in results:
        print(r)
