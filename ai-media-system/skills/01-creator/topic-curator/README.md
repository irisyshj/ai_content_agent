# Topic Curator Skill

选题策划 Agent - 从采集内容中生成候选选题

## 功能

基于采集的内容池，分析素材价值，提取核心观点，生成3-5个候选选题卡片。

## 输入格式

```json
{
  "content_pool": [
    {
      "id": "string",
      "type": "geektime",
      "title": "文章标题",
      "content": "正文内容",
      "author": "作者"
    }
  ],
  "user_preferences": {
    "preferred_style": "tech-explorer | business-analyst",
    "topics_of_interest": ["AI", "LLM", "Agent"]
  }
}
```

## 输出格式

```json
{
  "candidates": [
    {
      "id": "topic_001",
      "source_id": "article_id",
      "title": "选题标题",
      "recommended_style": "tech-explorer",
      "core_idea": "核心观点摘要",
      "estimated_words": 1800,
      "estimated_images": 2,
      "key_points": ["要点1", "要点2"],
      "target_audience": "技术探索者"
    }
  ]
}
```
