# WeChat Formatter

公众号排版 Agent - 将 Markdown 转换为微信兼容的 HTML

## 功能特点

- 内联 CSS 样式（微信不支持外部样式表）
- 响应式设计（移动端优化）
- 代码高亮支持
- 自定义配色方案
- 微信安全域名图片处理

## 输入格式

```json
{
  "title": "文章标题",
  "content": "Markdown格式正文",
  "author": "作者名称",
  "theme": "default | blue | green | purple"
}
```

## 输出格式

```json
{
  "success": true,
  "html": "<div>...</div>",
  "preview_url": "预览链接（可选）"
}
```
