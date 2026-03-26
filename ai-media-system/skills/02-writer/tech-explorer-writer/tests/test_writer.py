"""Tech Explorer Writer 测试"""

import pytest
from writer import TechExplorerWriter, ImagePrompt, write_from_dict


class TestTechExplorerWriter:
    """探索者写手测试"""

    def setup_method(self):
        self.writer = TechExplorerWriter()

    def test_generate_title(self):
        """测试标题生成"""
        title = self.writer.generate_title(
            "大语言模型推理",
            "LLM推理机制解析"
        )
        assert "大语言模型推理" in title
        assert len(title) > 10

    def test_simplify_technical_term_with_analogy(self):
        """测试术语简化（有预定义比喻）"""
        result = self.writer.simplify_technical_term("attention机制")
        assert "注意力" in result or "attention" in result

    def test_simplify_technical_term_without_analogy(self):
        """测试术语简化（无预定义比喻）"""
        result = self.writer.simplify_technical_term("新术语ABC")
        assert "**新术语ABC**" == result

    def test_add_analogy_explanation(self):
        """测试比喻解释"""
        result = self.writer.add_analogy_explanation("llm")
        assert "比喻" in result or "就像" in result

    def test_determine_image_positions(self):
        """测试配图位置计算"""
        positions = self.writer.determine_image_positions(1800)
        assert len(positions) == 2  # 800, 1600
        assert 800 in positions

    def test_count_words_chinese(self):
        """测试中文字数统计"""
        count = self.writer.count_words("这是一段中文测试内容，用来统计字数。")
        assert count > 0

    def test_count_words_mixed(self):
        """测试中英文混合统计"""
        count = self.writer.count_words("这是Hello混合World测试test")
        assert count > 0

    def test_write_success(self):
        """测试成功创作"""
        topic = {
            "id": "topic_001",
            "title": "测试选题",
            "core_idea": "测试核心观点"
        }

        result = self.writer.write(topic, source_content="测试内容")

        assert result.success is True
        assert result.draft is not None
        assert result.draft.title
        assert result.draft.content
        assert result.draft.word_count >= 0

    def test_write_with_image_prompts(self):
        """测试配图提示生成"""
        topic = {
            "id": "topic_001",
            "title": "AI技术",
            "core_idea": "AI核心概念"
        }

        result = self.writer.write(topic, target_words=1800)

        assert result.success is True
        assert len(result.draft.image_prompts) > 0


class TestWriteFromDict:
    """字典接口测试"""

    def test_write_from_dict_success(self):
        """测试成功情况"""
        input_data = {
            "topic": {
                "id": "topic_001",
                "title": "AI技术",
                "core_idea": "AI核心概念"
            },
            "source_content": "测试内容",
            "target_words": 1500
        }

        result = write_from_dict(input_data)

        assert result["success"] is True
        assert "article" in result
        assert result["article"]["title"]
        assert result["article"]["content"]

    def test_write_from_dict_empty_topic(self):
        """测试空选题"""
        input_data = {
            "topic": {},
            "source_content": ""
        }

        result = write_from_dict(input_data)

        # 应该能生成默认内容
        assert result["success"] is True


class TestImagePrompt:
    """配图提示测试"""

    def test_image_prompt_creation(self):
        """测试配图提示创建"""
        prompt = ImagePrompt(position=800, description="测试配图")
        assert prompt.position == 800
        assert prompt.description == "测试配图"
