# Lightsword nightly routine — 22:00 America/Chicago

**Operations.** Entry = Hermes cron job `Lightsword Nightly (22:00)` in the
profile store `lightsword` (`hermes -p lightsword cron list`). Schedule
`0 22 * * *`, timezone America/Chicago. Working directory = this clone
(`/home/jake/.hermes/lightsword/lightsword`). Delivery = Jake's Discord DM
(`discord:1558054081325695037`), failure notices included (same target).
Scheduler logs = `~/.hermes/profiles/lightsword/cron/output/<job-id>/` plus
`hermes -p lightsword cron runs`. In-repo logs = `logs/nightly.ndjson` (one
line per run) and `reports/nightly/YYYY-MM-DD.md` (the digest).

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
| 0 | 22:00 | Strategist | Pre-flight: tomorrow has a calendar row; non-empty rows need an unexpired brief | pass / `queue/escalations/` | Missing row or brief HALTS phases 3–7 only. Phases 1, 2, 8, 9 still run. |
| 1 | 22:00 | Analyst | Pull site analytics, Search Console, social, email | `metrics/YYYY-MM-DD.json` | No tag/credentials: record `unavailable` + reason. Never fabricate a number. |
| 2 | 22:05 | Distribution | Collect inbound since last run; flambeee client check (public surface only) | `queue/inbound/YYYY-MM-DD.json` | No accounts yet: record an empty set + warning. No sending. |
| 3 | 22:10 | Distribution | Draft replies to inbound | `queue/replies/*` | Max 5 replies; human sends for first 60 days. Nothing inbound = nothing written. |
| 4 | 22:20 | Content Lead | Generate tomorrow's assets from brief + calendar row | `queue/drafts/*` | Max 3 assets, every claim sourced. No brief = no asset. |
| 5 | 22:32 | Content Lead | Mechanical gate: `python3 workflows/gate.py <files>` | pass/fail mark per file | Fail closed. A FAIL blocks staging for that file. Time-boxed 3 min. |
| 6 | 22:35 | Strategist | Adjudicate gate failures: drop, re-brief, or escalate | `queue/escalations/` | Only failures reach here; 5-min budget; >3 failures = a brief problem, say so in the digest. |
| 7 | 22:40 | Distribution | Stage passing assets as social drafts | `queue/social/*.json` | Never publish (phase 1). Postiz absent = WARNING, not failure. |
| 8 | 22:50 | Analyst | Five-line morning digest from run log and snapshots | `reports/nightly/YYYY-MM-DD.md` | A line that says nothing gets deleted. |
| 9 | 22:55 | Strategist | "Needs Jake" list ordered by cost of delay, one line each | same file, appendix | Max 3 items; >3 = the approval gate is misconfigured — escalate that as the item. |
| 10 | 23:00 | Workflow | Hard stop | log line + final response | Unfinished work rolls to tomorrow, loudly. No retry storms. |

Phases 1 and 2 are independent and may run in any order. Everything after
phase 4 is serial. A failed step writes one line to the digest and stops the
chain — no silent continuation on stale data.

## Fail-closed rules (these override convenience)

- **Pre-flight row semantics** (tomorrow's row in `plans/calendar-30d.md`):
  - row exists with `type: empty` → PASS: deliberate blank, skip phases 3–7,
    note it in the digest. Do **not** escalate. Empty days are rows, not gaps.
  - row exists (`source`/`derived`) but no unexpired brief in `queue/briefs/`
    → HALT phases 3–7, write `queue/escalations/<today>-missing-brief.md`.
  - no row at all, or no calendar file → HALT phases 3–7, write
    `queue/escalations/<today>-no-calendar-row.md`. In week 0 a missing
    calendar is expected: escalate once; the Sunday planning job owns rows —
    never invent or rewrite the calendar here.
- **The two-part gate.** Mechanical: `workflows/gate.py` decides pass/fail;
  the Content Lead runs it and may not edit it or waive a result. Adjudicated:
  the Strategist reads only the failures and drops, re-briefs, or escalates.
  The writer never clears its own failure.
- **Scheduler absent (Postiz, etc.)** = one WARNING line in the digest;
  `queue/social/*.json` is still written for hand publishing. Never a failure.
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

2. Write `reports/nightly/YYYY-MM-DD.md`: five digest lines + the needs-Jake
   appendix (open `queue/escalations/*`, pending approvals, tonight's blockers).
3. Final response to the scheduler: max 5 lines, status flags first. It is
   delivered to Jake's Discord — one line per phase, then halt/warning flags,
   then paths written.

## Never

- `git commit`, `git push`, publishing, posting, sending (AGENTS.md rules 1–2).
- Reading flambeee internal files (AGENTS.md rule 4); the client check reads
  only public surfaces: `gh api repos/jakepi-bot/flambeee/releases`, the
  repo's `BLOG.md`/`README.md`, flambeee.com.
- More than 3 assets, 5 replies, or 3 escalations in one night.
- Clearing a gate failure as the Content Lead.
