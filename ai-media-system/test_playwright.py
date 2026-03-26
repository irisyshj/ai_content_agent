#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test real Geektime article collection using Playwright
"""
import os
import sys
import json

sys.path.insert(0, 'skills/00-collector/geektime-collector')

from dotenv import load_dotenv
load_dotenv()

print("Starting Playwright-based collection test...")

try:
    from playwright.sync_api import sync_playwright

    # Get cookie from env
    cookie_str = os.getenv("GEEKTIME_COOKIE", "")
    user_agent = os.getenv("GEEKTIME_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=user_agent)

        # Parse and set cookies
        if cookie_str:
            for item in cookie_str.split(';'):
                item = item.strip()
                if '=' in item:
                    name, value = item.split('=', 1)
                    name = name.strip()
                    value = value.strip()
                    if name and value:
                        try:
                            context.add_cookies([{
                                'name': name,
                                'value': value,
                                'domain': '.geekbang.org',
                                'path': '/'
                            }])
                        except:
                            pass

        page = context.new_page()

        # Navigate
        url = "https://time.geekbang.org/column/article/936334"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=60000)

        # Wait for Vue to render
        page.wait_for_timeout(3000)

        # Get page title
        title = page.title()
        print(f"Page title: {title}")

        # Try to find article content
        selectors_to_try = [
            '.article-title',
            '.article-content',
            '.article-text',
            'article',
            '.content',
            '.text-content',
            '.rich_media_content',
            '[class*="article"]',
            '[class*="content"]',
        ]

        content_found = False
        for selector in selectors_to_try:
            try:
                elements = page.query_selector_all(selector)
                for elem in elements:
                    text = elem.inner_text()
                    if text and len(text) > 100:
                        print(f"\n[SUCCESS] Found content with selector: {selector}")
                        print(f"Content length: {len(text)} chars")
                        print(f"Preview: {text[:500]}...")
                        content_found = True
                        break
                if content_found:
                    break
            except Exception as e:
                continue

        if not content_found:
            # Try to get all text
            print("\nNo specific content found, trying to get body text...")
            body_text = page.evaluate("document.body.innerText")
            print(f"Body text length: {len(body_text)}")
            print(f"Preview: {body_text[:500]}...")

        # Try to get any images
        images = page.query_selector_all('img')
        print(f"\nFound {len(images)} images on page")
        for i, img in enumerate(images[:5]):
            src = img.get_attribute('src')
            if src:
                print(f"  Image {i+1}: {src[:100]}")

        browser.close()
        print("\n[OK] Collection test completed")

except ImportError:
    print("[ERROR] Playwright not installed")
    print("Run: pip install playwright && playwright install chromium")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
