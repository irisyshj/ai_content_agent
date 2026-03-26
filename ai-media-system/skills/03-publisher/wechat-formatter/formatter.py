"""
WeChat Formatter - 公众号排版 Agent

将 Markdown 转换为微信兼容的 HTML（内联CSS）
"""

import re
import html
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FormatResult:
    """排版结果"""
    success: bool
    html: str = ""
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


class WeChatFormatter:
    """
    微信公众号排版器

    特点：
    - 内联 CSS（微信不支持外部样式）
    - 移动端优先设计
    - 自适应宽度
    - 代码高亮
    """

    # 主题配色
    THEMES = {
        "default": {
            "primary": "#1e1e1e",
            "accent": "#07c160",
            "background": "#ffffff",
            "text": "#333333",
            "secondary": "#666666",
            "border": "#e0e0e0",
            "code_bg": "#f5f5f5",
            "quote_bg": "#f0f7ff",
            "quote_border": "#4a90e2"
        },
        "blue": {
            "primary": "#2c3e50",
            "accent": "#3498db",
            "background": "#ffffff",
            "text": "#333333",
            "secondary": "#666666",
            "border": "#d0e3f5",
            "code_bg": "#ecf0f1",
            "quote_bg": "#eaf2f8",
            "quote_border": "#3498db"
        },
        "green": {
            "primary": "#27ae60",
            "accent": "#2ecc71",
            "background": "#ffffff",
            "text": "#333333",
            "secondary": "#666666",
            "border": "#d5f4e6",
            "code_bg": "#f0f9f4",
            "quote_bg": "#e8f8f0",
            "quote_border": "#27ae60"
        },
        "purple": {
            "primary": "#8e44ad",
            "accent": "#9b59b6",
            "background": "#ffffff",
            "text": "#333333",
            "secondary": "#666666",
            "border": "#e8daef",
            "code_bg": "#f4ecf7",
            "quote_bg": "#f5eef8",
            "quote_border": "#8e44ad"
        }
    }

    def __init__(self, theme: str = "default"):
        """
        初始化排版器

        Args:
            theme: 主题名称 (default | blue | green | purple)
        """
        self.theme = self.THEMES.get(theme, self.THEMES["default"])
        self._emoji_map = {
            "🤔": "思考",
            "📖": "核心概念",
            "🌟": "案例",
            "📚": "学习",
            "💡": "提示",
            "🚀": "开始",
            "💭": "思考",
            "✨": "亮点",
            "🤖": "AI",
            "📊": "数据",
            "⚠️": "注意",
            "✅": "完成"
        }

    def _build_css(self) -> str:
        """构建内联 CSS 样式字符串"""
        return f"""
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB',
               'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
line-height: 1.8;
color: {self.theme['text']};
        """.strip()

    def _escape_html(self, text: str) -> str:
        """转义 HTML 特殊字符"""
        return html.escape(text, quote=False)

    def _parse_headings(self, content: str) -> Tuple[str, List[dict]]:
        """
        解析标题并生成目录

        Returns:
            (处理后的内容, 标题列表)
        """
        headings = []
        lines = content.split('\n')
        result = []

        for line in lines:
            # 匹配 ## 标题
            match = re.match(r'^(#{2,3})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                # 移除 emoji
                clean_text = re.sub(r'^[\U00010000-\U0010ffff]+\s*', '', text)
                anchor = re.sub(r'[^\w\u4e00-\u9fff]+', '-', clean_text).strip('-')

                headings.append({
                    "level": level,
                    "text": clean_text,
                    "anchor": anchor
                })

                # 转换为带样式的 HTML
                font_size = "20px" if level == 2 else "18px"
                margin = "25px 0 15px" if level == 2 else "20px 0 10px"
                border = f"border-left: 4px solid {self.theme['accent']};"
                padding = "padding-left: 12px;"

                styled_heading = f'''
<h{level} style="
    font-size: {font_size};
    font-weight: bold;
    color: {self.theme['primary']};
    margin: {margin};
    {border}
    {padding}
">{text}</h{level}>
                '''
                result.append(styled_heading.strip())
            else:
                result.append(line)

        return '\n'.join(result), headings

    def _parse_paragraphs(self, content: str) -> str:
        """解析段落"""
        lines = content.split('\n')
        result = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 跳过已经是 HTML 的行
            if line.startswith('<'):
                result.append(line)
                continue

            # 处理列表项
            if line.startswith('* ') or line.startswith('- '):
                text = line[2:].strip()
                result.append(f'''
<li style="
    margin: 8px 0;
    padding-left: 20px;
    position: relative;
">{text}</li>
                '''.strip())
            elif re.match(r'^\d+\.\s', line):
                text = re.sub(r'^\d+\.\s', '', line)
                result.append(f'''
<li style="
    margin: 8px 0;
    padding-left: 20px;
    position: relative;
">{text}</li>
                '''.strip())
            else:
                # 普通段落
                result.append(f'''
<p style="
    margin: 15px 0;
    text-align: justify;
    font-size: 16px;
">{line}</p>
                '''.strip())

        return '\n'.join(result)

    def _parse_code_blocks(self, content: str) -> str:
        """解析代码块"""
        # 匹配 ``` 代码块
        def replace_code_block(match):
            code = match.group(1)
            escaped = self._escape_html(code)
            return f'''
<pre style="
    background: {self.theme['code_bg']};
    padding: 15px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 15px 0;
    font-size: 14px;
    line-height: 1.6;
"><code>{escaped}</code></pre>
            '''

        content = re.sub(r'```(\w+)?\n([\s\S]+?)```', replace_code_block, content)

        # 匹配行内代码 `code`
        content = re.sub(
            r'`([^`]+)`',
            r'<code style="background: ' + self.theme['code_bg'] + '; padding: 2px 6px; ' +
            r'border-radius: 4px; font-size: 14px; color: #e74c3c;">\1</code>',
            content
        )

        return content

    def _parse_blockquotes(self, content: str) -> str:
        """解析引用块"""
        def replace_quote(match):
            text = match.group(1).strip()
            return f'''
<blockquote style="
    margin: 20px 0;
    padding: 15px 20px;
    background: {self.theme['quote_bg']};
    border-left: 4px solid {self.theme['quote_border']};
    border-radius: 4px;
"><p style="margin: 0; font-size: 15px; color: {self.theme['secondary']};">{text}</p></blockquote>
            '''

        return re.sub(r'^>\s+(.+)$', replace_quote, content, flags=re.MULTILINE)

    def _parse_bold_italic(self, content: str) -> str:
        """解析粗体和斜体"""
        # 粗体 **text**
        content = re.sub(
            r'\*\*([^*]+)\*\*',
            r'<strong style="font-weight: bold; color: ' + self.theme['primary'] + ';">\1</strong>',
            content
        )

        # 斜体 *text*
        content = re.sub(
            r'(?<!\*)\*([^*]+)\*(?!\*)',
            r'<em style="font-style: italic;">\1</em>',
            content
        )

        return content

    def _build_container(self, content: str, title: str = "", author: str = "") -> str:
        """构建完整 HTML 容器"""
        # 生成标题区
        header_html = ""
        if title:
            header_html = f'''
<div style="
    text-align: center;
    margin: 30px 0 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid {self.theme['border']};
">
    <h1 style="
        font-size: 24px;
        font-weight: bold;
        color: {self.theme['primary']};
        margin: 0;
        line-height: 1.4;
    ">{title}</h1>
    {f'<p style="margin: 10px 0 0; color: {self.theme["secondary"]}; font-size: 14px;">{author}</p>' if author else ''}
</div>
            '''.strip()

        # 生成底部签名
        footer_html = f'''
<div style="
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid {self.theme['border']};
    text-align: center;
    color: {self.theme['secondary']};
    font-size: 14px;
">
    <p>—— 本文由 AI 媒体系统自动生成 ——</p>
</div>
        '''.strip()

        # 组合完整 HTML
        full_html = f'''
<div style="
    max-width: 677px;
    margin: 0 auto;
    padding: 20px;
    background: {self.theme['background']};
    {self._build_css()}
">
    {header_html}
    {content}
    {footer_html}
</div>
        '''.strip()

        return full_html

    def format(
        self,
        content: str,
        title: str = "",
        author: str = "",
        theme: Optional[str] = None
    ) -> FormatResult:
        """
        执行排版

        Args:
            content: Markdown 格式内容
            title: 文章标题
            author: 作者名称
            theme: 主题名称（覆盖初始化设置）

        Returns:
            FormatResult: 排版结果
        """
        try:
            # 更新主题
            if theme and theme in self.THEMES:
                self.theme = self.THEMES[theme]

            # 处理流程
            result = content

            # 1. 解析标题
            result, headings = self._parse_headings(result)

            # 2. 解析代码块
            result = self._parse_code_blocks(result)

            # 3. 解析引用块
            result = self._parse_blockquotes(result)

            # 4. 解析粗体斜体
            result = self._parse_bold_italic(result)

            # 5. 解析段落
            result = self._parse_paragraphs(result)

            # 6. 构建完整容器
            html = self._build_container(result, title, author)

            return FormatResult(
                success=True,
                html=html,
                metadata={
                    "headings": headings,
                    "theme": theme,
                    "char_count": len(content)
                }
            )

        except Exception as e:
            import traceback
            return FormatResult(
                success=False,
                error=f"排版失败: {str(e)}\n{traceback.format_exc()}"
            )

    def format_article_dict(self, article: dict) -> dict:
        """
        从文章字典排版

        Args:
            article: {"title", "content", "author"}

        Returns:
            dict: 结果字典
        """
        title = article.get("title", "")
        content = article.get("content", "")
        author = article.get("author", "AI媒体系统")
        theme = article.get("theme", "default")

        result = self.format(content, title, author, theme)

        if not result.success:
            return {
                "success": False,
                "error": result.error
            }

        return {
            "success": True,
            "html": result.html,
            "metadata": result.metadata
        }


def format_from_dict(input_data: dict) -> dict:
    """
    从字典输入执行排版

    Args:
        input_data: {"title", "content", "author", "theme"}

    Returns:
        dict: 结果字典
    """
    formatter = WeChatFormatter(theme=input_data.get("theme", "default"))
    return formatter.format_article_dict(input_data)


# CLI 接口
if __name__ == "__main__":
    import sys

    # 示例输入
    example_input = {
        "title": "🤔 大语言模型的推理能力解析",
        "content": """
## 📖 核心概念

大语言模型（LLM）的推理能力是当前AI研究的热点。

**Chain of Thought** 通过让模型逐步思考来提升推理效果。

> 💡 简单来说：就像考试时把解题步骤写下来，思路会更清晰。

## 🌟 实际应用

让我们看看实际中的应用：

*   ChatGPT
*   代码助手

觉得有用的话，点个赞呗~ ✨
        """,
        "author": "AI媒体系统",
        "theme": "blue"
    }

    result = format_from_dict(example_input)

    if result["success"]:
        # 输出 HTML 到文件
        output_file = "output.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["html"])
        print(f"✅ 排版完成，已保存到 {output_file}")
        print(f"   标题数量: {len(result['metadata'].get('headings', []))}")
    else:
        print(f"❌ 错误: {result['error']}")
        sys.exit(1)
