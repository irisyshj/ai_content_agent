"""Pytest configuration for topic-curator tests"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_content():
    """示例内容数据"""
    return {
        "id": "sample_001",
        "type": "geektime",
        "title": "大语言模型推理能力解析",
        "content": """
        大语言模型的推理能力是当前AI研究的热点。
        本文从Chain of Thought开始，探讨LLM的推理机制。

        思维链技术通过让模型逐步思考来提升推理效果。
        ReAct框架结合推理和行动，让模型能够使用工具。
        Self-Consistency通过多次采样取投票结果，提升准确性。
        """,
        "author": "AI专家"
    }


@pytest.fixture
def sample_content_pool(sample_content):
    """示例内容池"""
    return [sample_content]
