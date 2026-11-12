# TikTok, Instagram Reels & YouTube Shorts Transcript & Hook Scraper (Python CLI, SDK & MCP Server)

[![Apify Store](https://img.shields.io/badge/Apify_Store-cea__digital%2Finstagram--tiktok--youtube--transcript--scraper-00C853?style=flat-square)](https://apify.com/cea_digital/instagram-tiktok-youtube-transcript-scraper)
[![Direct Unified Key](https://img.shields.io/badge/Direct_Unified_Key-%242_Tripwire_%7C_%2429%2Fmo-2563EB?style=flat-square)](https://ceadigital.io/tools)
[![Run in Postman](https://img.shields.io/badge/Run_in_Postman-v2.1_Collection-FF6C37?style=flat-square&logo=postman&logoColor=white)](https://ceadigital.io/templates/postman-collection.json)
[![Glama MCP](https://img.shields.io/badge/Glama-MCP_Directory-8B5CF6?style=flat-square)](https://glama.ai/mcp/servers/ceadigital/tiktok-instagram-youtube-transcript-scraper)
[![Zero Charge on Silent](https://img.shields.io/badge/Miss_Guarantee-%240.00_on_Silent_or_Private_Videos-10B981?style=flat-square)](https://ceadigital.io/tools)

Extract **0–3s spoken hooks**, **0–3s burned-in visual OCR captions**, **hook retention scores**, **timecoded transcripts**, **UGC creator briefs**, and **localized ad scripts** (`es`, `de`, `pt`, `fr`) from TikTok, Instagram Reels, and YouTube Shorts over pure HTTP (`Accept-Encoding: gzip, deflate`, zero headless browser).

---

## 1-Click Ecosystem & No-Code Integrations

| Platform / Channel | Direct Link |
| :--- | :--- |
| **Direct $29/mo Stripe API Key & $2 Tripwire Pass (Free 1-Row Preview)** | **[https://ceadigital.io/tools](https://ceadigital.io/tools)** |
| **Apify Store Actor (`cea_digital/instagram-tiktok-youtube-transcript-scraper`)** | **[https://apify.com/cea_digital/instagram-tiktok-youtube-transcript-scraper](https://apify.com/cea_digital/instagram-tiktok-youtube-transcript-scraper)** |
| **Run in Postman (Public Collection v2.1)** | **[https://ceadigital.io/templates/postman-collection.json](https://ceadigital.io/templates/postman-collection.json)** |
| **1-Click Google Sheets Custom Function (`=VIDEOHOOK(A2, "es")`)** | **[https://ceadigital.io/templates/Code.gs](https://ceadigital.io/templates/Code.gs)** |
| **1-Click n8n Native Workflow Template (`.workflow.json`)** | **[https://ceadigital.io/templates/instagram-tiktok-youtube-transcript-scraper.workflow.json](https://ceadigital.io/templates/instagram-tiktok-youtube-transcript-scraper.workflow.json)** |
| **Clay.com HTTP API Column Blueprints** | **[https://ceadigital.io/templates/clay-http-column-blueprints.json](https://ceadigital.io/templates/clay-http-column-blueprints.json)** |
| **Glama MCP Server Directory** | **[https://glama.ai/mcp/servers/ceadigital/tiktok-instagram-youtube-transcript-scraper](https://glama.ai/mcp/servers/ceadigital/tiktok-instagram-youtube-transcript-scraper)** |

---

## Quickstart #1 — Direct Unified API Key (`https://ceadigital.io/tools`)

Use one **`cea_live_`** Unified API Key (**$2.00 One-Time 100-Hit Tripwire Pass** or **$29/mo Growth Plan for 5,000 hits**) across all 4 CEA Digital tools:

```bash
export CEA_API_KEY="cea_live_your_key_here"
python transcript_cli.py \
  --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --translate-to es
```

Or via `curl`:

```bash
curl -sS -X POST "https://ceadigital.io/v1/tools/instagram-tiktok-youtube-transcript-scraper" \
  -H "Authorization: Bearer $CEA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "videoUrls": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
    "generateUgcBrief": true,
    "translateTo": "es"
  }' | jq .
```

---

## Quickstart #2 — Apify Store (`cea_digital/instagram-tiktok-youtube-transcript-scraper`)

Run on Apify Pay-Per-Event (`$0.005/min` on Bronze+ plans, `$0.00` on private/deleted/silent videos) or chain directly to `apify/instagram-scraper` or `clockworks/tiktok-scraper` via `igOrTiktokDatasetId`:

```bash
export APIFY_TOKEN="apify_api_your_token_here"
python transcript_cli.py \
  --apify \
  --url "https://www.tiktok.com/@dtcgrowthlab/video/7391847291048291001"
```

```bash
curl -sS -X POST "https://api.apify.com/v2/acts/cea_digital~instagram-tiktok-youtube-transcript-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "videoUrls": ["https://www.tiktok.com/@dtcgrowthlab/video/7391847291048291001"],
    "generateUgcBrief": true
  }' | jq .
```

---

## Quickstart #3 — Model Context Protocol (MCP) for Claude, Cursor & Glama

### Remote Streamable-HTTP MCP (Zero Install)
```bash
claude mcp add --transport http ceadigital-b2a https://ceadigital.io/mcp
```

### Local Stdio MCP Server (`mcp_server.py`)
```json
{
  "mcpServers": {
    "cea-video-transcript": {
      "command": "python3",
      "args": ["/path/to/tiktok-instagram-youtube-transcript-scraper/mcp_server.py"],
      "env": {
        "CEA_API_KEY": "cea_live_optional_key_or_blank_for_free_preview"
      }
    }
  }
}
```

---

## License

MIT License — Copyright (c) 2026 CEA Digital ([ceadigital.io](https://ceadigital.io))
