#!/usr/bin/env python3
"""Post the second half of campaign post #08 as a reply to its root.

Deterministic, no LLM. Safe to run twice: the reply id key and the
logs/replies.ndjson target check both prevent a duplicate.
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/jake/.hermes/lightsword/lightsword")
CAMPAIGN = REPO / "queue" / "campaign" / "fb-campaign-2026-11-13.json"
OUTBOX = REPO / "queue" / "outbox" / "fb-camp-20261113-08.json"
MANIFEST = REPO / "published" / "manifest.ndjson"
REPLIES = REPO / "logs" / "replies.ndjson"
REPLY_DIR = REPO / "queue" / "replies"
ASSET_ID = "fb-camp-20261113-08"
ID_KEY = "fb-camp-20261113-08-reply"


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def root_uri() -> tuple[str | None, str]:
    try:
        item = json.loads(OUTBOX.read_text())
        if item.get("uri"):
            return item["uri"], "outbox"
    except (OSError, json.JSONDecodeError):
        pass
    try:
        for line in MANIFEST.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("asset_id") == ASSET_ID and row.get("uri"):
                return row["uri"], "manifest"
    except OSError:
        pass
    return None, "none"


def already_sent(uri: str) -> bool:
    try:
        for line in REPLIES.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("target_uri") == uri and row.get("result") == "posted":
                return True
    except OSError:
        pass
    return False


def main() -> int:
    campaign = json.loads(CAMPAIGN.read_text())
    post = next(p for p in campaign["posts"] if p["asset_id"] == ASSET_ID)
    text = post["thread"][0]["text"]

    uri, source = root_uri()
    if not uri:
        print(f"WARNING {ASSET_ID} root not published yet; thread part 2 not sent ({now_utc()})")
        return 0
    if already_sent(uri):
        print(f"SKIP {ASSET_ID} thread part 2 already logged for {uri}")
        return 0

    proc = subprocess.run(
        [sys.executable, "workflows/bsky.py", "--account", "fb", "reply",
         "--to", uri, "--text", text, "--id-key", ID_KEY],
        cwd=REPO, capture_output=True, text=True, timeout=120,
    )
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode != 0:
        print(f"FAILED {ASSET_ID} thread part 2 (exit {proc.returncode}): {err[:400] or out[:400]}")
        return 0  # a warning, not a cron failure; the daily summary will see it

    reply_uri = None
    for line in out.splitlines():
        if line.startswith("OK reply "):
            reply_uri = line.split()[-1]
    reply_uri = reply_uri or "unknown"

    REPLY_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d")
    numbered = sorted(REPLY_DIR.glob(f"{stamp}-bsky-*.md"))
    path = REPLY_DIR / f"{stamp}-bsky-{len(numbered) + 1:02d}.md"
    path.write_text(
        "---\n"
        f"target: {uri}\n"
        "author: @flambeee.bsky.social\n"
        f"received: {now_utc()}\n"
        "class: thread\n"
        "snippet: T1\n"
        f"sent_uri: {reply_uri}\n"
        "---\n\n"
        f"{text}\n\n"
        "## Sources\n\n"
        "- Campaign post #08 thread part 2, `queue/campaign/fb-campaign-2026-11-13.json`.\n"
        "- Echo Rounds keyboard-only and the game page: claims rows 13, 25; live page checked 2026-11-12.\n"
    )
    with REPLIES.open("a") as fh:
        fh.write(json.dumps({
            "ts": now_utc(),
            "account": "@flambeee.bsky.social",
            "target_uri": uri,
            "author": "self-thread",
            "class": "thread",
            "snippet": "T1",
            "text": text,
            "uri": reply_uri,
            "result": "posted",
        }, ensure_ascii=False) + "\n")

    print(f"POSTED {ASSET_ID} thread part 2 -> {reply_uri} (root from {source})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
