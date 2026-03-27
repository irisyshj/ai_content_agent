"""
Jianshu Adapter - 简书适配器

将文章内容转换为简书格式
"""

import re
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class JianshuPost:
    """简书文章"""
    title: str
    content: str
    categories: List[str]
    cover_image: str = ""


class JianshuAdapter:
    """
    简书内容适配器

    特点：
    - 支持Markdown
    - 文学性强
    - 分类清晰
    - 适合长文
    """

    def __init__(self):
        """初始化适配器"""
        pass

    def convert_article(self, article: Dict) -> JianshuPost:
        """
        将文章转换为简书格式

        Args:
            article: {"title", "content", "headings"}

        Returns:
            JianshuPost: 简书文章
        """
        title = article.get("title", "")
        content = self._format_content(article)
        categories = self._generate_categories(article)

        return JianshuPost(
            title=title,
            content=content,
            categories=categories
        )

    def _format_content(self, article: Dict) -> str:
        """格式化内容"""
        content = article.get("content", "")

        # 简书支持Markdown，直接返回
        # 添加一些简书特有的元素
        formatted = f"""{content}

---

*本文为原创内容，转载请注明出处。*

*欢迎关注我的简书账号，获取更多优质内容。*
"""
        return formatted

    def _generate_categories(self, article: Dict) -> List[str]:
        """生成分类"""
        categories = []

        title = article.get("title", "").lower()
        content = article.get("content", "").lower()

        # 简书常用分类
        category_keywords = {
            "编程": ["代码", "编程", "开发", "算法", "技术"],
            "人工智能": ["ai", "人工智能", "机器学习"],
            "产品": ["产品", "设计", "用户体验"],
            "职场": ["职场", "工作", "管理"],
            "学习方法": ["学习", "教育", "知识"],
            "随笔": ["感想", "思考", "感悟"],
        }

        for category, keywords in category_keywords.items():
            if any(kw in title + content for kw in keywords):
                categories.append(category)

        return categories[:3] if categories else ["随笔"]


def convert_to_jianshu(article: Dict) -> Dict:
    """
    将文章转换为简书格式

    Args:
        article: 文章数据

    Returns:
        dict: 简书格式数据
    """
    adapter = JianshuAdapter()
    post = adapter.convert_article(article)

    return {
        "title": post.title,
        "content": post.content,
        "categories": post.categories,
        "platform": "jianshu"
    }
