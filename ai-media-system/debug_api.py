#!/usr/bin/env python3
# Debug: Check for API endpoints or hidden content
import os
import sys

sys.path.insert(0, 'skills/00-collector/geektime-collector')

from collector import GeektimeCollector
from dotenv import load_dotenv
import requests

load_dotenv()

collector = GeektimeCollector()
headers = collector.auth.get_headers()

# Try different API endpoints that Geektime might use
test_url = "https://time.geekbang.org/column/article/936334"

# Check main.js for API patterns
print("Testing various endpoints...\n")

# Try the service API
api_urls = [
    f"https://time.geekbang.org/serv/v1/article/{936334}",
    f"https://time.geekbang.org/serv/v1/column/articles/{936334}",
    f"https://time.geekbang.org/serv/v1/article/{936334}/content",
]

for url in api_urls:
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"URL: {url}")
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Content length: {len(resp.text)}")
            print(f"First 300 chars: {resp.text[:300]}")
        print("-" * 40)
    except Exception as e:
        print(f"Error: {e}")
        print("-" * 40)