# Lightsword: what makes an effective marketing company

Internal strategy brief. Scope: a small AI-staffed marketing company, first client flambeee, site lightsword.org. Advisory only. No accounts created, nobody contacted.

Written 2026-11-04 by jakebot for task t_ffe8efb5.

---

## 1. The short version

Most marketing companies fail on one of three things, in this order:

1. **They sell output, not outcomes.** Deliverables ship, revenue does not move, the client leaves at month four.
2. **They cannot measure what they did.** No baseline, no attribution, no honest report. Every meeting is a vibe check.
3. **They drown in coordination.** Account managers relaying between specialists. At 8 people the overhead eats the margin.

Everything below is aimed at those three failure modes. The AI-staffed version has a different scarce resource than a human agency: not billable hours, but **Jake's review minutes**. Design the company so a human touches every deliverable once, briefly, and never twice.

The benchmarks that matter from the human agency world, for calibration only:

| Benchmark | Healthy | Source |
|---|---|---|
| Billable utilization, delivery roles | 65 to 75% | TMetric 2025, AMI 2025 |
| Labor cost as % of gross revenue | 55 to 65% | AMI Financial Performance 2025 |
| Revenue per employee | $150K to $200K | Forge / Predictable Profits 2025 |
| Net margin, small agency (<$1M) | 8 to 12% | AMI 2025 |
| Utilization below 55% | overstaffed | AMI 2025 |

Translation for an AI shop: labor cost drops to near zero, so the margin math changes completely. What does not change is the discipline. Utilization becomes **human minutes per deliverable**. Target under 20 minutes of review per published asset by month three. If a piece of content costs Jake 45 minutes to approve, the AI saved nothing.

---

## 2. Core functions

Five functions, in the order value flows. Each has a defined input and a falsifiable output.

**Strategy.** Turns a client goal into a plan with numbers on it: audience, positioning, channel mix, budget, the one metric that decides success. Output is a one-page brief plus a 90-day plan. Fails when it produces a deck instead of a decision.

**Content creation.** Long and medium form: site copy, blog, case studies, email, landing pages. This is where quality compounds. Output is draft assets in a queue, each with a source list and a claim check.

**Social media.** Distribution and conversation. Two different jobs that get conflated: publishing (scheduling, cadence, format) and community (replies, mentions, DMs). Output is scheduled posts plus a reply queue. Fails when it becomes a broadcast channel with no listening.

**Analytics.** Baseline, tracking, weekly read, post-mortems. Output is a report that says what changed, why, and what to do next. Fails when it reports impressions instead of qualified traffic and conversion.

**Client management.** Scope, approvals, expectation setting, the monthly call. At this size this is a **function of the strategist role**, not a separate headcount. Output is a written weekly status and an approval log.

---

## 3. Minimum viable roles

Four. Not three, not six. Each owns a different feedback loop, so nothing is merged that would hide a failure.

| # | Role | Owns | Primary outputs | Human dependency |
|---|---|---|---|---|
| 1 | **Strategist / Account Lead** | The brief, the plan, the client relationship, approvals | 90-day plan, weekly status, monthly review | Jake approves plan and scope changes |
| 2 | **Content Lead** | All written assets, brand voice, claims, SEO | Drafts with sources, editorial calendar | Jake approves publish-ready copy |
| 3 | **Distribution Lead** | Social publishing, community replies, repurposing | Scheduled queue, reply drafts, performance notes | Jake approves anything contentious |
| 4 | **Analyst** | Measurement, reporting, learning loop | Weekly report, post-mortems, metric definitions | Jake reads the weekly report |

Why four and not three: the tempting merge is Analyst into Strategist. That is exactly how agencies end up with a strategist who reports on their own work. Measurement has to be adversarial to strategy or it becomes marketing for the marketing. Keep them separate. The Analyst is also the cheapest role to run (read-only data access, no publishing rights).

**Not roles:**
- **Compliance** runs as a gate inside the publish workflow, not as a standing persona and not as its own scheduled job. Same rule as everywhere else: compliance inside workflows, never standalone.
- **Design** is a skill the Content Lead calls (image gen, templates), not a headcount, until there are three or more clients.
- **Sales / BD** is Jake until there is a second client. Do not build a persona for a pipeline that does not exist.

**Naming and persona files are task t_fde1bfae.** This brief only fixes the seat count and boundaries.

**Hard constraint: do not reuse Flambeee.** Different company, different repo, different profile, different cron, different voice. The pattern transfers; the assets do not. No shared persona files, no shared workflow code, no cross-profile cron. Lightsword writing about flambeee as a client is a client relationship, not shared infrastructure.

---

## 4. Operating cadence

### Nightly run, 22:00 America/Chicago

One job, sequential, with a hard stop. Order matters because later steps depend on earlier ones.

| Step | Time | Action | Guardrail |
|---|---|---|---|
| 1 | 22:00 | Pull metrics: site analytics, Search Console, social stats, email | Read-only credentials |
| 2 | 22:05 | Collect mentions, comments, replies since last run | No sending |
| 3 | 22:10 | Draft replies and route to `queue/replies/` | Human sends for first 60 days |
| 4 | 22:20 | Generate next day's content drafts from the calendar | Max 3 assets per night |
| 5 | 22:35 | Brand, claims, and compliance gate | Fail closed: no pass, no queue |
| 6 | 22:40 | Stage approved-format posts to the scheduler as **drafts** | Never auto-publish in phase 1 |
| 7 | 22:50 | Write run log: what ran, what failed, what needs a human | One screen, no filler |
| 8 | 23:00 | Hard stop. Unfinished work rolls to tomorrow, loudly | No 3am retry storms |

Design rules for the run:

- **Fail loud, fail once.** A failed step writes a line to the morning digest and stops the chain. It does not retry six times and it does not silently continue with stale data.
- **Idempotent.** Re-running the same night must not duplicate posts or replies. Key every action on date plus asset id.
- **Bounded.** 60 minutes wall clock. If content generation is slow, cut assets, not the gate.
- **Morning digest, not a status novel.** Five lines: published, drafted, blocked, needs approval, next action. If a line says nothing, delete it.

### Weekly and monthly

- **Monday 09:00:** strategist sets the week's three priorities against the plan. Written, not a meeting.
- **Friday:** analyst ships the weekly report. Four numbers, one paragraph of interpretation, one recommendation.
- **Monthly:** client review against the 90-day plan. Kill what did not work, in writing.
- **Quarterly:** re-baseline. If the plan is still right, say so in one line and move on.

---

## 5. Tooling

Principle: self-hosted where it is boring, hosted where self-hosting costs more than it saves. Jake owns his stack; do not rent the core.

| Need | Recommendation | Why |
|---|---|---|
| Site | Whatever lightsword.org already runs. Audit before changing | Inherited site, do not migrate for its own sake |
| Source of truth | Git repo, markdown, one folder per function | Diffable, reviewable, no lock-in |
| Social scheduling | Postiz (self-hosted) as primary; native APIs for Bluesky | Open source, multi-platform, no per-seat tax |
| Analytics | Plausible or Umami, self-hosted | Cookie-light, cheap, no GA4 consent mess |
| Search data | Google Search Console | Only real source of query data |
| Email | Listmonk, self-hosted | Owns the list |
| Images | Gemini image model via Hermes (local ComfyUI removed 2026-11-05) | Central provider, no local GPU cost |
| Orchestration | Hermes profile `lightsword` plus cron, isolated repo | Same pattern as Flambeee, separate everything |
| State | SQLite for queue and run logs | Queryable, no service to babysit |
| Reporting | Markdown to the repo, PDF only when a client asks | Nobody reads a dashboard twice |

Explicitly deferred: paid ads tooling, CRM, a BI layer, any SaaS with a per-seat price. None of them pay for themselves before client three.

Tooling rule: **one tool per job, and every tool must have an exit.** If the export is not a file Jake can read, it is not adopted.

---

## 6. KPIs

Three tiers. Report the top tier to the client, the middle tier to yourself, the bottom tier to nobody until it breaks.

**Tier 1, client outcomes** (the only numbers a client should hear):
- Qualified sessions from organic and social, month over month
- Conversions or leads, and cost per conversion
- Branded search volume (the honest proxy for awareness)
- Email list growth and 30-day open rate
- Share of voice against two named competitors

**Tier 2, operating health:**
- Human minutes per published asset. Target under 20 by month three
- First-pass approval rate. Target above 80% by week eight
- On-time publish rate. Target above 95%
- Draft rejection reasons, counted by category (voice, facts, strategy, taste). The top category is next month's prompt fix
- Review queue depth. Anything older than 72 hours is a process failure, not a backlog

**Tier 3, guardrails:**
- Published without approval: target zero, and it is a stop-the-line event
- Compliance or claims failures: zero
- Run failures per week: under two, each with a named cause
- Monthly tooling cost. Should stay under 5% of retainer

What not to report: impressions, follower count as a standalone, engagement rate without a denominator, "content produced." Those measure activity. Activity is not the product.

---

## 7. Structuring the AI-agent team

Five rules that decide whether this works.

**1. One owner per output.** Every artifact has exactly one role that signs it. Shared ownership is how a claim nobody checked gets published.

**2. Handoffs are files, not conversations.** Agents pass paths and structured records, not prose summaries. A summary is a lossy copy and the copy is what gets acted on. If the analyst needs the content, it reads the queue, not a description of the queue.

**3. Human approval sits at one point.** Publish. Not draft, not plan, not every intermediate step. One gate, clearly marked, with a reject reason that feeds back into the prompt.

**4. The agent that writes does not grade.** Content Lead drafts, analyst measures, strategist decides what to do about it. Collapsing these is how you get a team that reports its own success.

**5. Fail closed on brand and claims.** Anything unverified does not ship. Unsourced statistic, unnamed client, unapproved claim: drop it. A blank beats an invented number, and a wrong number costs more than a late post.

Practical shape: separate profile, separate repo, separate cron, shared nothing. Log every run to SQLite with inputs, outputs, duration, and human minutes. Read those logs monthly and delete the steps that never produce anything worth keeping.

---

## 8. Onboarding flambeee as first client

flambeee is a captive first client. That is useful for proof and dangerous for discipline. Write the scope as if flambeee could fire Lightsword, because the habits set here are the ones client two inherits.

**Week 0, before any content:**
1. One-page scope: goals, channels, cadence, what is out of scope, who approves, how either side exits. Signed off by Jake.
2. Access audit. List every account that exists and who owns it. Do not create new external accounts in this phase. Anything missing goes on a list for Jake to decide.
3. Baseline. Record current traffic, search queries, followers, email list, and conversion rate. No baseline, no claim of improvement later.

**Week 1:**
4. Brand and voice doc derived from flambeee's existing public writing. Voice only. Do not import Flambeee's personas, prompts, or workflows; read them as a client would.
5. Content pillars, three maximum, each tied to a product truth.
6. First 30-day calendar, 8 to 12 assets. Deliberately under-filled. Empty slots are cheaper than filler.

**Weeks 2 to 4:**
7. Publish on schedule, no auto-posting. Every asset through Jake once.
8. Weekly report every Friday, even when the news is bad, especially then.
9. Day 30 review: what moved, what did not, what gets killed.

**Standing rules for this client:**
- Deliverables live in the Lightsword repo. Changes to flambeee's own repo go through a PR that flambeee's owner approves. Lightsword does not push to flambeee's code.
- No cross-profile cron, no shared database, no shared persona files.
- Any claim about flambeee's product comes from flambeee's own documentation. No inferred features, no roadmap speculation.

---

## 9. Next steps

| # | Action | Owner | Depends on |
|---|---|---|---|
| 1 | Review and accept this brief; fix the four-role floor before personas get written | Jake | this doc |
| 2 | Write the four personas with scope, inputs, outputs, tool access, and handoffs | jakebot | t_fde1bfae, step 1 |
| 3 | Create `lightsword` Hermes profile, default model muse spark 1.3, isolated repo and cron | default | t_eaea7e15 / t_6f76aca1 |
| 4 | Create the GitHub repo under jake-bot, seed `docs/`, `plans/`, `personas/`, `queue/` | default | step 3 |
| 5 | Build the 22:00 workflow in dry-run mode: metrics pull, drafts, gate, log, digest. No publishing | default | t_7070f858, step 3 |
| 6 | Draft the 30-day social plan and calendar, grounded in this brief | default | t_575b5333, step 2 |
| 7 | Audit lightsword.org: current stack, analytics, who owns DNS and hosting | Jake or default | access from Jake |
| 8 | flambeee onboarding: scope page, access audit, baseline numbers | strategist persona | steps 2, 5 |
| 9 | Run the nightly job for 14 days in dry-run, then review human minutes per asset | Jake | step 5 |
| 10 | First live publish only after step 9 review, with the approval gate still on | Jake | step 9 |

Two things that must be true before anything publishes: the approval gate is wired, and there is a baseline to compare against. Without both, the first month produces content and no evidence.

---

## 10. What I would cut

- A fifth role. Four covers the loops. Add capacity, not seats.
- A dashboard. Markdown report, read by a human, beats a dashboard nobody opens.
- Paid social in month one. No baseline, no creative inventory, no budget justification.
- A brand book. Voice doc plus three examples is enough until client three.
- Any tool that requires a new external account before the first client signs. The stack can wait a week. The scope cannot.
