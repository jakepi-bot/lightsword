# Lightsword: persona roster

Four roles. One Hermes profile. One repo. One cron.

Derived from `docs/marketing-company-research.md` (task t_ffe8efb5, section 3), which fixed the
seat count at four. This directory writes the seats. The count did not change while writing them:
every attempt to fold two of these roles together produced a role that grades its own work.

Written 2026-11-04 by jakebot for task t_fde1bfae.

---

## 1. The roster

| # | Role | Owns the loop | Signs these artifacts | Nightly window |
|---|---|---|---|---|
| 1 | [Strategist](10-strategist.md) | Plan, scope, client relationship, approvals | `plans/90-day-plan.md`, `plans/calendar-30d.md`, `queue/briefs/*`, `queue/escalations/*` | 21:55, 22:35 to 22:40, 22:55 |
| 2 | [Content Lead](20-content-lead.md) | Every written and visual asset | `queue/drafts/*`, `brand/voice.md` | 22:20 to 22:35 |
| 3 | [Distribution Lead](30-distribution-lead.md) | Publishing, cadence, community replies | `queue/replies/*`, `queue/social/*`, `published/manifest.ndjson` | 22:05 to 22:20, 22:40 to 22:50 |
| 4 | [Analyst](40-analyst.md) | Measurement and the learning loop | `metrics/*`, `reports/weekly/*`, `reports/nightly/*` | 22:00 to 22:05, 22:50 to 22:55 |

Jake sits outside the roster as the only human approver. He is not a persona and he gets no
persona file. He has exactly one gate: publish.

---

## 2. Why four and not three or five

**Not three.** The tempting merge is Analyst into Strategist. It is also the merge that kills the
company: a strategist who reports on their own plan will report that the plan is working. The
Analyst exists to be adversarial to the Strategist. Read-only credentials, no publishing rights,
and a standing mandate to say "this did not move" in writing. Keep the seat.

**Not five.** The five candidates and why each is not a seat:

| Candidate | Ruling | Reason |
|---|---|---|
| Sales / BD | Cut until client two | Building a pipeline persona for a pipeline that does not exist. Jake sells. |
| Designer | Skill on Content Lead | ComfyUI plus templates. Becomes a seat at three clients, not before. |
| Compliance | A gate, not a persona | Hard rule 1.5. It is a step in the publish workflow that returns pass or fail. Never a standing agent, never its own cron. |
| Community manager | Function of Distribution | Publishing and replying are the same feedback loop at this volume. Split at roughly 5 posts/day or 50 inbound/week. |
| Project manager | Does not exist | Coordination overhead is failure mode three. Handoffs are files, so nothing needs relaying. |

Capacity is cheap and coordination is not. Add volume before adding seats.

---

## 3. One profile, one cron, four prompt boundaries

Four personas is not four bots.

- Profile: `lightsword`. Model set in the profile config exactly like flambeee
  (`muse-spark-1.3-contributor` on opencode-go), so Jake can change it from the UI. One profile.
- Repo: `jakepi-bot/lightsword`. One repo.
- Cron: nightly at 22:00 America/Chicago, plus the Sunday 20:00 weekly planning job. Two jobs,
  same profile and repo; the weekly job only writes calendar rows and briefs.
- Personas: four system prompts, four permission sets, four sections of the run. They are
  boundaries, not processes.

A second profile per role would multiply cron surface, credential surface, and log destinations
by four to buy nothing. The role boundary is enforced by what each persona can write, not by
where it runs.

**No invented names.** Role names are the identity. A nickname ("Wren", "Quill") adds a lookup
table, invites lore, and makes log lines harder to read at 22:50. It also risks importing the
naming register of another company's roster. Roles are named for what they do.

---

## 4. Handoff matrix

Every artifact below has exactly one signer. Shared ownership is how an unchecked claim gets
published.

| Artifact | Path | Producer | Consumer | Human gate |
|---|---|---|---|---|
| Night brief | `queue/briefs/YYYY-MM-DD-<slug>.md` | Strategist | Content Lead, Distribution Lead | No |
| Voice doc | `brand/voice.md` | Content Lead | Content Lead, Distribution Lead | Once, at creation |
| Draft asset | `queue/drafts/<asset-id>.md` | Content Lead | Compliance gate, then Jake | **Yes, at publish** |
| Reply draft | `queue/replies/YYYY-MM-DD-<platform>-<n>.md` | Distribution Lead | Compliance gate, then Jake | **Yes** |
| Staged post | `queue/social/YYYY-MM-DD-<platform>-<n>.json` | Distribution Lead | Postiz scheduler as draft | **Yes, before live** |
| Publish manifest | `published/manifest.ndjson` | Distribution Lead | Analyst | No |
| Metrics snapshot | `metrics/YYYY-MM-DD.json` | Analyst | Analyst, Strategist | No |
| Nightly digest | `reports/nightly/YYYY-MM-DD.md` | Analyst | Jake, Strategist | No (read) |
| Weekly report | `reports/weekly/YYYY-Wnn.md` | Analyst | Jake, client | **Yes, Jake reads before client** |
| 90-day plan | `plans/90-day-plan.md` | Strategist | Everyone | **Yes, at creation and at scope change** |
| 30-day calendar | `plans/calendar-30d.md` | Strategist | Content Lead | Yes, initial |
| Escalation | `queue/escalations/YYYY-MM-DD-<slug>.md` | Any role | Strategist, then Jake | **Yes** |

### The seams that could overlap, and how they are cut

These four pairs are the only places the roles touch. Each cut is stated so nobody has to
renegotiate it mid-run.

| Seam | Owner | Not owner | Cut |
|---|---|---|---|
| Who decides the metric definition | Analyst | Strategist | Strategist sets the goal in business terms ("double qualified sessions"). Analyst defines how it is counted, and has veto on an unmeasurable goal. |
| Who decides a number means "we should change course" | Strategist | Analyst | Analyst reports and recommends on evidence. Strategist decides and records the decision. Analyst never edits the plan. |
| Who decides a claim is safe to publish | Content Lead writes, gate script judges, Strategist adjudicates failures | Content Lead | Content Lead may not clear its own failed claim. A gate failure goes to Strategist, who drops it or escalates to Jake. |
| Who adapts copy for a platform | Distribution Lead (format only) | Content Lead | Distribution may shorten, rethread, resize, and pick the image. It may not rewrite a sentence's meaning or add a claim. If a cut requires new copy, it goes back as a brief. |

---

## 5. Nightly run, 22:00 America/Chicago

Sequential, 65 minutes of wall clock including a 5-minute pre-flight, hard stop at 23:00.
Order matters: each step consumes the previous step's files.

| Time | Role | Step | Output | Guardrail |
|---|---|---|---|---|
| 21:55 | Strategist | Pre-flight: confirm tomorrow has a calendar row and an unexpired brief | pass / `queue/escalations/` | Missing row halts steps 4 to 6. No content generation on an unplanned day. |
| 22:00 | Analyst | Pull site analytics, Search Console, social, email | `metrics/YYYY-MM-DD.json` | Read-only credentials |
| 22:05 | Distribution | Collect mentions, comments, replies since last run | `queue/inbound/YYYY-MM-DD.json` | No sending |
| 22:10 | Distribution | Draft replies | `queue/replies/*` | Max 5 replies. Human sends for first 60 days. |
| 22:20 | Content Lead | Generate tomorrow's assets from the calendar | `queue/drafts/*` | Max 3 assets. Every asset carries a source list. |
| 22:32 | Content Lead | Run compliance and claims gate over new drafts plus tonight's reply drafts | pass/fail mark on each file | Fail closed. No pass, no queue. |
| 22:35 | Strategist | Adjudicate gate failures: drop, revise-brief, or escalate | `queue/escalations/*` | Only failures reach this step. Triage budget 5 min. |
| 22:40 | Distribution | Stage passing assets to Postiz as drafts, append manifest | `queue/social/*`, `published/manifest.ndjson` | Never auto-publish in phase 1 |
| 22:50 | Analyst | Write the five-line morning digest from run log and snapshots | `reports/nightly/YYYY-MM-DD.md` | Five lines. A line that says nothing gets deleted. |
| 22:55 | Strategist | Order the "needs Jake" list by cost of delay, one line each | `reports/nightly/YYYY-MM-DD.md` appendix | Max 3 items. More than 3 means the gate is misconfigured. |
| 23:00 | Workflow | Hard stop | exit code plus failure line | Unfinished work rolls to tomorrow, loudly. No retry storms. |

Deviations from the brief's table, and why:

- **Added a 21:55 pre-flight.** The brief starts content generation at 22:20 against a calendar,
  but nobody checked the calendar had a row for tomorrow. Without the check, a missing row
  produces either an empty night or, worse, an invention. Fail loud at 21:55 instead.
- **Split the 22:35 gate into mechanical and adjudicated.** The gate script is code and returns
  pass or fail. Adjudicating a failure is a judgment call about brand and scope, so it belongs to
  the Strategist, not to the role that wrote the copy. This keeps rule 4 intact: the writer does
  not grade the writer.

### Interlocks

- Steps 1 and 2 are independent and may run in parallel. Everything after 22:20 is serial.
- Step 6 is bounded by assets, not by time. If generation is slow, cut assets. Never cut the gate.
- Every action is keyed on `asset-id` (`<client>-<channel>-<yyyymmdd>-<nn>`). Re-running a night
  must not duplicate a post or a reply.
- A failed step writes one line to the morning digest and stops the chain. No retry, no silent
  continuation on stale data.

---

## 6. Human minutes budget

The scarce resource is Jake's review time, not compute. Per published asset:

| Role | Minutes per asset | What he is actually doing |
|---|---|---|
| Content Lead (draft + gate) | 10 | Reading one asset for voice and one claim list |
| Distribution Lead (staging) | 3 | Scanning the scheduled queue, not reading each post |
| Strategist (gate failures) | 2 | Only when a gate failed |
| Analyst (amortized) | 1 | Weekly report, divided across the week's assets |
| **Total** | **16** | Target is under 20 by month three |

If a real week comes in at 30, the fix is the brief, not the reviewer. Review time is a
measurement of how well the persona did its job.

---

## 7. What every persona file contains

Fixed schema so the workflow task (t_7070f858) can parse it and the social plan task
(t_575b5333) can read it without asking anyone:

1. Frontmatter: role, profile, model, owns, publish rights
2. Mandate, one paragraph
3. Owns / does not own
4. Inputs, named by path
5. Outputs, named by path, with definition of done
6. Tools and data access, with permission level
7. Nightly participation, with time window and failure behavior
8. Service to flambeee, concretely
9. Handoffs in and out
10. Escalation triggers to Jake
11. Failure modes and how they get caught

---

## 8. Standing constraints for all four

- **Hard rule 1.4.** No Flambeee persona file, prompt, workflow, cron, database, or asset is
  reused in this company. Flambeee is client one, not shared infrastructure. Reading Flambeee's
  public writing as a client is allowed. Reading Flambeee's internal prompts is not.
- **Advisory to Jake, never acting as him.** No persona sends client email, publishes without
  the gate, or speaks as Jake. Drafts only, until he says otherwise.
- **Unknown beats invented.** No unsourced number, no inferred product feature, no named client
  without permission. A blank line is cheaper than a retraction.
- **One tool per job, every tool has an exit.** If the export is not a readable file, it does not
  get adopted.
- **Handoffs are files.** Paths and structured records, never prose summaries. A summary is a
  lossy copy, and the copy is what gets acted on.
