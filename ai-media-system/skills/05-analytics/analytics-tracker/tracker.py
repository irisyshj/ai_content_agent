"""
Analytics Dashboard - 数据分析仪表板

追踪内容表现、平台数据、用户互动
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass, field, asdict
from pathlib import Path
from collections import defaultdict


@dataclass
class ContentMetrics:
    """内容指标"""
    content_id: str
    title: str
    platform: str
    published_at: datetime
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    collects: int = 0
    click_rate: float = 0.0
    conversion_rate: float = 0.0

    def to_dict(self) -> dict:
        d = asdict(self)
        d['published_at'] = self.published_at.isoformat()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> 'ContentMetrics':
        if d.get('published_at'):
            d['published_at'] = datetime.fromisoformat(d['published_at'])
        return cls(**d)

    @property
    def engagement_rate(self) -> float:
        """互动率 = (likes + comments + shares) / views * 100"""
        if self.views == 0:
            return 0.0
        return (self.likes + self.comments + self.shares) / self.views * 100

    @property
    def total_engagement(self) -> int:
        """总互动数"""
        return self.likes + self.comments + self.shares + self.collects


@dataclass
class PlatformStats:
    """平台统计"""
    platform: str
    total_posts: int = 0
    total_views: int = 0
    total_likes: int = 0
    avg_engagement_rate: float = 0.0
    best_post_id: str = ""
    best_post_views: int = 0


@dataclass
class DailyStats:
    """每日统计"""
    date: str  # YYYY-MM-DD
    posts_published: int = 0
    total_views: int = 0
    total_engagement: int = 0


class AnalyticsTracker:
    """
    数据分析追踪器

    功能：
    - 记录内容发布数据
    - 追踪内容表现
    - 计算平台统计
    - 生成分析报告
    """

    def __init__(self, data_dir: str = "data/analytics"):
        """
        初始化分析追踪器

        Args:
            data_dir: 数据目录
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.metrics_file = self.data_dir / "metrics.json"
        self.daily_file = self.data_dir / "daily.json"

        self.metrics: List[ContentMetrics] = self._load_metrics()
        self.daily_stats: Dict[str, DailyStats] = self._load_daily()

    def _load_metrics(self) -> List[ContentMetrics]:
        """加载指标数据"""
        if not self.metrics_file.exists():
            return []

        try:
            with open(self.metrics_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [ContentMetrics.from_dict(item) for item in data]
        except:
            return []

    def _load_daily(self) -> Dict[str, DailyStats]:
        """加载每日统计"""
        if not self.daily_file.exists():
            return {}

        try:
            with open(self.daily_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    date: DailyStats(date=date, **stats)
                    for date, stats in data.items()
                }
        except:
            return {}

    def _save_metrics(self):
        """保存指标数据"""
        data = [m.to_dict() for m in self.metrics]
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _save_daily(self):
        """保存每日统计"""
        data = {
            date: asdict(stats)
            for date, stats in self.daily_stats.items()
        }
        with open(self.daily_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def track_content(
        self,
        content_id: str,
        title: str,
        platform: str,
        published_at: Optional[datetime] = None
    ) -> ContentMetrics:
        """
        追踪新内容

        Args:
            content_id: 内容ID
            title: 标题
            platform: 平台
            published_at: 发布时间

        Returns:
            ContentMetrics: 创建的指标对象
        """
        if published_at is None:
            published_at = datetime.now()

        metrics = ContentMetrics(
            content_id=content_id,
            title=title,
            platform=platform,
            published_at=published_at
        )

        self.metrics.append(metrics)
        self._save_metrics()

        # 更新每日统计
        date_str = published_at.strftime("%Y-%m-%d")
        if date_str not in self.daily_stats:
            self.daily_stats[date_str] = DailyStats(date=date_str)
        self.daily_stats[date_str].posts_published += 1
        self._save_daily()

        return metrics

    def update_metrics(
        self,
        content_id: str,
        views: Optional[int] = None,
        likes: Optional[int] = None,
        comments: Optional[int] = None,
        shares: Optional[int] = None,
        collects: Optional[int] = None
    ) -> bool:
        """
        更新内容指标

        Args:
            content_id: 内容ID
            views: 浏览数
            likes: 点赞数
            comments: 评论数
            shares: 分享数
            collects: 收藏数

        Returns:
            是否更新成功
        """
        for m in self.metrics:
            if m.content_id == content_id:
                if views is not None:
                    m.views = views
                if likes is not None:
                    m.likes = likes
                if comments is not None:
                    m.comments = comments
                if shares is not None:
                    m.shares = shares
                if collects is not None:
                    m.collects = collects

                self._save_metrics()
                return True
        return False

    def get_content_metrics(self, content_id: str) -> Optional[ContentMetrics]:
        """获取内容指标"""
        for m in self.metrics:
            if m.content_id == content_id:
                return m
        return None

    def get_platform_stats(self, platform: Optional[str] = None) -> List[PlatformStats]:
        """
        获取平台统计

        Args:
            platform: 指定平台，None表示所有平台

        Returns:
            平台统计列表
        """
        platforms = set(m.platform for m in self.metrics) if platform is None else {platform}
        stats_list = []

        for plat in platforms:
            platform_metrics = [m for m in self.metrics if m.platform == plat]

            if not platform_metrics:
                continue

            total_posts = len(platform_metrics)
            total_views = sum(m.views for m in platform_metrics)
            total_likes = sum(m.likes for m in platform_metrics)
            total_engagement = sum(m.total_engagement for m in platform_metrics)

            avg_engagement = total_engagement / total_views if total_views > 0 else 0

            # 找出最佳帖子
            best = max(platform_metrics, key=lambda m: m.views)

            stats_list.append(PlatformStats(
                platform=plat,
                total_posts=total_posts,
                total_views=total_views,
                total_likes=total_likes,
                avg_engagement_rate=avg_engagement,
                best_post_id=best.content_id,
                best_post_views=best.views
            ))

        return stats_list

    def get_top_posts(self, limit: int = 10, platform: Optional[str] = None) -> List[ContentMetrics]:
        """
        获取热门帖子

        Args:
            limit: 返回数量
            platform: 平台筛选

        Returns:
            热门帖子列表
        """
        metrics = self.metrics
        if platform:
            metrics = [m for m in metrics if m.platform == platform]

        return sorted(metrics, key=lambda m: m.views, reverse=True)[:limit]

    def get_summary(self, days: int = 30) -> Dict:
        """
        获取数据摘要

        Args:
            days: 统计天数

        Returns:
            摘要数据
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        recent_metrics = [m for m in self.metrics if m.published_at >= cutoff_date]

        if not recent_metrics:
            return {
                "period_days": days,
                "total_posts": 0,
                "total_views": 0,
                "total_engagement": 0,
                "avg_views_per_post": 0,
                "platforms": []
            }

        total_posts = len(recent_metrics)
        total_views = sum(m.views for m in recent_metrics)
        total_engagement = sum(m.total_engagement for m in recent_metrics)

        return {
            "period_days": days,
            "total_posts": total_posts,
            "total_views": total_views,
            "total_engagement": total_engagement,
            "avg_views_per_post": total_views / total_posts if total_posts > 0 else 0,
            "platforms": self.get_platform_stats()
        }

    def get_daily_trend(self, days: int = 30) -> List[Dict]:
        """
        获取每日趋势

        Args:
            days: 天数

        Returns:
            每日数据列表
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        trend = []

        for date_str in sorted(self.daily_stats.keys()):
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date >= cutoff_date:
                stats = self.daily_stats[date_str]
                trend.append({
                    "date": date_str,
                    "posts": stats.posts_published,
                    "views": stats.total_views,
                    "engagement": stats.total_engagement
                })

        return trend

    def generate_report(self, days: int = 30) -> str:
        """
        生成文本报告

        Args:
            days: 统计天数

        Returns:
            报告文本
        """
        summary = self.get_summary(days)
        platform_stats = self.get_platform_stats()
        top_posts = self.get_top_posts(5)

        lines = [
            "# 数据分析报告",
            f"统计周期: {days} 天",
            "",
            "## 总览",
            f"- 发布内容: {summary['total_posts']} 篇",
            f"- 总浏览量: {summary['total_views']:,}",
            f"- 总互动数: {summary['total_engagement']:,}",
            f"- 平均浏览: {summary['avg_views_per_post']:.0f}",
            "",
            "## 平台表现"
        ]

        for stats in platform_stats:
            lines.append(f"\n### {stats.platform}")
            lines.append(f"- 发布数: {stats.total_posts}")
            lines.append(f"- 总浏览: {stats.total_views:,}")
            lines.append(f"- 平均互动率: {stats.avg_engagement_rate:.2f}%")
            lines.append(f"- 最佳帖子: {stats.best_post_id} ({stats.best_post_views:,} 浏览)")

        lines.append("\n## 热门内容 TOP 5")
        for i, post in enumerate(top_posts[:5], 1):
            lines.append(f"\n{i}. {post.title}")
            lines.append(f"   - 平台: {post.platform}")
            lines.append(f"   - 浏览: {post.views:,}")
            lines.append(f"   - 互动率: {post.engagement_rate:.2f}%")

        return "\n".join(lines)


def get_analytics_from_dict(input_data: dict) -> dict:
    """
    从字典输入获取分析数据

    Args:
        input_data: {"action": "summary | top_posts | platform_stats", "days": 30}

    Returns:
        dict: 结果字典
    """
    tracker = AnalyticsTracker()
    action = input_data.get("action", "summary")
    days = input_data.get("days", 30)
    platform = input_data.get("platform")

    if action == "summary":
        return {"success": True, **tracker.get_summary(days)}
    elif action == "top_posts":
        return {
            "success": True,
            "posts": [m.to_dict() for m in tracker.get_top_posts(input_data.get("limit", 10), platform)]
        }
    elif action == "platform_stats":
        return {
            "success": True,
            "platforms": [asdict(s) for s in tracker.get_platform_stats(platform)]
        }
    elif action == "daily_trend":
        return {
            "success": True,
            "trend": tracker.get_daily_trend(days)
        }
    else:
        return {"success": False, "error": f"Unknown action: {action}"}


# CLI 接口
if __name__ == "__main__":
    import sys

    tracker = AnalyticsTracker()

    # 生成报告
    print(tracker.generate_report(30))

    # 显示每日趋势
    print("\n## 每日趋势 (最近7天)")
    trend = tracker.get_daily_trend(7)
    for day in trend:
        print(f"  {day['date']}: {day['posts']} 篇, {day['views']} 浏览")
