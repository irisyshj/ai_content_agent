# Import from parent package using relative import
import sys
from pathlib import Path

# Ensure we can import from parent package
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from collector import GeektimeCollector
from models import Article
import pytest


@pytest.fixture
def sample_html_path():
    # Path relative to this test file
    return Path(__file__).parent / "fixtures" / "sample_article.html"


def test_collector_extracts_title(sample_html_path):
    collector = GeektimeCollector()
    with open(sample_html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    article = collector._parse_html(html, "http://test.com/article/123")
    assert article.title == "测试文章标题"


def test_collector_extracts_author(sample_html_path):
    collector = GeektimeCollector()
    with open(sample_html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    article = collector._parse_html(html, "http://test.com/article/123")
    assert article.author == "测试作者"


def test_collector_extracts_content(sample_html_path):
    collector = GeektimeCollector()
    with open(sample_html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    article = collector._parse_html(html, "http://test.com/article/123")
    assert "第一段内容" in article.content
    assert "第二段内容" in article.content


def test_collector_extracts_images(sample_html_path):
    collector = GeektimeCollector()
    with open(sample_html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    article = collector._parse_html(html, "http://test.com/article/123")
    assert len(article.images) == 1
    assert "test.jpg" in article.images[0]


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


def test_collect_from_url_simple_success(mocker):
    """Test collect_from_url_simple with mocked requests."""
    mock_response = type('obj', (object,), {
        'status_code': 200,
        'raise_for_status': lambda self: None,
        'text': '<html><body><h1 class="article-title">Test Title</h1><div class="article-content"><p>Test content</p></div></body></html>'
    })()

    mocker.patch('requests.get', return_value=mock_response)
    collector = GeektimeCollector()
    result = collector.collect_from_url_simple("https://example.com/test")

    assert result.success, f"Should succeed: {result.error}"
    assert result.article is not None
    assert result.article.title == "Test Title"
    assert "Test content" in result.article.content


def test_collect_from_url_simple_failure(mocker):
    """Test collect_from_url_simple handles errors gracefully."""
    import requests as req
    mocker.patch('requests.get', side_effect=req.exceptions.Timeout("Request timed out"))
    collector = GeektimeCollector()
    result = collector.collect_from_url_simple("https://example.com/test")

    assert not result.success, "Should fail on timeout"
    assert "Timeout" in result.error or "timed out" in result.error
