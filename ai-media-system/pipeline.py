"""
MVP Pipeline - 内容生产流水线

集成采集、选题、创作、排版四个模块，实现端到端内容生成
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Windows 控制台编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class MVPPipeline:
    """
    MVP 内容生产流水线

    流程：
    1. Collector: 采集内容
    2. Curator: 选题策划
    3. Writer: 内容创作
    4. Formatter: 公众号排版
    """

    def __init__(self, project_root: Optional[Path] = None, mock_mode: bool = False):
        """
        初始化流水线

        Args:
            project_root: 项目根目录
            mock_mode: 强制使用模拟模式
        """
        if project_root is None:
            # 默认为 pipeline.py 所在的目录
            project_root = Path(__file__).parent

        self.project_root = project_root
        self.skills_path = project_root / "skills"
        self.mock_mode = mock_mode

        # 动态导入模块
        self._import_skills()

    def _import_skills(self):
        """动态导入 Skills"""
        try:
            # 导入采集器
            sys.path.insert(0, str(self.skills_path / "00-collector" / "geektime-collector"))
            from collector import GeektimeCollector
            self.Collector = GeektimeCollector

            # 导入选题器
            sys.path.insert(0, str(self.skills_path / "01-creator" / "topic-curator"))
            from curator import TopicCurator
            self.Curator = TopicCurator

            # 导入写手
            sys.path.insert(0, str(self.skills_path / "02-writer" / "tech-explorer-writer"))
            from writer import TechExplorerWriter
            self.Writer = TechExplorerWriter

            # 导入排版器
            sys.path.insert(0, str(self.skills_path / "03-publisher" / "wechat-formatter"))
            from formatter import WeChatFormatter
            self.Formatter = WeChatFormatter

            self.skills_loaded = True
        except ImportError as e:
            print(f"⚠️  警告: 无法导入 Skills - {e}")
            print("   将使用简化模式运行")
            self.skills_loaded = False

    def step_collect(self, url: str) -> Dict[str, Any]:
        """
        步骤1: 采集内容

        Args:
            url: 要采集的文章URL

        Returns:
            采集结果
        """
        if self.mock_mode or not self.skills_loaded:
            return self._mock_collect(url)

        collector = self.Collector()
        result = collector.collect_from_url(url)

        if result.success:
            return {
                "success": True,
                "content": result.article.to_dict()
            }
        else:
            return {
                "success": False,
                "error": result.error
            }

    def _mock_collect(self, url: str) -> Dict[str, Any]:
        """模拟采集（用于测试）"""
        return {
            "success": True,
            "content": {
                "id": "mock_001",
                "type": "geektime",
                "url": url,
                "title": "大语言模型推理能力解析",
                "content": "大语言模型（LLM）的推理能力是当前AI研究的热点。Chain of Thought通过让模型逐步思考来提升推理效果。",
                "author": "AI专家"
            }
        }

    def step_curate(self, content_pool: list) -> Dict[str, Any]:
        """
        步骤2: 选题策划

        Args:
            content_pool: 采集的内容列表

        Returns:
            选题结果
        """
        if self.mock_mode or not self.skills_loaded:
            return self._mock_curate(content_pool)

        from curator import ContentSource

        # 构建输入
        sources = [
            ContentSource(
                id=c.get("id", ""),
                type=c.get("type", ""),
                title=c.get("title", ""),
                content=c.get("content", ""),
                author=c.get("author", ""),
                url=c.get("url", "")
            )
            for c in content_pool
        ]

        curator = self.Curator()
        result = curator.curate_from_pool(sources, max_candidates=3)

        if result.success:
            return {
                "success": True,
                "candidates": [c.to_dict() for c in result.candidates],
                "summary": result.summary
            }
        else:
            return {
                "success": False,
                "error": result.error
            }

    def _mock_curate(self, content_pool: list) -> Dict[str, Any]:
        """模拟选题（用于测试）"""
        return {
            "success": True,
            "candidates": [
                {
                    "id": "topic_001",
                    "title": "🤔 大语言模型推理能力——小白也能懂的解读",
                    "recommended_style": "tech-explorer",
                    "core_idea": content_pool[0]["title"] if content_pool else "",
                    "estimated_words": 1800,
                    "estimated_images": 2
                }
            ],
            "summary": "从内容池中策划了 1 个选题"
        }

    def step_write(self, topic: dict, source_content: str = "") -> Dict[str, Any]:
        """
        步骤3: 内容创作

        Args:
            topic: 选题信息
            source_content: 原始内容（可选）

        Returns:
            创作结果
        """
        if self.mock_mode or not self.skills_loaded:
            return self._mock_write(topic)

        writer = self.Writer()
        result = writer.write(topic, source_content)

        if result.success:
            return {
                "success": True,
                "article": result.draft.to_dict()
            }
        else:
            return {
                "success": False,
                "error": result.error
            }

    def _mock_write(self, topic: dict) -> Dict[str, Any]:
        """模拟创作（用于测试）"""
        return {
            "success": True,
            "article": {
                "title": topic.get("title", "测试文章"),
                "content": f"""## 📖 核心概念

{topic.get('core_idea', '这是核心概念')}

> 💡 简单来说：这就像一个超级聪明的学生在思考问题。

## 🌟 实际应用

让我们看看实际中的应用：

*   ChatGPT
*   代码助手

## 📚 学习建议

想深入了解？建议先理解概念，再动手实践。

觉得有用的话，点个赞呗~ ✨
                """,
                "word_count": 500,
                "image_prompts": [
                    {"position": 800, "description": "概念图解"}
                ]
            }
        }

    def step_format(self, article: dict, theme: str = "blue") -> Dict[str, Any]:
        """
        步骤4: 公众号排版

        Args:
            article: 文章内容
            theme: 主题

        Returns:
            排版结果
        """
        if self.mock_mode or not self.skills_loaded:
            return self._mock_format(article)

        formatter = self.Formatter(theme=theme)
        result = formatter.format(
            article.get("content", ""),
            article.get("title", ""),
            "AI媒体系统",
            theme
        )

        if result.success:
            return {
                "success": True,
                "html": result.html,
                "metadata": result.metadata
            }
        else:
            return {
                "success": False,
                "error": result.error
            }

    def _mock_format(self, article: dict) -> Dict[str, Any]:
        """模拟排版（用于测试）"""
        html = f"""
<div style="max-width: 677px; margin: 0 auto; padding: 20px;">
    <h1 style="font-size: 24px; font-weight: bold;">{article.get('title', '')}</h1>
    <div style="margin-top: 20px;">{article.get('content', '').replace(chr(10), '<br>')}</div>
    <p style="margin-top: 40px; text-align: center; color: #666;">
        —— 本文由 AI 媒体系统自动生成 ——
    </p>
</div>
        """
        return {
            "success": True,
            "html": html.strip(),
            "metadata": {}
        }

    def run(self, url: str, theme: str = "blue") -> Dict[str, Any]:
        """
        运行完整流水线

        Args:
            url: 要采集的文章URL
            theme: 排版主题

        Returns:
            完整结果
        """
        print("🚀 启动 MVP 内容生产流水线")
        print("=" * 50)

        # 步骤1: 采集
        print("\n📂 步骤1: 采集内容...")
        collect_result = self.step_collect(url)
        if not collect_result["success"]:
            return {"success": False, "error": f"采集失败: {collect_result.get('error')}"}
        print(f"   ✅ 采集完成: {collect_result['content']['title']}")

        # 步骤2: 选题
        print("\n💡 步骤2: 选题策划...")
        curate_result = self.step_curate([collect_result["content"]])
        if not curate_result["success"]:
            return {"success": False, "error": f"选题失败: {curate_result.get('error')}"}
        candidates = curate_result["candidates"]
        selected = candidates[0] if candidates else None
        print(f"   ✅ 策划完成: {selected['title'] if selected else '无选题'}")

        # 步骤3: 创作
        print("\n✍️  步骤3: 内容创作...")
        write_result = self.step_write(
            selected,
            collect_result["content"]["content"]
        )
        if not write_result["success"]:
            return {"success": False, "error": f"创作失败: {write_result.get('error')}"}
        print(f"   ✅ 创作完成: {write_result['article']['word_count']} 字")

        # 步骤4: 排版
        print("\n🎨 步骤4: 公众号排版...")
        format_result = self.step_format(write_result["article"], theme)
        if not format_result["success"]:
            return {"success": False, "error": f"排版失败: {format_result.get('error')}"}
        print(f"   ✅ 排版完成")

        print("\n" + "=" * 50)
        print("✨ 流水线执行完成！")

        return {
            "success": True,
            "article": write_result["article"],
            "html": format_result["html"],
            "summary": curate_result.get("summary", "")
        }


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="MVP 内容生产流水线")
    parser.add_argument("--url", help="要采集的文章URL")
    parser.add_argument("--theme", default="blue", help="排版主题")
    parser.add_argument("--output", help="输出HTML文件路径")
    parser.add_argument("--mock", action="store_true", help="使用模拟模式")

    args = parser.parse_args()

    # 创建流水线
    pipeline = MVPPipeline(mock_mode=args.mock)

    # 运行
    url = args.url or "https://example.com/test"  # 默认值用于测试

    result = pipeline.run(url, theme=args.theme)

    if not result["success"]:
        print(f"\n❌ 错误: {result['error']}")
        sys.exit(1)

    # 保存输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result["html"])
        print(f"\n📄 HTML已保存到: {args.output}")
    else:
        # 默认输出
        output_file = "output.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["html"])
        print(f"\n📄 HTML已保存到: {output_file}")

    print("\n" + result.get("summary", ""))


if __name__ == "__main__":
    main()
