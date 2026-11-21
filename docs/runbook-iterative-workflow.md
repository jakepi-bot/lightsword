# Lightsword iterative workflow — runbook v1.0

Owner: Strategist. Status: live 2026-11-05 (kanban t_828e0fe1).
Inputs: AGENTS.md, personas/00-index.md, workflows/nightly-2200.md, workflows/weekly-plan-sunday.md,
plans/social-media-plan.md, plans/scope-flambeee.md, flambeee proposal v1.0 (t_669d591d).

## 1. The loop in one paragraph

Ship small, measure, revise. Weekly 30-minute Analyst plus Strategist check. Monthly 60-minute
all-persona review. Quarterly close with Jakebot consulted when indecisive and a human decision
on Discord when approval is needed. No goal changes weekly; tactics change monthly with a dated
record. (Proposal §6 cadence, from Lightsword goals.md.)

## 2. Scheduled tasks — what runs, where, and why two jobs cover four functions

Two cron jobs, one profile (`lightsword`), one repo clone as cwd. Both deliver to Jake's Discord
and log scheduler transcripts under `~/.hermes/profiles/lightsword/cron/output/<job-id>/`.

| Job | Schedule (America/Chicago) | Spec | State 2026-11-05 |
|---|---|---|---|
| Lightsword Nightly (22:00) | `0 22 * * *` | workflows/nightly-2200.md (phases 0–10) | enabled, next 2026-11-05 22:00, last ok 2026-11-04 |
| Lightsword Weekly Planning (Sun 20:00) | `0 20 * * 0` | workflows/weekly-plan-sunday.md | enabled, next 2026-11-08 20:00, last ok 2026-11-04 |

The task asked for four functions. They are phases inside these two jobs, not four separate
crons — one profile, one cron, four prompt boundaries (personas/00-index.md §3). A separate
cron per function would quadruple credential surface, log destinations, and failure modes.

| Requested function | Where it lives | Owner | Output |
|---|---|---|---|
| Content drafting | Nightly phases 4–5 (22:20 Content Lead, 22:32 gate) | Content Lead | queue/drafts/*.md, gate marks |
| Social posting / review | Nightly phases 2–3 (22:05–22:10 Distribution) + phase 7 (22:40 staging) | Distribution Lead | queue/inbound/*.json, queue/replies/*.md, queue/social/*.json |
| Performance check-ins | Nightly phases 1+8 (22:00 pull, 22:50 digest) + weekly 30-min Analyst/Strategist + Friday weekly report | Analyst | metrics/*.json, reports/nightly/*.md, reports/weekly/*.md |
| Iterative planning | Weekly Sun 20:00 job + monthly 60-min review + quarterly close | Strategist | plans/calendar-30d.md rows, queue/briefs/*.md, dated keep/kill decisions |

No new cron jobs were created in this setup. If volume ever justifies a third job (split at
~5 posts/day or ~50 inbound/week per 00-index §2), it needs a Strategist scope decision plus
Jake approval first — never an agent improvisation.

## 3. Nightly run (22:00, hard stop 23:00)

Pre-flight (Strategist, 22:00): tomorrow has a calendar row and an unexpired brief, or phases
3–7 halt. `type: empty` passes (deliberate blank, noted, not escalated). Missing row or
missing brief halts and writes queue/escalations/. Phases 1, 2, 8, 9 still run. Never invent
the calendar here; the Sunday job owns rows.

Then: Analyst pulls feeds (unavailable + reason, never a number) → Distribution collects
inbound and drafts ≤5 replies (human sends 60 days; pricing/outage/complaint/persona items
escalate, never drafted) → Content generates ≤3 assets from brief + calendar row (no brief =
no asset) → Content runs `python3 workflows/gate.py` (mechanical pass/fail, may not edit or
waive) → Strategist adjudicates failures only (drop / re-brief / escalate, 5-min budget) →
Distribution stages passing assets as `queue/social/*.json` drafts (never live in phase 1;
Postiz absent = WARNING) → Analyst writes the five-line digest → Strategist orders the
Needs-Jake list (max 3, by cost of delay).

Logging, every run: one NDJSON line in logs/nightly.ndjson plus reports/nightly/YYYY-MM-DD.md
(five lines + Needs-Jake appendix). Final scheduler response: max 5 lines, status flags first.

## 4. Weekly planning (Sunday 20:00)

Strategist, dates from `date`. Window is the coming Monday..Sunday (on the scheduled Sunday
run, tomorrow onward). Never write before 2026-11-09 (pre-launch days are escalations, not
rows). Every date gets exactly one row: `date | channel | pillar | asset-id | working title |
type | source | owner`, type source/derived/empty. Empty days carry a reason (weekends,
Thanksgiving, dead Friday) — blanks are rows, never gaps. Ground every row in the social
plan; never invent titles, channels, or numbers. Write briefs (<200 words: row, angle, 2–3
sourced facts, CTA) for each non-empty row lacking one. Log one `run: weekly-plan` line.
Never generate, gate, stage, publish, commit, or push from this job.

## 5. Owners (four roles, no names)

Strategist (account lead): plan, calendar, briefs, scope, gate adjudication. Signs plans/*,
queue/briefs/*, queue/escalations/*. Publish rights: none. Never writes copy.
Content Lead: every written/visual asset, sources under every claim, runs (never waives)
the gate. Signs queue/drafts/*. Publish rights: none. Never clears own failure.
Distribution Lead: staging, cadence, replies, manifest. Signs queue/replies/*,
queue/social/*, published/manifest.ndjson. Phase 1: draft-only; Jake publishes by hand.
Never rewrites a claim when formatting — new copy needs a new brief.
Analyst: measurement and the learning loop. Signs metrics/*, reports/*. Reports to Jake,
not the Strategist, so success is never self-graded. Read-only everywhere; owns baseline,
definitions, snapshots, digests, weekly reports. Never a zero for not-collected — null plus
reason.

Jake (only human approver): one gate — publish. Also resolves credentials, access, scope,
and the five gating questions. No persona file, never spoken as.

## 6. Escalation — including Jakebot

Jakebot (advisor, outside the roster): consulted when Lightsword is stuck or indecisive.
Advice only — not a publisher, not an approver. Do not assign it follow-up board work;
create a child card for the right specialist instead. The flambeee-materials channel
(scope-flambeee.md §7, Jake-authorized 2026-11-05) is separate: marketing/materials
questions and suggestions to the flambeee bot only, public-surface sources only, never
internal persona files, prompts, workflows, cron, databases, or assets.

Escalate to Jake (via queue/escalations/* + digest Needs-Jake list, max 3/night) when:
scope would change; money moves; a claim cannot be sourced and the asset matters; the plan
needs change before day 90; a gate failure is a rule problem; anything needs publish
approval; credentials/access block work. Do not escalate wording, image choice, posting
order, or which of two valid angles — those are the role's call.

## 7. When to message the human on Discord

The nightly and weekly jobs already deliver to Jake's Discord (job `deliver` target) — the
digest and the 5-line final response are the default channel. A separate direct message is
only for: (a) approval needed (publish review, proposal Checkpoint A, gating answers Q1–Q5);
(b) credentials/access/scope blockers no agent can resolve; (c) a decision no agent can
make (measurement option A/B/C, co-branding permission, SLA). Routine work never DMs.
Never invent an answer to unblock — block loudly (escalation file + digest line) and wait.

## 8. Iterative review loop (how tactics change without churning goals)

- Daily: digest five-liner + Needs-Jake appendix. Unfinished work rolls forward loudly. No retries.
- Weekly (30 min, Analyst + Strategist): four numbers week-over-week, one paragraph, one
  recommendation (Friday report). Small tactic tweaks allowed; goals frozen.
- Monthly (60 min, all personas): plan vs actuals in numbers. Name what gets killed.
  Losing variants retire with evidence and a dated record. Tactics change here.
- Quarterly (close): Analyst closes 90-day actuals vs proposal §2 targets; Strategist drafts
  next-quarter proposal; Jake decides. Deferred HubSpot goals (#6 customer value, #8 revenue,
  #9 internal brand) promote only with evidence.
- Kill rules live in the proposal experiments (§7): if neither variant earns a reply/repost
  after 8 posts, retire both and test the next framing; zero engagement on both audience
  probes means the audience hypothesis is wrong — escalate to Jakebot, then Jake.

## 9. Phase 1 guardrails (non-negotiable)

Dry run: nothing is ever published, posted, or sent from the repo. Staged posts are JSON;
replies are drafts; Jake publishes/sends by hand. Scheduled runs never commit or push.
Repo is public: queue/, metrics/, reports/, published/, state/, assets/images/, logs/ stay
out of git. Unknown beats invented: no unsourced numbers, no inferred features, no named
client without permission (weeks 1–4: "small web-games studio", never the name; no game
counts until flambeee rules; FB rows draft-only via owner path). Voice separation is a gate
failure, not a style note. Lightsword voice on the client account (or vice versa) fails.

## 10. Where things live

- Queue: queue/briefs/, queue/drafts/ (+gate marks), queue/social/*.json (staged drafts),
  queue/replies/, queue/escalations/, queue/inbound/
- Measurement: metrics/baseline.json (immutable), metrics/definitions.md,
  metrics/kpi-tracker.csv, metrics/YYYY-MM-DD.json, reports/nightly/, reports/weekly/
- Plan: plans/social-media-plan.md, plans/calendar-30d.md, plans/scope-flambeee.md,
  plans/social-accounts-and-site-plan.md, this runbook (docs/)
- Launch state: see launch report in the task workspace (what launched / queued / blocked)
  plus the KPI tracker. First campaign queue: 6 drafts gate-passed, 6 LT social JSON staged,
  2 FB drafts gated-held (no FB social JSON until Checkpoint A + Q1–3).
