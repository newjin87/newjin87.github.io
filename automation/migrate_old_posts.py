import os
import re
from pathlib import Path
import yaml

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
POSTS_DIR = BASE_DIR / "_posts"

# Categorization Rules (Keyword -> (Category, Tags))
RULES = {
    # 1. Jekyll & Blogging
    r"(jekyll|blog|seo|markdown|github|page|static)": ("Dev-Log", ["Jekyll", "Blog-Setup", "GitHub-Pages"]),
    
    # 2. Mac & Tech Tools
    r"(mac|apple|iphone|ipad|keynote|mirroring|facetime|missioncontrol|shortcut|usbc|todoist|naver)": ("Tech-Tips", ["Mac", "Productivity", "IT-Tools"]),
    
    # 3. Travel
    r"(travel|trip|tour|여행|호치민|베트남|vietnam)": ("Travel", ["Trip", "Vietnam", "Life"]),
    
    # 4. Investment (Future proof)
    r"(invest|stock|market|trade|주식|투자|경제)": ("Stock-Analysis", ["Investment", "Economy"]),
}

def analyze_content(title, filename):
    """Determine category and tags based on title/filename"""
    text = (title + " " + filename).lower()
    
    for pattern, (category, tags) in RULES.items():
        if re.search(pattern, text):
            return category, tags
            
    return "Daily-Log", ["General"]

def migrate_post(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find Front Matter
    front_matter_pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.search(front_matter_pattern, content, re.DOTALL)
    
    if not match:
        print(f"⚠️ Skipping (No Front Matter): {file_path.name}")
        return

    fm_text = match.group(1)
    body = match.group(2)
    
    try:
        # Load YAML safely
        fm = yaml.safe_load(fm_text)
        if not fm: fm = {}
    except Exception as e:
        print(f"❌ Error parsing YAML for {file_path.name}: {e}")
        return

    # --- Update Logic ---
    original_cat = fm.get('categories', [])
    if isinstance(original_cat, str):
        original_cat = [original_cat]
    
    original_tags = fm.get('tags', [])
    if isinstance(original_tags, str):
        original_tags = [original_tags]

    # Analyze Title/Filename
    title = fm.get('title', file_path.stem)
    new_cat, new_tags_suggestions = analyze_content(title, file_path.stem)
    
    # Merge Tags (Keep valid old ones, add new ones)
    # Filter out generic 'jekyll' if we are adding 'Jekyll' tag
    final_tags = set(original_tags)
    for t in new_tags_suggestions:
        final_tags.add(t)
    
    # Standardize Category
    # If old category exists, we might want to keep it or map it.
    # For now, let's enforce our new structure as primary.
    # But preserve 'travel' if it was explicitly set.
    
    # Simpler approach: Overwrite 'categories' with our standardized one
    fm['categories'] = [new_cat]
    
    # Convert set back to list for YAML
    fm['tags'] = list(final_tags)
    
    # Remove old capital 'Categories' if it exists (handling case sensitivity)
    keys_to_delete = [k for k in fm.keys() if k.lower() == 'categories' and k != 'categories']
    for k in keys_to_delete:
        del fm[k]

    # Reconstruct File
    print(f"✅ Migrating: {file_path.name}")
    print(f"   -> Category: {fm['categories']}")
    print(f"   -> Tags: {fm['tags']}")
    
    new_fm_text = yaml.dump(fm, default_flow_style=None, allow_unicode=True, sort_keys=False)
    new_content = f"---\n{new_fm_text}---\n{body}"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    print("🚀 Starting Blog Post Migration (Retro-Categorization)...")
    
    if not POSTS_DIR.exists():
        print(f"❌ Posts directory not found: {POSTS_DIR}")
        return

    count = 0
    for file_path in POSTS_DIR.glob("*.md"):
        migrate_post(file_path)
        count += 1
        
    print(f"\n🎉 Migration Complete! Processed {count} posts.")

if __name__ == "__main__":
    main()
