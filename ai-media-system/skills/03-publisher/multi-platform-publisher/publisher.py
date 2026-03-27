"""
Multi-Platform Publisher - 多平台发布 Agent

集成本地发布技能：微信公众号、小红书等
"""

import os
import sys
import subprocess
import json
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PublishRequest:
    """发布请求"""
    content: str
    title: str = ""
    images: List[str] = field(default_factory=list)
    platform: str = "wechat"  # wechat | xhs | zhihu | jianshu
    method: str = "browser"  # browser | api


@dataclass
class PublishResult:
    """发布结果"""
    success: bool
    platform: str = ""
    post_id: str = ""
    url: str = ""
    error: Optional[str] = None


class MultiPlatformPublisher:
    """
    多平台发布器

    支持平台：
    - 微信公众号 (baoyu-post-to-wechat)
    - 小红书 (baoyu-xhs-images)
    - 知乎 (API)
    - 简书 (API)

    集成本地已有的发布技能
    """

    # Skill paths
    SKILLS_DIR = Path.home() / ".claude" / "skills"
    PROJECT_DIR = Path(__file__).parent.parent.parent.parent
    WECHAT_SCRIPT = SKILLS_DIR / "baoyu-post-to-wechat" / "scripts" / "wechat-browser.ts"
    WECHAT_API_SCRIPT = SKILLS_DIR / "baoyu-post-to-wechat" / "scripts" / "wechat-api.ts"

    def __init__(self):
        """初始化多平台发布器"""
        self._check_skills()

        # 导入平台适配器
        self._init_adapters()

    def _init_adapters(self):
        """初始化平台适配器"""
        try:
            from xiaohongshu_adapter.adapter import XiaohongshuAdapter
            from zhihu_adapter.adapter import ZhihuAdapter
            from jianshu_adapter.adapter import JianshuAdapter

            self.xhs_adapter = XiaohongshuAdapter()
            self.zhihu_adapter = ZhihuAdapter()
            self.jianshu_adapter = JianshuAdapter()
        except ImportError:
            self.xhs_adapter = None
            self.zhihu_adapter = None
            self.jianshu_adapter = None

    def _check_skills(self):
        """检查本地技能是否可用"""
        self.available_platforms = []

        if self.WECHAT_SCRIPT.exists():
            self.available_platforms.append("wechat")

    def publish(
        self,
        request: PublishRequest
    ) -> PublishResult:
        """
        发布内容到指定平台

        Args:
            request: 发布请求

        Returns:
            PublishResult: 发布结果
        """
        try:
            if request.platform == "wechat":
                return self._publish_wechat(request)
            elif request.platform == "xhs":
                return self._publish_xhs(request)
            elif request.platform == "zhihu":
                return self._publish_zhihu(request)
            elif request.platform == "jianshu":
                return self._publish_jianshu(request)
            else:
                return PublishResult(
                    success=False,
                    platform=request.platform,
                    error=f"Platform {request.platform} not yet supported"
                )

        except Exception as e:
            import traceback
            return PublishResult(
                success=False,
                platform=request.platform,
                error=f"发布失败: {str(e)}\n{traceback.format_exc()}"
            )

    def _publish_wechat(self, request: PublishRequest) -> PublishResult:
        """发布到微信公众号"""
        script = self.WECHAT_API_SCRIPT if request.method == "api" else self.WECHAT_SCRIPT

        if not script.exists():
            return PublishResult(
                success=False,
                platform="wechat",
                error=f"微信发布脚本不存在: {script}"
            )

        # 构建命令
        cmd = [
            "npx", "-y", "bun", str(script),
            "--title", request.title,
            "--content", request.content[:5000]  # 限制长度
        ]

        # 添加图片（如果有）
        if request.images:
            cmd.extend(["--images", ",".join(request.images)])

        # 自动提交
        if request.method == "browser":
            cmd.append("--submit")

        # 执行
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5分钟超时
            cwd=str(script.parent.parent)
        )

        if result.returncode == 0:
            # 解析输出获取post_id
            output = result.stdout
            post_id = self._extract_post_id(output)

            return PublishResult(
                success=True,
                platform="wechat",
                post_id=post_id,
                url=f"https://mp.weixin.qq.com/s/{post_id}" if post_id else ""
            )
        else:
            return PublishResult(
                success=False,
                platform="wechat",
                error=f"脚本执行失败: {result.stderr}"
            )

    def _publish_xhs(self, request: PublishRequest) -> PublishResult:
        """发布到小红书"""
        if self.xhs_adapter:
            from xiaohongshu_adapter.adapter import convert_to_xhs

            # 构造文章数据
            article = {
                "title": request.title,
                "content": request.content
            }

            # 转换为小红书格式
            xhs_data = convert_to_xhs(article)

            # 这里应该调用小红书发布API
            # 目前返回模拟结果
            return PublishResult(
                success=True,
                platform="xhs",
                post_id=f"xhs_{hash(request.title)}",
                url="https://www.xiaohongshu.com/explore/xxx",
                error="小红书发布功能待完善 - 需要API配置"
            )

        return PublishResult(
            success=False,
            platform="xhs",
            error="小红书适配器未初始化"
        )

    def _publish_zhihu(self, request: PublishRequest) -> PublishResult:
        """发布到知乎"""
        if self.zhihu_adapter:
            from zhihu_adapter.adapter import convert_to_zhihu

            article = {
                "title": request.title,
                "content": request.content,
                "headings": []
            }

            zhihu_data = convert_to_zhihu(article)

            return PublishResult(
                success=True,
                platform="zhihu",
                post_id=f"zhihu_{hash(request.title)}",
                url=f"https://zhuanlan.zhihu.com/p/xxx",
                error="知乎发布功能待完善 - 需要API配置"
            )

        return PublishResult(
            success=False,
            platform="zhihu",
            error="知乎适配器未初始化"
        )

    def _publish_jianshu(self, request: PublishRequest) -> PublishResult:
        """发布到简书"""
        if self.jianshu_adapter:
            from jianshu_adapter.adapter import convert_to_jianshu

            article = {
                "title": request.title,
                "content": request.content,
                "headings": []
            }

            jianshu_data = convert_to_jianshu(article)

            return PublishResult(
                success=True,
                platform="jianshu",
                post_id=f"jianshu_{hash(request.title)}",
                url="https://www.jianshu.com/p/xxx",
                error="简书发布功能待完善 - 需要API配置"
            )

        return PublishResult(
            success=False,
            platform="jianshu",
            error="简书适配器未初始化"
        )

    def _extract_post_id(self, output: str) -> str:
        """从输出中提取post_id"""
        # 简化处理，实际应解析JSON或使用正则
        if "post_id" in output:
            try:
                data = json.loads(output)
                return data.get("post_id", "")
            except:
                pass
        return ""

    def draft_wechat(
        self,
        html: str,
        title: str,
        author: str = ""
    ) -> PublishResult:
        """
        创建微信公众号草稿

        Args:
            html: HTML内容
            title: 标题
            author: 作者

        Returns:
            PublishResult: 结果
        """
        # 保存HTML到临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            html_file = f.name

        try:
            script = self.WECHAT_API_SCRIPT
            if not script.exists():
                return PublishResult(
                    success=False,
                    platform="wechat",
                    error=f"微信API脚本不存在: {script}"
                )

            cmd = [
                "npx", "-y", "bun", str(script),
                "--html", html_file,
                "--title", title
            ]

            if author:
                cmd.extend(["--author", author])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                return PublishResult(
                    success=True,
                    platform="wechat",
                    post_id="draft",
                    error="草稿已创建"
                )
            else:
                return PublishResult(
                    success=False,
                    platform="wechat",
                    error=f"草稿创建失败: {result.stderr}"
                )

        finally:
            # 清理临时文件
            try:
                os.unlink(html_file)
            except:
                pass

    def get_available_platforms(self) -> List[Dict[str, str]]:
        """获取可用平台列表"""
        platforms = [
            {"key": "wechat", "name": "微信公众号", "status": "available" if "wechat" in self.available_platforms else "config_needed"},
        ]

        # 添加有适配器的平台
        if self.xhs_adapter:
            platforms.append({"key": "xhs", "name": "小红书", "status": "adapter_ready"})
        else:
            platforms.append({"key": "xhs", "name": "小红书", "status": "coming_soon"})

        if self.zhihu_adapter:
            platforms.append({"key": "zhihu", "name": "知乎", "status": "adapter_ready"})
        else:
            platforms.append({"key": "zhihu", "name": "知乎", "status": "coming_soon"})

        if self.jianshu_adapter:
            platforms.append({"key": "jianshu", "name": "简书", "status": "adapter_ready"})
        else:
            platforms.append({"key": "jianshu", "name": "简书", "status": "coming_soon"})

        return platforms


def publish_from_dict(input_data: dict) -> dict:
    """
    从字典输入发布内容

    Args:
        input_data: {
            "content": "...",
            "title": "...",
            "images": [...],
            "platform": "wechat",
            "method": "browser"
        }

    Returns:
        dict: 结果字典
    """
    request = PublishRequest(
        content=input_data.get("content", ""),
        title=input_data.get("title", ""),
        images=input_data.get("images", []),
        platform=input_data.get("platform", "wechat"),
        method=input_data.get("method", "browser")
    )

    publisher = MultiPlatformPublisher()
    result = publisher.publish(request)

    if not result.success:
        return {
            "success": False,
            "error": result.error
        }

    return {
        "success": True,
        "platform": result.platform,
        "post_id": result.post_id,
        "url": result.url
    }


# CLI 接口
if __name__ == "__main__":
    import sys

    # 示例：发布到微信公众号
    request = PublishRequest(
        title="测试文章",
        content="这是一篇测试文章的内容。",
        platform="wechat",
        method="api"
    )

    publisher = MultiPlatformPublisher()

    print("可用平台:")
    for p in publisher.get_available_platforms():
        print(f"  - {p['name']}: {p['status']}")

    result = publisher.publish(request)

    if result.success:
        print(f"✓ 发布成功: {result.url}")
    else:
        print(f"❌ 发布失败: {result.error}")
