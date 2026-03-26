# AI自媒体自动生成系统 - 资源汇总

> 收录调研过程中发现的所有有价值的工具、API、文档和社区资源

---

## 一、AI内容生成工具

### 商业化工具

| 工具 | 官网 | 核心功能 | 价格参考 |
|-----|------|---------|---------|
| **优采云AI内容工厂** | - | 全网采集+深度原创+自动发布+文生视频 | 付费 |
| **内容特工队AI** | - | 一句话+一张图生成营销短视频 | 付费 |
| **智文大师** | - | 文学性调校，多文风模板 | 付费 |
| **内容魔方Pro** | - | 营销文案、社交媒体帖子生成 | 付费 |
| **Jasper** | jasper.ai | AI写作助手，11,000+字体，25+语言 | $39-69/月 |
| **Pictory** | pictory.ai | 文章转视频，自动字幕 | $19-39/月 |
| **Pressmaster.ai** | pressmaster.ai | PR内容自动化，Trendmaster趋势扫描 | 付费 |
| **Sprinklr** | sprinklr.com | 企业级社交媒体AI管理 | 企业报价 |

### 开源项目

| 项目 | GitHub | 技术栈 | Stars |
|-----|--------|-------|-------|
| **Remotion** | remotion-dev/remotion | React视频生成 | 21k+ |
| **MoneyPrinterTurbo** | - | 中文通用自动化视频 | - |
| **Bilive** | - | B站专用自动化 | - |
| **AutoClipper** | - | YouTube高光片段 | - |
| **Lighthouse** | - | 学术视频检索 | - |

---

## 二、视频生成与编辑

### AI视频生成模型

| 模型 | 来源 | 特点 | 部署难度 |
|-----|------|------|---------|
| **HunyuanVideo 1.5** | 腾讯 | 当前最强，1080p输出 | 高（需GPU） |
| **Wan2.1（万象）** | 阿里 | 中文最友好 | 高 |
| **CogVideoX** | 清华大学 | 开源代表 | 中 |
| **Veo 3** | Google | 商业API | API调用 |
| **Sora 2** | OpenAI | 商业API | API调用 |
| **LTX-Video** | Lightricks | 低延迟 | 中 |

### 视频编辑工具

| 工具 | 类型 | 特点 |
|-----|------|------|
| **FFmpeg** | 命令行 | 万物基础，转码/裁剪/合并/滤镜 |
| **Remotion** | React | 程序化生成，数据驱动 |
| **MoviePy** | Python | 脚本化处理，快速原型 |
| **Whisper** | 开源 | 最强ASR，语音转文字 |
| **faster-whisper** | 开源 | Whisper加速版，快4-8x |

### API服务

| 服务 | 官网 | 功能 |
|-----|------|------|
| **Fal.ai** | fal.ai | 媒体生成API（图/视频/音频） |
| **Replicate** | replicate.com | 模型托管API |
| **Together AI** | together.ai | 多模型推理API |

---

## 三、语音克隆与TTS

### 开源模型（中文友好）

| 模型 | GitHub/来源 | 样本需求 | 特点 |
|-----|------------|---------|------|
| **GPT-SoVITS V4** | - | 5秒~1分钟 | 中文最佳，跨语言 |
| **CosyVoice 3.0** | 阿里 | 10秒+ | 情感控制精细 |
| **IndexTTS 2.5** | B站开源 | 3秒+ | 小显存，速度快 |
| **F5-TTS** | - | 3秒+ | 轻量级 |
| **Fish Speech** | - | 10秒+ | 多语言 |
| **Kokoro TTS** | - | - | 82M参数，轻量 |
| **Bert-VITS2** | - | - | 推理速度快 |

### 商业TTS服务

| 服务 | 官网 | 特点 |
|-----|------|------|
| **ElevenLabs** | elevenlabs.io | 最真实TTS |
| **MiniMax** | minimax.io | 国内API，稳定 |
| **Azure TTS** | azure.microsoft.com | 微软服务 |
| **Google TTS** | cloud.google.com | 谷歌云 |

### 数字人/口型同步

| 工具 | 功能 |
|-----|------|
| **MuseTalk** | 实时口型同步 |
| **SadTalker** | 图片→说话 |
| **Wav2Lip** | 任意视频换口型 |
| **EchoMimicV2** | 音频驱动照片 |

---

## 四、多平台发布方案

### 开源发布工具

| 工具 | 平台支持 | 技术方案 |
|-----|---------|---------|
| **WechatSync** | 公众号/知乎/CSDN/掘金 | 浏览器插件+Cookie |
| **xpub** | 全平台10+ | 浏览器自动化 |
| **微信公众号同步助手** | 微信为主+多平台 | Chrome扩展 |
| **多平台一键同步发布脚本** | 抖音/小红书/B站/油管等 | Tampermonkey脚本 |

### 商业API聚合

| 服务 | 官网 | 覆盖平台 |
|-----|------|---------|
| **TikHub API** | api.tikhub.io | 抖音/小红书/B站/快手/微信/微博等 |
| **字流** | - | AI驱动多平台适配 |

### 平台官方API

| 平台 | API文档 | 认证方式 |
|-----|---------|---------|
| **微信公众号** | mp.weixin.qq.com | AppID/AppSecret |
| **B站** | openhome.bilibili.com | 官方开发者平台 |
| **抖音开放平台** | open.douyin.com | 企业资质申请 |
| **快手开放平台** | open.kuaishou.com | 开发者账号 |
| **微博开放平台** | open.weibo.com | 应用审核 |

### 平台API支持情况汇总

| 社交媒体 | 是否支持API | 支持格式 | 自动化难度 |
|---------|------------|---------|-----------|
| 公众号 | ✅ 官方API | docx, doc | 低 |
| 微博头条文章 | ✅ 官方API | html, docx | 低 |
| CSDN | ❌ 不支持 | markdown, html | 高 |
| 知乎 | ❌ 不支持 | markdown, docx | 高 |
| 掘金 | ❌ 不支持 | markdown | 高 |
| 百家号 | ❌ 不支持 | docx, pdf, txt | 高 |
| 小红书 | ⚠️ 非官方API | 图文 | 高 |
| 抖音 | ✅ 官方API | 图文, 视频 | 中 |
| B站 | ✅ 官方API | 视频 | 中 |

---

## 五、内容采集工具

### 爬虫框架

| 工具 | 语言 | 特点 |
|-----|------|------|
| **Playwright** | Node.js/Python | 现代Web，CDP支持 |
| **Puppeteer** | Node.js | Chrome DevTools Protocol |
| **Scrapy** | Python | 成熟框架 |
| **Selenium** | 多语言 | 传统方案 |

### 网页解析

| 工具 | 用途 |
|-----|------|
| **BeautifulSoup** | HTML解析 |
| **Readability** | 正文提取 |
| **Trafilatura** | 网页内容提取 |

### 反爬虫工具

| 工具 | 用途 |
|-----|------|
| **代理IP池** | 隐藏真实IP |
| **Fake Useragent** | UA轮换 |
| **Undetected Chromedriver** | 绕过检测 |

### 视频下载工具

| 工具 | 平台支持 |
|-----|---------|
| **yt-dlp** | YouTube/B站等1000+站点 |
| **you-get** | 多个视频网站 |
| **annie** | B站等 |

---

## 六、AI模型与API

### 大语言模型

| 模型 | 上下文 | 特点 | 官网 |
|-----|-------|------|------|
| **Claude Opus 4.6** | 200K+ | 推理能力强 | anthropic.com |
| **DeepSeek-V3** | 200K+ | 开源友好 | deepseek.com |
| **GPT-4o** | 128K | 多模态 | openai.com |
| **Gemini 2.5** | 1M+ | 超长上下文 | gemini.google.com |
| **Qwen3** | 32K+ | 阿里出品 | tongyi.aliyun.com |

### 搜索增强工具

| 工具 | 官网 | 特点 |
|-----|------|------|
| **Perplexity** | perplexity.ai | AI搜索引擎 |
| **Tavily** | tavily.com | AI研究搜索 |
| **Exa** | exa.ai | 神经网络搜索 |

### 图像生成

| 模型/服务 | 官网 | 特点 |
|----------|------|------|
| **Midjourney** | midjourney.com | 艺术质量高 |
| **DALL-E 3** | openai.com | 商业API |
| **Stable Diffusion** | stability.ai | 开源可控 |
| **Flux** | - | 新一代模型 |
| **Nano Banana** | Google | Gemini集成 |

---

## 七、工作流与编排

### 可视化工作流工具

| 工具 | 官网 | 特点 |
|-----|------|------|
| **n8n** | n8n.io | 开源工作流自动化 |
| **Windmill** | windmill.dev | 开源开发者平台 |
| **Make** | make.com | 商业工作流平台 |
| **Zapier** | zapier.com | 商业自动化平台 |

### Agent框架

| 框架 | 官网 | 语言 |
|-----|------|------|
| **LangChain** | langchain.com | Python/JS |
| **LlamaIndex** | llamaindex.ai | Python |
| **AutoGPT** | agpt.co | Python |
| **CrewAI** | crewai.com | Python |

---

## 八、Claude Code Skills相关

### 已有相关Skills

| Skill | 功能 | 来源 |
|-------|------|------|
| **remotion-video** | Remotion视频生成 | LobeHub |
| **video-editing** | AI视频编辑工作流 | LobeHub |
| **fliz-ai-video-generator** | Fliz API视频生成 | LobeHub |
| **baoyu-image-gen** | AI图像生成 | 本地 |
| **baoyu-infographic** | 专业信息图生成 | 本地 |
| **gemini-infographic** | 竖版信息图生成 | 本地 |
| **wechat-post-to-wechat** | 微信公众号发布 | 本地 |
| **wechat-writer** | 微信公众号写作 | 本地 |

---

## 九、学习资源

### 官方文档

| 资源 | 链接 |
|-----|------|
| Remotion文档 | https://www.remotion.dev/docs |
| Playwright文档 | https://playwright.dev/docs |
| FastAPI文档 | https://fastapi.tiangolo.com |

### 社区资源

| 社区 | 链接 |
|-----|------|
| LobeHub Skills | https://lobehub.com/zh/skills |
| GitHub Awesome Lists | https://github.com/topics/awesome |
| Indie Hackers | https://www.indiehackers.com |

### 技术博客

| 来源 | 链接 |
|-----|------|
| 腾讯云开发者社区 | https://cloud.tencent.com/developer |
| 掘金 | https://juejin.cn |
| CSDN | https://blog.csdn.net |

---

## 十、极客时间相关

### 极客时间官网
- 主站：https://time.geekbang.org/
- 企业版：https://b.geekbang.org/

### 采集注意事项
- 需要登录认证
- Cookie管理是关键
- 视频内容需要下载后进行语音识别
- 遵守网站使用条款

---

## 资源更新日志

- 2025-03-25：初始版本创建，收录核心工具和API
