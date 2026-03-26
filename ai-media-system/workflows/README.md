# n8n 工作流配置

AI Media Agent System 的 n8n 工作流配置

## 工作流架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        MVP 工作流                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Webhook触发] → [采集] → [选题] → [创作] → [排版] → [输出]      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 工作流文件说明

- `mvp-content-pipeline.json` - MVP 内容流水线
- `collector-workflow.json` - 采集子流程
- `creator-workflow.json` - 创作子流程
- `publisher-workflow.json` - 排版发布子流程

## 使用方法

1. 导入工作流到 n8n
2. 配置环境变量
3. 启动工作流
4. 发送 Webhook 触发

## 环境变量

```bash
# API 配置
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# 飞书配置
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret

# 微信配置
WECHAT_APPID=your_appid
WECHAT_SECRET=your_secret
```
