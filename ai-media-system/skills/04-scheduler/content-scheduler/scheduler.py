"""
Content Scheduler - 内容调度 Agent

管理内容队列和定时发布
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class ScheduledContent:
    """待调度内容"""
    id: str
    title: str
    html: str
    images: List[str] = field(default_factory=list)
    platform: str = "wechat"
    status: str = "pending"  # pending | scheduled | published | failed
    scheduled_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d['scheduled_at'] = self.scheduled_at.isoformat() if self.scheduled_at else None
        d['created_at'] = self.created_at.isoformat()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> 'ScheduledContent':
        if d.get('scheduled_at'):
            d['scheduled_at'] = datetime.fromisoformat(d['scheduled_at'])
        if d.get('created_at'):
            d['created_at'] = datetime.fromisoformat(d['created_at'])
        return cls(**d)


@dataclass
class ScheduleResult:
    """调度结果"""
    success: bool
    content_id: str = ""
    scheduled_at: Optional[datetime] = None
    error: Optional[str] = None


class ContentScheduler:
    """
    内容调度器

    功能：
    - 添加内容到队列
    - 设置发布时间
    - 获取待发布内容
    - 标记发布状态
    """

    def __init__(self, queue_dir: str = "data/schedule"):
        """
        初始化调度器

        Args:
            queue_dir: 队列数据目录
        """
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self.queue_file = self.queue_dir / "queue.json"
        self._counter = 0

        # 加载现有队列
        self.queue = self._load_queue()

    def _load_queue(self) -> List[ScheduledContent]:
        """加载队列"""
        if not self.queue_file.exists():
            return []

        try:
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [ScheduledContent.from_dict(item) for item in data]
        except:
            return []

    def _save_queue(self):
        """保存队列"""
        data = [item.to_dict() for item in self.queue]
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(
        self,
        title: str,
        html: str,
        platform: str = "wechat",
        images: List[str] = None,
        delay_hours: int = 0,
        schedule_at: Optional[datetime] = None
    ) -> ScheduleResult:
        """
        添加内容到调度队列

        Args:
            title: 标题
            html: HTML内容
            platform: 发布平台
            images: 图片列表
            delay_hours: 延迟小时数（相对于现在）
            schedule_at: 指定发布时间

        Returns:
            ScheduleResult: 调度结果
        """
        try:
            self._counter += 1
            content_id = f"sc_{self._counter:04d}"

            # 计算发布时间
            if schedule_at:
                scheduled_at = schedule_at
            elif delay_hours > 0:
                scheduled_at = datetime.now() + timedelta(hours=delay_hours)
            else:
                scheduled_at = None  # 立即发布

            content = ScheduledContent(
                id=content_id,
                title=title,
                html=html,
                images=images or [],
                platform=platform,
                status="scheduled" if scheduled_at else "pending",
                scheduled_at=scheduled_at
            )

            self.queue.append(content)
            self._save_queue()

            return ScheduleResult(
                success=True,
                content_id=content_id,
                scheduled_at=scheduled_at
            )

        except Exception as e:
            import traceback
            return ScheduleResult(
                success=False,
                error=f"添加失败: {str(e)}\n{traceback.format_exc()}"
            )

    def get_pending(self) -> List[ScheduledContent]:
        """获取待发布内容"""
        now = datetime.now()
        return [
            item for item in self.queue
            if item.status in ["pending", "scheduled"]
            and (item.scheduled_at is None or item.scheduled_at <= now)
        ]

    def get_all(self) -> List[Dict]:
        """获取所有队列项"""
        return [item.to_dict() for item in self.queue]

    def mark_status(self, content_id: str, status: str) -> bool:
        """
        更新内容状态

        Args:
            content_id: 内容ID
            status: 新状态

        Returns:
            是否成功
        """
        for item in self.queue:
            if item.id == content_id:
                item.status = status
                self._save_queue()
                return True
        return False

    def remove(self, content_id: str) -> bool:
        """从队列中移除"""
        original_len = len(self.queue)
        self.queue = [item for item in self.queue if item.id != content_id]
        if len(self.queue) < original_len:
            self._save_queue()
            return True
        return False

    def get_optimal_times(self, platform: str = "wechat") -> List[str]:
        """
        获取最佳发布时间

        Args:
            platform: 平台

        Returns:
            最佳时间列表
        """
        # 不同平台的最佳发布时间
        optimal_times = {
            "wechat": ["08:00", "12:00", "18:00", "21:00"],
            "xhs": ["07:00", "09:00", "19:00", "22:00"],
            "zhihu": ["09:00", "14:00", "20:00"],
            "jianshu": ["08:00", "20:00"]
        }

        return optimal_times.get(platform, ["08:00", "12:00", "18:00", "21:00"])

    def suggest_schedule(self, platform: str = "wechat") -> datetime:
        """
        建议下一个最佳发布时间

        Args:
            platform: 平台

        Returns:
            建议的发布时间
        """
        optimal = self.get_optimal_times(platform)

        now = datetime.now()
        current_time = now.strftime("%H:%M")

        # 找下一个最佳时间
        for time_str in optimal:
            if time_str > current_time:
                hour, minute = map(int, time_str.split(':'))
                return now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        # 如果今天没有合适的，用明天的第一个时间
        hour, minute = map(int, optimal[0].split(':'))
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)

    def get_queue_stats(self) -> Dict:
        """获取队列统计"""
        pending = len([i for i in self.queue if i.status == "pending"])
        scheduled = len([i for i in self.queue if i.status == "scheduled"])
        published = len([i for i in self.queue if i.status == "published"])
        failed = len([i for i in self.queue if i.status == "failed"])

        return {
            "total": len(self.queue),
            "pending": pending,
            "scheduled": scheduled,
            "published": published,
            "failed": failed
        }


def schedule_from_dict(input_data: dict) -> dict:
    """
    从字典输入调度内容

    Args:
        input_data: {
            "title": "...",
            "html": "...",
            "platform": "wechat",
            "delay_hours": 2
        }

    Returns:
        dict: 结果字典
    """
    scheduler = ContentScheduler()
    result = scheduler.add(
        title=input_data.get("title", ""),
        html=input_data.get("html", ""),
        platform=input_data.get("platform", "wechat"),
        images=input_data.get("images", []),
        delay_hours=input_data.get("delay_hours", 0),
        schedule_at=input_data.get("schedule_at")
    )

    if not result.success:
        return {
            "success": False,
            "error": result.error
        }

    return {
        "success": True,
        "content_id": result.content_id,
        "scheduled_at": result.scheduled_at.isoformat() if result.scheduled_at else None
    }


# CLI 接口
if __name__ == "__main__":
    import sys

    scheduler = ContentScheduler()

    # 显示统计
    stats = scheduler.get_queue_stats()
    print("📊 调度队列统计:")
    print(f"   总计: {stats['total']}")
    print(f"   待发布: {stats['pending']}")
    print(f"   已调度: {stats['scheduled']}")
    print(f"   已发布: {stats['published']}")
    print(f"   失败: {stats['failed']}")

    # 显示最佳时间
    print("\n⏰ 最佳发布时间 (微信公众号):")
    for t in scheduler.get_optimal_times("wechat"):
        print(f"   {t}")

    # 建议下一个时间
    next_time = scheduler.suggest_schedule("wechat")
    print(f"\n📅 建议下一个发布时间: {next_time.strftime('%Y-%m-%d %H:%M')}")

    # 待发布内容
    pending = scheduler.get_pending()
    if pending:
        print(f"\n📝 待发布内容 ({len(pending)}):")
        for item in pending:
            print(f"   - {item.title}")
    else:
        print("\n📝 暂无待发布内容")
