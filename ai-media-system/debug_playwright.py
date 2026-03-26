#!/usr/bin/env python3
# Use Playwright to get dynamic content
import os
import sys
import json

# Add project path
sys.path.insert(0, 'skills/00-collector/geektime-collector')

from collector import GeektimeCollector
from dotenv import load_dotenv

load_dotenv()

print("Testing with Playwright (headless browser)...\n")

# Use Playwright to render JavaScript
try:
    from playwright.sync_api import sync_playwright

    collector = GeektimeCollector()
    headers = collector.auth.get_headers()
    cookies = collector.auth.cookie

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=headers.get('User-Agent')
        )

        # Add cookies
        if cookies:
            # Parse cookies
            cookie_dict = {}
            for item in cookies.split(';'):
                if '=' in item:
                    key, val = item.strip().split('=', 1)
                    cookie_dict[key] = val

            # Add cookies to context
            for name, value in cookie_dict.items():
                context.add_cookies([{
                    'name': name,
                    'value': value,
                    'domain': '.geekbang.org',
                    'path': '/'
                }])

        page = context.new_page()

        # Navigate to article
        url = "https://time.geekbang.org/column/article/936334"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=60000)

        # Wait for content to load
        page.wait_for_timeout(3000)

        # Get title
        title = page.title()
        print(f"Page title: {title}")

        # Try to find article content
        # Look for common selectors
        selectors = [
            '.article-content',
            '.article-title',
            'article',
            '.content',
            '.text-content',
            '#app',
            '.main-content'
        ]

        content_found = False
        for selector in selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    text = element.inner_text()
                    if text and len(text) > 50:
                        print(f"\n[Found] Selector: {selector}")
                        print(f"Content preview: {text[:500]}...")
                        content_found = True
                        break
            except:
                pass

        if not content_found:
            # Get all text
            body_text = page.evaluate("document.body.innerText")
            print(f"\nBody text preview: {body_text[:500]}...")

        browser.close()

except ImportError as e:
    print(f"Playwright not installed: {e}")
    print("\nTo install:")
    print("  pip install playwright")
    print("  playwright install chromium")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()