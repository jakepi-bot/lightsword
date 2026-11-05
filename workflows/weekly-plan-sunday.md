# Lightsword weekly planning — Sunday 20:00 America/Chicago

**Operations.** Entry = Hermes cron job `Lightsword Weekly Planning (Sun 20:00)`
in the profile store `lightsword` (`hermes -p lightsword cron list`). Schedule
`0 20 * * 0`, timezone America/Chicago. Working directory = this clone.
Delivery and logging: same Discord target as the nightly, one line appended to
`logs/nightly.ndjson` with `"run":"weekly-plan"`, scheduler transcripts in
`~/.hermes/profiles/lightsword/cron/output/<job-id>/`.

**Why Sunday 20:00 and not Monday 09:00** (social plan §5.4, operator ruling
2026-11-04): Monday's post is generated Sunday night at 22:20 (T-1), so
Monday's calendar row and brief must exist before the Sunday pre-flight.
Planning at Monday 09:00 is 13 hours too late for the first post of the week.
Monday 09:00 remains the client-facing status note — a persona activity, not
this job.

## What this run does (Strategist role)

1. Get dates from `date`. Compute the seven dates Monday..Sunday starting
   tomorrow.
2. Ensure `plans/calendar-30d.md` exists and that **every one of the seven
   dates has exactly one row**. Schema (social plan §8):

   `date | channel | pillar | asset-id | working title | type | source | owner`

   - `type` is `source`, `derived`, or `empty`.
   - **Deliberate blanks are rows, never gaps.** A day with no post gets
     `type: empty` and a reason (e.g. `empty: weekend`, `empty: Thanksgiving`).
     The plan names six: Sat Nov 14, 21, 28 and Dec 5 (weekend), Thu Nov 26
     (Thanksgiving), Fri Nov 27 (dead Friday). A pre-flight that fails every
     Saturday gets muted by week two — that is the failure this rule prevents.
   - Source of truth for what goes on a day: `plans/social-media-plan.md` §8.1
     once it is merged. Do NOT invent assets, titles, channels, or numbers that
     the plan does not contain (unknown beats invented).
   - Never duplicate an existing row; never edit a row that already exists.
3. Write briefs: `queue/briefs/<date>-<slug>.md` for each **non-empty** row of
   the coming week that lacks one. Under 200 words each: the calendar row, the
   angle, the two or three facts that must appear (each with its source), and
   the call to action.
4. Append one line to `logs/nightly.ndjson` (`"run":"weekly-plan"`, rows added,
   briefs written, escalations written) and report.

## Fail closed

- `plans/social-media-plan.md` missing **and** no calendar rows for the week →
  write `queue/escalations/<date>-no-calendar-source.md` and stop. Do not
  invent a week. (Expected state before the social plan PR merges; the
  escalation, not a guess, is the correct output.)
- Any row you cannot ground in the plan → leave it out, escalate in one line.
- This job never generates assets, never runs the gate, never stages, never
  publishes, never `git commit`s or `git push`es.

## Final response

Max 5 lines: rows added, empty rows written, briefs written, escalations
written, anything missing. Delivered to Jake's Discord.
