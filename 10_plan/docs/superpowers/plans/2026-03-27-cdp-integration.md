# CDP Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Playwright/Chrome CDP support to GeektimeCollector for handling JavaScript-rendered pages.

**Architecture:** Add Playwright methods to existing collector.py. Keep requests fallback. Default to browser mode.

**Tech Stack:** Python 3.9+, Playwright, BeautifulSoup, requests

---

## Task 1: Add Playwright Method

**Files:**
- Modify: `ai-media-system/skills/00-collector/geektime-collector/collector.py`

- [ ] **Step 1: Read current collector.py**

Read `collector.py` to understand the current structure and imports.

- [ ] **Step 2: Add _collect_with_playwright method**

Add this method to the `GeektimeCollector` class, after `_extract_article_id`:

```python
def _collect_with_playwright(self, url: str) -> CollectionResult:
    """
    Collect article using Playwright for JavaScript-rendered pages.

    Args:
        url: The article URL to collect from

    Returns:
        CollectionResult with the article or error message
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return CollectionResult(
            success=False,
            error="Playwright not installed. Run: pip install playwright && playwright install chromium"
        )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=self.auth.user_agent
            )

            # Set cookies from auth
            if self.auth.cookie:
                for item in self.auth.cookie.split(';'):
                    item = item.strip()
                    if '=' in item:
                        parts = item.split('=', 1)
                        name = parts[0].strip()
                        value = parts[1].strip()
                        if name and value:
                            try:
                                context.add_cookies([{
                                    'name': name,
                                    'value': value,
                                    'domain': '.geekbang.org',
                                    'path': '/'
                                }])
                            except Exception:
                                pass

            page = context.new_page()
            page.goto(url, wait_until="networkidle", timeout=60_000)
            page.wait_for_timeout(2000)  # Wait for Vue to render

            html = page.content()
            article = self._parse_html(html, url)

            browser.close()
            return CollectionResult(success=True, article=article)

    except Exception as e:
        return CollectionResult(
            success=False,
            error=f"Playwright collection failed: {str(e)}"
        )
```

- [ ] **Step 3: Add collect_from_url_simple method**

Add this method after `collect_from_url`:

```python
def collect_from_url_simple(self, url: str) -> CollectionResult:
    """
    Collect article using requests (no browser).

    Args:
        url: The article URL to collect from

    Returns:
        CollectionResult with the article or error message
    """
    try:
        import requests
        headers = self.auth.get_headers()

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        article = self._parse_html(response.text, url)

        return CollectionResult(success=True, article=article)

    except Exception as e:
        return CollectionResult(
            success=False,
            error=str(e)
        )
```

- [ ] **Step 4: Update collect_from_url to use browser by default**

Modify `collect_from_url` method signature:

```python
def collect_from_url(self, url: str, use_browser: bool = True) -> CollectionResult:
    """
    Collect article from a given URL.

    Args:
        url: The article URL to collect from
        use_browser: If True (default), use Playwright for dynamic content.
                     If False, use requests for simple pages.

    Returns:
        CollectionResult with the article or error message
    """
    if use_browser:
        return self._collect_with_playwright(url)
    else:
        return self.collect_from_url_simple(url)
```

- [ ] **Step 5: Run existing tests to ensure no regression**

Run: `cd ai-media-system && python -m pytest skills/00-collector/geektime-collector/tests/ -v`

Expected: All existing tests still pass

- [ ] **Step 6: Commit**

```bash
git add skills/00-collector/geektime-collector/collector.py
git commit -m "feat: add Playwright support for dynamic content"
```

---

## Task 2: Add Playwright Tests

**Files:**
- Modify: `ai-media-system/skills/00-collector/geektime-collector/tests/test_collector.py`

- [ ] **Step 1: Add test for collect_from_url with browser flag**

Add these tests to `test_collector.py`:

```python
def test_collect_from_url_with_browser_flag():
    """Test that collect_from_url accepts use_browser parameter."""
    collector = GeektimeCollector()

    # Test that method accepts the parameter (will fail without browser)
    # This tests the API, not the actual collection
    import inspect
    sig = inspect.signature(collector.collect_from_url)
    params = list(sig.parameters.keys())
    assert 'use_browser' in params, "collect_from_url should accept use_browser parameter"


def test_collect_from_url_simple_exists():
    """Test that collect_from_url_simple method exists."""
    collector = GeektimeCollector()
    assert hasattr(collector, 'collect_from_url_simple'), \
        "Collector should have collect_from_url_simple method"


def test_collect_with_playwright_exists():
    """Test that _collect_with_playwright method exists."""
    collector = GeektimeCollector()
    assert hasattr(collector, '_collect_with_playwright'), \
        "Collector should have _collect_with_playwright method"
```

- [ ] **Step 2: Run new tests**

Run: `cd ai-media-system && python -m pytest skills/00-collector/geektime-collector/tests/test_collector.py -v`

Expected: All new tests pass

- [ ] **Step 3: Commit**

```bash
git add skills/00-collector/geektime-collector/tests/test_collector.py
git commit -m "test: add Playwright integration tests"
```

---

## Task 3: Integration Test

**Files:**
- Modify: `ai-media-system/skills/00-collector/geektime-collector/tests/integration/test_e2e.py`

- [ ] **Step 1: Add Playwright integration test**

Add this test to `test_e2e.py`:

```python
@pytest.mark.integration
def test_collect_with_playwright():
    """Integration test using Playwright for dynamic content."""
    from geektime_collector import GeektimeCollector

    collector = GeektimeCollector()

    # This test requires actual browser
    result = collector.collect_from_url(
        "https://time.geekbang.org/column/article/936334",
        use_browser=True
    )

    assert result.success, f"Collection failed: {result.error}"
    assert result.article is not None
    assert result.article.id == "936334"
    # With browser, we should get content
    assert len(result.article.content) > 0, "Should get content with browser"


@pytest.mark.integration
def test_collect_from_url_simple_with_mock():
    """Test simple collection without browser using mock."""
    from unittest.mock import patch
    from geektime_collector import GeektimeCollector

    collector = GeektimeCollector()

    mock_response = type('obj', (object,), {
        'status_code': 200,
        'raise_for_status': lambda self: None,
        'text': '<html><h1>Test</h1><p>Content</p></html>'
    })()

    with patch('requests.get', return_value=mock_response):
        result = collector.collect_from_url_simple("https://example.com/test")

    assert result.success
    assert result.article is not None
```

- [ ] **Step 2: Run integration tests**

Run: `cd ai-media-system && python -m pytest skills/00-collector/geektime-collector/tests/integration/test_e2e.py -v -m integration`

Expected: Tests pass or skip if Playwright not available

- [ ] **Step 3: Commit**

```bash
git add skills/00-collector/geektime-collector/tests/integration/test_e2e.py
git commit -m "test: add Playwright integration tests"
```

---

## Task 4: Update test_real.py with Playwright

**Files:**
- Modify: `ai-media-system/test_real.py`

- [ ] **Step 1: Update test_real.py to use Playwright**

Replace the content with:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test real Geektime article collection with Playwright
"""
import os
import sys
import json

sys.path.insert(0, 'skills/00-collector/geektime-collector')

from dotenv import load_dotenv
load_dotenv()

def test_real_collection():
    from collector import GeektimeCollector

    print("[INFO] Starting collection with Playwright...")
    print()

    collector = GeektimeCollector()

    # Test article: user specified article
    test_url = "https://time.geekbang.org/column/article/936334"

    print(f"Target: {test_url}")
    print()

    # Use browser mode (default)
    result = collector.collect_from_url(test_url, use_browser=True)

    if result.success:
        article = result.article
        print("=" * 60)
        print("[SUCCESS] Collection completed!")
        print("=" * 60)
        print(f"Title: {article.title}")
        print(f"Author: {article.author}")
        print(f"ID: {article.id}")
        print()
        print(f"Content length: {len(article.content)} chars")
        print()
        print(f"Content preview:")
        print("-" * 40)
        preview = article.content[:300] + "..." if len(article.content) > 300 else article.content
        print(preview)
        print()
        print(f"Images: {len(article.images)}")
        if article.images:
            print("Image list:")
            for i, img in enumerate(article.images[:3], 1):
                print(f"  {i}. {img}")
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

if __name__ == "__main__":
    test_real_collection()
```

- [ ] **Step 2: Run test_real.py**

Run: `cd ai-media-system && python test_real.py`

Expected: Successfully collect article content

---

## Verification Steps

After all tasks complete:

- [ ] **Step 1: Run all tests**

```bash
cd ai-media-system
python -m pytest skills/00-collector/geektime-collector/tests/ -v
```

Expected: All tests pass (existing + new)

- [ ] **Step 2: Test with Playwright**

```bash
cd ai-media-system
python test_real.py
```

Expected: Article content successfully extracted

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "chore: complete CDP integration"
```

---

## Summary

This plan adds Playwright support to GeektimeCollector:
- ✅ `_collect_with_playwright()` - Private method using Playwright
- ✅ `collect_from_url_simple()` - Public method using requests
- ✅ `collect_from_url(use_browser=True)` - Default to browser
- ✅ New tests for Playwright integration
- ✅ Real article collection test

*Implementation Plan v1.0 - 2026-03-27*
