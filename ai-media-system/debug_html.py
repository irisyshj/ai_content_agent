#!/usr/bin/env python3
# Debug: fetch HTML and analyze structure
import os
import sys

sys.path.insert(0, 'skills/00-collector/geektime-collector')

from collector import GeektimeCollector
from dotenv import load_dotenv
import requests

load_dotenv()

collector = GeektimeCollector()
headers = collector.auth.get_headers()

test_url = "https://time.geekbang.org/column/article/936334"
response = requests.get(test_url, headers=headers, timeout=30)

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print()
print("=" * 60)
print("First 5000 chars of HTML:")
print("=" * 60)
print(response.text[:5000])