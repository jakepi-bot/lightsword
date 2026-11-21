# Lightsword nightly routine — 22:00 America/Chicago

**Operations.** Entry = Hermes cron job `Lightsword Nightly (22:00)` in the
profile store `lightsword` (`hermes -p lightsword cron list`). Schedule
`0 22 * * *`, timezone America/Chicago. Working directory = this clone
(`/home/jake/.hermes/lightsword/lightsword`). Delivery = Jake's Discord DM,
posted by `workflows/notify.py` (the gateway's own cron delivery for this
profile is `local`: the shared Discord route is held by another profile — see
`docs/discord-delivery.md`). Failure notices go to the same DM: the 22:10
fallback job sends the digest if this run did not, and a failure notice when no
digest exists.
Scheduler logs = `~/.hermes/profiles/lightsword/cron/output/<job-id>/` plus
`hermes -p lightsword cron runs`. In-repo logs = `logs/nightly.ndjson` (one
line per run), `reports/nightly/YYYY-MM-DD.md` (the digest) and
`reports/nightly/YYYY-MM-DD.digest.txt` (the five lines that go to Discord).

The job prompt says: read this file and execute it. This file is the spec;
`personas/00-index.md` §5 carries the same table with the role rationale.

**Deviation, stated once.** The roster's pre-flight row says 21:55; the job
fires at 22:00 (one nightly job, per `personas/00-index.md` §3), so the
pre-flight is phase 0 at the top of the run. The gate's purpose — halt
generation before anything is invented — is unchanged, and the Sunday 20:00
planning job lands the calendar rows and briefs well before it.

## Phases (wall clock, hard stop 23:00)

| # | Time | Role | Step | Output | Failure behavior |
|---|------|------|------|--------|------------------|
| 0 | 22:00 | Strategist | Pre-flight: tomorrow has calendar rows; every non-empty row needs an unexpired brief; `python3 workflows/schedule-check.py` must pass (config loads, nightly/tick/weekly jobs enabled) | pass / `queue/escalations/` | Missing row or brief HALTS phases 3–7 only. Phases 1, 2, 8, 9 still run. A schedule-check error (missing/disabled cron job) also HALTS phases 3–7. Warnings (future row not written yet, closed client window) are recorded, not fatal. |
| 1 | 22:00 | Analyst | Pull site analytics, Search Console, social, email | `metrics/YYYY-MM-DD.json` | No tag/credentials: record `unavailable` + reason. Never fabricate a number. |
| 2 | 22:05 | Distribution | Collect inbound since last run; flambeee client check (public surface only) | `queue/inbound/YYYY-MM-DD.json` | No accounts yet: record an empty set + warning. No sending. |
| 3 | 22:10 | Distribution | Publish safe-class replies; hold position/risk replies for Strategist decision | `queue/replies/*` | Max 5 replies. Safe class (thanks, doc links, hours) publishes; pricing/outage/complaint/person held, never templated. Nothing needing a position goes out undecided. |
| 4 | 22:20 | Content Lead | Generate tomorrow's assets from brief + calendar row | `queue/drafts/*` | Max 3 assets, every claim sourced. No brief = no asset. When the cap binds, the daily Lightsword post ships first; a Friday flambeee batch may roll to Saturday's run and still stage before the client's Monday 12:05 slot. |
| 5 | 22:32 | Content Lead | Mechanical gate: `python3 workflows/gate.py <files>` | pass/fail mark per file | Fail closed. A FAIL blocks staging for that file. Time-boxed 3 min. |
| 6 | 22:35 | Strategist | Adjudicate gate failures: drop, re-brief, or decide-and-log | `queue/escalations/` | Only failures reach here; 5-min budget; >3 failures = a brief problem, say so in the digest. Decisions are recorded with reasons; nothing waits on a human. |
| 7 | 22:40 | Distribution | Publish passing social assets live; write passing blog rows to the site dir; append manifest. A link post's staged asset carries the brief's `text_fallback` (the no-link CTA) so the 18:45 check can swap without new copy | `queue/social/*.json`, `~/share/lightsword-site/blog/`, `published/manifest.ndjson` | Postiz/scheduler or native API. Every publish appends the manifest with asset-id, platform, url, timestamp. **Lightsword Bluesky is armed, not posted early:** `python3 workflows/bsky.py arm --asset-id <id> --publish-at <date>T19:00:00-06:00` (the slot from `plans/posting-schedule.json`); the 5-minute tick publishes at 19:00. Postiz absent = publish via native API + WARNING, not failure. A blog row is a site page, never a Bluesky post. |
| 8 | 22:50 | Analyst | Five-line morning digest from run log and snapshots; on Fridays also the weekly report | `reports/nightly/YYYY-MM-DD.md`; `reports/nightly/YYYY-MM-DD.digest.txt`; `reports/weekly/YYYY-MM-DD.md` | A line that says nothing gets deleted. Weekly report: six numbers, one paragraph, one decision, every value traced to a file; `unavailable` stays `unavailable`. |
| 8b | 22:52 | Distribution | Deliver the digest: `python3 workflows/notify.py --digest-today --kind nightly` | `logs/notify.ndjson` | The script posts `reports/nightly/<today>.digest.txt` to Jake's Discord DM. ERROR = one warning line in the run's NDJSON and in the digest; one retry, never more. The 22:10 fallback job covers a miss. |
| 9 | 22:55 | Strategist | "Decisions taken" list ordered by cost of delay, one line each | same file, appendix | Max 3 items; decisions logged with reasons, policy questions noted for Jake's weekly review. |
| 10 | 23:00 | Workflow | Hard stop | log line + final response | Unfinished work rolls to tomorrow, loudly. No retry storms. |

Phases 1 and 2 are independent and may run in any order. Everything after
phase 4 is serial. A failed step writes one line to the digest and stops the
chain — no silent continuation on stale data.

## Fail-closed rules (these override convenience)

- **Pre-flight row semantics** (all rows for tomorrow in `plans/calendar-30d.md`):
  - every row is `type: empty` → PASS: deliberate blank, skip phases 3–7,
    note it in the digest. Do **not** escalate. Empty days are rows, not gaps.
  - one or more `source`/`derived` rows and every one has an unexpired brief in
    `queue/briefs/` → PASS.
  - any `source`/`derived` row without an unexpired brief → HALT phases 3–7,
    write `queue/escalations/<today>-missing-brief.md` naming the row(s).
  - no row at all, or no calendar file → HALT phases 3–7, write
    `queue/escalations/<today>-no-calendar-row.md`. In week 0 a missing
    calendar is expected: escalate once; the Sunday planning job owns rows —
    never invent or rewrite the calendar here.
- **Blog rows are site pages, not social posts.** A `channel: LT blog` row is
  written after a gate pass to
  `~/share/lightsword-site/blog/<date>-<slug>.html`, linked from
  `blog/index.html`, and added to `sitemap.xml`. It is never posted to Bluesky
  as the article. A social post that links to it may publish only after the
  live URL returns 200. The `Lightsword blog link check` job (`45 18 * * *`,
  `workflows/link-check.py`) runs at 18:45 for the 19:00 slot: it checks every
  URL in the armed item, swaps in the item's `text_fallback` when the brief
  staged one, and otherwise marks the item `held-link-dead` so the tick does
  not publish a dead link. Both outcomes go to Jake's DM and
  `logs/link-check.ndjson`. Never claim a page is live when it is not.
- **The two-part gate.** Mechanical: `workflows/gate.py` decides pass/fail;
  the Content Lead runs it and may not edit it or waive a result. Adjudicated:
  the Strategist reads only the failures and drops, re-briefs, or
  decides-and-logs with a reason. Nothing waits on a human. The writer never
  clears its own failure.
- **Client rows stage, then publish only inside a written window.** A
  `client: fb` row (calendar channel `FB Bluesky (staged)`) is still written to
  `queue/social/*.json` with `status: staged-awaiting-owner` by the nightly; the
  nightly itself does not publish client rows. The last written window was
  `plans/scope-flambeee.md` §14, 2026-11-16 07:10 → 2026-11-19 07:10 CT; it is
  closed and "draft-only resumes unless extended in writing." Outside an open
  window the credential does not authorize a publish, and `check_window` in
  `workflows/bsky.py` refuses it. A `status: superseded` or `do_not_publish`
  asset is never armed or handed over.
- **Scheduler.** As of 2026-11-12 there is one: `workflows/bsky.py arm` writes
  a gate-passed asset to `queue/outbox/` at its calendar slot, and the
  `Lightsword Bluesky outbox tick` cron job (`*/5 * * * *`, script only) posts
  it at that time with an audit line in `logs/bsky-actions.ndjson`. The
  Lightsword slot is **19:00 America/Chicago**, read from
  `plans/posting-schedule.json`; the nightly arms for the next day's 19:00 and
  never posts early to "fill" the slot. Prefer arming over publishing early, so
  `slot` is honoured. If `arm` fails or the slot has already passed, publish
  immediately through `workflows/bsky.py post` as before and record one WARNING
  line. `docs/bluesky-client.md` is the reference.
- **No credentials / no data** (analytics tag, social accounts, Search
  Console) = record `unavailable` with the reason + a warning line. Never a
  failure, never an invented number.
- **Idempotency.** Every artifact keys on asset-id + platform + date. Check
  before writing; re-running a night updates in place — no duplicate draft,
  reply, staged post, escalation, or log line for the same date/key.
- **Hard stop 23:00.** Cut assets, never the gate. No in-run retries.
- **Dates come from `date`**, never inferred. America/Chicago.

## Logging contract (every run, no exceptions)

1. Append exactly ONE line to `logs/nightly.ndjson` (append, never rewrite):

   ```json
   {"ts":"<ISO-8601>","date":"YYYY-MM-DD","run":"nightly","halted":false,"phases":{"preflight":"pass","metrics":"ok","inbound":"ok","replies":"0","generation":"0","gate":"pass","staging":"0"},"warnings":[],"drafts":0,"gate_pass":0,"gate_fail":0,"staged":0,"escalations":0}
   ```

2. Write `reports/nightly/YYYY-MM-DD.md`: five digest lines + the decisions-taken
   appendix (open `queue/escalations/*`, tonight's decisions with reasons, policy
   questions for Jake's weekly review).
3. Write the same five digest lines, plain text and nothing else, to
   `reports/nightly/YYYY-MM-DD.digest.txt`, then run
   `python3 workflows/notify.py --digest-today --kind nightly`. That script is
   the delivery path to Jake's Discord DM; its outcome lands in
   `logs/notify.ndjson`.
4. Final response to the scheduler: max 5 lines, status flags first. The same
   lines are the digest Jake receives — one line per phase, then halt/warning
   flags, then paths written.

## Never

- `git commit`, `git push`, publishing without a gate pass (AGENTS.md rules 1–2).
- Reading flambeee internal files (AGENTS.md rule 4); the client check reads
  only public surfaces: `gh api repos/jakepi-bot/flambeee/releases`, the
  repo's `BLOG.md`/`README.md`, flambeee.com.
- More than 3 assets, 5 replies, or 3 escalations in one night.
- Clearing a gate failure as the Content Lead.
