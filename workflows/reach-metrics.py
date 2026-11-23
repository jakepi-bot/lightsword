#!/usr/bin/env python3
"""Append one daily reach/engagement snapshot for an account. Read-only.

    python3 workflows/reach-metrics.py --client flambeee   # a registry client
    python3 workflows/reach-metrics.py --account lt        # the internal account
    python3 workflows/reach-metrics.py --client flambeee --print

Contract (plans/engagement-program.md §8): what is countable without an
analytics tag is followers, follows, posts and the notification list (likes,
reposts, replies, quotes, mentions, follows). What is not countable is
impressions, profile visits, site clicks, signups and play counts. Those are
recorded as "unavailable" with a reason, never as zero and never estimated.

Writes one NDJSON line to metrics/<slug>/reach.ndjson. The period counted is
the time since the previous snapshot in that file, so consecutive daily runs
give a per-day number without anyone subtracting dates by hand. The first run
falls back to a client's written window start, or 24 hours.

A client whose registry status is not 'active' is still snapshotted when it has
no open window (nothing to count, but the followers number keeps a continuous
record); it is never sent anything. Reading is not a write.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "workflows"))
import bsky  # noqa: E402  (the one client; importing does not authenticate)

REGISTRY = REPO / "plans" / "clients.json"
INBOUND = ("like", "repost", "reply", "quote", "mention", "follow")
ACTIONS_LOG = REPO / "logs" / "bsky-actions.ndjson"


def iso(when: datetime) -> str:
    return when.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_registry() -> dict:
    if not REGISTRY.exists():
        return {}
    return json.loads(REGISTRY.read_text(encoding="utf-8")).get("clients", {})


def resolve(client: str | None, account: str | None) -> dict:
    """Return {slug, account_key, handle, window_file, unavailable_notes}."""
    registry = load_registry()
    if client:
        if client not in registry:
            raise SystemExit(f"ERROR unknown client {client!r}; known: {', '.join(registry) or 'none'}")
        c = registry[client]
        notes = c.get("snapshot", {}).get("unavailable")
        return {
            "slug": client,
            "account_key": c["account_key"],
            "handle": c["handle"],
            "window_file": c.get("window_file"),
            "unavailable": notes,
        }
    if account:
        if account not in bsky.ACCOUNTS:
            raise SystemExit(f"ERROR unknown account {account!r}; known: {', '.join(bsky.ACCOUNTS)}")
        return {
            "slug": account,
            "account_key": account,
            "handle": bsky.ACCOUNTS[account][1],
            "window_file": None,
            "unavailable": None,
        }
    raise SystemExit("ERROR pass --client <slug> or --account <key>")


def default_unavailable(slug: str) -> dict:
    return {
        "impressions": "no analytics tag and no view count in the public API",
        "profile_visits": "not exposed by the AT Protocol",
        "site_clicks": "no analytics tag on the destination site",
        "signups": "no instrument",
        "play_counts": "no instrument",
    }


def period_start(out: Path, window_file: Path | None, now: datetime) -> tuple[datetime, str]:
    """Start of the period this snapshot counts, and why that start was chosen."""
    if out.exists():
        last = None
        for line in out.read_text(encoding="utf-8").splitlines():
            try:
                last = json.loads(line).get("ts")
            except ValueError:
                continue
        if last:
            return parse_ts(last), "previous snapshot"
    if window_file and window_file.exists():
        try:
            start = datetime.fromisoformat(json.loads(window_file.read_text())["start"])
            return start, "written window start"
        except (ValueError, KeyError):
            pass
    return now - timedelta(hours=24), "24 hours (no previous snapshot)"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", help="client slug from plans/clients.json")
    ap.add_argument("--account", help="account key from workflows/bsky.py ACCOUNTS (e.g. lt)")
    ap.add_argument("--print", dest="print_only", action="store_true")
    args = ap.parse_args(argv)

    who = resolve(args.client, args.account)
    slug, acct_key, handle = who["slug"], who["account_key"], who["handle"]

    out = REPO / "metrics" / slug / "reach.ndjson"
    window_file = Path(who["window_file"]).expanduser() if who["window_file"] else None

    profile = bsky.public_call("app.bsky.actor.getProfile", {"actor": handle})
    now = datetime.now(timezone.utc)
    start, start_reason = period_start(out, window_file, now)

    window = None
    if window_file and window_file.exists():
        raw = json.loads(window_file.read_text())
        w_start = datetime.fromisoformat(raw["start"])
        w_end = datetime.fromisoformat(raw["end"])
        window = {"start": raw["start"], "end": raw["end"], "open": w_start <= now <= w_end}

    acct = bsky.Account(acct_key)
    token = acct.session()
    notes = bsky.authed_get("app.bsky.notification.listNotifications",
                            {"limit": 100}, token).get("notifications") or []
    inbound = []
    for n in notes:
        try:
            when = parse_ts(n["indexedAt"])
        except (KeyError, ValueError):
            continue
        if not (start <= when <= now):
            continue
        if n.get("reason") not in INBOUND:
            continue
        if (n.get("author") or {}).get("did") == acct._did:
            continue  # our own actions are not audience engagement
        inbound.append({"reason": n["reason"], "author": (n.get("author") or {}).get("handle"),
                        "at": iso(when), "uri": n.get("uri")})

    replies_sent, posts_sent = [], []
    if ACTIONS_LOG.exists():
        for line in ACTIONS_LOG.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("account") != acct_key or r.get("status") != "ok":
                continue
            try:
                when = parse_ts(r["ts"])
            except (KeyError, ValueError):
                continue
            if not (start <= when <= now):
                continue
            if r.get("action") == "reply":
                replies_sent.append(r.get("uri"))
            elif r.get("action") == "post":
                posts_sent.append(r.get("uri"))

    snap = {
        "ts": iso(now),
        "account": acct_key,
        "handle": handle,
        "period": {"start": iso(start), "end": iso(now), "chosen_by": start_reason},
        "followers": profile.get("followersCount"),
        "follows": profile.get("followsCount"),
        "posts": profile.get("postsCount"),
        "pinned": bool(profile.get("pinnedPost")),
        "inbound_from_others": len(inbound),
        "inbound_by_reason": {k: sum(1 for i in inbound if i["reason"] == k) for k in INBOUND},
        "inbound_examples": inbound[:20],
        "replies_sent_in_period": len(replies_sent),
        "posts_sent_in_period": len(posts_sent),
        "unavailable": who["unavailable"] or default_unavailable(slug),
    }
    if window is not None:
        snap["window"] = window

    print(json.dumps(snap, indent=2, ensure_ascii=False))
    if not args.print_only:
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(snap, ensure_ascii=False) + "\n")
        print(f"\nappended {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
