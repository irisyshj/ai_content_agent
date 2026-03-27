"""
Xiaohongshu Adapter - 小红书适配器

将文章内容转换为小红书格式
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class XhsPost:
    """小红书帖子"""
    title: str
    content: str
    tags: List[str]
    images: List[str]
    cover_image: str = ""


class XiaohongshuAdapter:
    """
    小红书内容适配器

    特点：
    - 标题要吸引人（带emoji）
    - 内容分段清晰
    - 标签很重要
    - 首图决定点击率
    """

    # 热门标签
    HOT_TAGS = [
        "干货分享", "学习打卡", "知识科普", "成长励志",
        "职场干货", "技能提升", "自我提升", "学习笔记"
    ]

    # 表情符号
    EMOJIS = {
        "attention": ["👀", "💡", "✨", "🔥", "‼️"],
        "success": ["🎉", "✅", "👏", "🌟", "💪"],
        "tips": ["📝", "💡", "🔑", "⚡", "📌"],
        "warning": ["⚠️", "❌", "🚫", "💢"],
        "number": ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    }

    def __init__(self):
        """初始化适配器"""
        pass

    def convert_article(self, article: Dict) -> XhsPost:
        """
        将文章转换为小红书格式

        Args:
            article: {"title", "content", "headings"}

        Returns:
            XhsPost: 小红书帖子
        """
        # 生成标题
        title = self._generate_title(article.get("title", ""))

        # 生成内容
        content = self._generate_content(article)

        # 生成标签
        tags = self._generate_tags(article)

        return XhsPost(
            title=title,
            content=content,
            tags=tags,
            images=[]
        )

    def _generate_title(self, original_title: str) -> str:
        """生成小红书风格标题"""
        # 添加emoji
        emoji = self.EMOJIS["attention"][0]

        # 如果原标题太长，截取
        if len(original_title) > 15:
            title = original_title[:15] + "..."
        else:
            title = original_title

        # 添加吸引人的前缀
        prefixes = ["【干货】", "【必看】", "【收藏】", "", ""]
        import random
        prefix = random.choice(prefixes)

        return f"{emoji}{prefix}{title}"

    def _generate_content(self, article: Dict) -> str:
        """生成小红书风格内容"""
        content = article.get("content", "")
        headings = article.get("headings", [])

        lines = []

        # 开头
        lines.append("今天分享一个超实用的干货~")
        lines.append("")

        # 提取要点
        if headings:
            lines.append("📋 主要内容：")
            for i, h in enumerate(headings[:5], 1):
                text = h.get("text", "")
                if text:
                    num_emoji = self.EMOJIS["number"][min(i-1, 4)]
                    lines.append(f"{num_emoji} {text}")
            lines.append("")

        # 正文分段
        paragraphs = self._split_paragraphs(content, 3)
        for para in paragraphs:
            lines.append(para)
            lines.append("")

        # 结尾
        lines.append("✨ 觉得有用记得点赞收藏哦~")
        lines.append("")
        lines.append("#干货分享 #学习笔记 #知识科普")

        return "\n".join(lines)

    def _split_paragraphs(self, content: str, max_length: int = 150) -> List[str]:
        """将内容分割成适合小红书的段落"""
        # 移除markdown标记
        content = re.sub(r'[#*`>\-]', '', content)

        # 按句子分割
        sentences = re.split(r'[。！？\n]', content)

        paragraphs = []
        current = ""

        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue

            if len(current) + len(sent) < max_length:
                current += sent + "。"
            else:
                if current:
                    paragraphs.append(current)
                current = sent + "。"

        if current:
            paragraphs.append(current)

        return paragraphs[:5]  # 最多5段

    def _generate_tags(self, article: Dict) -> List[str]:
        """生成标签"""
        tags = []

        # 从标题和内容中提取关键词
        title = article.get("title", "").lower()
        content = article.get("content", "").lower()

        # 根据关键词添加标签
        if any(kw in title + content for kw in ["学习", "教程", "知识"]):
            tags.append("学习笔记")
        if any(kw in title + content for kw in ["职场", "工作", "技能"]):
            tags.append("职场干货")
        if any(kw in title + content for kw in ["ai", "人工智能", "技术"]):
            tags.append("知识科普")
        if any(kw in title + content for kw in ["成长", "提升", "进步"]):
            tags.append("成长励志")

        # 确保至少有一些标签
        if not tags:
            tags = ["干货分享", "知识科普"]

        return tags[:5]  # 最多5个标签

    def generate_caption(self, post: XhsPost) -> str:
        """生成完整的配文"""
        lines = [post.title, "", post.content]

        # 添加标签
        if post.tags:
            lines.append("\n" + " ".join(f"#{tag}" for tag in post.tags))

        return "\n".join(lines)


def convert_to_xhs(article: Dict) -> Dict:
    """
    将文章转换为小红书格式

    Args:
        article: 文章数据

    Returns:
        dict: 小红书格式数据
    """
    adapter = XiaohongshuAdapter()
    post = adapter.convert_article(article)

    return {
        "title": post.title,
        "content": post.content,
        "caption": adapter.generate_caption(post),
        "tags": post.tags,
        "platform": "xiaohongshu"
    }


# CLI 接口
if __name__ == "__main__":
    # 示例文章
    example_article = {
        "title": "大语言模型的推理能力解析",
        "content": """
        大语言模型的推理能力是当前AI研究的热点。
        本文将从Chain of Thought开始，探讨LLM的推理机制。
        首先是思维链技术，它通过让模型逐步思考来提升推理效果。
        实验表明，这种技术在数学和逻辑问题上特别有效。
        """,
        "headings": [
            {"level": 2, "text": "思维链技术"},
            {"level": 2, "text": "ReAct框架"},
            {"level": 2, "text": "Self-Consistency"}
        ]
    }

    result = convert_to_xhs(example_article)

    print("标题:", result['title'])
    print("\n配文:")
    print(result['caption'])
    print("\n标签:", result['tags'])
