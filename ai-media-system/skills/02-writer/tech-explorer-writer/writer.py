"""
Tech Explorer Writer - 探索者风格创作 Agent

费曼科普风，把复杂技术讲得通俗有趣
"""

import re
import json
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ImagePrompt:
    """配图提示"""
    position: int  # 插入位置（字数）
    description: str  # 配图描述


@dataclass
class ArticleDraft:
    """文章草稿"""
    title: str
    content: str  # Markdown格式
    word_count: int
    image_prompts: List[ImagePrompt] = field(default_factory=list)
    style: str = "tech-explorer"
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "word_count": self.word_count,
            "image_prompts": [
                {"position": p.position, "description": p.description}
                for p in self.image_prompts
            ],
            "style": self.style,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class WritingResult:
    """创作结果"""
    success: bool
    draft: Optional[ArticleDraft] = None
    error: Optional[str] = None


class TechExplorerWriter:
    """
    探索者风格写手

    核心特点：
    - 费曼学习法：用最简单的话解释复杂概念
    - 生活化比喻：把抽象概念变成生活中的例子
    - 幽默风趣：像朋友聊天一样轻松
    - 互动引导：每段结尾有提问或互动
    """

    def __init__(self):
        self._draft_counter = 0

        # 费曼科普风模板库
        self._opening_hooks = [
            "你有没有想过，为什么 {topic} 这么火？",
            "最近 {topic} 刷屏了，但到底是个啥？",
            "让我用大白话给你讲讲 {topic}",
            "别被 {topic} 吓到了，其实超简单！",
            "今天来聊聊 {topic}，保证你听得懂！",
        ]

        self._analogy_templates = {
            "神经网络": "就像餐厅的点餐系统",
            "模型": "就像一个超级聪明的学生",
            "训练": "就像让学生做大量练习题",
            "推理": "就像用学到的知识解决新问题",
            "attention": "就像上课时注意力集中在老师身上",
            "token": "就像中文里的一个字或词",
            "embedding": "把文字变成计算机能理解的坐标",
        }

        self._closing_templates = [
            "\n\n💭 你觉得 {topic} 有意思吗？评论区聊聊~",
            "\n\n🤔 还有什么想了解的？告诉我，下次安排！",
            "\n\n🚀 关注我，下次带你探索更多有趣技术！",
            "\n\n✨ 觉得有用的话，点个赞呗~",
        ]

    def generate_title(self, topic_title: str, core_idea: str) -> str:
        """
        生成吸引人的标题

        探索者风格标题特点：
        - 口语化
        - 引发好奇
        - 带emoji
        """
        templates = [
            f"🤔 {topic_title}——小白也能懂的解读",
            f"一分钟看懂：{topic_title}",
            f"{topic_title}：用大白话讲清楚",
            f"别被吓到了！{topic_title}其实超简单",
            f"💡 {topic_title}，我来给你翻译翻译",
        ]
        return templates[0]  # 可扩展为选择逻辑

    def simplify_technical_term(self, term: str, context: str = "") -> str:
        """
        简化技术术语

        将专业术语转化为通俗解释
        """
        # 查找预定义的比喻
        for key, analogy in self._analogy_templates.items():
            if key in term:
                return f"{term}（{analogy}）"

        # 如果没有预定义，返回原词+简单格式
        return f"**{term}**"

    def add_analogy_explanation(self, concept: str) -> str:
        """
        为核心概念添加生活化比喻

        基于第一性原理，找到概念的本质，然后用生活中的例子类比
        """
        analogies = {
            "llm": "就像一个读过全世界几乎所有书的超级学霸，"
                   "当你问它问题时，它根据学到的知识来回答。",
            "attention": "想象你在看一幅画，你的眼睛会不自觉地"
                        "聚焦在某些关键细节上——这就是注意力机制。",
            "transformer": "就像一个精密的翻译工厂，"
                          "同时考虑上下文的所有信息来生成翻译。",
            "fine-tuning": "就像一个已经大学毕业的学生，"
                         "再接受特定岗位的专业培训。",
            "rag": "就像考试时开卷答题，可以随时查阅参考书。",
        }

        concept_lower = concept.lower()
        for key, value in analogies.items():
            if key in concept_lower:
                return f"\n\n💡 **打个比方**：{value}\n\n"

        return ""

    def write_section_hook(self, topic: str) -> str:
        """写开篇钩子"""
        import random
        hook = random.choice(self._opening_hooks)
        return hook.format(topic=topic)

    def write_section_concept(self, topic: str, source_content: str) -> str:
        """
        写核心概念部分

        策略：
        1. 提取核心概念
        2. 用比喻解释
        3. 添加emoji增加趣味性
        """
        # 提取第一段作为核心内容（简化处理）
        sentences = [s.strip() for s in source_content.split('。') if s.strip()]
        core_content = sentences[0] if sentences else ""

        # 添加比喻解释
        analogy = self.add_analogy_explanation(topic)

        return f"""## 📖 核心概念

{analogy}
简单来说，{core_content}。

这里有几个关键点：

*   **要点1**：{sentences[1] if len(sentences) > 1 else '核心要点一'}
*   **要点2**：{sentences[2] if len(sentences) > 2 else '核心要点二'}
*   **要点3**：{sentences[3] if len(sentences) > 3 else '核心要点三'}

"""

    def write_section_case(self, source_content: str) -> str:
        """
        写实际案例部分

        展示技术在实际中的应用
        """
        return """## 🌟 实际案例

让我们看看实际中的应用：

> 💼 **案例1：ChatGPT**
> 大家都在用的ChatGPT，就是这个技术的典型应用。

> 💼 **案例2：代码助手**
> 帮程序员写代码的工具，也是基于同样的原理。

这些案例告诉我们：这项技术不是空中楼阁，而是实实在在能用的！

"""

    def write_section_learning(self, topic: str) -> str:
        """写学习建议部分"""
        return f"""## 📚 学习建议

想深入了解 {topic}？这里有几条建议：

1.  **先理解概念**：不要急着看代码，先把原理搞懂
2.  **动手实践**：理论知识要结合实践才能真正掌握
3.  **持续学习**：这个领域发展很快，要保持学习习惯

"""

    def write_section_closing(self, topic: str) -> str:
        """写结尾部分"""
        import random
        closing = random.choice(self._closing_templates)
        return closing.format(topic=topic)

    def determine_image_positions(self, word_count: int) -> List[int]:
        """
        确定配图位置

        规则：每800-1000字一张配图
        """
        positions = []
        pos = 800
        while pos < word_count:
            positions.append(pos)
            pos += 800

        return positions

    def generate_image_prompts(
        self,
        topic: str,
        content: str,
        positions: List[int]
    ) -> List[ImagePrompt]:
        """
        生成配图提示

        根据内容和位置生成适合的配图描述
        """
        prompts = []

        descriptions = [
            f"{topic}概念图解，简洁明了的技术架构图",
            f"{topic}应用场景示意图，生活化场景",
            f"{topic}学习路径图，步骤清晰",
        ]

        for i, pos in enumerate(positions):
            desc = descriptions[i % len(descriptions)]
            prompts.append(ImagePrompt(position=pos, description=desc))

        return prompts

    def count_words(self, text: str) -> int:
        """统计字数（中英文混合）"""
        # 移除markdown符号
        clean_text = re.sub(r'[#*`_\-\[\]()]', '', text)
        # 移除emoji（简单处理）
        clean_text = re.sub(r'[\U00010000-\U0010ffff]', '', clean_text)
        # 统计
        chinese = len(re.findall(r'[\u4e00-\u9fff]', clean_text))
        english = len(re.findall(r'[a-zA-Z]', clean_text))
        return chinese + english // 2  # 英文按0.5字计算

    def write(
        self,
        topic: Dict[str, Any],
        source_content: str = "",
        target_words: int = 1800
    ) -> WritingResult:
        """
        执行创作

        Args:
            topic: 选题信息 {"id", "title", "core_idea"}
            source_content: 原始采集内容
            target_words: 目标字数

        Returns:
            WritingResult: 创作结果
        """
        try:
            self._draft_counter += 1

            topic_title = topic.get("title", "")
            core_idea = topic.get("core_idea", "")
            topic_id = topic.get("id", "unknown")

            # 生成标题
            title = self.generate_title(topic_title, core_idea)

            # 组合内容源
            if not source_content:
                source_content = core_idea

            # 撰写各部分
            sections = []

            # 1. 开篇钩子
            hook = self.write_section_hook(topic_title)
            sections.append(hook)

            # 2. 核心概念
            concept = self.write_section_concept(topic_title, source_content)
            sections.append(concept)

            # 3. 实际案例
            case = self.write_section_case(source_content)
            sections.append(case)

            # 4. 学习建议
            learning = self.write_section_learning(topic_title)
            sections.append(learning)

            # 5. 结尾
            closing = self.write_section_closing(topic_title)
            sections.append(closing)

            # 组合全文
            full_content = "".join(sections)

            # 统计字数
            word_count = self.count_words(full_content)

            # 生成配图提示
            positions = self.determine_image_positions(target_words)
            image_prompts = self.generate_image_prompts(
                topic_title,
                full_content,
                positions
            )

            draft = ArticleDraft(
                title=title,
                content=full_content,
                word_count=word_count,
                image_prompts=image_prompts,
                style="tech-explorer"
            )

            return WritingResult(success=True, draft=draft)

        except Exception as e:
            import traceback
            return WritingResult(
                success=False,
                error=f"创作失败: {str(e)}\n{traceback.format_exc()}"
            )


def write_from_dict(input_data: dict) -> dict:
    """
    从字典输入执行创作

    Args:
        input_data: {"topic": dict, "source_content": str, "target_words": int}

    Returns:
        dict: 结果字典
    """
    topic = input_data.get("topic", {})
    source_content = input_data.get("source_content", "")
    target_words = input_data.get("target_words", 1800)

    writer = TechExplorerWriter()
    result = writer.write(topic, source_content, target_words)

    if not result.success:
        return {
            "success": False,
            "error": result.error
        }

    return {
        "success": True,
        "article": result.draft.to_dict()
    }


# CLI 接口
if __name__ == "__main__":
    import sys

    # 示例输入
    example_input = {
        "topic": {
            "id": "topic_001",
            "title": "大语言模型的推理能力",
            "core_idea": "LLM通过Chain of Thought和ReAct等机制实现推理"
        },
        "source_content": """
        大语言模型（LLM）的推理能力是当前AI研究的热点。
        Chain of Thought通过让模型逐步思考来提升推理效果。
        ReAct框架结合推理和行动，让模型能够使用工具。
        Self-Consistency通过多次采样取投票结果。
        """,
        "target_words": 1800
    }

    result = write_from_dict(example_input)

    if result["success"]:
        article = result["article"]
        print(f"标题: {article['title']}")
        print(f"字数: {article['word_count']}")
        print(f"配图: {len(article['image_prompts'])} 张")
        print(f"\n内容预览:\n{article['content'][:500]}...")
    else:
        print(f"❌ 错误: {result['error']}")
        sys.exit(1)
