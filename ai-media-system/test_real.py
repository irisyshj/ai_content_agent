#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test real Geektime article collection
Configure GEEKTIME_COOKIE in .env file before running
"""
import os
import sys
import json

# Add project path
sys.path.insert(0, 'skills/00-collector/geektime-collector')

try:
    from collector import GeektimeCollector
    from dotenv import load_dotenv

    load_dotenv()

    cookie = os.getenv("GEEKTIME_COOKIE")
    if not cookie or cookie.strip() == "":
        print("[ERROR] GEEKTIME_COOKIE not configured")
        print()
        print("How to configure Cookie:")
        print("1. Open browser and login to https://time.geekbang.org")
        print("2. Press F12 to open DevTools")
        print("3. Switch to Network tab")
        print("4. Refresh page, find any request")
        print("5. Copy Cookie value from Request Headers")
        print("6. Edit .env file, paste after GEEKTIME_COOKIE=")
        print()
        print("After configuration, run this script again")
        sys.exit(1)

    print("[OK] Cookie configured")
    print("Starting collection test...")

    collector = GeektimeCollector()

    # Test article: user specified article
    test_url = "https://time.geekbang.org/column/article/936334"

    print(f"Target: {test_url}")
    print()

    result = collector.collect_from_url(test_url)

    if result.success:
        article = result.article
        print("=" * 60)
        print("[SUCCESS] Collection completed!")
        print("=" * 60)
        print(f"Title: {article.title}")
        print(f"Author: {article.author}")
        print(f"ID: {article.id}")
        print()
        print(f"Content preview:")
        print("-" * 40)
        preview = article.content[:200] + "..." if len(article.content) > 200 else article.content
        print(preview)
        print()
        print(f"Images: {len(article.images)}")
        if article.images:
            print("Image list:")
            for i, img in enumerate(article.images[:3], 1):
                print(f"  {i}. {img}")
            if len(article.images) > 3:
                print(f"  ... {len(article.images) - 3} more images")
        print()
        print("=" * 60)

        # JSON output
        print("[JSON] Output:")
        print("-" * 40)
        print(json.dumps(article.to_dict(), ensure_ascii=False, indent=2))

    else:
        print("=" * 60)
        print("[FAILED] Collection failed")
        print("=" * 60)
        print(f"Error: {result.error}")
        print()
        print("Possible reasons:")
        print("1. Cookie expired - get fresh cookie")
        print("2. Article requires paid subscription")
        print("3. Network issue")

except Exception as e:
    print(f"[ERROR] Program error: {e}")
    import traceback
    traceback.print_exc()
