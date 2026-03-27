# AI Media System - 项目总结

> 自动化内容生产与发布系统 | 从采集到分析的全链路解决方案

## 系统概览

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Collector  │───▶│   Curator   │───▶│   Writer    │───▶│  Formatter  │
│             │    │             │    │             │    │             │
│ Geektime    │    │ Topics      │    │ Tech-Explore│    │ WeChat HTML │
│ CDP Ready   │    │ Analysis    │    │ Style       │    │ 17 Themes   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Source    │    │  Candidates │    │  Articles    │    │   HTML      │
│   Pool      │    │   ( ranked ) │    │  ( formatted )│    │   styled    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                  │
                    ┌─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Publishing Layer                           │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Infographic  │  │   Adapters   │  │   Scheduler  │              │
│  │   Generator   │  │ (XHS/Zhihu/  │  │              │              │
│  │  (17 styles)  │  │  Jianshu)    │  │  Queue       │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│           │                 │                 │                     │
│           ▼                 ▼                 ▼                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Multi-Platform Publisher                       │  │
│  │  WeChat │ XHS │ Zhihu │ Jianshu │ Bulk │ Auto              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│           │                 │                 │                     │
│           ▼                 ▼                 ▼                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  Analytics Tracker                            │  │
│  │  Views │ Likes │ Shares │ Trends │ Platform Stats          │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 采集层 | Playwright, CDP, BeautifulSoup |
| 处理层 | Python 3.12+, dataclasses, re, json |
| API层 | Flask, Flask-CORS |
| 发布层 | Node.js scripts (本地技能集成) |
| 数据层 | JSON 文件存储 |

## API 端点总览

### Pipeline 端点
- `POST /api/v1/pipeline/run` - 完整流水线
- `POST /api/v1/collect` - 采集内容
- `POST /api/v1/curate` - 选题策划
- `POST /api/v1/write` - 内容创作
- `POST /api/v1/format` - 格式排版

### 信息图端点
- `POST /api/v1/infographic` - 生成信息图
- `GET /api/v1/infographic/styles` - 可用风格列表

### 发布端点
- `POST /api/v1/publish` - 单平台发布
- `POST /api/v1/publish/bulk` - 批量发布
- `GET /api/v1/publish/platforms` - 平台列表

### 调度端点
- `POST /api/v1/schedule` - 添加到队列
- `GET /api/v1/schedule/queue` - 队列状态
- `GET /api/v1/schedule/optimal-times` - 最佳时间
- `PUT /api/v1/schedule/:id/status` - 更新状态

### 分析端点
- `GET /api/v1/analytics/summary` - 数据摘要
- `GET /api/v1/analytics/top-posts` - 热门内容
- `GET /api/v1/analytics/platform-stats` - 平台统计
- `GET /api/v1/analytics/daily-trend` - 每日趋势
- `POST /api/v1/analytics/track` - 追踪内容
- `PUT /api/v1/analytics/:id/metrics` - 更新指标

## 信息图风格 (17种)

1. 3D 黏土风 (claymorphism)
2. 毛玻璃质感 (glassmorphism)
3. 便当盒网格 (bento-grids)
4. 学霸笔记 (top-student-notes) - 推荐
5. 剪纸层叠 (paper-cutout)
6. 手绘涂鸦 (sketchnote)
7. 卡通手绘 (cartoon-hand-drawn)
8. 数字极简票券风 (ticket)
9. Notion风/知识卡片 (notion)
10. 极简线条/孟菲斯风 (corporate-memphis)
11. 美式波普 (pop-art)
12-17. 更多风格...

## 平台适配器

| 平台 | 状态 | 特点 |
|------|------|------|
| 微信公众号 | ✓ Available | API + Browser |
| 小红书 | ✓ Adapter | Emoji标题, 短段落, 标签 |
| 知乎 | ✓ Adapter | 专业严谨, Markdown, 话题 |
| 简书 | ✓ Adapter | 文学性强, 长文支持 |

## 最佳发布时间

| 平台 | 最佳时间 |
|------|----------|
| 微信公众号 | 08:00, 12:00, 18:00, 21:00 |
| 小红书 | 07:00, 09:00, 19:00, 22:00 |
| 知乎 | 09:00, 14:00, 20:00 |
| 简书 | 08:00, 20:00 |

## 数据存储

```
data/
├── analytics/
│   ├── metrics.json      # 内容指标
│   └── daily.json        # 每日统计
└── schedule/
    └── queue.json        # 调度队列
```

## 扩展性

系统采用模块化设计，可轻松扩展：

1. **新增采集源** - 在 `skills/00-collector/` 下添加新模块
2. **新增写作风格** - 在 `skills/02-writer/` 下添加新风格
3. **新增发布平台** - 在 `skills/03-publisher/` 下添加适配器
4. **新增分析维度** - 在 `skills/05-analytics/` 下添加指标

## 开发进度

- [x] Week 1: MVP 核心流水线
- [x] Week 1: n8n 工作流集成
- [x] Week 1: 信息图生成
- [x] Week 1: 多平台发布框架
- [x] Week 1: 内容调度系统
- [x] Week 2: 数据分析仪表板
- [x] Week 2: 平台内容适配器
- [x] Week 2: 批量发布功能
- [ ] Week 2+: API认证与权限管理
- [ ] Week 2+: WebUI 前端界面
- [ ] Week 2+: 更多采集源

## 配置文件

- `n8n-workflow-ai-media-pipeline.json` - n8n工作流
- `docs/n8n-setup-guide.md` - 配置指南
- `api_server.py` - API服务主文件
- `pipeline.py` - 流水线编排

## 运行项目

```bash
# 启动API服务
python api_server.py --port 5004

# 运行测试
python test_full_pipeline.py

# 运行单元测试
pytest skills/ -v
```

## 依赖安装

```bash
pip install flask flask-cors requests playwright python-dotenv pytest
playwright install chromium
```

## 许可证

MIT License
