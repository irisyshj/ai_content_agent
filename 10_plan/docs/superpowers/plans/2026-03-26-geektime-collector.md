# Geektime Collector Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code Skill that collects article content from Geektime courses, extracting text, images, and video transcripts into structured JSON output.

**Architecture:** A Python-based collector using Playwright for browser automation, Whisper for video transcription, and dataclasses for structured output. The skill integrates with Claude Code through a standard SKILL.md interface.

**Tech Stack:** Python 3.9+, Playwright, Whisper, dataclasses, pydantic

---

## Task 0: Project Initialization

**Files:**
- Create: `ai-media-system/requirements.txt`
- Create: `ai-media-system/.env.example`
- Create: `ai-media-system/config/collector_config.yaml`

- [ ] **Step 1: Create requirements.txt**

Create file with Python dependencies:

```txt
# ai-media-system/requirements.txt
playwright==1.40.0
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
openai-whisper==20231117
yt-dlp==2023.11.16
```

- [ ] **Step 2: Create .env.example**

```bash
# ai-media-system/.env.example
GEEKTIME_COOKIE=
GEEKTIME_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
PROXY_URL=
OUTPUT_DIR=./output
```

- [ ] **Step 3: Create config directory and YAML config**

```yaml
# ai-media-system/config/collector_config.yaml
collector:
  name: "geektime-collector"
  version: "1.0.0"

geektime:
  base_url: "https://time.geekbang.org"
  login_url: "https://account.geekbang.org/login"
  timeout: 30000
  retry: 3

output:
  format: "json"
  include_images: true
  include_video: true
  video_transcript: true

browser:
  headless: true
  user_agent: "${GEEKTIME_USER_AGENT}"
```

- [ ] **Step 4: Create base directory structure**

Run: `mkdir -p ai-media-system/skills/00-collector/geektime-collector/tests/fixtures`

- [ ] **Step 5: Commit**

```bash
git add requirements.txt .env.example config/collector_config.yaml
git commit -m "chore: initialize project structure and dependencies"
```

---

## Task 1: Data Models

**Files:**
- Create: `ai-media-system/skills/00-collector/geektime-collector/models.py`
- Create: `ai-media-system/skills/00-collector/geektime-collector/__init__.py`

- [ ] **Step 1: Write the failing test for data models**

Create `ai-media-system/skills/00-collector/geektime-collector/tests/test_models.py`:

```python
from geektime_collector.models import Article, VideoInfo, ContentSource

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ai-media-system && python -m pytest skills/00-collector/geektime-collector/tests/test_models.py -v`
Expected: `ModuleNotFoundError: No module named 'geektime_collector.models'`

- [ ] **Step 3: Implement data models**

Create `ai-media-system/skills/00-collector/geektime-collector/models.py`:

```python
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


@dataclass
class VideoInfo:
    url: str
    transcript: Optional[str] = None
    duration: Optional[int] = None  # in seconds


@dataclass
class Article:
    id: str
    type: str = "geektime"
    url: str = ""
    title: str = ""
    author: str = ""
    published_at: Optional[datetime] = None
    collected_at: datetime = field(default_factory=datetime.now)
    content: str = ""
    images: List[str] = field(default_factory=list)
    video: Optional[VideoInfo] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        result = {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "images": self.images,
            "collected_at": self.collected_at.isoformat()
        }
        if self.published_at:
            result["published_at"] = self.published_at.isoformat()
        if self.video:
            result["video"] = {
                "url": self.video.url,
                "transcript": self.video.transcript,
                "duration": self.video.duration
            }
        if self.metadata:
            result["metadata"] = self.metadata
        return result


@dataclass
class CollectionResult:
    success: bool
    article: Optional[Article] = None
    error: Optional[str] = None
```

- [ ] **Step 4: Create __init__.py**

Create `ai-media-system/skills/00-collector/geektime-collector/__init__.py`:

```python
from .models import Article, VideoInfo, CollectionResult

__all__ = ["Article", "VideoInfo", "CollectionResult"]
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ai-media-system && python -m pytest skills/00-collector/geektime-collector/tests/test_models.py -v`
Expected: `PASSED test_article_creation`, `PASSED test_article_with_video`

- [ ] **Step 6: Commit**

```bash
git add models.py __init__.py tests/test_models.py
git commit -m "feat: add data models for article collection"
```

---

## Task 2: Authentication Handler

**Files:**
- Create: `ai-media-system/skills/00-collector/geektime-collector/auth.py`
- Modify: `ai-media-system/skills/00-collector/geektime-collector/tests/test_auth.py`

- [ ] **Step 1: Write the failing test for authentication**

Create `ai-media-system/skills/00-collector/geektime-collector/tests/test_auth.py`:

```python
from geektime_collector.auth import AuthHandler
import os

def test_auth_handler_loads_from_env():
    os.environ["GEEKTIME_COOKIE"] = "test_cookie_value"
    auth = AuthHandler()
    assert auth.cookie == "test_cookie_value"

def test_auth_handler_get_headers():
    os.environ["GEEKTIME_COOKIE"] = "test_cookie"
    os.environ["GEEKTIME_USER_AGENT"] = "TestAgent/1.0"
    auth = AuthHandler()
    headers = auth.get_headers()
    assert "Cookie" in headers
    assert headers["Cookie"] == "test_cookie"
    assert headers["User-Agent"] == "TestAgent/1.0"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ai-media-system && python -m pytest skills/00-collector/geektime-collector/tests/test_auth.py::test_auth_handler_loads_from_env -v`
Expected: `ModuleNotFoundError: No module named 'geektime_collector.auth'`

- [ ] **Step 3: Implement authentication handler**

Create `ai-media-system/skills/00-collector/geektime-collector/auth.py`:

```python
import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class AuthHandler:
    def __init__(self):
        self.cookie = os.getenv("GEEKTIME_COOKIE", "")
        self.user_agent = os.getenv(
            "GEEKTIME_USER_AGENT",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        self.proxy_url = os.getenv("PROXY_URL", "")

    def get_headers(self) -> Dict[str, str]:
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        if self.cookie:
            headers["Cookie"] = self.cookie
        return headers

    def get_proxy_config(self) -> Optional[Dict[str, str]]:
        if not self.proxy_url:
            return None
        return {"server": self.proxy_url}

    def is_authenticated(self) -> bool:
        return bool(self.cookie)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ai-media-system && python -m pytest skills/00-collector/geektime-collector/tests/test_auth.py -v`
Expected: `PASSED test_auth_handler_loads_from_env`, `PASSED test_auth_handler_get_headers`

- [ ] **Step 5: Commit**

```bash
git add auth.py tests/test_auth.py
git commit -m "feat: add authentication handler"
```

---

## Task 3: Core Collector - Article Content Extraction

**Files:**
- Create: `ai-media-system/skills/00-collector/geektime-collector/collector.py`
- Modify: `ai-media-system/skills/00-collector/geektime-collector/tests/test_collector.py`

- [ ] **Step 1: Create test fixture**

Create `ai-media-system/skills/00-collector/geektime-collector/tests/fixtures/sample_article.html`:

```html
<!DOCTYPE html>
<html>
<head><title>测试文章标题</title></head>
<body>
    <article class="article">
        <h1 class="article-title">测试文章标题</h1>
        <div class="article-author">
            <span class="author-name">测试作者</span>
        </div>
        <div class="article-content">
            <p>这是第一段内容。</p>
            <p>这是第二段内容，包含<strong>加粗文字</strong>。</p>
            <img src="https://static001.geekbang.org/resource/image/test.jpg" alt="测试图片"/>
        </div>
    </article>
</body>
</html>
```

- [ ] **Step 2: Write the failing test for content extraction**

Create `ai-media-system/skills/00-collector/geektime-collector/tests/test_collector.py`:

```python
import pytest
from geektime_collector.collector import GeektimeCollector
from geektime_collector.models import Article

@pytest.fixture
def sample_html_path():
    return "skills/00-collector/geektime-collector/tests/fixtures/sample_article.html"

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
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd ai-media-system && python -m pytest skills/00-collector/geektime-collector/tests/test_collector.py -v`
Expected: `ModuleNotFoundError: No module named 'geektime_collector.collector'`

- [ ] **Step 4: Implement HTML parser**

Create `ai-media-system/skills/00-collector/geektime-collector/collector.py`:

```python
from bs4 import BeautifulSoup
import re
from typing import Optional
from urllib.parse import urljoin
from .models import Article, CollectionResult
from .auth import AuthHandler


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
        return hash(url)  # Fallback

    def collect_from_url(self, url: str) -> CollectionResult:
        """
        Collect article from a given URL.

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

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ai-media-system && python -m pytest skills/00-collector/geektime-collector/tests/test_collector.py -v`
Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add collector.py tests/test_collector.py tests/fixtures/sample_article.html
git commit -m "feat: add HTML content extraction"
```

---

## Task 4: SKILL.md Interface

**Files:**
- Create: `ai-media-system/skills/00-collector/geektime-collector/SKILL.md`
- Create: `ai-media-system/skills/00-collector/geektime-collector/README.md`

- [ ] **Step 1: Create SKILL.md**

Create `ai-media-system/skills/00-collector/geektime-collector/SKILL.md`:

```markdown
---
name: geektime-collector
description: Collect article content from Geektime (极客时间) courses and columns
version: 1.0.0
author: AI Media System
---

# Geektime Collector

Collect article content from Geektime courses, including text, images, and video transcripts.

## Usage

```
Use this skill when you need to:
- Collect article content from a Geektime URL
- Extract text, images, and video information from Geektime courses
- Structure the collected content for further processing
```

## Input

Provide a Geektime article URL:
- `https://time.geekbang.org/column/article/XXXXX`
- `https://time.geekbang.org/serv/v1/column/articles/XXXXX`

## Output

Returns a structured JSON object with:
- `id`: Article ID
- `title`: Article title
- `author`: Author name
- `content`: Article text content
- `images`: List of image URLs
- `video`: Video information (if present)
- `collected_at`: Collection timestamp

## Environment Variables

- `GEEKTIME_COOKIE`: Cookie for authentication (required)
- `GEEKTIME_USER_AGENT`: Custom user agent (optional)
- `PROXY_URL`: Proxy server URL (optional)

## Example

```python
from geektime_collector import GeektimeCollector

collector = GeektimeCollector()
result = collector.collect_from_url("https://time.geekbang.org/column/article/12345")

if result.success:
    print(f"Collected: {result.article.title}")
    print(f"Content length: {len(result.article.content)}")
else:
    print(f"Error: {result.error}")
```
```

- [ ] **Step 2: Create README.md**

Create `ai-media-system/skills/00-collector/geektime-collector/README.md`:

```markdown
# Geektime Collector

A Python-based content collector for Geektime (极客时间) articles.

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

## Configuration

Create a `.env` file:

```bash
GEEKTIME_COOKIE=your_cookie_here
```

## Development

Run tests:

```bash
pytest tests/
```

## License

MIT
```

- [ ] **Step 3: Commit**

```bash
git add SKILL.md README.md
git commit -m "docs: add SKILL.md and README.md"
```

---

## Task 5: Integration Test

**Files:**
- Create: `ai-media-system/skills/00-collector/geektime-collector/tests/integration/test_e2e.py`

- [ ] **Step 1: Create integration test**

Create `ai-media-system/skills/00-collector/geektime-collector/tests/integration/test_e2e.py`:

```python
import os
import pytest
from geektime_collector import GeektimeCollector

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
```

- [ ] **Step 2: Create tests/__init__.py**

Create `ai-media-system/skills/00-collector/geektime-collector/tests/__init__.py`:

```python
# Tests package
```

- [ ] **Step 3: Create tests/integration/__init__.py**

Create `ai-media-system/skills/00-collector/geektime-collector/tests/integration/__init__.py`:

```python
# Integration tests package
```

- [ ] **Step 4: Commit**

```bash
git add tests/integration/ tests/__init__.py
git commit -m "test: add integration tests"
```

---

## Task 6: Add beautifulsoup4 to requirements

**Files:**
- Modify: `ai-media-system/requirements.txt`

- [ ] **Step 1: Add beautifulsoup4**

```bash
sed -i '1a beautifulsoup4==4.12.2' ai-media-system/requirements.txt
```

Or manually edit to add at top:
```txt
beautifulsoup4==4.12.2
playwright==1.40.0
...
```

- [ ] **Step 2: Commit**

```bash
git add requirements.txt
git commit -m "fix: add beautifulsoup4 dependency"
```

---

## Task 7: Add missing import to models.py

**Files:**
- Modify: `ai-media-system/skills/00-collector/geektime-collector/models.py`

- [ ] **Step 1: Fix missing import**

Edit the top of `models.py` to ensure proper imports:

```python
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
```

- [ ] **Step 2: Commit**

```bash
git add models.py
git commit -m "fix: ensure proper dataclass imports"
```

---

## Verification Steps

After completing all tasks, verify the implementation:

- [ ] **Step 1: Run all tests**

```bash
cd ai-media-system
python -m pytest skills/00-collector/geektime-collector/tests/ -v
```

Expected: All tests pass

- [ ] **Step 2: Test manual import**

```bash
cd ai-media-system
python -c "from skills.00_collector.geektime_collector import GeektimeCollector; print('Import successful')"
```

Expected: `Import successful`

- [ ] **Step 3: Test with sample URL (if cookie available)**

```bash
cd ai-media-system
python -c "
from skills.00_collector.geektime_collector import GeektimeCollector
collector = GeektimeCollector()
result = collector.collect_from_url('https://time.geekbang.org/column/article/438296')
if result.success:
    print(f'Title: {result.article.title}')
    print(f'Content: {result.article.content[:100]}...')
else:
    print(f'Error: {result.error}')
"
```

Expected: Article title and content printed (or authentication error if no cookie)

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "chore: complete geektime-collector skill implementation"
```

---

## Summary

This plan implements a complete Geektime collector skill with:
- ✅ Data models for structured output
- ✅ Authentication handling
- ✅ HTML content extraction
- ✅ Test coverage (unit + integration)
- ✅ Claude Code Skill interface

Total estimated time: 2-3 hours for a skilled developer.

*Implementation Plan v1.0 - 2026-03-26*
