from bs4 import BeautifulSoup
import re
from typing import Optional
from urllib.parse import urljoin
from models import Article, CollectionResult
from auth import AuthHandler


class GeektimeCollector:
    def __init__(self, auth_handler: Optional[AuthHandler] = None):
        self.auth = auth_handler or AuthHandler()
        self.base_url = "https://time.geekbang.org"

    def _parse_html(self, html: str, url: str) -> Article:
        soup = BeautifulSoup(html, 'html.parser')

        # Extract title
        title_elem = soup.find('h1', class_='article-title') or soup.find('h1')
        title = title_elem.get_text(strip=True) if title_elem else ""

        # Extract author
        author_elem = soup.find('span', class_='author-name') or soup.find(class_='author')
        author = author_elem.get_text(strip=True) if author_elem else ""

        # Extract content
        content_elem = soup.find('div', class_='article-content') or soup.find('article')
        content = ""
        if content_elem:
            # Get all paragraphs
            paragraphs = content_elem.find_all('p')
            content = "\n\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

        # Extract images
        images = []
        if content_elem:
            for img in content_elem.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src:
                    # Convert relative URLs to absolute
                    absolute_url = urljoin(self.base_url, src)
                    images.append(absolute_url)

        # Generate ID from URL
        article_id = self._extract_article_id(url)

        return Article(
            id=article_id,
            type="geektime",
            url=url,
            title=title,
            author=author,
            content=content,
            images=images
        )

    def _extract_article_id(self, url: str) -> str:
        match = re.search(r'/article/(\d+)', url)
        if match:
            return match.group(1)
        return str(hash(url))  # Fallback

    def _collect_with_playwright(self, url: str) -> CollectionResult:
        """
        Collect article using Playwright for JavaScript-rendered pages.

        Args:
            url: The article URL to collect from

        Returns:
            CollectionResult with the article or error message
        """
        browser = None
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
                try:
                    page.goto(url, wait_until="networkidle", timeout=60_000)
                    page.wait_for_timeout(2000)  # Wait for Vue to render
                    html = page.content()
                    article = self._parse_html(html, url)
                finally:
                    page.close()
                    context.close()
                    browser.close()
                    browser = None

                return CollectionResult(success=True, article=article)

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            return CollectionResult(
                success=False,
                error=f"Playwright collection failed: {str(e)}\nTraceback:\n{tb}"
            )
        finally:
            if browser:
                browser.close()

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
            import traceback
            tb = traceback.format_exc()
            return CollectionResult(
                success=False,
                error=f"Requests collection failed: {str(e)}\nTraceback:\n{tb}"
            )

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
