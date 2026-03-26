# AI Media Agent System

> AI 媒体智能体系统 - 基于 Multi-Agent 架构的全自动内容生产与分发平台

## 项目进展 (2026-03-27)

### ✅ 已完成 (MVP 核心模块)

| 模块 | 状态 | 说明 |
|-----|------|------|
| `geektime-collector` | ✅ 完成 | 极客时间内容采集，支持 Playwright/requests |
| `topic-curator` | ✅ 完成 | 选题策划 Agent，从内容池生成候选选题 |
| `tech-explorer-writer` | ✅ 完成 | 探索者风格创作，费曼科普风 |
| `wechat-formatter` | ✅ 完成 | 公众号排版，Markdown → HTML |
| `pipeline` | ✅ 完成 | 端到端流水线集成 |

### 🚧 进行中

| 模块 | 状态 | 说明 |
|-----|------|------|
| `n8n-workflows` | 🚧 配置中 | 工作流配置文件 |
| 飞书集成 | 📋 待开发 | 知识库、数据存储 |
| 公众号发布 | 📋 待开发 | 草稿箱推送 |

### 📋 待开发 (V1.0)

| 模块 | 优先级 | 说明 |
|-----|--------|------|
| `wechat-collector` | P0 | 公众号内容采集 |
| `business-analyst-writer` | P1 | 商业分析师风格创作 |
| `xiaohongshu-adapter` | P1 | 小红书格式适配 |
| `senior-editor` | P1 | 资深编辑审核 |

## 项目结构

```
ai-media-system/
├── skills/
│   ├── 00-collector/          # 采集模块
│   │   └── geektime-collector/
│   ├── 01-creator/            # 创作模块
│   │   └── topic-curator/
│   ├── 02-writer/             # 写手模块
│   │   └── tech-explorer-writer/
│   └── 03-publisher/          # 分发模块
│       └── wechat-formatter/
├── workflows/                 # n8n 工作流配置
├── pipeline.py                # MVP 流水线
├── requirements.txt           # Python 依赖
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. 配置环境

创建 `.env` 文件：

```bash
GEEKTIME_COOKIE=your_cookie_here
ANTHROPIC_API_KEY=your_key_here
```

### 3. 运行流水线

```bash
# 使用采集 URL
python pipeline.py --url https://time.geekbang.org/article/12345

# 使用模拟模式（测试）
python pipeline.py --mock
```

## MVP 验收标准

- [x] 能从极客时间采集文章内容
- [x] 能生成 3-5 个候选选题
- [x] 能创作费曼科普风格文章
- [x] 能生成公众号兼容 HTML
- [x] 能端到端运行完整流程

## 下一步

1. 集成 Claude API 提升创作质量
2. 添加飞书知识库支持
3. 实现公众号草稿箱推送
4. 开发商业分析师风格写手

## 许可证

MIT
