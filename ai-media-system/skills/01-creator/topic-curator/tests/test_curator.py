"""Topic Curator 测试"""

import pytest
from curator import TopicCurator, ContentSource, curate_from_dict


class TestContentSource:
    """内容来源测试"""

    def test_create_content_source(self):
        content = ContentSource(
            id="test_001",
            type="geektime",
            title="测试标题",
            content="测试内容"
        )
        assert content.id == "test_001"
        assert content.type == "geektime"


class TestTopicCurator:
    """选题策划器测试"""

    def setup_method(self):
        self.curator = TopicCurator(default_style="tech-explorer")

    def test_analyze_content_value(self):
        """测试内容价值分析"""
        content = ContentSource(
            id="test_001",
            type="geektime",
            title="AI技术突破",
            content="这是一项革命性的突破，首次发现了新的方法。",
            author="专家"
        )

        analysis = self.curator.analyze_content_value(content)

        assert "signals" in analysis
        assert "total_score" in analysis
        assert analysis["total_score"] > 0  # 包含"突破"、"首次"等关键词

    def test_determine_style_tech(self):
        """测试技术风格判断"""
        content = ContentSource(
            id="test_001",
            type="geektime",
            title="技术架构设计",
            content="本文讨论系统架构和代码开发技术。",
            author="工程师"
        )

        style = self.curator.determine_style(content, {})
        assert style == "tech-explorer"

    def test_determine_style_business(self):
        """测试商业风格判断"""
        content = ContentSource(
            id="test_001",
            type="geektime",
            title="市场竞争分析",
            content="本文讨论行业市场和投资竞争。",
            author="分析师"
        )

        style = self.curator.determine_style(content, {})
        assert style == "business-analyst"

    def test_curate_from_pool_empty(self):
        """测试空内容池"""
        result = self.curator.curate_from_pool([])

        assert result.success is True
        assert len(result.candidates) == 0

    def test_curate_from_pool_with_content(self):
        """测试正常内容池"""
        content_pool = [
            ContentSource(
                id="test_001",
                type="geektime",
                title="AI技术革命性的新突破",
                content="这是一项革命性的AI技术突破，首次发现新的方法。"
                "这个实践方法非常有用，可以解决很多问题。"
                "未来发展趋势值得关注，将对行业产生深远影响。",
                author="专家"
            )
        ]

        result = self.curator.curate_from_pool(content_pool)

        assert result.success is True
        assert len(result.candidates) == 1
        assert result.candidates[0].source_id == "test_001"
        assert result.candidates[0].recommended_style == "tech-explorer"

    def test_generate_summary(self):
        """测试总结生成"""
        from curator import TopicCandidate

        candidates = [
            TopicCandidate(
                id="topic_001",
                source_id="test_001",
                title="测试选题",
                recommended_style="tech-explorer",
                core_idea="测试",
                estimated_words=1500,
                estimated_images=2
            )
        ]

        summary = self.curator._generate_summary(candidates, [])
        assert "选题策划总结" in summary
        assert "1" in summary  # 候选数量


class TestCurateFromDict:
    """字典接口测试"""

    def test_curate_from_dict_success(self):
        """测试成功情况"""
        input_data = {
            "content_pool": [
                {
                    "id": "test_001",
                    "type": "geektime",
                    "title": "AI技术突破",
                    "content": "革命性的AI技术突破，首次发现新方法。",
                    "author": "专家"
                }
            ],
            "user_preferences": {
                "preferred_style": "tech-explorer"
            }
        }

        result = curate_from_dict(input_data)

        assert result["success"] is True
        assert "candidates" in result
        assert len(result["candidates"]) >= 0

    def test_curate_from_dict_empty_pool(self):
        """测试空内容池"""
        input_data = {
            "content_pool": [],
            "user_preferences": {}
        }

        result = curate_from_dict(input_data)

        assert result["success"] is True
        assert len(result["candidates"]) == 0
