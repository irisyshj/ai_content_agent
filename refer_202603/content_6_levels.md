# 内容 Skills 六层递进架构

从原始素材采集到最终多平台分发，35 个内容 Skills 按照数据流转方向形成 6 个功能层级，每一层的输出即为下一层的输入。

1

## 采集层

从多个外部平台自动化抓取原始内容素材，是整条内容流水线的「进水口」。

daily-content-curatorx-viral-collectorai-income-storiesattentionvc-ai-dailywechat-collectwechat-subscribewechat (选题监控)meme-search

**IN**YouTube / 小宇宙 / X / 公众号 / 梗图网站

**OUT**转录文本、推文、文章全文、梗图素材



原始素材

2

## 翻译层

对外文素材进行本地化处理。并非所有内容都经过此层 -- 仅外文素材需要，中文内容可直接跳到创作层。

baoyu-translate

**IN**英文文章、外文文档

**OUT**精翻中文文本（快速/标准/精翻三级）



可理解文本

3

## 创作层

核心引擎。多写手竞争、案例论证、访谈提炼等机制产出高质量文章或脚本。

article-rewritersolo-writercase-writer-hybridinterviewad-writing / v2meme-to-scripthokkaido-writerviral-video-script

**IN**翻译后文本 / 播客转录 / 热点案例 / 梗图

**OUT**公众号 Markdown / 视频脚本（含画面提示）



文章 & 脚本

4

## 排版 & 视觉层

将裸文本「穿衣打扮」：公众号排版、AI 配图、封面生成，让内容具备发布级视觉品质。

wechat-formattergenerate-imagecover-generatorcover-4stylesxhs-cover-templatexiaolvshu-cover

**IN**Markdown 文章 / 标题关键词 / 头像素材

**OUT**公众号 HTML / 信息图 / 封面



脚本 & 配图

5

## 视频 & 音频层

文字转多媒体：TTS 配音、分镜合成视频、AI 视频生成，同时爆款拆解反哺创作。

minimax-ttsvideo-from-storyboardgenerate-videovideo-optimizevideo-local-analyze

**IN**视频脚本 / 分镜图片 / 文案文本

**OUT**带字幕成片 / AI 语音 / 拆解报告



成品内容

6

## 分发 & 同步层

内容流水线的「出水口」。推送各平台 + 飞书归档，沉淀内容资产。

obsidian-to-xxiaohongshu-note-generatorfeishu-bitable-syncauto-curatewechat-fullwechat-report

**IN**排版后 HTML / 视频成片 / 图文素材

**OUT**X 推文 / 小红书笔记 / 飞书表格

## 架构洞察

### 单向主管道 + 旁路

主数据流 1->2->3->4->5->6 线性递进，但翻译层是可选旁路，中文内容可直接跳到创作层。

### 反馈环路

视频拆解（video-optimize）的报告可以反馈到创作层的 viral-video-script，形成「分析爆款 -> 复制爆款」闭环。

### 一鱼多吃

创作层的一篇文章可同时流向排版层（公众号）、视频层（口播成片）、分发层（X / 小红书），一份素材多平台复用。

### 飞书作为中枢

feishu-bitable-sync 横跨采集与分发，既是归档库也是小红书数据源，充当内容资产中央存储。