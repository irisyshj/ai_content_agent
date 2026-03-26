"""
Topic Curator - 选题策划 Agent

从采集内容池中分析素材价值，生成候选选题
"""

import json
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TopicCandidate:
    """选题候选"""
    id: str
    source_id: str
    title: str
    recommended_style: str  # "tech-explorer" | "business-analyst"
    core_idea: str
    estimated_words: int
    estimated_images: int
    key_points: List[str] = field(default_factory=list)
    target_audience: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "title": self.title,
            "recommended_style": self.recommended_style,
            "core_idea": self.core_idea,
            "estimated_words": self.estimated_words,
            "estimated_images": self.estimated_images,
            "key_points": self.key_points,
            "target_audience": self.target_audience,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ContentSource:
    """内容来源"""
    id: str
    type: str
    title: str
    content: str
    author: str = ""
    url: str = ""


@dataclass
class CuratorResult:
    """选题策划结果"""
    success: bool
    candidates: List[TopicCandidate] = field(default_factory=list)
    error: Optional[str] = None
    summary: str = ""


class TopicCurator:
    """选题策划 Agent"""

    def __init__(self, default_style: str = "tech-explorer"):
        """
        初始化选题策划 Agent

        Args:
            default_style: 默认推荐风格 (tech-explorer | business-analyst)
        """
        self.default_style = default_style
        self._topic_counter = 0

    def analyze_content_value(self, content: ContentSource) -> Dict[str, Any]:
        """
        分析内容价值

        评估维度：
        - 新颖性：是否有新观点/新数据
        - 实用性：是否可转化为干货
        - 话题性：是否引发讨论
        - 深度：是否有足够内容支撑
        """
        content_lower = content.content.lower()

        # 简单关键词分析（实际应使用 Claude API）
        value_signals = {
            "novelty": 0,
            "practicality": 0,
            "discussability": 0,
            "depth": 0
        }

        # 新颖性信号
        novelty_keywords = ["突破", "首次", "新发现", "最新", "革命性", "前沿"]
        for kw in novelty_keywords:
            value_signals["novelty"] += content_lower.count(kw)

        # 实用性信号
        practical_keywords = ["方法", "技巧", "工具", "实践", "应用", "如何"]
        for kw in practical_keywords:
            value_signals["practicality"] += content_lower.count(kw)

        # 话题性信号
        discussion_keywords = ["争议", "挑战", "未来", "趋势", "影响"]
        for kw in discussion_keywords:
            value_signals["discussability"] += content_lower.count(kw)

        # 深度信号（以字数作为简单指标）
        value_signals["depth"] = min(len(content.content) // 500, 10)

        # 计算总分
        total_score = sum(value_signals.values())

        return {
            "signals": value_signals,
            "total_score": total_score,
            "is_worth_creating": total_score > 3
        }

    def extract_key_points(self, content: str, max_points: int = 5) -> List[str]:
        """
        提取关键要点

        简化实现：按段落提取，实际应使用 LLM
        """
        # 按段落分割
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

        # 选择前几段作为关键点（简化逻辑）
        key_points = []
        for para in paragraphs[:max_points]:
            if len(para) > 20 and len(para) < 200:
                # 截取前100字作为摘要
                point = para[:100] + "..." if len(para) > 100 else para
                key_points.append(point)

        return key_points[:max_points]

    def determine_style(self, content: ContentSource, value_analysis: Dict) -> str:
        """
        确定推荐风格

        规则：
        - 偏技术/教程 → tech-explorer
        - 偏商业/分析 → business-analyst
        """
        content_lower = content.content.lower()

        tech_indicators = ["技术", "算法", "模型", "代码", "开发", "系统", "架构"]
        business_indicators = ["商业", "市场", "公司", "投资", "行业", "竞争"]

        tech_score = sum(1 for kw in tech_indicators if kw in content_lower)
        business_score = sum(1 for kw in business_indicators if kw in content_lower)

        if tech_score > business_score:
            return "tech-explorer"
        elif business_score > tech_score:
            return "business-analyst"
        else:
            return self.default_style

    def generate_topic_title(self, content: ContentSource, style: str) -> str:
        """
        生成选题标题

        根据风格生成不同类型的标题
        """
        original_title = content.title

        if style == "tech-explorer":
            # 探索者风格：更口语化、引发好奇
            templates = [
                f"🤔 {original_title}：小白也能懂的解读",
                f"一分钟看懂：{original_title}",
                f"{original_title}——用大白话说清楚",
            ]
        else:
            # 商业分析风格：更专业、数据驱动
            templates = [
                f"深度解析：{original_title}",
                f"{original_title}：商业影响与趋势分析",
                f"从{original_title}看行业变革",
            ]

        # 返回第一个模板（实际应使用 LLM 生成更优标题）
        return templates[0]

    def curate_from_pool(
        self,
        content_pool: List[ContentSource],
        max_candidates: int = 5,
        user_preferences: Optional[Dict] = None
    ) -> CuratorResult:
        """
        从内容池策划选题

        Args:
            content_pool: 采集的内容列表
            max_candidates: 最多生成候选数量
            user_preferences: 用户偏好设置

        Returns:
            CuratorResult: 策划结果
        """
        try:
            candidates = []

            # 分析每篇内容的价值
            analyzed_contents = []
            for content in content_pool:
                value_analysis = self.analyze_content_value(content)

                # 只保留有价值的
                if value_analysis["is_worth_creating"]:
                    analyzed_contents.append({
                        "content": content,
                        "analysis": value_analysis
                    })

            # 按价值分数排序
            analyzed_contents.sort(
                key=lambda x: x["analysis"]["total_score"],
                reverse=True
            )

            # 生成选题候选
            for item in analyzed_contents[:max_candidates]:
                content = item["content"]
                analysis = item["analysis"]

                # 确定风格
                style = self.determine_style(content, analysis)

                # 生成标题
                title = self.generate_topic_title(content, style)

                # 提取要点
                key_points = self.extract_key_points(content.content)

                # 确定目标读者
                if style == "tech-explorer":
                    target_audience = "技术探索者、高中生知识水平"
                    estimated_words = 1500
                else:
                    target_audience = "科技公司管理层、决策者"
                    estimated_words = 2000

                # 估算配图数量
                estimated_images = max(1, estimated_words // 800)

                self._topic_counter += 1
                candidate = TopicCandidate(
                    id=f"topic_{self._topic_counter:03d}",
                    source_id=content.id,
                    title=title,
                    recommended_style=style,
                    core_idea=content.title,
                    estimated_words=estimated_words,
                    estimated_images=estimated_images,
                    key_points=key_points,
                    target_audience=target_audience
                )

                candidates.append(candidate)

            # 生成总结
            summary = self._generate_summary(candidates, content_pool)

            return CuratorResult(
                success=True,
                candidates=candidates,
                summary=summary
            )

        except Exception as e:
            import traceback
            return CuratorResult(
                success=False,
                error=f"选题策划失败: {str(e)}\n{traceback.format_exc()}"
            )

    def _generate_summary(
        self,
        candidates: List[TopicCandidate],
        content_pool: List[ContentSource]
    ) -> str:
        """生成策划总结"""
        tech_count = sum(1 for c in candidates if c.recommended_style == "tech-explorer")
        business_count = len(candidates) - tech_count

        return f"""📋 选题策划总结

从 {len(content_pool)} 篇采集内容中，筛选出 {len(candidates)} 个优质选题：

📊 风格分布：
  • 技术探索者风格：{tech_count} 篇
  • 商业分析师风格：{business_count} 篇

📝 预计产出：
  • 总字数：约 {sum(c.estimated_words for c in candidates)} 字
  • 配图：约 {sum(c.estimated_images for c in candidates)} 张

💡 建议：选择最感兴趣的选题开始创作
"""


def curate_from_dict(input_data: dict) -> dict:
    """
    从字典输入策划选题

    Args:
        input_data: 输入数据字典

    Returns:
        dict: 结果字典
    """
    # 解析输入
    content_dicts = input_data.get("content_pool", [])
    preferences = input_data.get("user_preferences", {})

    # 构建 ContentSource 列表
    content_pool = [
        ContentSource(
            id=c.get("id", ""),
            type=c.get("type", ""),
            title=c.get("title", ""),
            content=c.get("content", ""),
            author=c.get("author", ""),
            url=c.get("url", "")
        )
        for c in content_dicts
    ]

    # 设置默认风格
    default_style = preferences.get("preferred_style", "tech-explorer")

    # 执行策划
    curator = TopicCurator(default_style=default_style)
    result = curator.curate_from_pool(
        content_pool=content_pool,
        max_candidates=input_data.get("max_candidates", 5),
        user_preferences=preferences
    )

    # 返回结果
    if not result.success:
        return {
            "success": False,
            "error": result.error
        }

    return {
        "success": True,
        "candidates": [c.to_dict() for c in result.candidates],
        "summary": result.summary
    }


# CLI 接口
if __name__ == "__main__":
    import sys

    # 示例输入
    example_input = {
        "content_pool": [
            {
                "id": "gt_001",
                "type": "geektime",
                "title": "大语言模型的推理能力解析",
                "content": """
                大语言模型（LLM）的推理能力是当前AI研究的热点。
                本文将从Chain of Thought开始，探讨LLM的推理机制。

                首先是思维链技术，它通过让模型逐步思考来提升推理效果。
                实验表明，这种技术在数学和逻辑问题上特别有效。

                其次是ReAct框架，结合推理和行动，让模型能够使用工具。
                这种方法在Agent应用中非常流行。

                最后是Self-Consistency，通过多次采样取投票结果，
                进一步提升了推理的准确性。
                """,
                "author": "AI专家"
            }
        ],
        "user_preferences": {
            "preferred_style": "tech-explorer"
        }
    }

    result = curate_from_dict(example_input)

    if result["success"]:
        print(result["summary"])
        for c in result["candidates"]:
            print(f"\n📌 {c['title']}")
            print(f"   风格: {c['recommended_style']}")
            print(f"   受众: {c['target_audience']}")
            print(f"   字数: {c['estimated_words']}")
            print(f"   配图: {c['estimated_images']}")
    else:
        print(f"❌ 错误: {result['error']}")
        sys.exit(1)
