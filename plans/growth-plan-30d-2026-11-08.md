---
title: Lightsword 30-day growth and deliverables plan
version: 1.0
date: 2026-11-08 07:35 America/Chicago
owner: Strategist (account lead)
status: active
window: 2026-11-08 to 2026-12-08 (31 days)
supersedes: plans/social-media-plan.md §8.1-§8.2 for this window
inputs: reports/audit/2026-11-08-baseline.md (t_80de805d); plans/client-brief-flambeee.md v1.0 (t_2cb5b910); plans/scope-flambeee.md; plans/social-media-plan.md; personas/00-index.md; published/manifest.ndjson; queue/drafts; queue/social; metrics/*
---

# Lightsword 30-day growth and deliverables plan

This plan replaces the part of the 2026-11-04 social plan that led to six posts, one follower, and zero replies. It keeps the operating model that works (four roles, one nightly run, one mechanical gate) and changes the part that did not: distribution, audience fit, and proof.

The plan is executable from the hour it lands. The first action is in §8; the 14-day calendar is in §7; the targets in §3 are numeric and traceable to the 2026-11-08 audit in every row.

---

## 0. The one screen

| Decision | Ruling |
|---|---|
| Goal | End the stall with a repeatable publishing and conversation loop, not a bigger calendar. |
| Primary number | Lightsword Bluesky followers: **1 → 25** by 2026-12-08. |
| Secondary number | Average interactions per Lightsword post: **0.0 → ≥1.0**; replies received **0 → ≥5**. |
| Cadence | **5 Lightsword Bluesky posts + 2 blog articles + 3 flambeee drafts staged + 10 outbound actions per week.** |
| Pillars | Four for Lightsword, three for flambeee. Every row names one. A row without a pillar is invalid. |
| Publishing | Lightsword channels: autonomous after gate pass + Strategist adjudication. flambeee: drafts staged, owner posts. |
| Voice | Lightsword house voice and flambeee player voice stay separate. A Lightsword-voice sentence on the client channel is a gate failure. |
| Not in this plan | LinkedIn (unavailable), paid promotion, video, email capture, client results claims, flambeee logo on Lightsword channels. |
| First action | **Open the front door** within 24 hours: one pinned intro post, bio updated, 20 follows, 10 substantive replies (§8). |

---

## 1. What the audit says (the baseline this plan is built on)

Source: `reports/audit/2026-11-08-baseline.md` (t_80de805d), read-only, 2026-11-08 07:05-07:15 CST.

| Fact | Baseline | Source |
|---|---|---|
| Lightsword Bluesky followers / following | **1 / 2** | audit §2.1 |
| Lightsword posts | **6 lifetime**; 4 posted in one minute on 11-06; last post 11-07 05:22 CST; **0 in the 24h before audit** | audit §2.1, §4.3 |
| Lightsword engagement | **0 likes, 0 reposts, 0 replies, 0 quotes** on 6 posts; **0.0 per post**; 0.0% of followers | audit §2.1 |
| Lightsword media | **0 of 6 posts** carried an image or card | audit §2.1 |
| Lightsword link destinations | **4 of 6** posts linked GitHub plan files, not lightsword.org | audit §4.3 |
| Lightsword profile | **No pinned post**; bio is the unnamed variant; does not follow `@flambeee.bsky.social` | audit §4.1, §4.3 |
| Website | 3 pages live; **0 blog articles** and 6 "Pending." cards; **7 of 7 download buttons 404**; no CTA; no favicon; 0 OG tags; **no analytics tag** | audit §2.2, §3.2, §3.3 |
| Site speed / mobile | TTFB 49-81 ms; load 149 ms; no mobile overflow; contrast passes AA | audit §3.4 |
| flambeee Bluesky | **4 followers / 41 posts**; self-labelled bot; release-note voice | brief §6; audit §1 |
| flambeee GitHub | 0 stars; 26 repo views / 1 unique in 14 days; 2 external humans lifetime | brief §6 |
| Client deliverables shipped | **0 of 9** in brief §6; brief v1.0 delivered 2026-11-08 | brief §6 |
| Site traffic | **`unavailable`**, not zero: no analytics tag, no Search Console | audit §2.2, W5 |

**The read: this is not a content shortage.** Six posts exist. The failures are distribution (no outbound, no pinned post, no reply work), audience fit (all six posts were about Lightsword's operating model, none named a buyer pain or a next step), and proof (no media, no site traffic, links away from the site). The 30-day plan fixes those three things in that order.

**One finding the audit did not cover.** Four of the eight week-1 drafts in `queue/drafts/` are gate-passed but factually stale. They describe Phase 1 ("one human gate", "Jake approves each asset", "nothing auto-posts"). That stopped being true on 2026-11-05. The gate is mechanical and does not test whether a sentence is still current, so these drafts must not be published as-is. Quarantine list: Appendix B.

---

## 2. Positioning

### 2.1 Lightsword

**Positioning statement.** For small product teams that can ship but cannot explain what they shipped, Lightsword is the marketing company that operates in public: four defined roles, one nightly run, a mechanical gate, and a published record of what it refused and what it corrected. Unlike an agency or an AI content farm, every claim is traced to a source and every number is reported with its denominator.

**One-line value proposition.** Clear marketing for small product teams, with every claim sourced and every number published.

**Buyer.** The founder or technical lead of a 2-15 person product team with a live product and no marketing hire. They can build; they cannot justify a retainer; they have been burned by an agency that sent reports or an AI tool that sent volume.

**Pain we name.** Shipping is not the problem. Explaining what shipped, to the people who would pay for it, is the problem.

**Proof that exists today.** Three live pages; a documented four-role roster; a gate script that returns pass or fail; a publish manifest with six live URLs; four nightly reports; a 30-day plan written as the first asset. None of that is a client result, and the plan does not pretend it is.

**What we do not say.** No growth, revenue, or client-result claims. No "AI-powered" as a benefit. No "full-service". No claim that cannot be traced to a file in this repo or a public page. No named client result before a measured baseline exists.

### 2.2 flambeee

**Positioning statement (from the client brief, §3).** For casual mobile break players who want two minutes of play without a signup, flambeee is the free browser arcade that opens in one tap and asks for nothing: no install, no account, no ads, no tracking. Eight games and six small apps, playable in the browser, with progress kept on your own device.

**One-line value proposition.** Free browser games that open in one tap and ask for nothing: no install, no account, no ads, no tracking.

**Player sentence (client-approved).** "Pick a game and play in your browser. Nothing to install, no account, no ads."

**Audience.** Primary: casual mobile break players, two-minute sessions, no signup. Secondary: daily word and puzzle players (Wordfire, Cinder, Afterglow). Not the audience: competitive or esports players, multiplayer/accounts/cloud saves, console/AAA, developer/open-source browsers, under-13.

**Proof that exists today.** Eight live game pages and six app pages, all HTTP 200 on 2026-11-08; zero-friction play; progress in browser storage; no analytics or trackers by architecture. Canonical counts are **8 games / 6 apps**; never 5 or 7.

**What we do not say.** The full off-limits list is `plans/client-brief-flambeee.md` §3. Short version: no player counts, play totals, traffic, retention, revenue, roadmap, "soon", license/open-source claim, WCAG/compliance claim, competitor "better than", or unshipped feature. No flambeee logo on Lightsword channels until Jake rules on co-branding.

---

## 3. 30-day targets

Window: 2026-11-08 to 2026-12-08. Day 30 = **2026-12-08**. Every baseline below is a number from the audit or explicitly `unavailable`; no target below is presented as a forecast.

### 3.1 The five required targets

| Metric | Baseline (source) | Day-30 target | How it is counted | Owner |
|---|---|---|---|---|
| **Follower count — Lightsword** | **1** (audit §2.1) | **25** (net +24) | `app.bsky.actor.getProfile.followersCount`, daily snapshot | Analyst |
| **Follower count — flambeee** | **4** (brief §6; public API 11-08) | **40** (client-proposed, adopted) | public `getProfile`, daily snapshot | Analyst |
| **Posts per week** | **0 scheduled**; 6 lifetime in a 3-day burst, 0 in the 24h before audit (audit §2.1) | **5 Lightsword Bluesky posts + 2 blog articles published; 3 flambeee drafts staged** per week. 30-day totals: **21 / 8 / 12** (the Thanksgiving week carries 3 posts, not 5) | `published/manifest.ndjson` + live URL checks; staged count in `queue/social/` | Distribution Lead |
| **Average engagement rate** | **0.0 interactions per post** (0 interactions ÷ 6 posts); **0.0%** of followers (audit §2.1) | **≥1.0 interaction per post**, averaged over posts ≥72h old, weeks 3-4; **≥4.0%** interactions ÷ follower base at day 30; **≥5 replies received** | `app.bsky.feed.getPosts`: likes + reposts + replies + quotes, divided by original posts. Denominator always printed | Analyst |
| **Site traffic** | **`unavailable`**: no analytics tag or Search Console (audit W5) | Instrument by **11-10**; rebaseline **11-15**; target **≥120 sessions in 2026-11-25..12-08**, of which **≥40 with `utm_source=bsky`** | Umami sessions + UTM parameters; if no tag, record `unavailable` and no claim | Analyst |
| **Client deliverables shipped** | **0 of 9** (brief §6; brief v1.0 landed 11-08) | **7 of 9 unconditional by 12-08; 9 of 9 if two new-game releases ship and the Typewreck sign-off lands by 11-14** | Deliverables table (§9), each with a file or live URL | Strategist |

**One baseline is not from the audit.** Client deliverables shipped (0 of 9) comes from `plans/client-brief-flambeee.md` §6; the 2026-11-08 audit measured Lightsword's footprint, not client output. Every other baseline above is an audit number or an explicit `unavailable` from it.

**Why 25 and not 250.** The account has one follower and has never had an outbound conversation. A 25-follower target is reachable by 21 posts and 40 outbound actions; 250 would require a reach event the plan cannot produce and would turn month one into a fiction. The client's 4 → 40 target is adopted because the client set it and it has the same shape.

**Why site traffic is a planning number.** The honest baseline is `unavailable`, not zero. The final 14 days carry roughly 11 link-bearing assets (8 Bluesky posts + 3 blog articles), so 120 sessions implies about 11 sessions per asset. That is an assumption, not evidence. It is rebased on 11-15 from the first five instrumented days. If the tag is not installed by 11-10, the target is withdrawn and the weekly report says `unavailable` with the reason; the plan does not invent a number.

### 3.2 Supporting targets (leading indicators)

| Metric | Baseline (source) | Day-30 target | Owner |
|---|---|---|---|
| Outbound substantive actions | **0 recorded** (audit §4.3) | **10 per week, 40 in window** | Distribution Lead |
| Lightsword posts with an image | **0 of 6** (audit §2.1) | **≥8 of 21** (38%), using the six-format kit in `brand/visual/`; alt text from `brand/visual/exports/alt-text.md` | Content Lead |
| Blog articles live | **0** live, 6 "Pending." (audit §2.2) | **8 live** by 12-08; first live 11-09 | Content Lead |
| Broken download links | **7 of 7** (audit §3.3 W1) | **0 reachable broken links** by 11-14: either 7/7 return 200, or `/downloads/` is retired with a 301 to `/` (site refresh spec P0 #3) | Content Lead |
| Pages with favicon + OG tags | **0 of 3** (audit §3.3 W7/W9) | **3 of 3** by 11-14 | Content Lead |
| Publishes without a gate pass | not applicable (no publish script) | **0**; stop-the-line if nonzero | Analyst |
| First-pass gate rate | not measured | **≥80%** by 12-08 | Content Lead |
| Client copy defects filed | 0 | **4 filed** to Ember by 11-12 (brief deliverable #5) | Strategist |

### 3.3 Checkpoints

| Checkpoint | Date | LT followers | FB followers | Interactions / post | Site sessions | Deliverables |
|---|---|---|---|---|---|---|
| Day 3 | 11-11 | 3 | 6 | 0.2 | instrumenting | 1 of 9 (#5 filed) |
| Day 7 | 11-15 | 6 | 10 | 0.3 | first 5-day baseline | 2 of 9 |
| Day 14 | 11-22 | 12 | 18 | 0.6 | ≥20 in week 2 | 4 of 9 |
| Day 21 | 11-29 | 18 | 28 | 0.8 | ≥60 in week 3 | 5 of 9 |
| Day 30 | 12-08 | 25 | 40 | ≥1.0 | ≥120 in final 14 days | 7-9 of 9 |

Checkpoints are targets, not forecasts. A missed checkpoint triggers a written decision (change the tactic, not the number) in the Friday report.

---

## 4. What changes, and where it shows

| Audit finding | Change in this plan | Where it shows |
|---|---|---|
| 1 follower, 0 replies, no outbound motion | Outbound first: 10 substantive replies and 20 follows per week, logged | §6, §8, §11 |
| All 6 posts were process meta | A fixed Tuesday **Fixes** slot from week 2, and every receipt post names a buyer-facing lesson | §5, §7 (1 Fix per week from 11-17) |
| 0 of 6 posts had media | Image cards on ≥8 of 21 posts; six-format kit in `brand/visual/` (T01 quote, T02 announcement, T03 thread cover, T05 link card, T06 metric; T04 client-work is gated) | §3.2, §7 |
| 4 of 6 posts linked GitHub plan files | Every social link goes to lightsword.org or the specific game page; GitHub only for an explicit build-log post | §5, §7 |
| Burst then idle: 4 posts in one minute, then 0 for 26 hours | One post per slot, daily 19:00; no batching; empty days are rows | §6, §7 |
| No pinned post, no CTA, no analytics | Front door pinned in 24h; one site CTA; tag installed by 11-10 | §3, §8, §9 |
| Stale Phase-1 copy in gate-passed drafts | Quarantine list and a Currency Check in every brief; re-draft before publish | Appendix B, §7 |

---

## 5. Content pillars

Every calendar row names exactly one pillar. A row that needs two is two rows. A pillar with no proof source is a mood, and a mood produces filler.

### 5.1 Lightsword: four pillars

| Pillar | What it is | Proof it rests on | Formats | Example hook | CTA |
|---|---|---|---|---|---|
| **L1 Receipts** | The operating numbers, published weekly, failures included | `logs/nightly.ndjson`, `published/manifest.ndjson`, `metrics/*` | Text post (Fri), image metric card | "Six posts in three days. One follower. Zero replies. The plan was not the problem." | "The log is public." |
| **L2 Fixes** | One concrete fix a small team can copy in under 10 minutes, with a before/after | The audit's 13 site issues and the fixes Lightsword ships on its own site | Image, text, thread for steps | "All 7 download buttons on our own site returned 404. The check that found it is 12 lines." | "Reply with a URL; we will run the check." |
| **L3 Cuts** | What was refused, killed, or corrected, and why | Gate records and marks, escalations, the stale-copy quarantine, the off-limits claim list | Thread, text post | "Our homepage said nothing auto-publishes. That stopped being true on 2026-11-05." | "If you find a stale claim on our site, reply with the URL." |
| **L4 Proof** | How the work ships, shown: the client keeps the account, the gate is real, the handoff has no password | `plans/scope-flambeee.md` §1/§3; `queue/social/` staged records | Text post, image | "Our first client posts on their own account. We draft, stage, and hand off. No password, no takeover." | "Read how the handoff works." |

L1 carries the weekly rhythm: the receipt every Friday, plus the plan and cost posts that make the receipts mean something. L2 is the growth experiment: a fixed Tuesday slot from week 2, where a fix can be copied without hiring anyone. L3 and L4 are the trust and sales pillars: what was refused, and how the work actually ships.

### 5.2 flambeee: three pillars

| Pillar | What it is | Proof it rests on | Formats | Example hook | CTA |
|---|---|---|---|---|---|
| **F1 Zero friction** | No install, no account, one tap | flambeee.com and live game pages | Image + link | "One word a day. No install, no account." | "Play Wordfire: [game URL]" |
| **F2 The fix note** | The honest defect note, pointed at rather than rewritten | Public `BLOG.md` sessions and release notes | Link | "The timer ran 7 minutes while the field said 7.5. The fix shipped in v0.43.0." | "Read the note." |
| **F3 One idea per game** | One mechanic, done well, described precisely | Public game pages and client descriptions; Rook reviews mechanic claims | Text, image | "The board lights up, goes dark, and takes moves from memory." | "Play Afterglow: [game URL]" |

F1 carries the volume. F2 is the differentiator: flambeee already publishes the kind of writing most studios never do, and the social job is to point at it. F3 is used sparingly and never on mobile creative for Echo Rounds (keyboard-only).

### 5.3 The pillar test

1. The row names one pillar.
2. The pillar has a proof source that exists today.
3. The draft carries the source line. No source, no post.
4. If a post could appear on any agency account unchanged, it is not a Lightsword post.

---

## 6. Cadence

### 6.1 Per surface

| Surface | Volume per week | Days | Slot (America/Chicago) | Publisher | Notes |
|---|---|---|---|---|---|
| Lightsword Bluesky | **7 posts (daily)** | Mon-Sun | **19:00** | Lightsword (native API) | The only always-on growth surface. **Changed 2026-11-21** (operator, kanban `t_3e006185`): 5/week Mon-Fri 09:00 → daily 19:00. Rationale and evidence: `plans/posting-schedule.md`; machine-readable: `plans/posting-schedule.json`. |
| Lightsword blog | **2 articles** | Mon + Thu | Draft at 22:00 T-1; site write 22:40; live verify 18:45 | Content Lead drafts; Distribution Lead writes the page | Owned spine; social links point here, not GitHub. Deploy latency is B3: verify 200 before the 19:00 post, text-only fallback |
| flambeee Bluesky | **3 drafts staged** | Friday batch, by 11:00 | client posts 12:05 | Client owner | No Lightsword credentials; `staged-awaiting-owner` |
| Outbound | **10 actions** (2 replies + 2 follows per weekday, max **5 replies in 24h**, ≥10 min apart) | Mon-Fri | 09:30-09:50 | Distribution Lead | No links in replies, no pitch; log every action. Cap per AGENTS.md rule 7 — the platform scores reply bursts as spam |
| Weekly report | 1 | Friday | 16:00 | Analyst | 6 numbers, 1 paragraph, 1 decision |
| Weekly planning | 1 | Sunday | 20:00 | Strategist | Existing cron; rows + briefs |
| Nightly run | 7 | Daily | 22:00 | All four roles | Existing cron; T-1 generation + gate + publish |

**2026-11-21 amendment (operator, kanban `t_3e006185`).** The Lightsword Bluesky
row is daily at 19:00, not five posts Mon-Fri at 09:00. The nightly stays at
22:00: it generates T's asset and arms it for T 19:00; the 5-minute outbox tick
publishes at the slot. The client row is unchanged. The campaign final report's
recommendation 5 ("drop the daily post cadence") is superseded by the operator
directive, with the reason recorded in `plans/posting-schedule.md`. The slot is a
prior from the published evidence, not a measured finding for this account.

### 6.2 Volume math

- 7 posts a week, 28 over four weeks, plus the 11-08 launch post = **29 posts**.
  Daily adds six posts to the previous 21 (the 30-day window's weeks 3-4 and the
  close now carry daily rows).
- 2 blog articles × 4 weeks = **8 articles**.
- 3 flambeee drafts × 4 weeks = **12 drafts**.
- Total produced: **10 pieces per week, 47 in the window** (39 social posts: 27
  Lightsword + 12 flambeee).
- Baseline for comparison: 6 posts in 3 days, 0 scheduled, 0 blog articles, 0 outbound actions.

### 6.3 Cadence rules

1. **One post per slot.** No batching. The 11-06 four-posts-in-one-minute burst is the failure this rule prevents. The daily Lightsword slot is 19:00; a second post on the same day needs its own calendar row and its own slot.
2. **Empty days are rows.** Daily means the slot exists every day; it does not mean every day gets a post. A day with no grounded asset stays `type: empty` with a reason and the nightly records a planned skip. Never fill a blank with an unplanned post. Weeks 3-4 name a grounded asset for each day in §7.4, so those days are not blank.
3. **Blog first, link second.** The article is generated at 22:00 T-1, written into the site directory at 22:40, and verified at 18:45. The 19:00 Bluesky link post ships only after the live URL returns 200. If the cloud sync has not landed by 18:45, the post ships text-only and the link moves to the next slot. No GitHub URL substitution.
4. **The client's account is not ours.** flambeee drafts are staged in `queue/social/` with `status: staged-awaiting-owner`; the client posts one at a time. No password, no parallel account, no cross-post.
5. **The gate is not a style check.** `workflows/gate.py` pass + Strategist adjudication. The writer never clears its own failure. A Currency Check (§6.4) is additional to the gate.
6. **No LinkedIn this month.** There is no page and no token (audit §6). LinkedIn variants in the queue are dead; they are not calendar rows.

### 6.4 The Currency Check

The mechanical gate does not know whether a sentence is still true. Every brief and every draft gets a five-line manual check before staging:

1. Does it say "human gate", "Jake approves", "nothing auto-publishes", or "phase 1"? **Fail.**
2. Does it mention LinkedIn as an active channel? **Fail.**
3. Does it use a game count other than 8 games / 6 apps? **Fail.**
4. Does it claim a client result, player count, traffic, or retention number? **Fail.**
5. Does it link to a GitHub plan file without the post being explicitly a build-log post? **Fail.**

A Currency Check failure goes to the Strategist as a gate failure: drop, re-brief, or decide-and-log.

---

## 7. 14-day content calendar

Window: **2026-11-08 to 2026-11-21** (14 days), plus **2026-11-22** because it is the last day of the week-2 planning window and the weekly job expects a row for every date.

Schema: `date | channel | format | pillar | asset-id | topic | hook | CTA | owner`. Format is one of `text post`, `image`, `thread`, `link`, or `empty`. Owner is the accountable role; publishing is Distribution Lead unless stated.

### 7.1 Lightsword and flambeee, day by day

| Date | Channel | Format | Pillar | Asset | Topic | Hook (first line) | CTA | Owner |
|---|---|---|---|---|---|---|---|---|
| **Sun 11-08** | LT Bluesky | image | L1 | `lt-bsky-20261108-01` | What Lightsword is, what it costs, what it refuses (pinned intro; T01 quote card, new copy) | "Four roles, one nightly run, one gate. Lightsword is a marketing company that publishes its own numbers, including the bad ones." | "Follow; the 30-day plan is the first thing we publish." | Content Lead (Distribution Lead pins) |
| **Mon 11-09** | LT blog | link | L1 | `lt-blog-20261109-02` | The plan, in public, v2: what changed after the stall | "The first 30-day plan produced six posts and one follower. This is the plan that replaces it, with the numbers that made us rewrite it." | "Read the plan; reply with the one number you want us to publish next." | Content Lead |
| **Mon 11-09** | LT Bluesky | text post | L1 | `lt-bsky-20261109-01` | Six posts, one follower, zero replies: the stall in numbers | "We published six posts in three days. One follower. Zero replies. The plan was not the problem." | "Follow for the receipts; the fix starts here." | Content Lead |
| **Tue 11-10** | LT Bluesky | link | L1 | `lt-bsky-20261110-02` | The plan we are replacing it with (link to A00 v2) | "Our first plan produced six posts and one follower. The second starts with 10 conversations a week and a number we have to publish." | "Read it: lightsword.org/blog/..." | Content Lead |
| **Wed 11-11** | LT Bluesky | thread | L3 | `lt-bsky-20261111-01` | Our homepage said nothing auto-publishes. That stopped being true on 2026-11-05. (T02 correction card if the site fix is live; text-only otherwise) | "Our own homepage has been wrong for three days. It says every asset passes one human gate and nothing auto-publishes." | "If you find a stale claim on our site, reply with the URL." | Content Lead |
| **Thu 11-12** | LT blog | link | L3 | `lt-blog-20261112-01` | Four roles, one nightly run, one gate (Phase 2 truth) | "Four roles run this company. No office, no standups, and no human approval step." | "Read the roster; every role has a named output." | Content Lead |
| **Thu 11-12** | LT Bluesky | link | L3 | `lt-bsky-20261112-02` | The role that exists to disagree with the plan | "Four roles run this company. The one that matters most is the one that can say no." | "Read the post: lightsword.org/blog/..." | Content Lead |
| **Fri 11-13** | LT Bluesky | text post | L1 | `lt-bsky-20261113-03` | Week 1 receipt: planned, shipped, killed, missed | "Week 1: [posts] planned, [posts] shipped, [kills] killed, [corrections] correction. Followers: 1 before, [n] after." | "The run log is public." | Content Lead (Analyst supplies numbers) |
| **Fri 11-13** | FB Bluesky (staged) | image | F1 | `fb-blog-20261113-01` | Wordfire: one word a day | "One word a day. No install, no account." | "Play Wordfire: [game URL]" | Content Lead / Distribution Lead stages |
| **Fri 11-13** | FB Bluesky (staged) | image | F1 | `fb-bsky-20261113-02` | Afterglow: a memory maze you play in the dark | "The board lights up, goes dark, and takes moves from memory." | "Play Afterglow: [game URL]" | Content Lead / Distribution Lead stages |
| **Fri 11-13** | FB Bluesky (staged) | image | F1 | `fb-bsky-20261113-03` | Cinder: a new quest every UTC day | "A new quest every UTC day. Open the page and play." | "Play Cinder: [game URL]" | Content Lead / Distribution Lead stages |
| **Sat 11-14** | none | empty | — | — | Empty: weekend | — | — | Strategist |
| **Sun 11-15** | none | empty | — | — | Empty: weekend; weekly planning 20:00, day-7 rebaseline | — | — | Strategist |
| **Mon 11-16** | LT blog | link | L1 | `lt-blog-20261116-01` | What one published asset costs now | "One post, from brief to live: 40 minutes of wall clock, 0 minutes of approval. Here is where the 40 goes." | "Read the log." | Content Lead |
| **Mon 11-16** | LT Bluesky | link | L1 | `lt-bsky-20261116-01` | The old review number is retired | "The old plan said one asset costs 16 minutes of review. Phase 2 retired the review gate. Here is the real cost." | "Read it: lightsword.org/blog/..." | Content Lead |
| **Tue 11-17** | LT Bluesky | image | L2 | `lt-bsky-20261117-01` | The 19-pixel tap target (T06 metric card) | "Our nav links were 19 pixels tall. The minimum is 44. The fix is six lines of CSS." | "Check yours with a thumb; reply with a screenshot." | Content Lead |
| **Wed 11-18** | LT Bluesky | text post | L4 | `lt-bsky-20261118-01` | We do not ask for your account password | "Our first client posts on their own account. We draft, stage, and hand off. No password, no takeover." | "Read how the handoff works." | Content Lead |
| **Thu 11-19** | LT blog | link | L3 | `lt-blog-20261119-01` | The gate passed four drafts that were still wrong | "Four drafts passed the mechanical gate and were still unpublishable. The script checks words, not whether the sentence is still true." | "Read the check we added." | Content Lead |
| **Thu 11-19** | LT Bluesky | link | L3 | `lt-bsky-20261119-01` | A gate pass is not a fact check (T02 card) | "Four drafts passed our gate and were still wrong. The script checks words, not whether the sentence is still true." | "Read it: lightsword.org/blog/..." | Content Lead |
| **Fri 11-20** | LT Bluesky | text post | L1 | `lt-bsky-20261120-01` | Week 2 receipt and the provisional day-14 pillar read | "Week 2: [posts] shipped, [replies] replies, [followers] followers. Two weeks in, here is what the numbers say about each pillar." | "The log is public." | Content Lead (Analyst supplies numbers) |
| **Fri 11-20** | FB Bluesky (staged) | link | F2 | `fb-bsky-20261120-01` | The timer that lied about 7.5 minutes | "The timer ran 7 minutes while the field said 7.5. The fix shipped in v0.43.0." | "Read the note: [BLOG URL]" | Content Lead / Distribution Lead stages |
| **Fri 11-20** | FB Bluesky (staged) | text post | F1 | `fb-bsky-20261120-02` | Six small browser utilities | "Timer, Tally, Dice, Coin Flip, Convert, Day Pad. Six small tools that open in the browser." | "flambeee.com/apps/" | Content Lead / Distribution Lead stages |
| **Fri 11-20** | FB Bluesky (staged) | image | F1 | `fb-bsky-20261120-03` | Simon, with a colorblind mode | "Simon, with a colorblind mode. No install, no account." | "Play Simon: [game URL]" | Content Lead / Distribution Lead stages |
| **Sat 11-21** | none | empty | — | — | Empty: weekend | — | — | Strategist |
| **Sun 11-22** | none | empty | — | — | Empty: weekend; weekly planning writes week 3 rows | — | — | Strategist |

**Daily, not listed as rows:** the outbound block, 09:30-09:50 Mon-Fri, 2 replies + 2 follows. Logged in `queue/engagement/YYYY-MM-DD.md`, not in the content calendar. The first block is §8.

### 7.2 Calendar rules

1. Every non-empty row has a brief in `queue/briefs/` before the pre-flight. No brief, no asset.
2. Every non-empty row carries one pillar and one source line in the draft.
3. `[bracketed]` values in a receipt row are filled from the record at T-1 generation; never from memory or a guess.
4. flambeee rows are staging rows. `status: staged-awaiting-owner`; the client posts. No Lightsword credential.
5. The 11-10 link post has one fallback: if the blog page is not live by 18:45, it ships text-only with the three plan commitments and the link moves to 11-11. No GitHub link.
6. The 11-13 and 11-20 FB batches are three drafts each, staged by Friday 11:00 for the client's Mon/Wed/Fri 12:05 slots.
7. Empty rows are deliberate. No filler on any day. A weekend post must be grounded in the plan like any other; if it is not, the day stays `empty`.
8. Images use the `brand/visual/` templates; alt text is the matching line in `brand/visual/exports/alt-text.md`. T04 (client-work) is gated. No stock photography.

### 7.3 What is deliberately not in the calendar

| Not included | Why |
|---|---|
| LinkedIn posts | No page, no token (audit §6); deferral stands |
| Video / short-form | No asset budget (social plan §4.2); not a month-one capability |
| Paid promotion | No entity, privacy policy, or terms (brief §10) |
| Email/newsletter | No list, no MX record (audit B2) |
| Client results or case study | No measured baseline; naming is allowed, results are not |
| flambeee logo on Lightsword channels | Co-branding decision open with Jake (brief §10 #2) |
| T04 client-work card | Built and rendered in `brand/visual/`, but gated until Jake's co-branding sign-off (brief §10 #2); never a calendar row before then |
| Typewreck Game-of-the-Week campaign | 30-day deliverable #8, window 11-30..12-07; needs sign-off by 11-14. Not a 14-day row |
| Launch posts for new flambeee games | Triggered by a release, not by a date: verify releases on build days; publish within 24h of a qualifying ship (brief deliverable #4) |

### 7.4 Weeks 3-4 shape (the rest of the 30 days)

The 14-day table above is the detailed commitment. Weeks 3-4 are shaped here at week level; the Sunday planning job writes the dated rows and briefs on 11-15 and 11-22, using the same pillars and slots.

| Week | Dates | Lightsword Bluesky | Blog | flambeee staging | Notes |
|---|---|---|---|---|---|
| 3 | 11-23..11-29 | **7 posts (daily 19:00)** | 1 (Mon 11-23) | 3 drafts, Fri 11-27 batch | Daily rows below; A07 is the week's source article. Thanksgiving is a post day under the daily directive. |
| 4 | 11-30..12-06 | **7 posts (daily 19:00)** | 2 (Mon 11-30, Fri 12-04) | 3 drafts, Fri 12-04 batch | Daily rows below; A08 and A10 are the source articles. Day-21 checkpoint 11-29; day-28 check 12-06. |
| Close | 12-07..12-08 | 2 posts (Mon day-30 article, Tue receipt) | 1 (Mon 12-07) | — | Day-30 review 12-08 |

Totals across the window: **27 Lightsword posts, 8 blog articles, 12 flambeee drafts**
(39 social posts). That is six more Lightsword posts than the original 21, all
from the daily directive; no new pillar or product claim is introduced.

### 7.5 Daily rows, weeks 3-4 (2026-11-21 amendment)

The Sunday planning job writes these rows and a brief for every non-empty row.
Each post ships at 19:00 America/Chicago. The source column is the grounding for
the brief; bracketed values are read at T-1 and are never invented.

| Date | Channel | Pillar | Asset | Working title | Type | Source |
|---|---|---|---|---|---|---|
| Mon 11-23 | LT blog | L1 | `lt-blog-20261123-01` | A07 Three weeks in: what the run log says about us | source | `metrics/*`, `logs/nightly.ndjson`, `published/manifest.ndjson` |
| Mon 11-23 | LT Bluesky | L1 | `lt-bsky-20261123-01` | Three weeks in: [n] planned, [n] live, [n] held | derived | `lt-blog-20261123-01` (A07) |
| Tue 11-24 | LT Bluesky | L1 | `lt-bsky-20261124-01` | The number that did not move | derived | A07; `metrics/2026-11-23.json` vs `metrics/2026-11-09.json` |
| Wed 11-25 | LT Bluesky | L3 | `lt-bsky-20261125-01` | Six followers is not a sample | source | `reports/campaign/2026-11-19-reach-final.md` §Unavailable measurements |
| Thu 11-26 | LT Bluesky | L1 | `lt-bsky-20261126-01` | The run does not take holidays | source | `workflows/nightly-2200.md`; cron job `b83aa855e26a` |
| Fri 11-27 | LT Bluesky | L1 | `lt-bsky-20261127-01` | Week 3 receipt: shipped, held, skipped | derived | `logs/nightly.ndjson`, `published/manifest.ndjson` |
| Sat 11-28 | LT Bluesky | L3 | `lt-bsky-20261128-01` | The part of the plan that is not automated | source | `workflows/weekly-plan-sunday.md`, `plans/calendar-30d.md` |
| Sun 11-29 | LT Bluesky | L2 | `lt-bsky-20261129-01` | What the reply cap costs | source | `AGENTS.md` rule 7; `logs/bsky-actions.ndjson` |
| Mon 11-30 | LT blog | L3 | `lt-blog-20261130-01` | A08 Cadence math: why nine posts became this | source | this document §5-§6; `plans/posting-schedule.md` |
| Mon 11-30 | LT Bluesky | L3 | `lt-bsky-20261130-01` | Cadence math: the daily slot is not a daily post | derived | `lt-blog-20261130-01` (A08) |
| Tue 12-01 | LT Bluesky | L3 | `lt-bsky-20261201-01` | The post we did not write | derived | A08; `plans/posting-schedule.md` §4 |
| Wed 12-02 | LT Bluesky | L3 | `lt-bsky-20261202-01` | The cost of a daily anything | source | `plans/posting-schedule.md` §3; `workflows/nightly-2200.md` |
| Thu 12-03 | LT Bluesky | L3 | `lt-bsky-20261203-01` | A daily schedule is not a daily post | source | `plans/posting-schedule.md`; `reports/campaign/2026-11-19-reach-final.md` rec. 5 |
| Fri 12-04 | LT blog | L2 | `lt-blog-20261204-01` | A10 What thirty reply drafts taught us | source | `queue/replies/*`, `logs/bsky-actions.ndjson` |
| Fri 12-04 | LT Bluesky | L2 | `lt-bsky-20261204-01` | The reply that needed a position | derived | `lt-blog-20261204-01` (A10) |
| Sat 12-05 | LT Bluesky | L2 | `lt-bsky-20261205-01` | Week 4 receipt: the replies, the holds, the silence | derived | `logs/nightly.ndjson`, `queue/replies/*` |
| Sun 12-06 | LT Bluesky | L1 | `lt-bsky-20261206-01` | Day 28: three numbers with denominators | source | `metrics/*`, `reports/weekly/*` |
| Mon 12-07 | LT blog | L1 | `lt-blog-20261207-01` | A11 Day 30: what we're killing | source | `reports/weekly/*`, day-30 review |
| Mon 12-07 | LT Bluesky | L1 | `lt-bsky-20261207-01` | Day 30: the plan that ends, and what replaces it | derived | `lt-blog-20261207-01` (A11) |
| Tue 12-08 | LT Bluesky | L1 | `lt-bsky-20261208-01` | Three numbers, each with its denominator | derived | A11; `metrics/*`, `reports/weekly/*` |

The 2026-11-21 and 2026-11-22 rows stay `empty`: the directive landed after
those rows were written, and the first daily post is 2026-11-23 19:00. The
client (flambeee) rows are unchanged: 3 staged drafts a week, client posts at
12:05. Daily client posting needs a new written window (`plans/scope-flambeee.md`
§14), and the bot cannot waive it.

---

## 8. The first 24 hours

### 8.1 The single highest-impact action: open the front door

**The action: open the front door — a pinned intro post, the naming bio, and substantive replies at a capped, human rate. The cap is AGENTS.md rule 7 (operator directive 2026-11-08): at most 5 replies in any 24 hours, at least 10 minutes apart, never more than 2 in one thread. A burst of 10 replies in an hour reads as spam to the platform and to the reader; the platform acts on it. Start the block within 24 hours of this plan landing and let it run over two days rather than one. The setup it needs — one pinned intro post, the naming bio, 20 follows — is in §8.2 and takes less than an hour.**

Why this one, and not the site fixes: with 1 follower and 0 replies, more posts cannot compound. The site fixes convert traffic that does not exist yet; this action creates the first traffic. A pinned post turns every profile visit into a follow decision, and 10 replies put the account in front of people who already care about small products and browser games. It is the only action in the plan that changes the denominator.

### 8.2 Done when

1. `lt-bsky-20261108-01` is live, and `app.bsky.actor.getProfile` returns its URI as `pinnedPost`.
2. The bio carries variant A exactly as staged: "Lightsword — clear marketing for small product teams. First client: flambeee. lightsword.org" (scope §2, granted 2026-11-07; `~/share/lightsword-handoff-2026-11-05/bluesky/profile-update.json`). The bot applies it under Phase 2. No logo, no results claim. If the profile write is rejected, record a WARNING and continue: the bio is setup, not the action.
3. Replies are sent from `@lightsword.bsky.social` at the AGENTS.md rule 7 rate: at most 5 in any 24 hours, ≥10 minutes apart, one specific observation each, no link, no pitch. URLs are logged in `queue/engagement/YYYY-MM-DD.md`. Five per day over two days, not ten in one sitting.
4. Follows stay under 20 per day, including `@flambeee.bsky.social`; the list is logged in the same file.
5. No reply touches pricing, an outage, a complaint, or a person. Those escalate per `plans/scope-flambeee.md` §4.

### 8.3 What not to do in the first 24 hours

- Do not publish the stale A00 blog draft. Its copy says "one human gate" and "nothing auto-posts"; it is false (Appendix B).
- Do not post a thread, a launch, or a "we are back" announcement. One post, then conversations.
- Do not dump the week's content in one burst. The 11-06 four-in-one-minute burst is the failure this plan exists to stop.
- Do not link to GitHub plan files.
- Do not wait for the site fixes, the analytics tag, or the client cadence amendment. None of them gate this action.

### 8.4 The rest of day one, in order

1. Post and pin `lt-bsky-20261108-01`; verify `pinnedPost`.
2. Update the bio to variant A; verify with `getProfile`.
3. Find threads with `app.bsky.feed.searchPosts` on `#gamedev`, `#indiedev`, `#buildinpublic`, and `browser game`. Reply only where there is a specific observation. Follow the authors you reply to, plus `@flambeee.bsky.social`; log the 20 handles.
4. Send the 10 replies; log the URLs and the one-line reason for each.
5. Open the 11-09 briefs and confirm the blog live check for 08:45 Monday.

---

## 9. Deliverables

### 9.1 Client deliverables (brief §6)

| # | Deliverable | Due | Owner | Status 11-08 |
|---|---|---|---|---|
| 1 | Claims list `brand/claims-flambeee.md` | Sat 11-14 | Content Lead; Strategist review | Not started |
| 2 | Voice sheet `brand/voice-flambeee.md` | Sat 11-14 | Content Lead; Ember sign-off | Not started |
| 3 | 12 flambeee Bluesky drafts, 3/week, staged | Batches 11-13, 11-20, 11-27, 12-04 | Content Lead → Distribution Lead | 2 staged from week 1; 0 on the new cadence |
| 4 | 2 Lightsword launch posts for new-game days | Within 24h of each release; first checkpoint 11-13 | Content Lead → Distribution Lead | 0; release-triggered |
| 5 | Copy defect list to Ember | Thu 11-12 | Strategist | Not started |
| 6 | Asset gap list and requests | Sat 11-21 | Content Lead | Not started |
| 7 | Weekly proxy report | Fri 11-13, 11-20, 11-27, 12-04 | Analyst | Template not written |
| 8 | Typewreck GOTW campaign window | Mon 12-07; sign-off requested by 11-14 | Strategist + Content Lead | Decision open with Jake |
| 9 | Day-30 review | Tue 12-08 | Analyst + Strategist | Scheduled |

Floor: **7 of 9** are unconditional (1, 2, 3, 5, 6, 7, 9). #4 depends on client releases; #8 depends on Jake's sign-off. Both are reported with their actual count, never as a miss hidden in a percentage.

### 9.2 Lightsword deliverables

| Deliverable | Due | Owner | Status 11-08 |
|---|---|---|---|
| This plan, published as `plans/growth-plan-30d-2026-11-08.md` | 11-08 | Strategist | Done |
| Calendar rows 11-08..11-22 in `plans/calendar-30d.md` | 11-08 | Strategist | Done with this plan |
| Visual kit: six formats, alt text, render script (`brand/visual/`) | 11-08 | Content Lead | Landed (t_0d6141f0); T04 gated |
| Site integrity: 0 broken downloads (retire `/downloads/` per `plans/site-refresh-spec.md`, or 7/7 fixed), gate copy corrected, CTA, favicon/OG, 404 page, 0 "Pending." cards | 11-14 | Content Lead / Distribution Lead | Spec landed (`plans/site-refresh-spec.md`); execution in t_fc324943 |
| First blog article live | 11-09 | Content Lead | Draft exists; re-draft required (stale) |
| 8 blog articles live | 12-08 | Content Lead | 0 |
| 4 weekly reports | 11-13, 11-20, 11-27, 12-04 | Analyst | 0 |
| Day-30 review | 12-08 | Analyst + Strategist | Scheduled |

The site-integrity work is a parallel workstream, not a calendar dependency. No post waits on it; the 11-11 correction thread is publishable whether or not the site copy has deployed.

---

## 10. Dependencies and open decisions

**No calendar row in §7 is blocked on an unresolved dependency.** This table is the evidence.

| Dependency | State 11-08 | Does a calendar row wait on it? | Workaround in force |
|---|---|---|---|
| Analytics tag / Search Console (B1) | Absent | No | Record `unavailable`; rebaseline 11-15; no traffic claim until instrumented |
| Contact email / MX (B2) | Absent | No | Every CTA is a Bluesky reply or profile follow; no email ask |
| Site deploy trigger (B3) | Cloud cron, no trigger, latency unknown | No | Blog rows verify live by 18:45; text-only fallback; no GitHub link |
| Custom Bluesky handle (B4) | Absent | No | `.bsky.social` handle used |
| Scheduler / Postiz (B5) | Absent | No | Native API publishes; manifest appended; WARNING in digest |
| LinkedIn (B6) | Deferred | No | Removed from the plan |
| flambeee cadence amendment | Open, target 11-12 | No | Lightsword stages 3 drafts/week; the client posts what it chooses |
| flambeee co-branding / logo | Open, target 11-14 | No | Text naming only; no logo on Lightsword channels |
| Typewreck campaign sign-off | Open | Not in the 14-day calendar | Request by 11-14; deliverable #8 reports actual status |
| Paid promotion | Blocked | No | Organic only |
| Client FB approval per item | Owner-side | No | Drafts stage; client clears and posts |

**What is genuinely blocked, and therefore not promised:** paid promotion, LinkedIn presence, email lead capture, co-branded case study, and any client-results claim. These are out of the plan, not hidden inside it.

---

## 11. Measurement and review

### 11.1 Definitions

- **Post:** an original `app.bsky.feed.post` record published by the account. Replies and reposts are not posts.
- **Interaction:** like + repost + reply + quote on an original post. Counts from `app.bsky.feed.getPosts`, not the AppView feed (the audit found the feed returned 3 of 6 records; the PDS is the source of truth).
- **Average engagement per post:** interactions ÷ original posts, over posts **at least 72 hours old**. The denominator is printed.
- **Engagement rate:** interactions per post ÷ follower count at the measurement date. Printed with the follower count, never alone.
- **Site session:** a Umami session on `lightsword.org`. Until the tag exists: `unavailable`, not 0.
- **Outbound action:** a substantive reply or a follow from `@lightsword.bsky.social`, logged with URL or handle and a one-line reason.
- **On-time post:** published on its calendar date, in its slot, ±60 minutes. A missed slot is recorded, not hidden.

### 11.2 Rhythm

| When | Who | What |
|---|---|---|
| Daily 22:00 | Analyst | Snapshot: followers, posts, interactions, `unavailable` fields with reasons |
| Friday 16:00 | Analyst | Weekly report: 6 numbers, one paragraph on what worked, one on what did not, one decision |
| Sunday 20:00 | Strategist | Next week's rows and briefs; review the weekly report |
| Day 7 (11-15) | Analyst | Site-traffic rebaseline from the first five instrumented days |
| Day 14 (11-22) | Strategist + Analyst | Pillar check: keep/cut by interactions per post, not by opinion |
| Day 30 (12-08) | Analyst + Strategist | Plan vs actuals; keep/kill recommendation; month-2 input |

### 11.3 What is never reported

- Follower count alone as success.
- Impressions or reach (not available from the Bluesky API).
- Engagement rate without its denominator.
- A site session number while the tag is absent.
- "Growing", "viral", or any adjective standing in for a number.

`unavailable` is a valid result. An invented number is not.

---

## 12. Risks and kill criteria

| Risk | Signal | Response |
|---|---|---|
| Outbound reads as spam | Replies get no engagement; follows do not return | Cut to 5 actions/week, reply only to threads where we have a specific observation; never use a template |
| Cadence outruns quality | First-pass gate rate <70% for two weeks | Cut the blog to 1/week first; never cut the gate or the Currency Check |
| Blog deploy latency | Page not live by 18:45 on a publish day | Text-only post; move the link to the next slot; log the deploy latency |
| Stale copy ships | A draft contains "human gate", "phase 1", "nothing auto-publishes", or LinkedIn | Currency Check fails; Strategist adjudicates; re-draft |
| Client cadence amendment delayed | No Jake amendment by 11-12 | Staging continues; client posts release notes only; log the gap |
| Audience mismatch | <6 Lightsword followers by day 7 | Change the L2 examples from marketing fixes to product-page fixes for game/app teams; keep the pillar |
| Traffic target is fiction | Tag not live by 11-10 | Withdraw the numeric target; report the instrument gap as the failure; no traffic claim |

**Kill criteria.** A pillar with fewer than 0.3 interactions per post across at least 3 posts is cut or re-briefed at the day-14 review. A pillar with fewer than 3 posts gets its review at day 21, not day 14. A slot with no measured difference by day 21 moves. No slot survives week four without data.

---

## 13. Acceptance check

| Requirement | Where |
|---|---|
| Positioning and a one-line value proposition for Lightsword and flambeee | §2.1, §2.2 |
| Numeric targets traceable to the audit baseline | §3.1, §3.2, Appendix A |
| Day-by-day calendar for 14 days with date, channel, format, topic, hook, CTA, owner | §7.1 (15 days, 25 rows) |
| Posting cadence and 3-5 repeatable pillars | §5, §6 |
| Single highest-impact action in the first 24 hours | §8 |
| No item blocked on an unresolved dependency | §10 |
| Every calendar entry has a date, format, and topic | §7.1 (empty rows carry `empty` + reason) |

---

## Appendix A — Baseline ledger

All values below are from `reports/audit/2026-11-08-baseline.md` unless marked otherwise.

| Metric | Value | Audit location |
|---|---|---|
| LT Bluesky followers | 1 | §2.1 |
| LT Bluesky following | 2 | §2.1 |
| LT Bluesky posts | 6 | §2.1 |
| LT total interactions | 0 (0 likes, 0 reposts, 0 replies, 0 quotes) | §2.1, §4.2 |
| LT average interactions per post | 0.0 | §2.1 |
| LT posts with media | 0 of 6 | §2.1 |
| LT posts with link facet | 4 of 6, all GitHub plan files | §2.1, §4.3 |
| LT last post | 2026-11-07 05:22 CST | §2.1 |
| LT pinned post | none | §2.1 |
| LT followers trend | 1 / 1 / 1 / 1 on 11-05..11-08 | §2.1 |
| Website pages | 3 | §2.2 |
| Blog articles live | 0; 6 "Pending." cards | §2.2 |
| Broken download links | 7 of 7 | §2.2, §3.3 W1 |
| Analytics tag | absent | §2.2, W5 |
| Favicon / OG tags | absent / 0 | §2.2, W7, W9 |
| Site traffic | `unavailable` | §2.2, W5 |
| flambeee Bluesky followers / posts | 4 / 41 | brief §6 |
| flambeee GitHub stars | 0 | brief §6 |
| flambeee repo views (14d) | 26 views / 1 unique | brief §6 |
| flambeee external humans (lifetime) | 2 | brief §6 |
| Client deliverables shipped | 0 of 9 | brief §6 |

---

## Appendix B — Stale asset quarantine

The gate is mechanical. These files carry a gate pass and are still not publishable.

| Asset | State | Why it cannot ship | Action |
|---|---|---|---|
| `queue/drafts/lt-blog-20261109-01.md` | Gate pass; social variant published 11-06; blog never published | Says "one human gate", "Jake approves each asset", "nothing auto-posts in phase 1"; nine posts/week includes LinkedIn | Do not publish. Re-draft as `lt-blog-20261109-02` |
| `queue/drafts/lt-bsky-20261110-01.md` | Published 11-06 | "16 minutes of review" framing is Phase 1; LinkedIn variant dead | Consumed. Do not reuse |
| `queue/drafts/lt-blog-20261111-01.md` | Gate pass; never published | Says Jake is "the only human approver, and his gate is publish" | Do not publish. Re-draft as `lt-blog-20261112-01` |
| `queue/drafts/lt-bsky-20261112-01.md` | Published 11-06 | Phase-1 review framing; LinkedIn variant dead | Consumed. Do not reuse |
| `queue/drafts/lt-bsky-20261113-01.md` | Published 11-07 | Accurate receipt, but the numbers are week 1 as of 11-07 | Consumed. Do not republish |
| `queue/drafts/lt-bsky-20261113-02.md` | Published 11-07 | Naming note; permission is recorded | Consumed. Do not republish |
| `queue/drafts/fb-blog-20261113-01.md` | Gate pass; JSON staged 11-13 | Reusable; Wordfire copy is current | Keep; use as `fb-blog-20261113-01` |
| `queue/drafts/fb-bsky-20261115-01.md` | Gate pass; JSON staged 11-15 | Reusable; re-slot into the 11-13 batch | New id `fb-bsky-20261113-02`; re-run gate; mark `queue/social/2026-11-15-fb-bsky-1.json` superseded and do not hand it to the client |
| `queue/social/2026-11-10-linkedin-1.json`, `2026-11-12-linkedin-1.json` | Staged | LinkedIn is not available this month | Mark `status: dead`; do not publish |
| `queue/social/2026-11-09-bsky-1.json` through `2026-11-13-bsky-2.json` | Published 11-06/11-07 | Already live; not future rows | Archive; do not republish |

**Rule:** a gate pass means "no banned words, no unsourced number the script can see, sources section present". It does not mean "still true". The Currency Check (§6.4) is the second half of that judgment, and the Strategist owns it.

---

## Appendix C — Immediate operating checklist (today)

1. Write the 11-08/11-09 rows into `plans/calendar-30d.md`; mark 11-09..11-13 old rows as consumed in the notes (done with this plan).
2. Write `queue/briefs/2026-11-09-stall-receipt.md` and the brief for `lt-blog-20261109-02` (done with this plan).
3. Patch `plans/social-media-plan.md` §8 with the supersession notice so the Sunday job does not re-add the old rows (done with this plan).
4. Quarantine the stale drafts per Appendix B; do not delete them.
5. Execute §8: publish, pin, bio, 20 follows, 10 replies. Log the replies.
6. Verify `pinnedPost` and the bio through the API before calling the action done.
7. At 20:00 the weekly planning job runs; it should find one row per date for 11-09..11-15 and write any missing brief.
8. At 22:00 the nightly runs; the 11-09 row must resolve to the new briefs, not the old A00 brief.

---

*Written 2026-11-08 by the Strategist role for task t_deac80df. Inputs: the 2026-11-08 footprint audit (t_80de805d) and `plans/client-brief-flambeee.md` v1.0 (t_2cb5b910). No flambeee internal file, persona, prompt, workflow, cron, database, or asset was read or reused. Client claims trace to `plans/client-brief-flambeee.md` and its public-surface verification log.*
