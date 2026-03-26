# CDP Integration for Dynamic Content Collection

> Design for adding Playwright/Chrome CDP support to handle JavaScript-rendered pages

---

## Context

The existing `geektime-collector` skill uses `requests` + `BeautifulSoup` for content extraction. However, Geektime (and many modern sites) use Vue.js for dynamic content rendering, which returns empty content through plain HTTP requests.

**Solution:** Integrate Playwright (Chrome CDP) for dynamic content extraction.

---

## Design

### Architecture

```
GeektimeCollector
├── _collect_with_requests()  # Original: requests + BeautifulSoup
├── _collect_with_playwright() # New: Playwright for dynamic content
└── collect_from_url(url, use_browser=True)  # Main API
```

### Changes to `collector.py`

| Addition | Description |
|----------|-------------|
| `_collect_with_playwright(url)` | Private method using Playwright to extract content |
| `collect_from_url_simple(url)` | Public method using requests (backup) |
| `collect_from_url(url, use_browser=True)` | Main method, defaults to Playwright |

### API Signature

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
```

### Playwright Method

```python
def _collect_with_playwright(self, url: str) -> CollectionResult:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=self.auth.user_agent)

        # Set cookies from auth
        if self.auth.cookie:
            for item in self.auth.cookie.split(';'):
                item = item.strip()
                if '=' in item:
                    name, value = item.split('=', 1)
                    context.add_cookies([{
                        'name': name.strip(),
                        'value': value.strip(),
                        'domain': '.geekbang.org',
                        'path': '/'
                    }])

        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=60_000)
        page.wait_for_timeout(2000)  # Wait for Vue to render

        html = page.content()
        article = self._parse_html(html, url)

        browser.close()
        return CollectionResult(success=True, article=article)
```

### Error Handling

| Scenario | Behavior |
|----------|----------|
| Playwright not installed | Return error with install instructions |
| Page load timeout | Return error with timeout message |
| No content found | Return article with empty content |
| Cookie not set | Log warning, try anyway |

---

## File Changes

| File | Change |
|------|--------|
| `collector.py` | Add Playwright methods |
| `test_collector.py` | Add Playwright tests |
| `requirements.txt` | Add `playwright` (already present) |

---

## Testing

### Unit Tests
- `test_collect_with_requests()` - Existing functionality
- `test_collect_with_playwright()` - New functionality
- `test_collect_from_url_with_browser_flag()` - Parameter test

### Integration Test
- `test_collect_real_geektime_article()` - Against real article

---

## Dependencies

Already in `requirements.txt`:
```
playwright==1.40.0
beautifulsoup4==4.12.2
requests==2.31.0
```

---

## Success Criteria

1. ✅ Can collect article from Geektime using Playwright
2. ✅ `collect_from_url()` defaults to browser mode
3. ✅ `collect_from_url_simple()` uses requests fallback
4. ✅ All 14 existing tests continue to pass
5. ✅ New tests for Playwright integration pass

---

## Notes

- Playwright is already installed from earlier setup
- Browser launches headless (no UI)
- Cookie parsing follows same format as existing auth handler
- 2-second wait after page load for Vue hydration
