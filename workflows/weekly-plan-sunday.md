# Lightsword weekly planning — Sunday 20:00 America/Chicago

**Operations.** Entry = Hermes cron job `Lightsword Weekly Planning (Sun 20:00)`
in the profile store `lightsword` (`hermes -p lightsword cron list`). Schedule
`0 20 * * 0`, timezone America/Chicago. Working directory = this clone.
Logging: one line appended to `logs/nightly.ndjson` with `"run":"weekly-plan"`;
scheduler transcripts in `~/.hermes/profiles/lightsword/cron/output/<job-id>/`.
Delivery: the same Discord DM as the nightly, posted by
`python3 workflows/notify.py --file reports/weekly/<today>.digest.txt --kind
weekly` (see `docs/discord-delivery.md` for why the gateway does not deliver it).

**Why Sunday 20:00 and not Monday 09:00** (social plan §5.4, operator ruling
2026-11-04): Monday's post is generated Sunday night at 22:20 (T-1), so
Monday's calendar row and brief must exist before the Sunday pre-flight.
Planning at Monday 09:00 is 13 hours too late for the first post of the week.
Monday 09:00 remains the client-facing status note — a persona activity, not
this job.

## What this run does (Strategist role)

1. Get dates from `date`. Compute the coming Monday..Sunday window. On the
   scheduled Sunday run that window starts tomorrow. If this is a manual run on
   any other day, it starts on the next Monday. Never write a date before
   2026-11-09, the plan's first day: those are pre-launch days, and a row for
   them is an escalation, not a calendar entry.
2. Read the live calendar and its sources:
   - `plans/calendar-30d.md` — the live calendar. Rows already in it are
     authoritative and are never edited, deleted, reordered, or duplicated.
   - `plans/growth-plan-30d-2026-11-08.md` §7 (dated rows through 2026-11-22),
     §7.4 (week-level shape for weeks 3–4) and **§7.5 (daily rows for weeks
     3–4, added 2026-11-21)** — the only source for new rows.
   - `plans/posting-schedule.json` — the daily slot. Every Lightsword Bluesky
     row ships at `publish_time` (19:00 America/Chicago); do not write a row
     with a 09:00 slot. The schedule and its evidence are in
     `plans/posting-schedule.md`.
   - `plans/social-media-plan.md` §8.1 is **superseded** for
     2026-11-08..2026-12-08. Never use it to add or rewrite a row in that
     window.

   Schema: `date | channel | pillar | asset-id | working title | type | source | owner`
   (`type` is `source`, `derived`, or `empty`).

   **Multi-row by design (since 2026-11-08).** A date may carry several rows:
   a blog asset, a Lightsword social asset, and flambeee staging assets.
   Multiple rows on one date are normal. The requirement is **at least one row
   per date**, not exactly one. Never collapse a multi-row date to one row.

   - If a date in the window has no row, add rows only from the growth plan
     §7/§7.4. If the plan names a post but not a grounded asset-id and title,
     add one `type: empty` row with the reason `empty: no planned asset in
     growth plan` — never invent an asset.
   - **Daily cadence (2026-11-21):** every date gets a row, and §7.5 names a
     grounded Lightsword post for each day of weeks 3–4. Write those rows and
     briefs; a day with no grounded asset still gets `type: empty` with a
     reason. Never invent a title or an asset to fill the daily slot.
   - **Deliberate blanks are rows, never gaps.** A day with no post gets
     `type: empty` and a reason (e.g. `empty: no grounded asset`).
     A pre-flight that fails every Saturday gets muted by week two — that is
     the failure this rule prevents.
   - Do NOT invent assets, titles, channels, or numbers that the growth plan
     does not contain (unknown beats invented).
   - Never duplicate an asset-id; never edit or delete a row that exists.
3. Write briefs: for **every non-empty row** in the coming week that lacks one
   (not one per date), write `queue/briefs/<date>-<slug>.md`. Under 200 words
   each: the calendar row's channel and asset-id, the angle, the two or three
   facts that must appear (each with its source), and the call to action.
   Never rewrite an existing brief.
4. Append one line to `logs/nightly.ndjson` (`"run":"weekly-plan"`, rows added,
   briefs written, escalations written) and report.

## Fail closed

- `plans/growth-plan-30d-2026-11-08.md` missing **and** no calendar rows for
  the week → write `queue/escalations/<date>-no-calendar-source.md` and stop.
  Do not invent a week.
- Any row you cannot ground in the growth plan → leave it out, escalate in one
  line.
- Never edit or delete a row that already exists; never write a second row
  with an asset-id that already exists.
- This job never generates assets, never runs the gate, never stages, never
  publishes, never `git commit`s or `git push`es.

## Final response

Max 5 lines: rows added, empty rows written, briefs written, escalations
written, anything missing. The same five lines go to `reports/weekly/<today>.digest.txt`
and through `workflows/notify.py` to Jake's Discord DM.
