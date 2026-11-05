# AGENTS.md — Lightsword repo standing rules

This clone is the working directory for scheduled workflows run by the Hermes
profile `lightsword` (see below). Every agent working here obeys these rules;
they also load automatically into any cron run with this directory as cwd.

## Hard rules

1. **Phase 1 is dry-run. Nothing is ever published, posted, or sent from this
   repo.** Staged posts live as JSON in `queue/social/`; Jake publishes by hand.
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
6. **Never speak as Jake.** No persona sends client email, publishes without the
   gate, or approves its own work.

## Scheduled workflows

| Job | Schedule (America/Chicago) | Spec |
|---|---|---|
| Lightsword Nightly (22:00) | daily `0 22 * * *` | `workflows/nightly-2200.md` |
| Lightsword Weekly Planning (Sun 20:00) | Sunday `0 20 * * 0` | `workflows/weekly-plan-sunday.md` |

Both run under the Hermes profile `lightsword`, cwd = this clone. Scheduler
transcripts: `~/.hermes/profiles/lightsword/cron/output/<job-id>/` and
`hermes -p lightsword cron runs`. In-repo log: `logs/nightly.ndjson` (one line
per run) plus `reports/nightly/YYYY-MM-DD.md` (the digest).

## Personas

Four roles, one profile, one run: `personas/00-index.md` is the roster. Roles
are prompt-and-write-scope boundaries inside a single cron run, not separate
bots. The compliance gate is `workflows/gate.py` — mechanical pass/fail; the
Strategist adjudicates failures. The writer never clears its own failure.
