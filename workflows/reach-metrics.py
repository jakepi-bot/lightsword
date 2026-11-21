#!/usr/bin/env python3
"""Append one reach snapshot for @flambeee. Read-only against Bluesky.

    python3 workflows/reach-metrics.py            # append a snapshot
    python3 workflows/reach-metrics.py --print    # print only, do not write

What is countable without an analytics tag: followers, follows, posts, and the
notification list (likes, reposts, replies, quotes, mentions, follows). What is
not countable: impressions, profile visits, site clicks, signups, play counts.
Those are recorded as "unavailable" with a reason, never as zero and never as an
estimate. The campaign window comes from the same state file the posting client
enforces, so the snapshot and the write guard cannot disagree.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "workflows"))
import bsky  # noqa: E402  (the one client; importing does not authenticate)

OUT = REPO / "metrics" / "campaign" / "2026-11-19-reach.ndjson"
HANDLE = "flambeee.bsky.social"
INBOUND = ("like", "repost", "reply", "quote", "mention", "follow")


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", dest="print_only", action="store_true")
    args = ap.parse_args(argv)

    profile = bsky.public_call("app.bsky.actor.getProfile", {"actor": HANDLE})
    window = json.loads(bsky.WINDOW_FILE.read_text())
    start = datetime.fromisoformat(window["start"])
    end = datetime.fromisoformat(window["end"])
    now = datetime.now(timezone.utc)

    acct = bsky.Account("fb")
    token = acct.session()
    notes = bsky.authed_get("app.bsky.notification.listNotifications",
                            {"limit": 100}, token).get("notifications") or []
    inbound = []
    for n in notes:
        try:
            when = datetime.fromisoformat(n["indexedAt"].replace("Z", "+00:00"))
        except (KeyError, ValueError):
            continue
        if not (start <= when <= end):
            continue
        if n.get("reason") not in INBOUND:
            continue
        if (n.get("author") or {}).get("did") == acct._did:
            continue  # our own actions are not audience engagement
        inbound.append({"reason": n["reason"], "author": (n.get("author") or {}).get("handle"),
                        "at": iso(when), "uri": n.get("uri")})

    replies_sent, posts_sent = [], []
    log = REPO / "logs" / "bsky-actions.ndjson"
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("account") != "fb" or r.get("status") != "ok":
                continue
            when = datetime.fromisoformat(r["ts"].replace("Z", "+00:00"))
            if not (start <= when <= end):
                continue
            if r.get("action") == "reply":
                replies_sent.append(r.get("uri"))
            elif r.get("action") == "post":
                posts_sent.append(r.get("uri"))

    snap = {
        "ts": iso(now),
        "window": {"start": window["start"], "end": window["end"],
                   "open": start <= now <= end},
        "followers": profile.get("followersCount"),
        "follows": profile.get("followsCount"),
        "posts": profile.get("postsCount"),
        "pinned": bool(profile.get("pinnedPost")),
        "inbound_from_others": len(inbound),
        "inbound_by_reason": {k: sum(1 for i in inbound if i["reason"] == k) for k in INBOUND},
        "inbound_examples": inbound[:20],
        "replies_sent_in_window": len(replies_sent),
        "posts_sent_in_window": len(posts_sent),
        "unavailable": {
            "impressions": "no analytics tag on flambeee.com and no view count in the public API",
            "profile_visits": "not exposed by the AT Protocol",
            "site_clicks": "no analytics tag on flambeee.com",
            "signups": "no signup exists; no instrument",
            "play_counts": "client keeps play counts in localStorage; no network call",
        },
    }
    print(json.dumps(snap, indent=2, ensure_ascii=False))
    if not args.print_only:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(snap, ensure_ascii=False) + "\n")
        print(f"\nappended {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
