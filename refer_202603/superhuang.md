------

## 一、内容相关 Skills 总览（按功能分 7 大类，共 35 个）

### 1. 内容采集层（8个）

| Skill                     | 功能简述                                                     |
| ------------------------- | ------------------------------------------------------------ |
| **daily-content-curator** | 从预配置的 YouTube 频道和小宇宙播客自动抓取音视频，获取字幕/转录文本并改写 |
| **x-viral-collector**     | 通过 Apify 采集 X(Twitter) 上 AI 相关的高互动推文和长文，生成热门内容报告 |
| **ai-income-stories**     | 从 X 采集「用 AI 编程工具赚钱」的真实故事，提取收入/工具/背景等结构化数据 |
| **attentionvc-ai-daily**  | 从 AttentionVC.ai 抓取 X 上 AI 热门长文，用 Jina Reader 获取全文，生成日报 |
| **wechat-collect**        | 公众号文章采集                                               |
| **wechat-subscribe**      | 公众号订阅管理                                               |
| **wechat**                | 公众号选题监控（主菜单）                                     |
| **meme-search**           | 全网梗图搜索引擎，通过多策略并行搜索返回相关梗图集合及解读   |

### 2. 内容创作层（9个）

| Skill                  | 功能简述                                                     |
| ---------------------- | ------------------------------------------------------------ |
| **article-rewriter**   | 外文 URL 精读 → 讨论角度 → 三写手竞争创作 → 审稿 → 选稿 → 信息图 → 公众号 HTML |
| **case-writer-hybrid** | 用户提供核心观点 → 搜索案例 → 3 条论证路径 → 3 个版本 → 六维评分 → 选择 |
| **solo-writer**        | 播客文字稿 → 精读 → 讨论角度 → 单写手写作（去 AI 味）→ 信息图 → 公众号 HTML |
| **interview**          | 多轮深度访谈挖掘用户故事 → 智能推荐文章方向 → 输出公众号爆款文章 |
| **ad-writing**         | 读取广告主 PDF Brief → 设计测试用例 → 输出约 3000 字公众号推广文章 |
| **ad-writing-v2**      | Brief → 全网调研 → 3 版大纲审批 → 用户实测 → 基于真实结果写作 |
| **meme-to-script**     | 用户上传梗图 → AI 深度解读 → 网络搜索补充素材 → 三编剧竞写 → 评审打分 → 公众号 HTML |
| **hokkaido-writer**    | Skills 工具书写作助手，专门优化案例、补充章节、润色文字      |
| **viral-video-script** | 输入文章 → 三写手并行竞写 → 评审打分 → 输出含时间标记/画面提示/情绪线的视频脚本 |

### 3. 翻译层（1个）

| Skill               | 功能简述                                                   |
| ------------------- | ---------------------------------------------------------- |
| **baoyu-translate** | 三种模式（快速/标准/精翻）翻译文章和文档，支持自定义术语表 |

### 4. 排版/格式化层（1个）

| Skill                | 功能简述                                                     |
| -------------------- | ------------------------------------------------------------ |
| **wechat-formatter** | 将 Markdown 转为微信公众号可粘贴的 HTML，CSS 内联、微信兼容性适配、自定义主题 |

### 5. 视觉/封面层（6个）

| Skill                  | 功能简述                                                     |
| ---------------------- | ------------------------------------------------------------ |
| **generate-image**     | AI 图片生成和变换                                            |
| **cover-generator**    | 上传照片 + 参考封面 → 交互式弹框 → 多尺寸专业视频封面        |
| **cover-4styles**      | 上传头像 + 标题 → 一键批量生成 4 种预设风格视频封面          |
| **xhs-cover-template** | 小红书封面（Premium Split 风格）上深下白                     |
| **xiaolvshu-cover**    | 公众号小绿书封面，输入标题/副标题/作者 → 4 种视觉风格竖版封面 |
| **generate-video**     | AI 视频生成                                                  |

### 6. 视频/音频处理层（4个）

| Skill                     | 功能简述                                                     |
| ------------------------- | ------------------------------------------------------------ |
| **video-optimize**        | 支持 B站/YouTube/小红书/抖音链接，豆包大模型视频理解，8 维度爆款拆解报告 |
| **video-local-analyze**   | 仅支持本地视频文件，同样豆包 API 原生视频理解，输出拆解报告  |
| **video-from-storyboard** | 分镜图片 + 音频 + 文案 → Whisper 语音对齐字幕 → 自动合成带字幕视频 |
| **minimax-tts**           | MiniMax T2A API 文字转语音，支持多种音色                     |

### 7. 内容分发/同步层（6个）

| Skill                          | 功能简述                                                     |
| ------------------------------ | ------------------------------------------------------------ |
| **feishu-bitable-sync**        | 将 content-archive 内容同步到飞书多维表格，基于原始链接去重  |
| **xiaohongshu-note-generator** | 从飞书多维表格拉取内容 → 转化为小红书爆款图文笔记（连续长图切片卡片） |
| **obsidian-to-x**              | 发布内容到 X(Twitter)，支持常规推文/X Articles/公众号 HTML   |
| **auto-curate**                | 一体化：daily-content-curator + feishu-bitable-sync 的整合流程 |
| **wechat-full**                | 完整流程：wechat-collect + wechat-report                     |
| **wechat-report**              | 生成 Skills 潜力分析报告                                     |



现在来分析它们之间的关联关系



------

## 核心发现：35 个内容 Skills 形成了完整的「采-创-美-发」内容流水线

### 七大功能层

| 层级           | Skills 数量 | 代表                                                         |
| -------------- | ----------- | ------------------------------------------------------------ |
| **内容采集**   | 8           | daily-content-curator, x-viral-collector, wechat-collect 等  |
| **翻译**       | 1           | baoyu-translate                                              |
| **内容创作**   | 9           | article-rewriter, case-writer-hybrid, solo-writer 等         |
| **排版格式化** | 1           | wechat-formatter                                             |
| **视觉/封面**  | 6           | generate-image, cover 系列, xhs-cover 等                     |
| **视频/音频**  | 5           | video-optimize, video-from-storyboard, minimax-tts 等        |
| **分发/同步**  | 6           | feishu-bitable-sync, obsidian-to-x, xiaohongshu-note-generator 等 |

### 关键关联模式

1. **采集 → 创作**：采集层抓回的素材直接喂给创作层（如播客转录 → solo-writer，X热点 → case-writer）
2. **创作 → 排版/视觉**：所有写作 Skill 的输出都可以流入 wechat-formatter 排版，或调用 generate-image 生成配图
3. **创作 → 视频链路**：viral-video-script 生成脚本后，可串联 minimax-tts 配音 + video-from-storyboard 合成视频
4. **飞书作为中枢**：feishu-bitable-sync 是内容存储中枢，上游接采集，下游供小红书笔记生成
5. **组合型 Skill**：auto-curate = daily-content-curator + feishu-bitable-sync；wechat-full = wechat-collect + wechat-report

HTML 关系图支持交互：鼠标悬停节点可查看详细描述和关联，点击图例可按分类高亮筛选。下方还列出了 6 条典型端到端工作流。



**六层结构（自上而下）：**

1. **采集层** (8个 Skills) -- 从 YouTube / X / 小宇宙 / 公众号 / 梗图网站抓取原始素材
2. **翻译层** (1个 Skill) -- 外文本地化处理，可选旁路（中文内容直接跳过）
3. **创作层** (9个 Skills) -- 核心生产引擎，多写手竞争/案例论证/访谈提炼
4. **排版 & 视觉层** (7个 Skills) -- 为裸文本"穿衣打扮"：排版、配图、封面
5. **视频 & 音频层** (5个 Skills) -- 文字转多媒体：TTS配音、分镜合成、AI视频
6. **分发 & 同步层** (6个 Skills) -- 推送到 X / 小红书 / 飞书，内容资产沉淀

每一层都标注了 IN（接收什么）和 OUT（输出什么），层与层之间用箭头标注数据流转类型。底部还有四个架构洞察卡片（单向管道+旁路、反馈环路、一鱼多吃、飞书中枢）。





