# AI媒体智能体系统 - 子项目分解

> 依据 Superpowers brainstorming skill 的范围检查要求
> 将大型项目分解为可独立实施的子项目
>
> 创建时间：2026年3月26日

---

## 分解原则

根据 Superpowers brainstorming skill：

> 如果项目描述多个独立子系统，应该先分解为 sub-projects。
> 每个 sub-project 获得独立的 spec → plan → implementation cycle。

---

## 子项目划分

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        父项目：AI媒体智能体系统                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐           │
│  │   Sub-Project 1│  │   Sub-Project 2│  │   Sub-Project 3│           │
│  │  采集子系统    │  │  创作子系统    │  │  审核子系统    │           │
│  │  (MVP阶段)     │  │  (MVP阶段)     │  │  (V1.0阶段)    │           │
│  └────────────────┘  └────────────────┘  └────────────────┘           │
│                                                                         │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐           │
│  │   Sub-Project 4│  │   Sub-Project 5│  │   Sub-Project 6│           │
│  │  分发子系统    │  │  视频子系统    │  │  数据闭环系统  │           │
│  │  (MVP阶段)     │  │  (V2.0阶段)    │  │  (V2.0阶段)    │           │
│  └────────────────┘  └────────────────┘  └────────────────┘           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Sub-Project 1: 采集子系统 (MVP)

### 目标
从极客时间采集课程内容，输出结构化数据

### 输入
- 极客时间专栏 URL
- Cookie 认证信息

### 输出
```json
{
  "id": "string",
  "type": "geektime",
  "url": "string",
  "title": "string",
  "author": "string",
  "published_at": "datetime",
  "content": "text",
  "images": ["url"],
  "video": {
    "url": "url",
    "transcript": "text"
  }
}
```

### 包含的 Agent
1. `geektime-collector` - 极客时间采集
2. `research-specialist` - 资料增强（可选，V1.0）

### 成功标准
- 能成功采集指定专栏的一篇文章
- 正确提取文字和图片
- 视频转文字准确率 > 90%

---

## Sub-Project 2: 创作子系统 (MVP)

### 目标
基于采集内容，生成技术探索者风格的文章

### 输入
- 采集子系统输出的结构化数据
- 风格选择：tech-explorer

### 输出
```json
{
  "id": "string",
  "topic_id": "string",
  "style": "tech-explorer",
  "title": "string",
  "content": "markdown",
  "word_count": 1800,
  "image_prompts": [
    {"position": 800, "description": "string"}
  ]
}
```

### 包含的 Agent
1. `topic-curater` - 选题策划
2. `tech-explorer-writer` - 技术探索者写手

### 成功标准
- 生成 1500-2000 字文章
- 幽默通俗，高中生能懂
- 结构完整（钩子+概念+案例+建议+结尾）

---

## Sub-Project 3: 审核子系统 (V1.0)

### 目标
对创作的文章进行质量评分，输出审核报告

### 输入
- 创作子系统输出的草稿

### 输出
```json
{
  "id": "string",
  "draft_id": "string",
  "reviewer": "senior-editor",
  "scores": {
    "language": {"score": 8, "max": 10},
    "structure": {"score": 9, "max": 10},
    "compliance": {"score": 7, "max": 10}
  },
  "total_score": 24,
  "max_score": 30,
  "passed": true,
  "suggestions": ["string"]
}
```

### 包含的 Agent
1. `senior-editor` - 资深编辑审核
2. `first-principle-reviewer` - 第一性原理审核 (V2.0)

### 成功标准
- 单项≥7分，总分≥24分：通过
- 输出具体修改建议

---

## Sub-Project 4: 分发子系统 (MVP)

### 目标
将审核通过的内容推送到公众号草稿箱

### 输入
- 审核通过的草稿
- 配图（可选）

### 输出
```json
{
  "id": "string",
  "draft_id": "string",
  "platform": "wechat",
  "url": "string",
  "status": "draft",
  "published_at": "datetime"
}
```

### 包含的 Agent
1. `wechat-formatter` - 公众号排版
2. `wechat-publisher` - 公众号发布

### 成功标准
- 成功推送到公众号草稿箱
- HTML 格式正确
- 图片正常显示

---

## Sub-Project 5: 视频子系统 (V2.0)

### 目标
基于文章生成视频内容

### 输入
- 审核通过的草稿
- 语音样本

### 输出
- 视频文件 (MP4)
- 字幕文件 (SRT)

### 包含的 Agent
1. `video-script-writer` - 视频脚本转换
2. `video-editor` - 视频剪辑
3. `voice-cloner` - 语音克隆

### 成功标准
- 1080p 输出
- 音画同步
- 字幕准确

---

## Sub-Project 6: 数据闭环系统 (V2.0)

### 目标
采集发布后数据，反哺知识库

### 输入
- 发布记录
- 平台数据 API

### 输出
- 数据分析报告
- 知识库更新建议

### 包含的 Agent
1. `data-collector` - 数据采集
2. `analyst` - 数据分析
3. `knowledge-updater` - 知识库更新

### 成功标准
- 自动采集阅读量、点赞数
- 识别爆款（阅读>2倍均值）
- 提取成功要素

---

## MVP 实施顺序

```
Phase 1 (Week 1-2): 端到端单线
┌─────────────────────────────────────────────────────────────┐
│  Sub-Project 1 (采集) → Sub-Project 2 (创作) → Sub-Project 4 (分发) │
└─────────────────────────────────────────────────────────────┘
                验收：极客时间 → 公众号草稿箱

Phase 2 (Week 3-4): 扩展功能
┌─────────────────────────────────────────────────────────────┐
│  + Sub-Project 3 (审核) + 公众号采集 + 小红书适配             │
└─────────────────────────────────────────────────────────────┘

Phase 3 (Week 5-8): 完整闭环
┌─────────────────────────────────────────────────────────────┐
│  + Sub-Project 5 (视频) + Sub-Project 6 (数据闭环)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 下一步行动

根据 Superpowers workflow：

1. ✅ Sub-Project 分解完成（本文件）
2. ⏭️ 调用 `writing-plans` skill，为 **Sub-Project 1** 创建实施计划
3. ⏭️ 调用 `executing-plans` 或 `subagent-driven-development` 执行
4. ⏭️ 每个 Sub-Project 独立完成 spec → plan → implementation cycle

---

*子项目分解文档 - 2026年3月26日*
