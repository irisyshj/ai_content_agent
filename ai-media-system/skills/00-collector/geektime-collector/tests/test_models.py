# Import from parent package using relative import
import sys
from pathlib import Path

# Ensure we can import from parent package
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Article, VideoInfo, CollectionResult

def test_article_creation():
    article = Article(
        id="test-123",
        type="geektime",
        url="https://time.geekbang.org/column/article/123",
        title="Test Article",
        author="Test Author",
        content="Test content",
        images=["https://example.com/img1.jpg"]
    )
    assert article.id == "test-123"
    assert article.type == "geektime"
    assert len(article.images) == 1

def test_article_with_video():
    video = VideoInfo(
        url="https://example.com/video.mp4",
        transcript="This is a transcript"
    )
    article = Article(
        id="test-456",
        type="geektime",
        url="https://time.geekbang.org/column/article/456",
        title="Video Article",
        author="Test Author",
        content="Content",
        video=video
    )
    assert article.video.transcript == "This is a transcript"

def test_collection_result_success():
    article = Article(
        id="test-789",
        type="geektime",
        url="https://time.geekbang.org/column/article/789",
        title="Success Article"
    )
    result = CollectionResult(success=True, article=article)
    assert result.success is True
    assert result.article is not None
    assert result.article.id == "test-789"
    assert result.error is None

def test_collection_result_failure():
    result = CollectionResult(
        success=False,
        error="Failed to fetch article"
    )
    assert result.success is False
    assert result.article is None
    assert result.error == "Failed to fetch article"

def test_article_to_dict():
    article = Article(
        id="test-101",
        type="geektime",
        url="https://time.geekbang.org/column/article/101",
        title="Test Dict Article",
        author="Test Author",
        content="Test content for to_dict",
        images=["https://example.com/img1.jpg", "https://example.com/img2.jpg"]
    )
    result = article.to_dict()
    assert result["id"] == "test-101"
    assert result["type"] == "geektime"
    assert result["url"] == "https://time.geekbang.org/column/article/101"
    assert result["title"] == "Test Dict Article"
    assert result["author"] == "Test Author"
    assert result["content"] == "Test content for to_dict"
    assert len(result["images"]) == 2
    assert "collected_at" in result

def test_article_to_dict_with_video():
    video = VideoInfo(
        url="https://example.com/video.mp4",
        transcript="Video transcript",
        duration=120
    )
    article = Article(
        id="test-102",
        type="geektime",
        url="https://time.geekbang.org/column/article/102",
        title="Video Test",
        video=video
    )
    result = article.to_dict()
    assert "video" in result
    assert result["video"]["url"] == "https://example.com/video.mp4"
    assert result["video"]["transcript"] == "Video transcript"
    assert result["video"]["duration"] == 120

def test_article_to_dict_with_metadata():
    article = Article(
        id="test-103",
        type="geektime",
        url="https://time.geekbang.org/column/article/103",
        title="Metadata Test",
        metadata={"key1": "value1", "key2": 123}
    )
    result = article.to_dict()
    assert "metadata" in result
    assert result["metadata"]["key1"] == "value1"
    assert result["metadata"]["key2"] == 123
