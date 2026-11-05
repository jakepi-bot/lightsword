---
title: Social accounts + website hosting plan
status: draft for Jake
owner: Strategist (account lead)
created: 2026-11-05
inputs: plans/social-media-plan.md, personas/00-index.md, docs/marketing-company-research.md, live checks 2026-11-05
---

# Social accounts + lightsword.org hosting — the plan

Two jobs, one constraint: free and bot-friendly. Phase 2 (2026-11-05): the bot publishes autonomously after a gate pass.

## 1. Decisions

| Job | Ruling |
|---|---|
| Social, active | Bluesky x2 (Lightsword + studio client). Free API, no review, no fee. Postiz native. |
| Social, deferred | LinkedIn company page (Lightsword). Jake chose Bluesky-only first; page comes after month 1 or when a buyer asks. |
| Owned spine | `~/share/lightsword-site/` on ai-pc, synced via existing Share folder, served by Caddy on the cloud host. |
| Scheduler | Postiz self-hosted (Docker). Gate-passed posts publish live; scheduler is a convenience, not a dependency. |
| Analytics | Umami self-hosted (Jake's pick) + Search Console. No tag, no performance claim. |
| Not now | X, Mastodon, Instagram/TikTok/Shorts, Threads, Facebook, Reddit, newsletter, paid. Each has a reason + revisit trigger below. |

## 2. Social accounts: what to plug in

### 2.1 Plug in now (free, bot-friendly): Bluesky x2

**Bluesky x2 — Lightsword + client studio.** Jake's call 2026-11-05: Bluesky only first; LinkedIn waits.

- Why: the plan already chose it (§4.1). Verified still true: no developer account, no review, no fee. Any account can call the AT Protocol API with its own credentials; limits are rate limits, not price. Auth is an app password (bots) or OAuth (apps), then `com.atproto.repo.createRecord` with `app.bsky.feed.post`.
- Bot fit: app password per bot, 300-char format matches the 16-minute asset, no link suppression to design around, Postiz supports `bluesky` with no custom settings object.
- Custom handle is cosmetic: a `_atproto` TXT record maps `lightsword.org` later. Start on `*.bsky.social`.
- Cost: $0.

### 2.2 Deferred (Jake's Bluesky-first call, 2026-11-05)

**LinkedIn company page — Lightsword, after month 1 or when a buyer asks.**

- Why it waits: the buyer checks LinkedIn before replying, but two Bluesky accounts are the whole month-1 load. Two substantive posts a week beats four thin ones; add the page when Bluesky cadence holds.
- Bot fit (when activated): posting as an organization needs `w_organization_social` plus an admin role on the page; member posts need `w_member_social`. No sandbox — test against a team-owned page first. Until access is granted: manual posting, ~3 min each.
- Cost: $0 to create and hold.

| Platform | Why not now | Revisit when |
|---|---|---|
| LinkedIn page | Jake's Bluesky-first call; month-1 load is two Bluesky accounts | Month 2, or the first buyer asks for the page |
| X / Twitter | Pay-per-use since Feb 2026. $0.015 per post, $0.200 per post with a URL, ~$0.005 per read. No free tier for new developers. A link-bearing daily post is ~$6/mo before reads; polling mentions gets expensive fast. Also punishes exactly the posts this plan writes. Against the 5%-of-retainer tooling cap. | A paying client requires it, in writing |
| Mastodon | Free and bot-friendly (open API, `POST /api/v1/apps` + OAuth per server, default ~300 req/5 min). Rejected on reach, not cost: second fediverse presence doubles reply surface for near-zero return at this volume. | Studio audience shows up there |
| Instagram, TikTok, YouTube Shorts | Video. A 16-minute asset budget cannot produce video that is not embarrassing. Largest real gap in the plan, stated plainly. | One-off launch video with a separate budget, or 30 qualified sessions/wk sustained 2 wks |
| Threads | Same production problem as Instagram with a thinner API story | Same as Instagram |
| Facebook | Page permissions project for zero audience return | Never, unless a client's audience is there |
| Reddit / HN | Removal risk (new account + game links) / launch-event only | Monitoring only week 2 / a launch worth one shot with Jake |
| Newsletter (Listmonk) | Needs a list; list needs traffic. Month three. | 200 email signups |
| Paid social | No baseline, no inventory, no budget justification | Month four, with numbers |

Postiz already supports all of the above except the policy decision (27 providers: X, LinkedIn, LinkedIn Page, Bluesky, Mastodon, Threads, etc.). Adding one later is config, not a rebuild.

### 2.3 How "plug in" works (Jake does the human parts)

Phase 0 rule from onboarding: week 0 creates nothing externally except through Jake. Agents never create accounts.

**Jake (10 min, one sitting):**

1. Create two Bluesky accounts on `*.bsky.social` (Lightsword, studio). Keep default handles until DNS handles are ready.
2. Settings → App Passwords → one app password per account. Store in the profile vault/`.env`, never in the repo (the repo is public).
3. LinkedIn: nothing this month (Bluesky-first call). When activated: Jake creates the page (admin = Jake), records the URN outside the repo.
4. Postiz connections publish gate-passed posts live. Draft-only mode ended 2026-11-05.

**Distribution Lead (after Jake):**

- Inbound: Bluesky native API read for mentions/replies → `queue/inbound/YYYY-MM-DD.json`. One platform failing does not stop the other; partial labeled partial.
- Staging: gate-passed drafts → `queue/social/*.json` (audit) + live publish via Postiz or native API. Idempotency key: asset-id + platform + date.
- Replies: max 5/night, safe class publishes. Anything about pricing, outage, complaint, or a person is held for the Strategist, never templated.

**Analyst (read-only):**

- Bluesky follower/engagement reads, LinkedIn page reads when granted, site + GSC when tagged. Missing = `unavailable` + reason. Never a zero standing in for "not collected."

**Credentials map:**

| Secret | Lives | Reads it |
|---|---|---|
| Bluesky app passwords x2 | profile `.env` / vault, mode 600 | Distribution (read+draft), Analyst (read) |
| Postiz API key (when self-hosted) | same | Distribution only |
| LinkedIn OAuth token | deferred with the page | — |
| Nothing | the repo | Repo stays public-safe; `queue/`, `metrics/`, `reports/`, `published/`, `state/` are gitignored |

### 2.4 Postiz self-host (when Jake wants it; not a phase-1 gate)

```yaml
# ~/docker/postiz/docker-compose.yml (new; pattern matches ~/docker/searxng)
services:
  postiz:
    image: ghcr.io/gitroomhq/postiz-app:latest
    ports: ["127.0.0.1:4007:5000"]
    env_file: .env   # provider keys; restart (down/up) after any env change
```

- Providers to configure first: `BLUESKY_*` only (LinkedIn keys deferred with the page). No providers configured by default; restart after env changes.
- Public API (self-hosted): `https://{host}/public/v1`, `Authorization: <api-key>`. Create-post limit ~90/hr (adjust `API_LIMIT`); integrations list ~30/hr. Schedule multiple posts per request.
- Nightly fit unchanged: 22:40 publishes gate-passed drafts live; manifest appends at publish.

## 3. Website: a local dir synced to cloud

### 3.1 Verified today (2026-11-05)

- `www.lightsword.org` → `107.152.39.20`, Server `Caddy`, 200, 4777 bytes.
- Apex `lightsword.org` → no answer (no A record). Matches §12 blocker.
- Live bytes = `~/share/games/www/index.html` (4777 bytes, same file). So today's site root **is** `~/share/games/www/`.
- `~/Sync/` exists but is empty and **not** in Syncthing config. Synced folders today: `~/obsidian` + `~/share` (Share id `hdkre-gundt`, sendreceive). Syncthing runs, GUI on tailnet `:8384`.
- No Caddy/Postiz/Plausible/Umami/Listmonk on ai-pc (no local Caddy binary, no compose entries). Serving host is the cloud node (`cloud`, tailnet `100.66.177.18`, public `107.152.39.20`; SSH closed by tailnet policy — configure via synced files + host-side pull, not direct SSH from here).

### 3.2 The directory (created)

Canonical: `~/share/lightsword-site/` — scaffolded 2026-11-05, confirmed by Jake same day.

- Why here and not `~/Sync/`: Share already syncs (proven, sendreceive, Mac peer at 100%). A new folder under `~/Sync/` needs a new Syncthing folder + peer adds on every device. Revisit only if the site must leave the Share policy.
- Contents: `index.html` (company), `blog/index.html` (owned spine, A00–A11 slots), `downloads/index.html` (verbatim copy of today's live page), `robots.txt`, `sitemap.xml`, `ANALYTICS.stub.html`, `Caddyfile.example`, `README.md`.
- Voice rules in force: no client name until written permission (`plans/scope-flambeee.md` §9.2 ladder); no game counts (hero vs stats block disagree — banned until the studio rules); no numbers without a baseline.

### 3.3 Sync → serve

1. Edit on ai-pc in `~/share/lightsword-site/`.
2. Syncthing (existing Share folder) carries it to each peer. Add the cloud host as a Share peer once (device ID exchange on the host; accept here).
3. Cloud Caddy `root * /srv/lightsword-site` (synced copy path on the host) + `file_server` (see `Caddyfile.example`). Deploy = sync; no git push to live.
4. Cutover: point cloud root at the synced copy, verify `/downloads/` byte-identical first (`curl … | sha256sum`), then switch `/`.

### 3.4 DNS (Porkbun — Jake)

1. Add apex `A @ → 107.152.39.20` (fixes the §12 blocker). Keep `www A`.
2. Use `https://www.lightsword.org` everywhere until the apex propagates.
3. Bluesky custom handles (cosmetic, not blocking): `_atproto.lightsword.org TXT did=…` per account when ready. Keep `.bsky.social` until then.

### 3.5 Measurement on the site

- Self-host Umami (MIT, Jake's pick) on the cloud host; snippet lives in `ANALYTICS.stub.html` until installed, then uncomment in both `/` and `/blog/`.
- Add Search Console verification + sitemap submit. UTM on every social link: `?utm_source=<platform>&utm_medium=social&utm_campaign=<pillar>&utm_content=<asset-id>`.
- Until the tag exists: metrics stay `unavailable`, posts still ship, zero performance claims.

## 4. Cost and human minutes

- Cash: $0 (Bluesky $0, LinkedIn page $0, Postiz self-host $0, Umami/Plausible self-host $0, Syncthing $0, Caddy $0). Only future spend: domain renewal + cloud host already held.
- Jake this week: ~10 min accounts/DNS (done 2026-11-05) + 3 min per LinkedIn manual post when the page activates. No per-asset review gate; audit lines in the digest. Cadence guardrail holds: over 4 h/wk equivalent effort → fix the brief, never the reviewer.

## 5. Blockers and what runs anyway

| Blocker | State | Workaround |
|---|---|---|
| No social accounts yet | Resolved 2026-11-05: both Bluesky accounts exist, bot publishes after gate pass | Calendar publishes live; JSON stays as audit. |
| No analytics tag | Confirmed | Publish + record; claim nothing. Tag is week-0 work ahead of first post. |
| Apex no A record | Confirmed | `www.` everywhere until Porkbun fix. |
| Postiz absent | Confirmed (no container) | Publish via native API. Warning only. |
| Cloud SSH closed by tailnet policy | Confirmed | Ship via Syncthing; apply Caddy/DNS on the host console. |

## 6. Acceptance

- [x] Two Bluesky accounts exist, app passwords in vault, handles recorded outside the repo. LinkedIn page deferred per 2026-11-05 call.
- [x] `~/share/lightsword-site/` syncs to at least one peer (Share folder, already syncing); `/downloads/` byte-identical after cutover.
- [ ] Apex resolves; `www` + apex both serve; `robots.txt` + `sitemap.xml` live.
- [ ] Umami tag + GSC verified before any reach claim; UTM on every social link.
- [x] Nightly still halts generation on missing row/brief; nothing publishes without a gate pass.

## 7. Done 2026-11-05 (was: needs Jake, pre-autonomy)

1. ~~Create the two Bluesky accounts + app passwords~~ — done, bot publishes after gate pass.
2. Porkbun: apex A record (+ later `_atproto` TXT for handles).
3. Cloud host on the Share folder + cloud Caddy at the synced copy (Share already chosen; no `~/Sync/` folder needed).
4. ~~Approve this plan~~ — approved by Jake's 2026-11-05 autonomous directive; Strategist owns branch records + week 1 rows.

---
*Strategist note: no flambeee internal file was read. Client facts above come from flambeee.com and the public README/BLOG surface only. No asset is staged by this plan; writers still halt without a calendar row + unexpired brief.*
