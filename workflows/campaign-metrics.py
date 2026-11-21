#!/usr/bin/env python3
"""Read-only metrics snapshot for the flambeee 72-hour campaign.

Every number is measured from the public AppView or read from a repo file.
Fields with no instrument are emitted as ``unavailable`` with a reason; this
script never estimates.

Usage:
    python3 workflows/campaign-metrics.py --label 2026-11-13-t0
    python3 workflows/campaign-metrics.py --label 2026-11-13-day1 --out metrics/campaign/2026-11-13.json

Sources:
  * profile: app.bsky.actor.getProfile?actor=flambeee.bsky.social
  * posts:   app.bsky.feed.getPostThread?uri=<post>&depth=6
  * URIs:    queue/outbox/*.json first, published/manifest.ndjson fallback
  * replies: logs/bsky-actions.ndjson (ours), campaign JSON (the plan)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

PUB = "https://public.api.bsky.app/xrpc"
REPO = Path("/home/jake/.hermes/lightsword/lightsword")
CAMPAIGN = REPO / "queue" / "campaign" / "fb-campaign-2026-11-13.json"
OUTBOX = REPO / "queue" / "outbox"
MANIFEST = REPO / "published" / "manifest.ndjson"
ACTIONS = REPO / "logs" / "bsky-actions.ndjson"
HANDLE = "flambeee.bsky.social"


def get(method: str, **params):
    url = f"{PUB}/{method}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read())


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return default


def asset_uris(campaign: dict) -> dict[str, dict]:
    """asset_id -> {uri, url, status, publish_at}; outbox wins, manifest fills gaps."""
    found: dict[str, dict] = {}
    for path in sorted(OUTBOX.glob("*.json")):
        item = load_json(path, None)
        if not item or not item.get("asset_id"):
            continue
        found[item["asset_id"]] = {
            "uri": item.get("uri"),
            "url": item.get("url"),
            "status": item.get("status"),
            "publish_at": item.get("publish_at"),
            "source": "outbox",
        }
    try:
        for line in MANIFEST.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            asset_id = row.get("asset_id")
            if not asset_id:
                continue
            entry = found.setdefault(asset_id, {"source": "manifest"})
            entry.setdefault("uri", row.get("uri"))
            entry.setdefault("url", row.get("url"))
            entry.setdefault("status", "published")
            entry.setdefault("published_at", row.get("timestamp"))
    except OSError:
        pass
    return found


def walk_replies(node: dict | None, out: list[dict], depth: int = 0):
    if not node or depth > 8:
        return
    for reply in node.get("replies") or []:
        post = reply.get("post")
        if post:
            out.append(post)
            walk_replies(reply, out, depth + 1)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True, help="snapshot label, e.g. 2026-11-13-day1")
    parser.add_argument("--out", help="output path (default metrics/campaign/<label>.json)")
    args = parser.parse_args(argv)

    campaign = load_json(CAMPAIGN, None)
    if not campaign:
        print(f"REFUSED: cannot read {CAMPAIGN}", file=sys.stderr)
        return 2
    uris = asset_uris(campaign)

    profile = get("app.bsky.actor.getProfile", actor=HANDLE)
    own_did = profile.get("did")
    own_handle = (profile.get("handle") or HANDLE).lower()

    posts = []
    totals = {"likes": 0, "reposts": 0, "replies": 0, "quotes": 0, "actions": 0, "stranger_replies": 0}
    for planned in campaign["posts"]:
        rec = uris.get(planned["asset_id"], {})
        row = {
            "n": planned["n"],
            "slot_ct": planned["slot_ct"],
            "asset_id": planned["asset_id"],
            "uri": rec.get("uri"),
            "url": rec.get("url"),
            "outbox_status": rec.get("status"),
            "likes": None,
            "reposts": None,
            "replies": None,
            "quotes": None,
            "actions": None,
            "stranger_replies": None,
            "reply_authors": [],
            "measured": False,
        }
        uri = rec.get("uri")
        if uri:
            try:
                thread = get("app.bsky.feed.getPostThread", uri=uri, depth=6)["thread"]
                post = thread.get("post") or {}
                replies = []
                walk_replies(thread, replies)
                strangers = []
                for reply in replies:
                    author = (reply.get("author") or {})
                    if author.get("did") != own_did:
                        handle = author.get("handle")
                        if handle and handle not in strangers:
                            strangers.append(handle)
                row.update(
                    likes=post.get("likeCount", 0),
                    reposts=post.get("repostCount", 0),
                    replies=post.get("replyCount", 0),
                    quotes=post.get("quoteCount", 0),
                    stranger_replies=sum(
                        1 for reply in replies if (reply.get("author") or {}).get("did") != own_did
                    ),
                    reply_authors=strangers,
                    measured=True,
                )
                row["actions"] = row["likes"] + row["reposts"] + row["replies"] + row["quotes"]
            except Exception as exc:  # AppView lag or not found: record it, do not invent
                row["error"] = str(exc)[:200]
        posts.append(row)
        if row["measured"]:
            for key in totals:
                if key == "stranger_replies":
                    totals[key] += row["stranger_replies"]
                else:
                    totals[key] += row[key]

    live = [p for p in posts if p["measured"]]

    # Replies we sent inside the campaign window, from the audit ledger.
    window_start = dt.datetime.fromisoformat(
        campaign["window"]["start_utc"].replace("Z", "+00:00")
    )
    replies_sent = []
    try:
        for line in ACTIONS.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("account") != "fb" or row.get("action") != "reply" or row.get("status") != "ok":
                continue
            try:
                ts = dt.datetime.fromisoformat(row["ts"].replace("Z", "+00:00"))
            except (KeyError, ValueError):
                continue
            if ts >= window_start:
                replies_sent.append(
                    {"ts": row["ts"], "uri": row.get("uri"), "reply_to": row.get("reply_to"), "chars": row.get("chars")}
                )
    except OSError:
        pass

    snapshot = {
        "campaign": campaign["campaign"],
        "label": args.label,
        "captured_at": iso_now(),
        "account": {
            "handle": profile.get("handle"),
            "did": own_did,
            "followers": profile.get("followersCount"),
            "following": profile.get("followsCount"),
            "posts": profile.get("postsCount"),
            "bio": profile.get("description"),
        },
        "window": campaign["window"],
        "kpi": {
            "K1_posts_live": len(live),
            "K1_posts_planned": len(campaign["posts"]),
            "K2_followers": profile.get("followersCount"),
            "K3_actions": totals["actions"],
            "K3_stranger_replies": totals["stranger_replies"],
        },
        "totals": totals,
        "posts": posts,
        "replies_sent_in_window": replies_sent,
        "replies_sent_in_window_count": len(replies_sent),
        "unavailable": {
            "impressions": "unavailable (no instrument: Bluesky exposes no impression count)",
            "profile_visits": "unavailable (no instrument: no Bluesky endpoint)",
            "site_clicks": "unavailable (no instrument: no analytics tag on flambeee.com)",
            "signups": "unavailable (no instrument: no account system)",
            "play_counts": "unavailable (no instrument: no aggregate counter at flambeee.com)",
        },
        "queries": {
            "profile": f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={HANDLE}",
            "post_thread": "https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?uri=<post>&depth=6",
        },
    }

    out = Path(args.out) if args.out else REPO / "metrics" / "campaign" / f"{args.label}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    print(f"WROTE {out}")
    print(
        f"K1 {len(live)}/{len(campaign['posts'])} live | K2 {snapshot['kpi']['K2_followers']} followers | "
        f"K3 {totals['actions']} actions, {totals['stranger_replies']} stranger replies | "
        f"our replies in window {len(replies_sent)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
