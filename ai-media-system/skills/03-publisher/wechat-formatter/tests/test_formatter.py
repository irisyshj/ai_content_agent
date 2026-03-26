"""WeChat Formatter 测试"""

import pytest
from formatter import WeChatFormatter, FormatResult, format_from_dict


class TestWeChatFormatter:
    """微信排版器测试"""

    def setup_method(self):
        self.formatter = WeChatFormatter(theme="default")

    def test_init_with_theme(self):
        """测试初始化主题"""
        formatter = WeChatFormatter(theme="blue")
        assert formatter.theme["accent"] == "#3498db"

    def test_init_with_invalid_theme(self):
        """测试无效主题"""
        formatter = WeChatFormatter(theme="invalid")
        assert formatter.theme == WeChatFormatter.THEMES["default"]

    def test_escape_html(self):
        """测试 HTML 转义"""
        result = self.formatter._escape_html("<script>alert('xss')</script>")
        assert "&lt;" in result
        assert "&gt;" in result

    def test_parse_headings(self):
        """测试标题解析"""
        content = "## 标题一\n### 标题二"
        result, headings = self.formatter._parse_headings(content)

        assert len(headings) == 2
        assert headings[0]["level"] == 2
        assert headings[0]["text"] == "标题一"

    def test_parse_code_blocks(self):
        """测试代码块解析"""
        content = "```python\nprint('hello')\n```"
        result = self.formatter._parse_code_blocks(content)

        assert "<pre>" in result
        assert "<code>" in result

    def test_parse_bold_italic(self):
        """测试粗体斜体解析"""
        content = "**粗体** 和 *斜体*"
        result = self.formatter._parse_bold_italic(content)

        assert "<strong>" in result
        assert "<em>" in result

    def test_format_success(self):
        """测试成功排版"""
        content = """
## 测试标题

这是一段**粗体**文字和*斜体*文字。

> 这是引用块
        """

        result = self.formatter.format(content, title="测试文章")

        assert result.success is True
        assert result.html
        assert "<h2>" in result.html
        assert "<strong>" in result.html
        assert "<blockquote>" in result.html

    def test_format_with_theme(self):
        """测试主题切换"""
        content = "# 测试"
        result = self.formatter.format(content, theme="green")

        assert result.success is True
        assert "#27ae60" in result.html or "#2ecc71" in result.html

    def test_build_container(self):
        """测试容器构建"""
        content = "<p>测试内容</p>"
        container = self.formatter._build_container(
            content,
            title="测试标题",
            author="测试作者"
        )

        assert "测试标题" in container
        assert "测试作者" in container
        assert "测试内容" in container
        assert "<div" in container


class TestFormatFromDict:
    """字典接口测试"""

    def test_format_from_dict_success(self):
        """测试成功情况"""
        input_data = {
            "title": "测试文章",
            "content": "## 测试标题\n\n测试内容",
            "author": "AI",
            "theme": "blue"
        }

        result = format_from_dict(input_data)

        assert result["success"] is True
        assert result["html"]
        assert "测试文章" in result["html"]

    def test_format_from_dict_empty_content(self):
        """测试空内容"""
        input_data = {
            "title": "",
            "content": "",
            "author": ""
        }

        result = format_from_dict(input_data)

        # 应该能处理
        assert result["success"] is True


class TestThemes:
    """主题测试"""

    def test_all_themes_exist(self):
        """测试所有主题存在"""
        for theme_name in WeChatFormatter.THEMES:
            formatter = WeChatFormatter(theme=theme_name)
            assert formatter.theme == WeChatFormatter.THEMES[theme_name]

    def test_theme_has_required_colors(self):
        """测试主题包含必需颜色"""
        required_keys = ["primary", "accent", "background", "text",
                        "secondary", "border", "code_bg"]

        for theme_name, theme_colors in WeChatFormatter.THEMES.items():
            for key in required_keys:
                assert key in theme_colors, f"{theme_name} missing {key}"
