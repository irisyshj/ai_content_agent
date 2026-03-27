"""
Infographic Generator - 信息图生成 Agent

调用本地 gemini-infographic 和 xhs-infographic skill
"""

import os
import sys
import subprocess
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class InfographicRequest:
    """信息图请求"""
    content: str
    style: str = "auto"
    output: str = "infographic.png"
    platform: str = "general"  # general | xhs


@dataclass
class InfographicResult:
    """信息图生成结果"""
    success: bool
    image_path: str = ""
    error: Optional[str] = None
    style_used: str = ""


class InfographicGenerator:
    """
    信息图生成器

    调用本地已有的 infographic skills:
    - gemini-infographic: 通用信息图，17种风格
    - xhs-infographic: 小红书风格，手绘涂鸦
    """

    # Skill paths
    SKILLS_DIR = Path.home() / ".claude" / "skills"
    GEMINI_SCRIPT = SKILLS_DIR / "gemini-infographic" / "scripts" / "generate_infographic.py"
    XHS_SCRIPT = SKILLS_DIR / "xhs-infographic" / "scripts" / "generate_xhs_infographic.py"

    # 通用风格
    STYLES = [
        "claymorphism",      # 3D 黏土/膨胀风
        "glassmorphism",     # 毛玻璃/磨砂质感
        "bento-grids",       # 便当盒网格风
        "top-student-notes", # 学霸笔记
        "paper-cutout",      # 剪纸/层叠风
        "cartoon-hand-drawn", # 卡通手绘
        "sketchnote",        # 手绘涂鸦
        "ticket",            # 数字极简票券风
        "notion",            # Notion风/知识卡片
        "corporate-memphis", # 极简线条/孟菲斯风
        "pop-art",           # 美式波普
    ]

    def __init__(self, default_style: str = "auto"):
        """
        初始化信息图生成器

        Args:
            default_style: 默认风格
        """
        self.default_style = default_style

    def generate(
        self,
        content: str,
        style: str = "auto",
        output: str = "infographic.png",
        platform: str = "general"
    ) -> InfographicResult:
        """
        生成信息图

        Args:
            content: 文章内容
            style: 视觉风格
            output: 输出路径
            platform: 平台 (general | xhs)

        Returns:
            InfographicResult: 生成结果
        """
        try:
            if platform == "xhs":
                return self._generate_xhs(content, output)
            else:
                return self._generate_gemini(content, style, output)

        except Exception as e:
            import traceback
            return InfographicResult(
                success=False,
                error=f"信息图生成失败: {str(e)}\n{traceback.format_exc()}"
            )

    def _generate_gemini(
        self,
        content: str,
        style: str,
        output: str
    ) -> InfographicResult:
        """调用 gemini-infographic 生成"""
        script_path = self.GEMINI_SCRIPT

        if not script_path.exists():
            return InfographicResult(
                success=False,
                error=f"找不到 gemini-infographic 脚本: {script_path}"
            )

        # 构建命令
        cmd = [
            sys.executable,
            str(script_path),
            content,
            "--style", style or self.default_style,
            "--output", output
        ]

        # 执行
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            return InfographicResult(
                success=True,
                image_path=output,
                style_used=style
            )
        else:
            return InfographicResult(
                success=False,
                error=f"脚本执行失败: {result.stderr}"
            )

    def _generate_xhs(self, content: str, output: str) -> InfographicResult:
        """调用 xhs-infographic 生成"""
        script_path = self.XHS_SCRIPT

        if not script_path.exists():
            return InfographicResult(
                success=False,
                error=f"找不到 xhs-infographic 脚本: {script_path}"
            )

        # xhs-infographic 需要特定的参数格式
        # 需要提取主题和图片数量，这里简化处理
        cmd = [
            sys.executable,
            str(script_path),
            "--content", content[:500],  # 截取前500字作为内容
            "--output", output
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            return InfographicResult(
                success=True,
                image_path=output,
                style_used="xhs-hand-drawn"
            )
        else:
            return InfographicResult(
                success=False,
                error=f"脚本执行失败: {result.stderr}"
            )

    def generate_from_article(
        self,
        article: Dict,
        style: str = "auto",
        platform: str = "general"
    ) -> InfographicResult:
        """
        从文章生成信息图

        Args:
            article: 文章数据 {"title", "content", "headings"}
            style: 视觉风格
            platform: 平台

        Returns:
            InfographicResult: 生成结果
        """
        # 构建信息图内容
        title = article.get("title", "")
        content = article.get("content", "")

        # 提取关键要点
        key_points = self._extract_key_points(article)

        # 组合内容
        infographic_content = f"# {title}\n\n{key_points}\n\n{content[:1000]}"

        # 生成文件名
        safe_title = re.sub(r'[^\w\u4e00-\u9fff]+', '-', title)[:30]
        output = f"output/infographics/{safe_title}.png"

        return self.generate(infographic_content, style, output, platform)

    def _extract_key_points(self, article: Dict) -> str:
        """提取文章要点"""
        headings = article.get("headings", [])
        if not headings:
            return ""

        points = []
        for h in headings[:6]:  # 最多6个要点
            text = h.get("text", "")
            if text:
                points.append(f"• {text}")

        return "\n".join(points)

    def get_available_styles(self) -> List[Dict[str, str]]:
        """获取可用风格列表"""
        return [
            {"key": "auto", "name": "自动检测", "tier": 0},
            {"key": "top-student-notes", "name": "学霸笔记", "tier": 1},
            {"key": "glassmorphism", "name": "毛玻璃/磨砂质感", "tier": 1},
            {"key": "bento-grids", "name": "便当盒网格风", "tier": 1},
            {"key": "claymorphism", "name": "3D 黏土风", "tier": 1},
            {"key": "sketchnote", "name": "手绘涂鸦", "tier": 1},
            {"key": "cartoon-hand-drawn", "name": "卡通手绘", "tier": 1},
            {"key": "paper-cutout", "name": "剪纸/层叠风", "tier": 1},
        ]

    def recommend_style(self, article: Dict) -> str:
        """根据文章推荐风格"""
        title = article.get("title", "").lower()
        content = article.get("content", "").lower()

        # 学习/教程类
        if any(kw in title + content for kw in ["学习", "教程", "笔记", "知识点", "入门"]):
            return "top-student-notes"

        # 科技/分析类
        if any(kw in title + content for kw in ["科技", "技术", "分析", "数据", "研究"]):
            return "glassmorphism"

        # 营销/产品类
        if any(kw in title + content for kw in ["营销", "产品", "推广", "销售"]):
            return "claymorphism"

        # 流程/步骤类
        if any(kw in title + content for kw in ["流程", "步骤", "方法", "指南"]):
            return "sketchnote"

        # 对比/列表类
        if any(kw in title + content for kw in ["对比", "区别", "选择", "推荐"]):
            return "bento-grids"

        # 默认学霸笔记
        return "top-student-notes"


def generate_infographic_from_dict(input_data: dict) -> dict:
    """
    从字典输入生成信息图

    Args:
        input_data: {"article": {...}, "style": "...", "platform": "..."}

    Returns:
        dict: 结果字典
    """
    article = input_data.get("article", {})
    style = input_data.get("style", "auto")
    platform = input_data.get("platform", "general")

    generator = InfographicGenerator()

    # 如果指定auto，自动推荐风格
    if style == "auto":
        style = generator.recommend_style(article)

    result = generator.generate_from_article(article, style, platform)

    if not result.success:
        return {
            "success": False,
            "error": result.error
        }

    return {
        "success": True,
        "image_path": result.image_path,
        "style_used": result.style_used,
        "platform": platform
    }


# CLI 接口
if __name__ == "__main__":
    import re

    # 示例文章
    example_article = {
        "title": "大语言模型的推理能力解析",
        "content": "本文将深入探讨大语言模型的推理能力，包括思维链技术、ReAct框架等前沿内容...",
        "headings": [
            {"level": 2, "text": "思维链技术"},
            {"level": 2, "text": "ReAct框架"},
            {"level": 2, "text": "Self-Consistency"},
            {"level": 2, "text": "应用场景"},
            {"level": 2, "text": "总结"}
        ]
    }

    generator = InfographicGenerator()

    # 推荐风格
    recommended = generator.recommend_style(example_article)
    print(f"推荐风格: {recommended}")

    # 生成信息图
    result = generator.generate_from_article(
        example_article,
        style=recommended,
        platform="general"
    )

    if result.success:
        print(f"✓ 信息图生成成功: {result.image_path}")
    else:
        print(f"❌ 错误: {result.error}")
