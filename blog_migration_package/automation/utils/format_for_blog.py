import os
import re
from datetime import datetime
from pathlib import Path

# 설정
TODAY = datetime.now().strftime("%Y-%m-%d")
SOURCE_DIR = Path(f"analysis_result/{TODAY}")
BLOG_POSTS_DIR = Path("_posts")  # GitHub Actions에서 실행될 때는 루트 기준 _posts 폴더

def format_and_move():
    if not SOURCE_DIR.exists():
        print(f"❌ No analysis found for {TODAY}")
        return

    BLOG_POSTS_DIR.mkdir(exist_ok=True, parents=True)

    # 정의: (소스 파일명 접미사, 제목 템플릿, 카테고리, 태그, 언어코드)
    configs = [
        ("_analysis_macro_Economy_KR.md", "🌍 {date} 글로벌 거시경제 브리핑", ["Macro", "Economy"], ["Global", "Market", "Analysis"], ""),
        ("_analysis_macro_Economy_EN.md", "🌍 {date} Global Macro Briefing", ["Macro", "Economy"], ["Global", "Market", "Analysis"], "-en"),
        ("_Korea_Market_Strategy_KR.md", "🇰🇷 {date} 한국 시장 투자 전략", ["Korea", "Strategy"], ["KOSPI", "RealEstate", "AI"], "-kr"),
        ("_Korea_Market_Strategy_EN.md", "🇰🇷 {date} Korea Market Strategy", ["Korea", "Strategy"], ["KOSPI", "RealEstate", "AI"], "-en"),
    ]

    for suffix, title_template, categories, tags, lang_suffix in configs:
        source_file = SOURCE_DIR / f"{TODAY}{suffix}"
        
        if source_file.exists():
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()

            title = title_template.format(date=TODAY)
            
            # Front Matter
            # Use distinct filenames to avoid collision if titles are similar, though date prefix helps
            # Jekyll format: YYYY-MM-DD-title.md
            
            clean_title = title.replace(" ", "-").replace("🌍", "Global").replace("🇰🇷", "Korea").replace("_", "-")
            clean_title = re.sub(r'[^\w\-\.]', '', clean_title) # Remove emojis and special chars
            
            target_filename = f"{TODAY}-{clean_title}{lang_suffix}.md"
            target_path = BLOG_POSTS_DIR / target_filename
            
            blog_content = f"""---
layout: post
title: "{title}"
date: {TODAY} 09:00:00 +0900
categories: {categories}
tags: {tags}
---

{content}
"""
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(blog_content)
            print(f"✅ Created Blog Post: {target_path}")

if __name__ == "__main__":
    format_and_move()
