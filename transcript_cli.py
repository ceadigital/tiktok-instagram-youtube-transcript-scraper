#!/usr/bin/env python3
"""
CLI & SDK for CEA Digital Actor #2: Instagram, TikTok & YouTube Transcript & Hook Scraper.
Supports both Direct Unified Key (`https://ceadigital.io/tools`) and Apify Store (`cea_digital/instagram-tiktok-youtube-transcript-scraper`).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import httpx

DIRECT_ENDPOINT = "https://ceadigital.io/v1/tools/instagram-tiktok-youtube-transcript-scraper"
APIFY_ENDPOINT = "https://api.apify.com/v2/acts/cea_digital~instagram-tiktok-youtube-transcript-scraper/run-sync-get-dataset-items"


def extract_transcripts(
    video_urls: list[str],
    generate_ugc_brief: bool = True,
    translate_to: str | None = None,
    use_apify: bool = False,
    api_key: str | None = None,
) -> dict[str, Any] | list[dict[str, Any]]:
    payload: dict[str, Any] = {
        "videoUrls": video_urls,
        "generateUgcBrief": generate_ugc_brief,
    }
    if translate_to:
        payload["translateTo"] = translate_to

    headers = {"Accept-Encoding": "gzip, deflate", "Content-Type": "application/json"}
    with httpx.Client(timeout=30.0, headers=headers) as client:
        if use_apify:
            token = api_key or os.environ.get("APIFY_TOKEN", "").strip()
            if not token:
                raise RuntimeError("Missing APIFY_TOKEN. Set APIFY_TOKEN or use https://ceadigital.io/tools with CEA_API_KEY.")
            resp = client.post(f"{APIFY_ENDPOINT}?token={token}", json=payload)
            resp.raise_for_status()
            return resp.json()

        key = api_key or os.environ.get("CEA_API_KEY", "").strip()
        if not key:
            raise RuntimeError("Missing CEA_API_KEY. Claim a $2 Tripwire Pass or $29/mo Growth Key at https://ceadigital.io/tools")
        resp = client.post(DIRECT_ENDPOINT, headers={"Authorization": f"Bearer {key}"}, json=payload)
        resp.raise_for_status()
        return resp.json()


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract 0-3s spoken hooks, visual OCR hooks, and timecoded transcripts.")
    parser.add_argument("--url", action="append", default=[], help="TikTok, Instagram Reel, or YouTube Shorts URL (repeatable)")
    parser.add_argument("--translate-to", default=None, help="Optional target language code (es, de, pt, fr)")
    parser.add_argument("--no-ugc-brief", action="store_true", help="Disable UGC creator brief generation")
    parser.add_argument("--apify", action="store_true", help="Route via Apify Store (cea_digital/instagram-tiktok-youtube-transcript-scraper)")
    parser.add_argument("--api-key", default=None, help="Explicit CEA_API_KEY or APIFY_TOKEN")
    args = parser.parse_args()

    urls = args.url or ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    try:
        res = extract_transcripts(
            video_urls=urls,
            generate_ugc_brief=not args.no_ugc_brief,
            translate_to=args.translate_to,
            use_apify=args.apify,
            api_key=args.api_key,
        )
        print(json.dumps(res, indent=2))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
