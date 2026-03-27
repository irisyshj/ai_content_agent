# n8n Workflow Setup Guide

## AI Media Content Pipeline Integration

This guide shows you how to configure n8n to use the AI Media System API.

---

## Prerequisites

1. **n8n installed** - Download from [n8n.io](https://n8n.io)
2. **API Server running** - Start the AI Media API server:
   ```bash
   python api_server.py --host 127.0.0.1 --port 5004
   ```
3. Verify the API is working:
   ```bash
   curl http://127.0.0.1:5004/health
   ```

---

## Option 1: Import Workflow (Recommended)

1. Open n8n in your browser
2. Click **"Import from File"** in the top right
3. Select `n8n-workflow-ai-media-pipeline.json`
4. The workflow will be loaded with all nodes configured

---

## Option 2: Manual Setup

### Step 1: Create Webhook Trigger

1. Add a **Webhook** node
2. Configure:
   - **HTTP Method**: `POST`
   - **Path**: `ai-media-trigger`
   - **Response Mode**: `Using 'Respond to Webhook' node`

3. Click **"Listen for Test Event"**
4. Copy the webhook URL for testing

### Step 2: Add HTTP Request Node

1. Add an **HTTP Request** node
2. Connect it after the Webhook
3. Configure:
   - **Method**: `POST`
   - **URL**: `http://localhost:5004/api/v1/pipeline/run`
   - **Body**: `JSON`
   ```json
   {
     "content": "{{$json.content}}",
     "title": "{{$json.title}}",
     "theme": "{{$json.theme}}"
   }
   ```

### Step 3: Add Success Check

1. Add an **IF** node
2. Condition:
   - **Field**: `success`
   - **Operation**: `Equal`
   - **Value**: `true`

### Step 4: Format Responses

**Success branch** (Set node):
```json
{
  "status": "success",
  "title": "{{$json.article.title}}",
  "html": "{{$json.html}}"
}
```

**Error branch** (Set node):
```json
{
  "status": "error",
  "error": "{{$json.error}}"
}
```

### Step 5: Respond to Webhook

1. Add a **Respond to Webhook** node
2. Configure:
   - **Respond With**: `JSON`
   - **Response Body**: `={{ $json }}`

3. Connect both branches to this node

---

## Testing the Workflow

### Test with Sample Data

Send a POST request to your webhook:

```bash
curl -X POST https://your-n8n-instance.com/webhook/ai-media-trigger \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Artificial Intelligence is transforming how we work and live. Machine learning models can now understand and generate human-like text.",
    "title": "AI Technology Overview",
    "theme": "green"
  }'
```

### Expected Response

```json
{
  "status": "success",
  "title": "🤔 AI Technology Overview：小白也能懂的解读",
  "html": "<div>...</div>"
}
```

---

## Advanced: Add More Skills

### Add Geektime Collector

1. Add a new HTTP Request node
2. URL: `http://localhost:5004/api/v1/collect/geektime`
3. Body:
```json
{
  "url": "{{$json.article_url}}"
}
```

### Add Image Generation

After getting the HTML response:
1. Extract key points from the article
2. Call an image generation API (DALL-E, Midjourney, etc.)
3. Insert images into the HTML

### Add WeChat Publishing

1. Use the WeChat Official Account API
2. Upload the HTML as a draft
3. Publish when approved

---

## Troubleshooting

**Error: Connection refused**
- Ensure the API server is running on port 5004
- Check firewall settings

**Error: Invalid JSON response**
- Verify the API is returning valid JSON
- Check n8n execution logs

**Error: Missing content field**
- Ensure your webhook receives the `content` field
- Check the JSON body format

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/pipeline/run` | POST | Run full pipeline |
| `/api/v1/collect/geektime` | POST | Collect from Geektime |
| `/api/v1/curate` | POST | Generate topics |
| `/api/v1/write` | POST | Write article |
| `/api/v1/format` | POST | Format to HTML |

---

## Next Steps

- [ ] Set up n8n webhook with external services (e.g., content CMS)
- [ ] Add authentication to the API
- [ ] Configure error handling and retries
- [ ] Set up monitoring for pipeline runs
