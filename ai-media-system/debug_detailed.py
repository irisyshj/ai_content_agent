#!/usr/bin/env python3
# Check what the actual response contains more carefully
import os
import sys
import re

sys.path.insert(0, 'skills/00-collector/geektime-collector')

from dotenv import load_dotenv
import requests

load_dotenv()

# Get cookie from .env
cookie = os.getenv("GEEKTIME_COOKIE")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Cookie": cookie,
    "Referer": "https://time.geekbang.org/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

url = "https://time.geekbang.org/column/article/936334"
resp = requests.get(url, headers=headers, timeout=30)

print(f"Status: {resp.status_code}")
print(f"Headers: {dict(resp.headers)}")

# Check if content is JSON
content_type = resp.headers.get('Content-Type', '')
print(f"Content-Type: {content_type}")

# Try to find any data in the response
text = resp.text

# Look for JSON data in script tags
json_pattern = r'<script[^>]*>(.*?)</script>'
scripts = re.findall(json_pattern, text, re.DOTALL)

print(f"\nFound {len(scripts)} script tags")

# Look for API calls or data
for i, script in enumerate(scripts[:3]):
    if 'article' in script.lower() or 'content' in script.lower() or 'data' in script.lower():
        print(f"\n--- Script {i} (contains relevant keywords) ---")
        # Print first 500 chars
        print(script[:500])

# Check for any hidden content or API endpoints
api_pattern = r'/serv/v[0-9]+/[a-z]+/[0-9]+'
api_matches = re.findall(api_pattern, text)
print(f"\nAPI patterns found: {api_matches}")

# Try to find any text content directly in HTML
text_content = re.findall(r'>([^<>]{10,200})<', text)
print(f"\nText content found: {text_content[:10]}")