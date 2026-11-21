# Bluesky client

`workflows/bsky.py` is the only path from this repo to Bluesky. Posts, replies,
threads, deletions, scheduling and mention monitoring all go through it, so
that every action is one command with one audit line.

Status 2026-11-13: **verified end to end on both accounts** — `@lightsword.bsky.social`
and `@flambeee.bsky.social`. The flambeee app password was installed in the
profile `.env` on 2026-11-13; the full selftest, reply path and scheduler were
re-run against the client account (see §6 and §9).

---

## 1. Credentials

Credentials live in the Hermes profile `.env`, which is mode 600:

```
/home/jake/.hermes/profiles/lightsword/.env

LIGHTSWORD_BSKY_HANDLE=lightsword.bsky.social
LIGHTSWORD_BSKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
FLAMBEEE_BSKY_HANDLE=flambeee.bsky.social
FLAMBEEE_BSKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

`--account lt` reads the `LIGHTSWORD_` pair, `--account fb` the `FLAMBEEE_`
pair. Anything missing is a refusal (exit 2) with the exact lines to add.

Rules that the client enforces or assumes:

- **App password, never the account password.** Bluesky: *Settings → Privacy
  and security → App passwords → Add app password*. The client prints a
  warning if the stored string does not have the `xxxx-xxxx-xxxx-xxxx` shape.
- **Never on the command line.** Passwords are read from `.env` only. A
  password in argv is a password in `ps` and in shell history.
- **Never in the repo.** `.env` is outside the clone and gitignored paths are
  not used for credentials at all. Nothing in `logs/` or `published/`
  contains a secret.
- **Sessions are cached**, `/home/jake/.hermes/profiles/lightsword/state/bsky-session-<account>.json`,
  mode 600. `com.atproto.server.createSession` is capped at **10 calls per
  24 h**, so a client that authenticates on every run locks itself out by
  lunchtime. The cache holds the refresh token; the client refreshes when the
  access token is within 3 minutes of expiry, and only calls `createSession`
  when there is no usable refresh token.

Check without posting:

```bash
python3 workflows/bsky.py --account lt probe
python3 workflows/bsky.py --account fb probe     # flambeee credential, installed 2026-11-13
```

## 2. Commands

Global flags anywhere: `--account {lt,fb}` (default `lt`), `--json`,
`--log PATH`, `--env-file PATH`.

| Command | What it does |
|---|---|
| `probe` | credential report + live profile counts |
| `post` | text, optional images with alt text, optional `--quote`, facets, idempotency key |
| `reply --to AT-URI` | reply with correct `root`/`parent` refs |
| `thread --from FILE` | chained posts from a JSON file |
| `delete --uri AT-URI` | delete; `--why` is recorded |
| `get --uri` | public read of one post |
| `replies --uri [--depth]` | conversation under a post |
| `mentions [--unread-only] [--mark-seen]` | mentions/replies/quotes — the monitoring surface |
| `limits [--all]` | local caps and what is left today |
| `arm --asset-id --publish-at` | schedule a gate-passed asset from `queue/social/` |
| `schedule --list / --disarm ID` | inspect or cancel the outbox |
| `tick [--now] [--dry-run]` | publish everything due (cron entry point) |
| `selftest` | post a marked test with image+alt, verify, delete, verify |
| `profile-get` / `profile-set` | read or update bio/avatar/banner, and pin one post (`--pin AT-URI` / `--unpin`) |
| `search` | authenticated post search (`--query`, `--sort latest/top`, `--since`, `--until`, `--author`); the public AppView 403s on `searchPosts`, the authenticated PDS does not |

Every command accepts `--dry-run` where it would otherwise publish; a dry run
prints the exact record it would send and never mutates the outbox.

### Posting

```bash
python3 workflows/bsky.py --account fb post \
  --text-file queue/drafts/fb-bsky-20261113-02.md \
  --image brand/visual/exports/announcement-1200x1200.png \
  --alt "Lightsword announcement card. Heading: ..." \
  --id-key fb-bsky-20261113-02+bsky+2026-11-13 \
  --asset-id fb-bsky-20261113-02
```

- Text limit is **300 graphemes**; over that is a refusal, not a truncation.
- Up to 4 images, each ≤ 1,000,000 bytes, PNG/JPEG/WebP, **alt text required**
  (one `--alt` per `--image`, otherwise refused).
- Links, `@mentions` and `#tags` become richtext facets with UTF-8 byte
  offsets. Mentions are resolved through the public API; an unresolvable
  handle is left as plain text rather than a broken link.
- `--id-key` makes the call idempotent: a second run with the same key returns
  `SKIPPED … already published` with the original URI.
- `--asset-id` appends a line to `published/manifest.ndjson`.
- `--quote AT-URI` publishes a quote post: the record carries
  `app.bsky.embed.record` with a strong ref (`uri` + `cid`) resolved from the
  public AppView at send time. A quote cannot also carry images (that needs
  `embed.recordWithMedia`, not implemented), and a target that is hidden or
  deleted is a refusal, not a silent plain post.

### Replying

```bash
python3 workflows/bsky.py --account fb reply --to at://did:plc:.../app.bsky.feed.post/3k... \
  --text "It runs in the browser — nothing to install."
```

The client resolves the parent's thread root from the public AppView and falls
back to an authenticated repo read when a post we just created is not indexed
yet. A two-level test (`A → B → C`) produced `root=A, parent=B` correctly.

Reply caps are enforced *before* the call (AGENTS.md rule 7): 5 replies per
rolling 24 h, at least 10 minutes apart, at most 2 per thread. A refusal names
the wait in seconds. `--force` overrides and records `forced: true`.

### Monitoring

```bash
python3 workflows/bsky.py --account fb mentions --limit 25
python3 workflows/bsky.py --account fb mentions --unread-only --mark-seen
python3 workflows/bsky.py --account fb replies --uri at://...
```

## 3. Scheduling

Two layers, both in the repo:

**The schedule.** `plans/posting-schedule.json` is the machine-readable cadence
and slot (Lightsword Bluesky: daily, 19:00 America/Chicago; the client channel:
3 staged drafts/week, client posts at 12:05, bot publishes only inside a written
window). The nightly arms the next day's item at that slot; the tick below
publishes it. `python3 workflows/schedule-check.py` verifies the config, the cron
jobs and the next planned row. Rationale: `plans/posting-schedule.md`.

**The outbox** — `queue/outbox/<id>.json`, one item per post:

```json
{
  "id": "fb-bsky-20261113-02",
  "account": "fb",
  "publish_at": "2026-11-13T15:30:00-06:00",
  "text": "...",
  "images": [],
  "alts": [],
  "idempotency_key": "fb-bsky-20261113-02+bsky+2026-11-13",
  "asset_id": "fb-bsky-20261113-02",
  "status": "queued",
  "attempts": 0
}
```

`publish_at` **must** carry a UTC offset; a naive timestamp is refused, because
"12:05" on its own is how a campaign posts at the wrong hour.

`text_fallback` is optional. When the post's text contains a link that may not
be live yet (a blog page), the staged asset carries the brief's no-link copy in
`text_fallback`; `arm` validates it and copies it to the item. The 18:45 link
check swaps it in if the URL is not 200. With no fallback, the check holds the
item instead of publishing a dead link.

**Quote items.** An item may carry `quote` (an AT-URI) or `quote_asset` (the id
of another outbox item). `quote_asset` is resolved at tick time, so a quote can
be armed before its target exists — used by `lt-quote-20261114-01`, which quotes
campaign post #12 at 19:20 after #12 publishes at 19:00. A quote item may not
also carry images. While the target is unpublished the item stays `queued`
without burning attempts (one `WAITING` warning per hour).

**Arming from the existing staging pipeline** — the normal path, so nothing is
hand-copied:

```bash
python3 workflows/bsky.py arm --asset-id fb-bsky-20261113-02 \
        --publish-at 2026-11-13T15:30:00-06:00
python3 workflows/bsky.py schedule --list
python3 workflows/bsky.py schedule --disarm fb-bsky-20261113-02 --why "NO-GO"
```

`arm` refuses an asset whose `gate` is not `pass`, or whose status is
`superseded` / `do_not_publish`.

`arm` reads `queue/social/*.json` only. The 72-hour campaign schedule lives in
`queue/campaign/fb-campaign-2026-11-13.json`; to arm it, either materialize
each post as a `queue/social/` JSON (gate pass, `status: ready-to-publish`,
`media` and `alt_text` as filed) and arm by `asset_id`, or write one outbox
item per post with `schedule --file`, using `slot_utc` as `publish_at` and the
post's `media` / `alt_text` as `images` / `alts`. A thread's `thread[0].text`
is a reply after the root publishes, not a second top-level item.

**The tick** — `workflows/bsky-tick.py`, Hermes cron job `84e5289134f4`,
`*/5 * * * *` America/Chicago, `no_agent` (no LLM, no token cost), `deliver:
local`. Its stdout and stderr are captured; when the tick printed anything it
is echoed to the job's own output file and posted to the operator Discord DM by
`workflows/notify.py --kind outbox-tick` (`docs/discord-delivery.md`). The tick
publishes items whose `publish_at` has passed, then exits. Rules:

| Situation | Behaviour |
|---|---|
| nothing due | silent, exit 0 (no message) |
| due and credentials present | publishes, prints `PUBLISHED … <at-uri>`, exit 0 |
| due, credentials missing | item stays `queued`; one warning per item per hour; exit 0 |
| slot more than 12 h old | item → `expired`, never auto-published, loud warning |
| transient API failure | `retry` with attempts, up to 3, then `failed` |
| quote target not published yet | item stays `queued`, no attempt burned; one `WAITING` warning per hour |
| already published (same id key) | `published-duplicate`, no second post |

A manual `tick` is safe to run at any time: it is idempotent, takes a lockfile
(`logs/.bsky-tick.lock`, stale after 10 minutes), and only touches due items.

**The 18:45 link check** — `workflows/link-check.py`, Hermes cron job
`e180ec9bc2cd`, `45 18 * * *` America/Chicago, `no_agent`, `deliver: local`.
Fifteen minutes before the 19:00 slot it checks every URL in the armed item:

| Situation | Behaviour |
|---|---|
| no non-empty Lightsword row today | one `SKIP` line, exit 0, no message |
| every URL 2xx | one `PASS` line, exit 0, no message |
| dead URL, item has `text_fallback` | item text replaced by the fallback, stays `queued`, DM + audit |
| dead URL, no fallback | item → `held-link-dead` (the tick never publishes it), DM + audit |
| row due today, nothing armed | `NOT ARMED` warning to the DM |

It never edits the calendar, the gate or a draft, and never invents copy. Its
audit trail is `logs/link-check.ndjson`; problems go to Jake's DM through
`workflows/notify.py --kind link-check`. `--now`, `--outbox`, `--dry-run` and
`--no-notify` make it testable without touching the live outbox.

Dry-check a whole day without credentials or side effects:

```bash
python3 workflows/bsky.py tick --now 2026-11-13T12:06:00-06:00 --dry-run
# DRY-RUN fb-bsky-20261113-02 (fb) 2026-11-13T15:30:00-06:00 202 graphemes, 0 image(s) creds=MISSING
```

## 4. Logging

`logs/bsky-actions.ndjson`, one JSON object per line, append-only:

```json
{"v":1,"ts":"2026-11-12T22:19:44Z","account":"lt","action":"post","status":"ok",
 "text":"...","chars":211,"idempotency_key":"...","asset_id":"...",
 "thread_root":null,"reply_to":null,"guard":{"posts_24h":2,"cap":20,"forced":false},
 "images":[{"path":"...","alt":"..."}],"uri":"at://did:.../app.bsky.feed.post/3n...",
 "cid":"bafy...","rkey":"3n...","url":"https://bsky.app/profile/lightsword.bsky.social/post/3n...",
 "http":200,"attempts":1,"duration_ms":812,
 "ratelimit":{"limit":"10","remaining":"9","reset":"...","policy":"10;w=86400"}}
```

`action` is one of `session`, `upload`, `post`, `reply`, `delete`, `profile`,
`tick`, `selftest`. Failures are recorded too (`status: "error"`, plus `http`
and `error`), so a refused call leaves a trace rather than a gap. Deletions log
the URI and the `--why` string. No credential and no token ever reaches a log
line.

Read it:

```bash
python3 - <<'PY'
import json
for line in open("logs/bsky-actions.ndjson"):
    r = json.loads(line)
    if r.get("action") in ("post", "reply"):
        print(r["ts"], r["account"], r["action"], r["status"], r.get("uri"))
PY
```

The log is also the rate-limit ledger: `limits` counts the last 24 h from it.
A deleted test post still counts as a post that day — the cap is on actions,
not on live records, which is the conservative reading.

`published/manifest.ndjson` gets one additional line per post that carries an
`--asset-id`, with the Bluesky URI, so the campaign KPI "12/12 live, URIs in the
manifest" is a file read, not a manual count.

## 5. Limits and failure modes

Platform facts the client is built around:

| Limit | Value | Where it bites |
|---|---|---|
| `createSession` | 10 / 24 h / IP | per-run logins would exhaust it; hence the session cache |
| post text | 300 graphemes | refusal before the call |
| image | 1,000,000 bytes, 4/post | refusal before upload, with the size printed |
| `uploadBlob` | ~5,000 / day | not reached at campaign volume |
| write ops | 5,000 points / day | not reached at campaign volume |

Local caps (tighter on purpose): 5 replies/24 h with a 10-minute gap and 2 per
thread; 20 posts/24 h per account.

Failure handling: 429 and 5xx are retried with exponential backoff (1, 2, 4 s +
jitter, up to 4 attempts), honouring `ratelimit-reset` when the remaining count
is 0. 4xx other than 429 is never retried — it is a bug in the request, and
retrying it just burns the rate limit.

Exit codes: `0` ok · `1` API error · `2` refused (missing credential, cap,
invalid input) · `3` tick completed with warnings. The cron wrapper
(`workflows/bsky-tick.py`) maps `3` to `0`, so a warning arrives as a delivered
message rather than as a job failure.

AppView lag: a post just created may not appear in `app.bsky.feed.getPosts` or
`getPostThread` for seconds to a minute. The client treats the authenticated
repo read as authoritative and the public read-back as evidence that can lag.

## 6. Verification record

### 2026-11-12 — `@lightsword.bsky.social`

Run against `@lightsword.bsky.social` (the only account with a credential at the time):

| Check | Result |
|---|---|
| `selftest` — session, post+image+alt, repo read-back, public read-back, reply fetch, mentions fetch, delete | **PASS 7/7**, text and alt matched on read-back, record gone after delete |
| reply to a fresh post (repo fallback for AppView lag) | PASS, `root`/`parent` correct on a 2-level chain |
| reply spacing guard (10 min) | REFUSED at 1 s: "last reply 1s ago, minimum 600s. Wait 599s." |
| thread guard (2 per thread) | enforced (same code path) |
| scheduler: item armed 75 s ahead | nothing at first tick; `PUBLISHED` at the next tick, 6 s after its slot |
| scheduler: 13 h old slot | marked `expired`, not published |
| scheduler: `fb` item, no credential | stays `queued`, one warning per hour |
| cron wiring | job `84e5289134f4` created and fired once |
| credentials | `.env` mode 600, app-password shape, no secret in any log line |
| unit tests — `python3 workflows/test_bsky.py` | **16/16 pass** (caps, spacing, per-thread, force, window, graphemes, naive timestamps, UTF-8 facet offsets, credential refusal) |

Every test post above was deleted in the same run; the deletion URI is in the
audit log. No test artifact is live.

### 2026-11-13 — `@flambeee.bsky.social` (client account)

Run after the owner installed `FLAMBEEE_BSKY_APP_PASSWORD` in the profile
`.env` (mode 600):

| Check | Result |
|---|---|
| `probe` | session OK via cached token, `did:plc:znmfziotsbcrkkec6ootjmzf`, 4 followers / 44 posts |
| `selftest` with image + alt | **PASS 7/7**; text and alt matched on the authenticated and public read-back; post deleted; public read of the URI returns NOT FOUND |
| reply path | `post` → `reply` → `replies`: one reply under the root with correct `root`/`parent`; both records deleted |
| scheduler | test item armed for `2026-11-13T06:02:00-06:00`; the live cron tick published it at `2026-11-13T12:05:29Z` (06:05:29 CT), URI logged, post deleted |
| mentions fetch | `listNotifications` ok; 2 historical notifications visible |
| credentials | `.env` mode 600, session cache mode 600, 0 repo files contain the app password |
| unit tests | `python3 workflows/test_bsky.py` — 16/16 pass |

Test records (all deleted; URIs retained for audit):

- `at://did:plc:znmfziotsbcrkkec6ootjmzf/app.bsky.feed.post/3n26woqyzyo26` — selftest, image + alt
- `at://did:plc:znmfziotsbcrkkec6ootjmzf/app.bsky.feed.post/3n26wzcsubo2e` — scheduler
- `at://did:plc:znmfziotsbcrkkec6ootjmzf/app.bsky.feed.post/3n26x2foefl2j` — reply root
- `at://did:plc:znmfziotsbcrkkec6ootjmzf/app.bsky.feed.post/3n26x2jcaai26` — reply

The three test posts count against the local 20/24 h post cap and the one test
reply against the 5/24 h reply cap; `limits` is the ledger, so the campaign
starts with that usage already recorded.

## 7. Isolation

The client is Lightsword's own code, written against the public AT Protocol
spec. It does not read, import, or copy the flambeee team's scripts, prompts,
workflows, or assets (AGENTS.md rule 4, hard rule 1.4). The `fb` credential, when
it exists, is a credential issued for this scope — revoke it at exit
(scope §11).

## 8. Not implemented, on purpose

- **Follows.** Rule 8 caps them and the campaign plans read-first follows; a
  follow command without a read-and-record step invites a spree. If the
  campaign needs it, it should be a separate reviewed addition, not a flag here.
- **DMs / chat.** Out of scope; Bluesky chat is a separate API surface.
- **Threads longer than one file.** `--from` takes an explicit list; there is
  no auto-threading of long text, because splitting is an editorial decision.

## 9. flambeee: credential installed 2026-11-13

`@flambeee.bsky.social` exists (`did:plc:znmfziotsbcrkkec6ootjmzf`). On
2026-11-13 the owner issued an app password named `lightsword-campaign` and it
was installed in `/home/jake/.hermes/profiles/lightsword/.env` (mode 600):

```
FLAMBEEE_BSKY_HANDLE=flambeee.bsky.social
FLAMBEEE_BSKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

`python3 workflows/bsky.py --account fb probe` now returns a live session, and
the §6 2026-11-13 record is the end-to-end verification (selftest with image +
alt, reply path, scheduler fire, delete, logging).

Reproduce:

```bash
python3 workflows/bsky.py --account fb probe
python3 workflows/bsky.py --account fb selftest \
  --image brand/flambeee-assets/exports/flambeee-ad-claim-1080x1080.png \
  --alt "INTERNAL TEST image: flambeee ad card, white and coral type on navy reading no installs, no accounts, no ads."
```

The credential is scoped to the campaign window in `plans/scope-flambeee.md`
§13. Revoke it at exit (§11 of that scope), and never store the account's main
password. If the app password is rotated or revoked, `fb` commands refuse with
exit 2 and print the two lines to add; they never fall back to another account.

## 10. Campaign helpers (72-hour flambeee campaign, 2026-11-13)

Two read-mostly helpers sit beside the client; neither is imported by it.

- `workflows/campaign-metrics.py --label <label>` — read-only snapshot of the
  12 campaign posts (likes, reposts, replies, quotes, stranger replies), the
  profile follower count, and our replies sent inside the window. Writes
  `metrics/campaign/<label>.json`. Impressions, profile visits, site clicks,
  signups and play counts are emitted as `unavailable` with the reason.
- `workflows/campaign-thread-reply.py` — posts campaign post #08's second half
  as a reply to the published root, resolved from the outbox or the manifest.
  Idempotent: it refuses to send twice for the same root.

The campaign schedule is `queue/campaign/fb-campaign-2026-11-13.json`; the
operating runbook is `reports/campaign/RUNBOOK.md`.
