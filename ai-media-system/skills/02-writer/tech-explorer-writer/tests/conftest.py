"""Pytest configuration for tech-explorer-writer tests"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_topic():
    """示例选题数据"""
    return {
        "id": "topic_001",
        "title": "大语言模型推理能力解析",
        "core_idea": "LLM通过Chain of Thought和ReAct等机制实现推理"
    }


@pytest.fixture
def sample_content():
    """示例内容"""
    return """
    大语言模型（LLM）的推理能力是当前AI研究的热点。
    Chain of Thought通过让模型逐步思考来提升推理效果。
    ReAct框架结合推理和行动，让模型能够使用工具。
    Self-Consistency通过多次采样取投票结果。
    """
