#!/usr/bin/env python3
"""
Zero-Dependency Python Stdio MCP Server for CEA Digital Actor #2:
TikTok, Instagram Reels & YouTube Shorts Transcript & 0-3s Hook Scraper.

Implements JSON-RPC 2.0 (initialize, tools/list, tools/call, ping) over stdio.
Routes tool calls to https://ceadigital.io/v1/tools/instagram-tiktok-youtube-transcript-scraper
(or https://ceadigital.io/v1/tools/free-preview in zero-config sandbox mode).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

DIRECT_ENDPOINT = "https://ceadigital.io/v1/tools/instagram-tiktok-youtube-transcript-scraper"
FREE_PREVIEW_ENDPOINT = "https://ceadigital.io/v1/tools/free-preview"
APIFY_ENDPOINT = "https://api.apify.com/v2/acts/cea_digital~instagram-tiktok-youtube-transcript-scraper/run-sync-get-dataset-items"

TOOLS: list[dict[str, Any]] = [
    {
        "name": "instagram_tiktok_youtube_transcript_scraper",
        "description": (
            "Extract 0-3s spoken hooks, 0-3s burned-in visual OCR frame captions, hook retention "
            "scores (0-100), full timecoded transcripts, 3-act UGC creator briefs, and localized "
            "ad scripts (es, de, pt, fr) from TikTok, Instagram Reels, and YouTube Shorts URLs. "
            "Use when an user or agent needs to reverse-engineer viral short-form video hooks, "
            "analyze competitor ad scripts, or generate localized UGC creative briefs. "
            "Supports zero-key 1-row live preview or full batch execution with CEA_API_KEY."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "videoUrls": {
                    "type": "array",
                    "items": {"type": "string", "minLength": 10, "maxLength": 500},
                    "minItems": 1,
                    "maxItems": 25,
                    "description": (
                        "Array of TikTok, Instagram Reels, or YouTube Shorts/Watch URLs to scrape "
                        "(1 to 25 URLs per request). Example: ['https://www.youtube.com/watch?v=dQw4w9WgXcQ']."
                    ),
                    "default": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
                },
                "generateUgcBrief": {
                    "type": "boolean",
                    "default": True,
                    "description": (
                        "When true, synthesizes a 3-act UGC creator script brief (0-3s Hook, Problem/Agitation, "
                        "Solution + Call to Action) ready for DTC ad production."
                    ),
                },
                "translateTo": {
                    "type": "string",
                    "enum": ["es", "de", "pt", "fr", "en"],
                    "default": "es",
                    "description": (
                        "Optional ISO 639-1 language code ('es', 'de', 'pt', 'fr', 'en') to translate "
                        "the extracted 0-3s hook and full ad script."
                    ),
                },
            },
            "required": ["videoUrls"],
        },
        "annotations": {
            "title": "TikTok, Instagram Reels & YouTube Shorts Transcript & Hook Scraper",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    }
]


def _call_upstream(args: dict[str, Any]) -> dict[str, Any] | list[Any]:
    video_urls = args.get("videoUrls") or ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    generate_ugc_brief = bool(args.get("generateUgcBrief", True))
    translate_to = args.get("translateTo")

    payload: dict[str, Any] = {
        "videoUrls": video_urls,
        "generateUgcBrief": generate_ugc_brief,
    }
    if translate_to:
        payload["translateTo"] = translate_to

    cea_key = os.environ.get("CEA_API_KEY", "").strip()
    apify_token = os.environ.get("APIFY_TOKEN", "").strip()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "ceadigital-transcript-mcp/1.2.0",
    }

    if cea_key:
        url = DIRECT_ENDPOINT
        headers["Authorization"] = f"Bearer {cea_key}"
        body = json.dumps(payload).encode("utf-8")
    elif apify_token:
        url = f"{APIFY_ENDPOINT}?token={apify_token}"
        body = json.dumps(payload).encode("utf-8")
    else:
        url = FREE_PREVIEW_ENDPOINT
        preview_payload = {
            "tool": "instagram-tiktok-youtube-transcript-scraper",
            "input": payload,
        }
        body = json.dumps(preview_payload).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as err:
        err_body = err.read().decode("utf-8", errors="replace")
        return {
            "status": "http_error",
            "code": err.code,
            "message": err_body[:500],
            "upgrade_url": "https://ceadigital.io/tools",
            "apify_actor_url": "https://apify.com/cea_digital/instagram-tiktok-youtube-transcript-scraper",
        }
    except Exception as exc:
        return {
            "status": "preview_fallback",
            "note": f"Upstream network unreachable in sandbox ({exc}); returning deterministic schema sample.",
            "sample": {
                "videoUrl": video_urls[0],
                "spokenHook0To3s": "Stop scrolling if your ROAS dropped below 2.0 this week—",
                "visualOcrHook0To3s": "3 AD HOOKS PRINTING IN Q4",
                "hookRetentionScore": 91,
                "upgradeUrl": "https://ceadigital.io/tools",
            },
        }


def handle_request(msg: dict[str, Any]) -> dict[str, Any] | None:
    method = msg.get("method")
    req_id = msg.get("id")

    if req_id is None:
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2025-03-26",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {
                    "name": "cea-tiktok-instagram-youtube-transcript-scraper",
                    "version": "1.2.0",
                },
            },
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        params = msg.get("params") or {}
        tool_name = params.get("name")
        arguments = params.get("arguments") or {}
        if tool_name != "instagram_tiktok_youtube_transcript_scraper":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Unknown tool: {tool_name}"},
            }
        data = _call_upstream(arguments)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(data, indent=2),
                    }
                ],
                "isError": False,
            },
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            resp = handle_request(msg)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {exc}"},
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
