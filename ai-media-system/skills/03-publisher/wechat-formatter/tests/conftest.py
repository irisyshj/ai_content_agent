"""Pytest configuration for wechat-formatter tests"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_article():
    """示例文章数据"""
    return {
        "title": "🤔 大语言模型推理能力解析",
        "content": """
## 📖 核心概念

大语言模型（LLM）的推理能力是当前AI研究的热点。

**Chain of Thought** 通过让模型逐步思考来提升推理效果。

> 💡 简单来说：就像考试时把解题步骤写下来。

## 🌟 实际应用

*   ChatGPT
*   代码助手
        """,
        "author": "AI媒体系统",
        "theme": "blue"
    }


@pytest.fixture
def sample_markdown():
    """示例 Markdown 内容"""
    return """
# 主标题

这是一段普通文字，包含**粗体**和*斜体*。

## 二级标题

```python
def hello():
    print("world")
```

> 这是引用块内容

*   列表项1
*   列表项2
    """
