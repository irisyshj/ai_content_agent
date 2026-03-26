# Tech Explorer Writer

探索者风格创作 Agent - 费曼科普风，把复杂技术讲得通俗有趣

## 功能特点

- **目标读者**：技术探索者，高中生知识水平
- **字数范围**：1500-2000字
- **语言风格**：幽默通俗、生活化比喻、适当Emoji
- **专业术语**：每500字不超过3个，必须有解释
- **结构要求**：开篇钩子+核心概念+实际案例+学习建议+互动结尾

## 输入格式

```json
{
  "topic": {
    "id": "topic_001",
    "title": "选题标题",
    "core_idea": "核心观点",
    "source_content": "原始采集内容"
  },
  "style": "tech-explorer",
  "target_words": 1800
}
```

## 输出格式

```json
{
  "success": true,
  "article": {
    "title": "文章标题",
    "content": "Markdown格式正文",
    "word_count": 1850,
    "image_prompts": [
      {
        "position": 800,
        "description": "配图描述"
      }
    ]
  }
}
```
