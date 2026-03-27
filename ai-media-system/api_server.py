"""
AI Media System API Server

提供 HTTP API 接口供 n8n 工作流调用
"""

import json
import sys
import logging
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 添加 skills 子模块路径
sys.path.insert(0, str(project_root / "skills" / "02-writer" / "infographic-generator"))
sys.path.insert(0, str(project_root / "skills" / "03-publisher" / "multi-platform-publisher"))
sys.path.insert(0, str(project_root / "skills" / "03-publisher" / "xiaohongshu-adapter"))
sys.path.insert(0, str(project_root / "skills" / "03-publisher" / "zhihu-adapter"))
sys.path.insert(0, str(project_root / "skills" / "03-publisher" / "jianshu-adapter"))
sys.path.insert(0, str(project_root / "skills" / "03-publisher" / "bulk-publisher"))
sys.path.insert(0, str(project_root / "skills" / "04-scheduler" / "content-scheduler"))
sys.path.insert(0, str(project_root / "skills" / "05-analytics" / "analytics-tracker"))

from pipeline import MVPPipeline
from generator import generate_infographic_from_dict
from publisher import publish_from_dict
from scheduler import schedule_from_dict
from tracker import get_analytics_from_dict, AnalyticsTracker
from bulk_publisher import bulk_publish_from_dict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 Flask 应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化流水线
pipeline = MVPPipeline(project_root=project_root, mock_mode=False)


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "service": "ai-media-system",
        "skills_loaded": pipeline.skills_loaded
    })


@app.route('/api/v1/pipeline/run', methods=['POST'])
def run_pipeline():
    """
    运行完整流水线

    请求体:
    {
        "url": "文章URL（可选）",
        "content": "直接输入内容（可选）",
        "title": "文章标题（配合content使用）",
        "theme": "排版主题"
    }

    响应:
    {
        "success": true,
        "article": {...},
        "html": "...",
        "summary": "..."
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400

        # 获取参数
        url = data.get('url')
        content = data.get('content')
        title = data.get('title', 'AI技术解析')
        theme = data.get('theme', 'blue')

        logger.info(f"Pipeline request: url={url}, has_content={bool(content)}, theme={theme}")

        # 验证输入
        if not url and not content:
            return jsonify({
                "success": False,
                "error": "Either 'url' or 'content' must be provided"
            }), 400

        # 如果直接提供内容，跳过采集
        if content:
            # 构造虚拟采集结果
            collect_result = {
                "success": True,
                "content": {
                    "id": "manual_001",
                    "type": "manual",
                    "url": url or "",
                    "title": title,
                    "content": content,
                    "author": "手动输入"
                }
            }
        else:
            # 步骤1: 采集
            logger.info("Step 1: Collecting content...")
            collect_result = pipeline.step_collect(url)
            if not collect_result["success"]:
                return jsonify({
                    "success": False,
                    "error": f"Collection failed: {collect_result.get('error')}"
                }), 400
            logger.info(f"Collected: {collect_result['content']['title']}")

        # 步骤2: 选题
        logger.info("Step 2: Curating topics...")
        curate_result = pipeline.step_curate([collect_result["content"]])
        if not curate_result["success"]:
            return jsonify({
                "success": False,
                "error": f"Curation failed: {curate_result.get('error')}"
            }), 400

        candidates = curate_result["candidates"]
        if not candidates:
            return jsonify({
                "success": False,
                "error": "No candidates generated"
            }), 400

        selected = candidates[0]
        logger.info(f"Selected topic: {selected['title']}")

        # 步骤3: 创作
        logger.info("Step 3: Writing content...")
        write_result = pipeline.step_write(
            selected,
            collect_result["content"]["content"]
        )
        if not write_result["success"]:
            return jsonify({
                "success": False,
                "error": f"Writing failed: {write_result.get('error')}"
            }), 400

        logger.info(f"Written {write_result['article']['word_count']} words")

        # 步骤4: 排版
        logger.info("Step 4: Formatting...")
        format_result = pipeline.step_format(write_result["article"], theme)
        if not format_result["success"]:
            return jsonify({
                "success": False,
                "error": f"Formatting failed: {format_result.get('error')}"
            }), 400

        logger.info("Pipeline completed successfully")

        return jsonify({
            "success": True,
            "article": write_result["article"],
            "html": format_result["html"],
            "metadata": {
                "summary": curate_result.get("summary", ""),
                "theme": theme
            }
        })

    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/collect', methods=['POST'])
def collect_content():
    """
    采集内容

    请求体:
    {
        "url": "要采集的文章URL"
    }

    响应:
    {
        "success": true,
        "content": {...}
    }
    """
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({
                "success": False,
                "error": "URL is required"
            }), 400

        logger.info(f"Collect request: url={url}")

        result = pipeline.step_collect(url)

        if result["success"]:
            logger.info(f"Collection successful: {result['content']['title']}")
        else:
            logger.warning(f"Collection failed: {result.get('error')}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Collection error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/curate', methods=['POST'])
def curate_topics():
    """
    选题策划

    请求体:
    {
        "content_pool": [
            {"title": "...", "content": "...", "author": "..."}
        ],
        "max_candidates": 5
    }

    响应:
    {
        "success": true,
        "candidates": [...],
        "summary": "..."
    }
    """
    try:
        data = request.get_json()
        content_pool = data.get('content_pool', [])
        max_candidates = data.get('max_candidates', 5)

        logger.info(f"Curate request: {len(content_pool)} contents, max={max_candidates}")

        result = pipeline.step_curate(content_pool)

        if result["success"]:
            logger.info(f"Curated {len(result['candidates'])} candidates")
        else:
            logger.warning(f"Curation failed: {result.get('error')}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Curation error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/write', methods=['POST'])
def write_content():
    """
    内容创作

    请求体:
    {
        "topic": {...},
        "source_content": "原始内容（可选）"
    }

    响应:
    {
        "success": true,
        "article": {...}
    }
    """
    try:
        data = request.get_json()
        topic = data.get('topic')
        source_content = data.get('source_content', '')

        if not topic:
            return jsonify({
                "success": False,
                "error": "Topic is required"
            }), 400

        logger.info(f"Write request: topic={topic.get('title')}")

        result = pipeline.step_write(topic, source_content)

        if result["success"]:
            logger.info(f"Write successful: {result['article']['word_count']} words")
        else:
            logger.warning(f"Write failed: {result.get('error')}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Writing error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/format', methods=['POST'])
def format_content():
    """
    公众号排版

    请求体:
    {
        "article": {"title": "...", "content": "..."},
        "theme": "blue"
    }

    响应:
    {
        "success": true,
        "html": "...",
        "metadata": {...}
    }
    """
    try:
        data = request.get_json()
        article = data.get('article')
        theme = data.get('theme', 'blue')

        if not article:
            return jsonify({
                "success": False,
                "error": "Article is required"
            }), 400

        logger.info(f"Format request: title={article.get('title')}, theme={theme}")

        result = pipeline.step_format(article, theme)

        if result["success"]:
            logger.info("Format successful")
        else:
            logger.warning(f"Format failed: {result.get('error')}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Formatting error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/infographic', methods=['POST'])
def generate_infographic():
    """
    生成信息图

    请求体:
    {
        "article": {"title": "...", "content": "...", "headings": [...]},
        "style": "top-student-notes | glassmorphism | auto",
        "platform": "general | xhs"
    }

    响应:
    {
        "success": true,
        "image_path": "output/infographics/...",
        "style_used": "top-student-notes",
        "platform": "general"
    }
    """
    try:
        data = request.get_json()
        article = data.get('article')
        style = data.get('style', 'auto')
        platform = data.get('platform', 'general')

        if not article:
            return jsonify({
                "success": False,
                "error": "Article is required"
            }), 400

        logger.info(f"Infographic request: title={article.get('title')}, style={style}, platform={platform}")

        result = generate_infographic_from_dict({
            "article": article,
            "style": style,
            "platform": platform
        })

        if result["success"]:
            logger.info(f"Infographic generated: {result['image_path']}")
        else:
            logger.warning(f"Infographic generation failed: {result.get('error')}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Infographic error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/infographic/styles', methods=['GET'])
def list_infographic_styles():
    """
    获取可用信息图风格列表

    响应:
    {
        "success": true,
        "styles": [
            {"key": "top-student-notes", "name": "学霸笔记", "tier": 1},
            ...
        ]
    }
    """
    try:
        from generator import InfographicGenerator

        generator = InfographicGenerator()
        styles = generator.get_available_styles()

        return jsonify({
            "success": True,
            "styles": styles
        })

    except Exception as e:
        logger.error(f"Styles error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/publish', methods=['POST'])
def publish_content():
    """
    发布内容到多平台

    请求体:
    {
        "content": "内容HTML/文本",
        "title": "标题",
        "images": ["图片路径"],
        "platform": "wechat | xhs | zhihu",
        "method": "browser | api"
    }

    响应:
    {
        "success": true,
        "platform": "wechat",
        "post_id": "...",
        "url": "..."
    }
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        title = data.get('title', '')
        images = data.get('images', [])
        platform = data.get('platform', 'wechat')
        method = data.get('method', 'browser')

        if not content:
            return jsonify({
                "success": False,
                "error": "Content is required"
            }), 400

        logger.info(f"Publish request: platform={platform}, method={method}, title={title}")

        result = publish_from_dict({
            "content": content,
            "title": title,
            "images": images,
            "platform": platform,
            "method": method
        })

        if result["success"]:
            logger.info(f"Publish successful: {result.get('url')}")
        else:
            logger.warning(f"Publish failed: {result.get('error')}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Publish error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/publish/platforms', methods=['GET'])
def list_platforms():
    """
    获取可用发布平台列表

    响应:
    {
        "success": true,
        "platforms": [
            {"key": "wechat", "name": "微信公众号", "status": "available"},
            ...
        ]
    }
    """
    try:
        from publisher import MultiPlatformPublisher

        publisher = MultiPlatformPublisher()
        platforms = publisher.get_available_platforms()

        return jsonify({
            "success": True,
            "platforms": platforms
        })

    except Exception as e:
        logger.error(f"Platforms error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/publish/bulk', methods=['POST'])
def bulk_publish():
    """
    批量发布到多个平台

    请求体:
    {
        "title": "标题",
        "content": "内容",
        "platforms": ["wechat", "xhs", "zhihu"],
        "delay_seconds": 5
    }

    响应:
    {
        "success": true,
        "total": 3,
        "successful": 2,
        "failed": 1,
        "results": [...],
        "errors": [...]
    }
    """
    try:
        data = request.get_json()
        title = data.get('title', '')
        content = data.get('content', '')
        platforms = data.get('platforms', ['wechat'])
        delay_seconds = data.get('delay_seconds', 5)

        if not title or not content:
            return jsonify({
                "success": False,
                "error": "Title and content are required"
            }), 400

        logger.info(f"Bulk publish request: title={title}, platforms={platforms}")

        result = bulk_publish_from_dict({
            "title": title,
            "content": content,
            "platforms": platforms,
            "delay_seconds": delay_seconds
        })

        if result["success"]:
            logger.info(f"Bulk publish completed: {result['successful']}/{result['total']} successful")
        else:
            logger.warning(f"Bulk publish partial failure: {result['failed']}/{result['total']} failed")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Bulk publish error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/schedule', methods=['POST'])
def schedule_content():
    """
    添加内容到调度队列

    请求体:
    {
        "title": "标题",
        "html": "HTML内容",
        "platform": "wechat",
        "delay_hours": 2,
        "schedule_at": "2026-03-27T18:00:00"
    }

    响应:
    {
        "success": true,
        "content_id": "sc_0001",
        "scheduled_at": "2026-03-27T18:00:00"
    }
    """
    try:
        data = request.get_json()
        title = data.get('title', '')
        html = data.get('html', '')
        platform = data.get('platform', 'wechat')
        delay_hours = data.get('delay_hours', 0)
        schedule_at_str = data.get('schedule_at')

        schedule_at = None
        if schedule_at_str:
            from datetime import datetime
            schedule_at = datetime.fromisoformat(schedule_at_str)

        logger.info(f"Schedule request: title={title}, platform={platform}, delay={delay_hours}")

        result = schedule_from_dict({
            "title": title,
            "html": html,
            "platform": platform,
            "delay_hours": delay_hours,
            "schedule_at": schedule_at
        })

        if result["success"]:
            logger.info(f"Content scheduled: {result['content_id']}")
        else:
            logger.warning(f"Schedule failed: {result.get('error')}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Schedule error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/schedule/queue', methods=['GET'])
def get_schedule_queue():
    """
    获取调度队列

    响应:
    {
        "success": true,
        "queue": [...],
        "stats": {...}
    }
    """
    try:
        from scheduler import ContentScheduler

        scheduler = ContentScheduler()

        return jsonify({
            "success": True,
            "queue": scheduler.get_all(),
            "stats": scheduler.get_queue_stats()
        })

    except Exception as e:
        logger.error(f"Queue error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/schedule/optimal-times', methods=['GET'])
def get_optimal_times():
    """
    获取最佳发布时间

    查询参数:
        platform: 平台名称

    响应:
    {
        "success": true,
        "platform": "wechat",
        "times": ["08:00", "12:00", "18:00", "21:00"],
        "next_suggested": "2026-03-27T18:00:00"
    }
    """
    try:
        from scheduler import ContentScheduler

        platform = request.args.get('platform', 'wechat')
        scheduler = ContentScheduler()

        return jsonify({
            "success": True,
            "platform": platform,
            "times": scheduler.get_optimal_times(platform),
            "next_suggested": scheduler.suggest_schedule(platform).isoformat()
        })

    except Exception as e:
        logger.error(f"Optimal times error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/schedule/<content_id>/status', methods=['PUT'])
def update_schedule_status(content_id):
    """
    更新调度内容状态

    请求体:
    {
        "status": "published | failed"
    }

    响应:
    {
        "success": true,
        "updated": true
    }
    """
    try:
        data = request.get_json()
        status = data.get('status')

        if status not in ['pending', 'scheduled', 'published', 'failed']:
            return jsonify({
                "success": False,
                "error": "Invalid status"
            }), 400

        from scheduler import ContentScheduler
        scheduler = ContentScheduler()

        updated = scheduler.mark_status(content_id, status)

        return jsonify({
            "success": True,
            "updated": updated
        })

    except Exception as e:
        logger.error(f"Status update error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """
    获取数据分析摘要

    查询参数:
        days: 统计天数 (默认30)

    响应:
    {
        "success": true,
        "period_days": 30,
        "total_posts": 10,
        "total_views": 5000,
        "total_engagement": 500,
        "avg_views_per_post": 500,
        "platforms": [...]
    }
    """
    try:
        days = int(request.args.get('days', 30))

        result = get_analytics_from_dict({"action": "summary", "days": days})

        return jsonify(result)

    except Exception as e:
        logger.error(f"Analytics summary error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/analytics/top-posts', methods=['GET'])
def get_top_posts():
    """
    获取热门内容

    查询参数:
        limit: 返回数量 (默认10)
        platform: 平台筛选

    响应:
    {
        "success": true,
        "posts": [...]
    }
    """
    try:
        limit = int(request.args.get('limit', 10))
        platform = request.args.get('platform')

        result = get_analytics_from_dict({
            "action": "top_posts",
            "limit": limit,
            "platform": platform
        })

        return jsonify(result)

    except Exception as e:
        logger.error(f"Top posts error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/analytics/platform-stats', methods=['GET'])
def get_platform_analytics():
    """
    获取平台统计数据

    查询参数:
        platform: 平台名称 (可选)

    响应:
    {
        "success": true,
        "platforms": [...]
    }
    """
    try:
        platform = request.args.get('platform')

        result = get_analytics_from_dict({
            "action": "platform_stats",
            "platform": platform
        })

        return jsonify(result)

    except Exception as e:
        logger.error(f"Platform stats error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/analytics/daily-trend', methods=['GET'])
def get_daily_trend():
    """
    获取每日趋势

    查询参数:
        days: 天数 (默认30)

    响应:
    {
        "success": true,
        "trend": [
            {"date": "2026-03-27", "posts": 2, "views": 500, "engagement": 50},
            ...
        ]
    }
    """
    try:
        days = int(request.args.get('days', 30))

        result = get_analytics_from_dict({
            "action": "daily_trend",
            "days": days
        })

        return jsonify(result)

    except Exception as e:
        logger.error(f"Daily trend error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/analytics/track', methods=['POST'])
def track_content():
    """
    追踪新内容

    请求体:
    {
        "content_id": "xxx",
        "title": "文章标题",
        "platform": "wechat"
    }

    响应:
    {
        "success": true,
        "tracked": true
    }
    """
    try:
        data = request.get_json()
        content_id = data.get('content_id')
        title = data.get('title')
        platform = data.get('platform', 'wechat')

        if not content_id or not title:
            return jsonify({
                "success": False,
                "error": "content_id and title are required"
            }), 400

        tracker = AnalyticsTracker()
        tracker.track_content(content_id, title, platform)

        logger.info(f"Tracked content: {content_id}")

        return jsonify({
            "success": True,
            "tracked": True
        })

    except Exception as e:
        logger.error(f"Track error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/v1/analytics/<content_id>/metrics', methods=['PUT'])
def update_content_metrics(content_id):
    """
    更新内容指标

    请求体:
    {
        "views": 1000,
        "likes": 50,
        "comments": 10,
        "shares": 5
    }

    响应:
    {
        "success": true,
        "updated": true
    }
    """
    try:
        data = request.get_json()

        tracker = AnalyticsTracker()
        updated = tracker.update_metrics(
            content_id,
            views=data.get('views'),
            likes=data.get('likes'),
            comments=data.get('comments'),
            shares=data.get('shares'),
            collects=data.get('collects')
        )

        return jsonify({
            "success": True,
            "updated": updated
        })

    except Exception as e:
        logger.error(f"Metrics update error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


def main():
    """启动服务器"""
    import argparse

    parser = argparse.ArgumentParser(description="AI Media System API Server")
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()

    logger.info(f"Starting AI Media System API on {args.host}:{args.port}")
    print(f"🚀 AI Media System API Server")
    print(f"   URL: http://{args.host}:{args.port}")
    print(f"   Health: http://{args.host}:{args.port}/health")
    print(f"   Pipeline: http://{args.host}:{args.port}/api/v1/pipeline/run")
    print(f"   Infographic: http://{args.host}:{args.port}/api/v1/infographic")
    print(f"   Publish: http://{args.host}:{args.port}/api/v1/publish")
    print(f"   Bulk Publish: http://{args.host}:{args.port}/api/v1/publish/bulk")
    print(f"   Schedule: http://{args.host}:{args.port}/api/v1/schedule")
    print(f"   Analytics: http://{args.host}:{args.port}/api/v1/analytics")
    print()
    print("Press Ctrl+C to stop")

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
