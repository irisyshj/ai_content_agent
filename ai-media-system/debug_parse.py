#!/usr/bin/env python3
# Debug: Check Playwright rendered HTML structure
import sys
sys.path.insert(0, 'skills/00-collector/geektime-collector')

from collector import GeektimeCollector
from dotenv import load_dotenv
load_dotenv()

collector = GeektimeCollector()
result = collector._collect_with_playwright("https://time.geekbang.org/column/article/936334")

if result.success:
    print("=== Raw HTML ===")
    print(result.article.content[:2000] if result.article.content else "(empty)")

    # Try to find what's actually in the HTML
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(result.article.content or "<html></html>", 'html.parser')

    print("\n=== Available CSS Classes ===")
    classes = set()
    for elem in soup.find_all(class_=True):
        classes.update(elem.get('class', []))
    print(sorted(classes)[:50])

    print("\n=== h1 tags ===")
    for h1 in soup.find_all('h1')[:5]:
        print(f"  {h1.get('class')}: {h1.get_text()[:50]}")

    print("\n=== div.article ===")
    article = soup.find('div', class_='article')
    if article:
        print(f"Found div.article: {article.get_text()[:200]}")
    else:
        print("No div.article found")
        # Try to find any content
        print("\n=== Any large text blocks ===")
        for div in soup.find_all('div')[:10]:
            text = div.get_text(strip=True)
            if len(text) > 100:
                print(f"  class={div.get('class')}: {text[:100]}")
else:
    print(f"Error: {result.error}")
