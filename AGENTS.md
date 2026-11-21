# AGENTS.md — Lightsword repo standing rules

This clone is the working directory for scheduled workflows run by the Hermes
profile `lightsword` (see below). Every agent working here obeys these rules;
they also load automatically into any cron run with this directory as cwd.

## Hard rules

1. **Phase 2 is autonomous (Jake directive 2026-11-05). Publish, post, and send
   through approved surfaces after a gate pass plus Strategist adjudication of
   any failure.** Staged JSON in `queue/social/` is still written for every
   asset, as the audit trail. Replies in the safe class go out; replies needing
   a position go to the Strategist, who decides and logs it.
2. **Scheduled runs never `git commit` and never `git push`.** `git pull
   --ff-only origin main` at the start of a run is allowed (how merged plans
   arrive). Humans and review tasks push.
3. **The repo is PUBLIC.** Client and runtime artifacts stay out of git:
   `queue/`, `metrics/`, `reports/`, `published/`, `state/`, `assets/images/`
   and `logs/` are gitignored. Never force-add them.
4. **Hard rule 1.4: no Flambeee persona file, prompt, workflow, cron, database,
   or asset is read, reused, or copied into this repo.** flambeee is client one,
   not shared infrastructure. Reading flambeee's PUBLIC writing (BLOG.md, README,
   releases, flambeee.com) as a client is allowed; internal team files are not.
5. **Unknown beats invented.** No unsourced number, no inferred product feature,
   no named client without permission. A blank line is cheaper than a retraction.
6. **Never speak as Jake.** No persona sends client email as Jake or approves
   its own work. Publishing runs under the bot's own authority per the
   2026-11-05 directive; naming the client still needs the written permission
   in `plans/scope-flambeee.md`.
7. **Reply rate is capped (operator directive 2026-11-08).** No more than
   **5 replies in any 24-hour window**, at least **10 minutes apart**, and
   never more than 2 in the same thread. A burst of replies — even good ones —
   is what the platform scores as spam and what a reader sees as a bot
   working through a list. When the cap is reached the block ends; the rest
   rolls to tomorrow, loudly. The 10-replies-in-24-hours line in growth plan
   §8 was written before this cap existed and is superseded by it.
8. **No automated following sprees.** Follows stay under 20 per day and only
   accounts whose post we actually read in that session.
9. **One posting path.** Every Bluesky action goes through
   `workflows/bsky.py`; no ad-hoc createSession/createRecord scripts. It
   enforces rule 7 in code, logs every action with its URI to
   `logs/bsky-actions.ndjson`, caches sessions (`createSession` is capped at
   10 calls/day), and refuses rather than guessing. `@flambeee` posts only
   while the `plans/scope-flambeee.md` §13 window is open and only with
   `FLAMBEEE_BSKY_APP_PASSWORD` in the profile `.env`. A main account password
   is never stored, never passed on the command line, and never logged.


## Scheduled workflows

| Job | Schedule (America/Chicago) | Spec |
|---|---|---|
| Lightsword Nightly (22:00) | daily `0 22 * * *` | `workflows/nightly-2200.md` |
| Lightsword Weekly Planning (Sun 20:00) | Sunday `0 20 * * 0` | `workflows/weekly-plan-sunday.md` |
| Lightsword Bluesky outbox tick | every 5 minutes `*/5 * * * *` | `workflows/bsky-tick.py` (script only, no LLM) |

Both run under the Hermes profile `lightsword`, cwd = this clone. Scheduler
transcripts: `~/.hermes/profiles/lightsword/cron/output/<job-id>/` and
`hermes -p lightsword cron runs`. In-repo log: `logs/nightly.ndjson` (one line
per run) plus `reports/nightly/YYYY-MM-DD.md` (the digest).

The outbox tick is a `no_agent` job: it publishes due items from
`queue/outbox/`, prints nothing when the queue is empty or not yet due, and
delivers only real events (a publish, an expired slot, a missing credential) to
the operator channel. Its audit trail is `logs/bsky-actions.ndjson`. Commands,
caps and failure modes: `docs/bluesky-client.md`.

## Personas

Four roles, one profile, one run: `personas/00-index.md` is the roster. Roles
are prompt-and-write-scope boundaries inside a single cron run, not separate
bots. The compliance gate is `workflows/gate.py` — mechanical pass/fail; the
Strategist adjudicates failures. The writer never clears its own failure.
