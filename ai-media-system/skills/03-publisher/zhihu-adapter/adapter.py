"""
Zhihu Adapter - 知乎适配器

将文章内容转换为知乎格式
"""

import re
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ZhihuPost:
    """知乎文章/回答"""
    title: str
    content: str
    topics: List[str]
    summary: str = ""


class ZhihuAdapter:
    """
    知乎内容适配器

    特点：
    - 专业严谨
    - 支持Markdown
    - 话题分类
    - 段落清晰
    """

    def __init__(self):
        """初始化适配器"""
        pass

    def convert_article(self, article: Dict) -> ZhihuPost:
        """
        将文章转换为知乎格式

        Args:
            article: {"title", "content", "headings"}

        Returns:
            ZhihuPost: 知乎帖子
        """
        title = article.get("title", "")
        content = self._format_content(article)
        topics = self._generate_topics(article)
        summary = self._generate_summary(article)

        return ZhihuPost(
            title=title,
            content=content,
            topics=topics,
            summary=summary
        )

    def _format_content(self, article: Dict) -> str:
        """格式化内容"""
        content = article.get("content", "")
        headings = article.get("headings", [])

        lines = []

        # 开头
        lines.append(content[:200])
        lines.append("")
        lines.append("---")
        lines.append("")

        # 目录
        if headings:
            lines.append("## 目录")
            for i, h in enumerate(headings[:8], 1):
                text = h.get("text", "")
                level = h.get("level", 2)
                indent = "  " * (level - 1)
                lines.append(f"{indent}{i}. {text}")
            lines.append("")
            lines.append("---")
            lines.append("")

        # 完整内容
        lines.append(content)

        # 结尾
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("如果这个问题对你有帮助，欢迎点赞关注，我会持续分享优质内容。")

        return "\n".join(lines)

    def _generate_topics(self, article: Dict) -> List[str]:
        """生成话题"""
        topics = []

        title = article.get("title", "").lower()
        content = article.get("content", "").lower()

        # 根据关键词匹配话题
        topic_keywords = {
            "人工智能": ["ai", "人工智能", "机器学习", "深度学习"],
            "编程": ["代码", "编程", "开发", "算法"],
            "产品": ["产品", "设计", "用户体验"],
            "职场": ["职场", "工作", "职业"],
            "学习": ["学习", "教育", "知识"],
        }

        for topic, keywords in topic_keywords.items():
            if any(kw in title + content for kw in keywords):
                topics.append(topic)

        return topics[:5]

    def _generate_summary(self, article: Dict) -> str:
        """生成摘要"""
        content = article.get("content", "")
        # 取前100字作为摘要
        summary = re.sub(r'[#*`>\-]', '', content)
        return summary[:100] + "..."


def convert_to_zhihu(article: Dict) -> Dict:
    """
    将文章转换为知乎格式

    Args:
        article: 文章数据

    Returns:
        dict: 知乎格式数据
    """
    adapter = ZhihuAdapter()
    post = adapter.convert_article(article)

    return {
        "title": post.title,
        "content": post.content,
        "topics": post.topics,
        "summary": post.summary,
        "platform": "zhihu"
    }
