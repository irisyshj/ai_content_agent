#!/usr/bin/env python3
# Debug: Find free articles or check article details
import os
import sys

sys.path.insert(0, 'skills/00-collector/geektime-collector')

from collector import GeektimeCollector
from dotenv import load_dotenv
import requests

load_dotenv()

collector = GeektimeCollector()
headers = collector.auth.get_headers()

# Try to find a free article - usually lower article IDs are older/free
print("Testing different article IDs for free content...\n")

# Try some known free articles
test_ids = ["1001", "1002", "1003", "1004", "1005", "2001", "2002", "3001", "4001", "5001"]

for article_id in test_ids:
    url = f"https://time.geekbang.org/serv/v1/article/{article_id}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            print(f"[{article_id}] Status: {resp.status_code} - Free article found!")
            data = resp.json()
            print(f"  Title: {data.get('article_title', 'N/A')}")
            print(f"  Content length: {len(data.get('article_content', ''))}")
            print()
    except:
        pass

print("\nTrying the original article with more debug info...")
# Try the original article
url = "https://time.geekbang.org/column/article/936334"
resp = requests.get(url, headers=headers, timeout=30)
print(f"Status: {resp.status_code}")

# Check if there's any content in the response
if "付费" in resp.text or "购买" in resp.text or "购买" in resp.text:
    print("Page indicates: 需要付费/购买")
elif "专栏" in resp.text:
    print("Page indicates: 专栏文章")
else:
    # Try to find any text content
    import re
    # Look for any visible text
    texts = re.findall(r'[\u4e00-\u9fff]{4,}', resp.text[:10000])
    print(f"Found Chinese text samples: {texts[:5]}")