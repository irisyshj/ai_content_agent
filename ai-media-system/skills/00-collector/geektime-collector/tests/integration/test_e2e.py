import os
import sys
from pathlib import Path

# Ensure we can import from parent package
if str(Path(__file__).parent.parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from collector import GeektimeCollector

@pytest.mark.integration
def test_collect_article():
    """Integration test - requires valid GEEKTIME_COOKIE"""
    cookie = os.getenv("GEEKTIME_COOKIE")
    if not cookie:
        pytest.skip("GEEKTIME_COOKIE not set")

    collector = GeektimeCollector()
    result = collector.collect_from_url(
        "https://time.geekbang.org/column/article/438296"
    )

    assert result.success, f"Collection failed: {result.error}"
    assert result.article is not None
    assert result.article.title != ""
    assert len(result.article.content) > 100
    assert result.article.id == "438296"

def test_invalid_url():
    collector = GeektimeCollector()
    result = collector.collect_from_url("https://example.com/not-geektime")
    # Should handle gracefully - either fail with clear error or succeed with empty content
    assert result.article is None or result.article.title == ""
