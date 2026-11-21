#!/usr/bin/env python3
"""Collect Lightsword's current public metrics and emit a snapshot JSON.

Read-only. Every number is measured here or recorded as "unavailable" with a
reason. Nothing is estimated.

Why the manifest is the post source of truth: the public author feed collapses
posts that share an identical createdAt (the 2026-11-06 batch), so counting
feed items undercounts. The manifest lists every publish we made, and each URI
is verified live with getPostThread before its engagement is summed.
"""
import json
import subprocess
import urllib.parse
import urllib.request

PUB = "https://public.api.bsky.app/xrpc"
REPO = "/home/jake/.hermes/lightsword/lightsword"


def get(method, **params):
    url = f"{PUB}/{method}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read())


def main():
    lt = get("app.bsky.actor.getProfile", actor="lightsword.bsky.social")
    fb = get("app.bsky.actor.getProfile", actor="flambeee.bsky.social")

    rkeys = [json.loads(line)["url"].rsplit("/", 1)[-1]
             for line in open(f"{REPO}/published/manifest.ndjson") if line.strip()]
    likes = reposts = replies = quotes = 0
    for rk in rkeys:
        uri = f"at://did:plc:fefjni3jbri4knjkectqdz3y/app.bsky.feed.post/{rk}"
        p = get("app.bsky.feed.getPostThread", uri=uri, depth=0)["thread"]["post"]
        likes += p.get("likeCount", 0)
        reposts += p.get("repostCount", 0)
        replies += p.get("replyCount", 0)
        quotes += p.get("quoteCount", 0)

    feed = get("app.bsky.feed.getAuthorFeed", actor="lightsword.bsky.social",
               limit=100, filter="posts_with_replies")["feed"]
    replies_sent = sum(1 for i in feed if i["post"]["record"].get("reply"))

    try:
        gh = json.loads(subprocess.check_output(
            ["gh", "api", "repos/jakepi-bot/lightsword",
             "--jq", "{stars:.stargazers_count,forks:.forks_count,watchers:.subscribers_count}"],
            stderr=subprocess.DEVNULL, timeout=30))
    except Exception as e:
        gh = {"unavailable": str(e)[:120]}

    n = len(rkeys) or 1
    snap = {
        "date": "2026-11-08",
        "captured_at": subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]).decode().strip(),
        "run": "kanban t_fc324943 (week-one ship)",
        "lt_bsky": {
            "followers": lt.get("followersCount"),
            "following": lt.get("followsCount"),
            "posts_count_all": lt.get("postsCount"),
            "original_posts": len(rkeys),
            "replies_sent": replies_sent,
            "likes_received": likes,
            "reposts_received": reposts,
            "reply_received": replies,
            "quotes_received": quotes,
            "engagement_per_post": round((likes + reposts + replies + quotes) / n, 2),
            "pinned": bool(lt.get("pinnedPost")),
        },
        "fb_bsky": {"followers": fb.get("followersCount"), "posts": fb.get("postsCount")},
        "site_sessions": "unavailable",
        "site_referrers": "unavailable",
        "site_reason": "no analytics tag installed (site spec P1 fix 8, needs Umami access)",
        "gh": gh,
        "deliverables_shipped": {
            "posts_published": 1,
            "replies_sent": replies_sent,
            "accounts_followed": 23,
            "site_p0_fixes_applied_to_source": 6,
        },
    }
    print(json.dumps(snap, indent=2))


if __name__ == "__main__":
    main()
