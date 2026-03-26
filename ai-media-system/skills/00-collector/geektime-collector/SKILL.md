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
