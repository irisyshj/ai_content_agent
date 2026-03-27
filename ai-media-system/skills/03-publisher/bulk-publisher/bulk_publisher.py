"""
Bulk Publisher - 批量发布器

一键发布到多个平台
"""

import asyncio
from typing import Dict, List
from dataclasses import dataclass, field
from datetime import datetime
import sys
from pathlib import Path

# Add the absolute path to multi-platform-publisher
publisher_dir = Path(__file__).parent.parent / "multi-platform-publisher"
sys.path.insert(0, str(publisher_dir))
from publisher import MultiPlatformPublisher, PublishRequest


@dataclass
class BulkPublishRequest:
    """批量发布请求"""
    title: str
    content: str
    platforms: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    delay_seconds: int = 5  # 平台间发布延迟


@dataclass
class BulkPublishResult:
    """批量发布结果"""
    success: bool
    total: int = 0
    successful: int = 0
    failed: int = 0
    results: List[Dict] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class BulkPublisher:
    """
    批量发布器

    功能：
    - 一键发布到多个平台
    - 平台间自动延迟
    - 汇总发布结果
    """

    def __init__(self):
        """初始化批量发布器"""
        self.publisher = MultiPlatformPublisher()

    async def publish_bulk(
        self,
        request: BulkPublishRequest
    ) -> BulkPublishResult:
        """
        批量发布到多个平台

        Args:
            request: 批量发布请求

        Returns:
            BulkPublishResult: 批量发布结果
        """
        result = BulkPublishResult(success=True)
        result.total = len(request.platforms)

        for platform in request.platforms:
            # 创建发布请求
            pub_request = PublishRequest(
                content=request.content,
                title=request.title,
                images=request.images,
                platform=platform
            )

            # 发布到平台
            pub_result = self.publisher.publish(pub_request)

            # 记录结果
            platform_result = {
                "platform": platform,
                "success": pub_result.success,
                "post_id": pub_result.post_id,
                "url": pub_result.url,
                "timestamp": datetime.now().isoformat()
            }
            result.results.append(platform_result)

            if pub_result.success:
                result.successful += 1
            else:
                result.failed += 1
                result.errors.append(f"{platform}: {pub_result.error}")

            # 延迟（避免平台限流）
            if platform != request.platforms[-1]:  # 不是最后一个
                await asyncio.sleep(request.delay_seconds)

        # 判断整体是否成功
        result.success = result.failed == 0

        return result

    def publish_bulk_sync(
        self,
        request: BulkPublishRequest
    ) -> BulkPublishResult:
        """
        同步批量发布（无async）

        Args:
            request: 批量发布请求

        Returns:
            BulkPublishResult: 批量发布结果
        """
        result = BulkPublishResult(success=True)
        result.total = len(request.platforms)

        for platform in request.platforms:
            pub_request = PublishRequest(
                content=request.content,
                title=request.title,
                images=request.images,
                platform=platform
            )

            pub_result = self.publisher.publish(pub_request)

            platform_result = {
                "platform": platform,
                "success": pub_result.success,
                "post_id": pub_result.post_id,
                "url": pub_result.url,
                "timestamp": datetime.now().isoformat()
            }
            result.results.append(platform_result)

            if pub_result.success:
                result.successful += 1
            else:
                result.failed += 1
                result.errors.append(f"{platform}: {pub_result.error}")

        result.success = result.failed == 0

        return result

    def get_supported_platforms(self) -> List[Dict]:
        """获取支持的平台列表"""
        return self.publisher.get_available_platforms()


def bulk_publish_from_dict(input_data: dict) -> dict:
    """
    从字典输入批量发布

    Args:
        input_data: {
            "title": "...",
            "content": "...",
            "platforms": ["wechat", "xhs", "zhihu"],
            "delay_seconds": 5
        }

    Returns:
        dict: 结果字典
    """
    request = BulkPublishRequest(
        title=input_data.get("title", ""),
        content=input_data.get("content", ""),
        platforms=input_data.get("platforms", ["wechat"]),
        images=input_data.get("images", []),
        delay_seconds=input_data.get("delay_seconds", 5)
    )

    publisher = BulkPublisher()
    result = publisher.publish_bulk_sync(request)

    return {
        "success": result.success,
        "total": result.total,
        "successful": result.successful,
        "failed": result.failed,
        "results": result.results,
        "errors": result.errors
    }


# CLI 接口
if __name__ == "__main__":
    import sys

    # 示例批量发布
    request = BulkPublishRequest(
        title="AI技术解析：大语言模型的推理能力",
        content="这是一篇关于AI技术深度解析的文章...",
        platforms=["wechat", "xhs", "zhihu"],
        delay_seconds=2
    )

    publisher = BulkPublisher()

    print("📤 批量发布到多个平台")
    print(f"   标题: {request.title}")
    print(f"   平台: {', '.join(request.platforms)}")
    print()

    result = publisher.publish_bulk_sync(request)

    print(f"✓ 发布完成: {result.successful}/{result.total} 成功")

    if result.errors:
        print("\n❌ 失败的平台:")
        for error in result.errors:
            print(f"   - {error}")

    print("\n📊 详细结果:")
    for r in result.results:
        status = "✓" if r["success"] else "✗"
        print(f"   {status} {r['platform']}: {r.get('url', 'N/A')}")
