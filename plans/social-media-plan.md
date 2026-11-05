---
title: Lightsword social media presence and content plan
status: draft for Jake
owner: Strategist (account lead)
created: 2026-11-04
window: 2026-11-09 to 2026-12-08
inputs: docs/marketing-company-research.md, personas/00-index.md
---

# Lightsword social media plan

Thirty days, two brands, one pipeline, one human gate.

## 1. The one screen

| Decision | Ruling |
|---|---|
| Platforms | Bluesky active for both brands. LinkedIn maintained for Lightsword. Blog is the owned spine. Nothing else in month one. |
| Cadence | 9 posts a week in a normal week. 12 source assets and 35 social posts across 30 days. |
| Pillars | Three per brand, each tied to something already documented. No pillar, no row. |
| Channels | Two. Lightsword's own accounts and flambeee's accounts. Same pipeline, different gates. |
| flambeee | Not named on Lightsword's channels until permission is recorded. Amplify only, never announce first. |
| Human cost | About 3 hours of Jake's week. That is the binding constraint, not compute. |
| Not happening | Video, X, paid, hashtags, engagement bait, auto-posting, a fifth platform. |

The reason this plan is narrow is not caution. A 22:00 job with four roles and one reviewer can hold nine posts a week at a quality worth reading. It cannot hold thirty. The failure mode of a content plan is not too few posts, it is a month of posts nobody would miss.

## 2. What this plan is not

It is not the 90-day plan. It does not set the deciding metric, the retainer, or the scope document. The Strategist owns those.

It is not a channel strategy for client two. Every rule here is written so that it survives flambeee firing Lightsword, because the habits set on the captive first client are the ones the second client inherits.

It is not a growth forecast. There is no baseline on either site today, so there is no honest reach target to print. Month one produces a baseline and a publishing record. Numbers come after.

## 3. Two channels, one pipeline

The card asks for Lightsword's social presence and for how flambeee will be represented. Those are two different jobs that share a machine, and conflating them is the most likely way this goes wrong.

| | Channel A: Lightsword's own | Channel B: flambeee's |
|---|---|---|
| Whose voice | Lightsword's operator voice | flambeee's player voice |
| Who drafts | Content Lead | Content Lead, from flambeee's public docs |
| Who approves | Jake | flambeee's owner, then Jake |
| Approval records | `state/lightsword.db` `approvals` | Separate rows, same table, different `client` key |
| Can name the other | Only after written permission | It is their own brand, so yes |
| Failure if merged | The agency's voice eats the client's | A client post commits the client to something it did not decide |

Channel B has two humans in the chain even when one person holds both roles today. The records stay separate on purpose. If the approval trail for client work looks identical to the approval trail for house work, the company has learned a habit it cannot bill for and cannot survive client two with.

**Consequence worth stating:** Lightsword's own channels carry no client results for the first 45 days. A brand new company posting "our client grew 40%" is either lying or lucky, and both are worse than silence. What it can post is its own operating record, which is real from week one.

## 4. Platforms

### 4.1 Chosen

| Platform | Brand | Why this one | Account state today | Cost | Path |
|---|---|---|---|---|---|
| Bluesky | Lightsword | Free API with no paywall, no link suppression worth designing around, and a text-first format that fits a 16-minute asset. Postiz supports it natively. The indie-dev and small-web-games audience is actually there. | Does not exist | $0 | Native API, drafts only in phase 1 |
| Bluesky | flambeee | Same reasons, plus the audience overlap is direct: people who play a browser game in one tap are the people scrolling Bluesky. | Does not exist | $0 | Same |
| LinkedIn (company page) | Lightsword | The buyer of a marketing retainer checks LinkedIn before they reply to an email. Two posts a week keeps the page from looking abandoned. | Does not exist | $0 | Postiz if page API access is granted, manual otherwise |
| Owned: `lightsword.org` blog | Lightsword | The canonical asset. Social posts derive from it. Without an owned spine, every post is disposable and unmeasurable. | Exists, but is a game-downloads page, not a company site | $0 | Static, Caddy |
| Owned: flambeee blog and releases | flambeee | Already publishing. Lightsword amplifies it, does not author it. | Live, sessions 47 to 50 in `BLOG.md` | $0 | No write access |

Two active platforms, one maintained, one owned spine. That is the whole stack.

### 4.2 Rejected, with the reason and the trigger to revisit

| Platform | Why not now | Revisit when |
|---|---|---|
| X / Twitter | API cost and rate limits against a tooling budget capped at 5% of retainer, plus link treatment that punishes exactly the posts this plan writes. | A paying client requires it, in writing |
| Instagram, TikTok, YouTube Shorts | Video. A 16-minute asset budget cannot produce a video that is not embarrassing, and no faces of real people without releases. This is the plan's largest real gap, not a claim that video does not work for games. | A one-off launch video with a separate budget, or 30 qualified sessions a week sustained for two weeks |
| Facebook | No audience for either brand, and page posting is a permissions project for zero return | Never, unless a client's audience is there |
| Threads | Same production problem as Instagram with a thinner API story | Same as Instagram |
| Mastodon | Cheap to post to and doubles the reply surface for near-zero reach. One fediverse presence is enough at this volume. | flambeee's audience shows up there |
| Reddit | Not a broadcast channel. A new account posting game links gets removed in week one and the removal is permanent. | Monitoring only, starting week 2 |
| Hacker News | A launch event, not a cadence. Belongs in a launch plan, not a content calendar. | A launch worth one shot, with Jake |
| Newsletter | Needs a list and a list needs traffic. Month three. | 200 email signups |
| Paid social | No baseline, no creative inventory, no budget justification. Already cut in the research brief. | Month four, with numbers |

### 4.3 The video gap, stated plainly

Short-form video is where consumer web games get discovered. This plan does not do it, and that is a choice forced by the asset budget rather than a judgment that it does not work. If month one shows social traffic worth scaling, video is the first place the next dollar and the next skill should go, not a fifth text platform. Writing it down here so nobody later mistakes the omission for an oversight.

## 5. Cadence

### 5.1 The constraint is review minutes, not generation

The nightly run can generate three assets a night, which is twenty-one a week. This plan uses about a third of that. The real limit is Jake: at sixteen minutes per published asset, forty-seven assets in thirty days costs about twelve and a half hours, roughly three hours a week.

| Resource | Weekly capacity | This plan uses | Headroom |
|---|---|---|---|
| Content generation (3/night cap) | 21 assets | 3 source assets plus 6 short posts | 12 |
| Human review (16 min/asset) | Not capped, but it is the scarce thing | ~12 assets, ~3.2 h | The only number worth watching |
| Distribution staging (10 min/night) | 70 min | ~20 min | Large |

If a week comes in over four hours of Jake's time, the fix is the brief or the cadence, never a faster review.

### 5.2 Per platform

| Channel | Posts/week | Days | Slot (America/Chicago) | Status |
|---|---|---|---|---|
| Lightsword Bluesky | 4 | Mon, Tue, Thu, Fri | 09:00 | Active |
| flambeee Bluesky | 3 | Wed, Fri, Sun | 17:30 | Active |
| Lightsword LinkedIn | 2 | Tue, Thu | 07:30 | Maintained |

LinkedIn is maintained rather than active for month one. That is a deliberate deviation from the three-to-four-a-week floor, and the reason is that a page with two substantive posts a week reads as a real company while a page with four thin ones reads as a content farm. It gets promoted to active the first week LinkedIn produces one qualified session.

Slots are a starting hypothesis, not a finding. There is no traffic data on either brand, so the first two weeks of the Analyst's numbers move them. No slot survives week four without a measured difference, and no slot is defended on vibes.

### 5.3 Why nine and not thirty

Nine posts a week is one and a quarter a day. Thirty would need either four assets a night at review quality, or a reviewer who skims. Both produce the same outcome: a feed that looks busy and converts nothing, plus a reviewer who stops reading carefully around week three, which is precisely how an unapproved claim eventually ships.

The brief's cadence floor is three to four posts a week per active platform. Nine across two active platforms sits at the floor by design, not below it.

### 5.4 The weekly rhythm, mapped to the nightly run

| When | Who | What |
|---|---|---|
| Sunday 20:00 | Strategist | Write next week's calendar rows and briefs for the seven days starting Monday |
| Sunday 21:55 | Strategist | Pre-flight: tomorrow has a row and a brief |
| Sunday 22:20 | Content Lead | Generate Monday's source asset plus its social variants |
| Monday 08:00 | Jake | Approve or reject. Rejections carry a reason code. |
| Monday 09:00 | Distribution | Post goes out. Manifest appended. |
| Tue to Fri | same loop | T-minus one night for each day's asset |
| Friday 22:50 | Analyst | Weekly report: four numbers, one paragraph, one recommendation |

**One amendment this plan requires.** The Strategist persona puts weekly planning at Monday 09:00. That cannot work: Monday's post has to be generated Sunday night, which means the calendar row and brief must exist by Sunday 21:55. Weekly planning moves to Sunday 20:00 for the week starting the next day, and Monday 09:00 stays as the client-facing status note. This is an open item for the workflow task (t_7070f858) and a one-line change to the Strategist persona.

### 5.5 Empty slots are rows too

The 21:55 pre-flight halts generation when tomorrow has no calendar row. That is correct and it means every day needs a row, including days with no post. Empty rows carry `type: empty` and a reason. A pre-flight that passes on a deliberate blank is a working gate. A pre-flight that fails every Saturday gets muted by week two.

## 6. Content pillars

Three per brand, each tied to something that already exists and can be cited. A pillar with no proof source is a mood, and a mood produces filler.

### 6.1 Lightsword: the operator's three

| Pillar | What it is | The truth it rests on | What it looks like |
|---|---|---|---|
| **L1 Receipts** | The company's own operating numbers, published | Every run logs inputs, outputs, duration, and human minutes | "Last week: 9 posts staged, 2 killed at the gate, 11 minutes of my time each" |
| **L2 Cuts** | What was refused and why | The gate fails closed, and the writer cannot clear its own failure | "Three claims died this week. Here is the one that cost a night." |
| **L3 Craft** | How one marketing decision gets made, with its cost | Judgment is the product. Output is a byproduct. | "Why we post nine times a week and not thirty" |

L1 is the differentiator. Almost no agency publishes its own cost per asset and its own gate failures. It is credible from week one because it needs no client result, only a run log.

L2 is the trust builder. A company that shows what it killed is a company whose published claims are worth reading.

L3 is the sales pillar. It demonstrates the judgment a retainer buys, which is the thing a prospect cannot evaluate from a portfolio.

### 6.2 flambeee: the player's three

| Pillar | What it is | The truth it rests on | What it looks like |
|---|---|---|---|
| **F1 Zero friction** | No account, no install, one tap | flambeee.com and README: "No sign-up, no download, no paywall" | "The whole arcade. Zero accounts. Open the link and play." |
| **F2 The session log** | The honest fix note | `BLOG.md` sessions 47 to 50, published per release | "The timer was lying about decimals. Here is the fix, in one plain line." |
| **F3 One idea per game** | Small and sharp, one mechanic done well | Echo Rounds shipped as "the smallest playable answer" | "One room, one mechanic, one trade-off per shot" |

These are not invented positioning. F2 in particular is a gift: flambeee already publishes the kind of writing most studios never do, and the social job is to point at it rather than rewrite it.

### 6.3 The pillar test

Every calendar row names exactly one pillar. A row without one fails validation. A row that needs two is two rows, and probably neither is worth a night.

## 7. Voice and tone

### 7.1 Lightsword house voice

Plain, specific, and willing to be unflattering about itself. Numbers before adjectives. Short sentences. If a post could have been written by any agency, it should not go out.

| Rule | Why |
|---|---|
| One claim per post, maximum | Two claims in 300 characters is zero claims remembered |
| A number, or a named decision, in every post | Otherwise it is a mood |
| Say what did not work in the same post as what did | Half a record is a sales pitch |
| No hashtags | They are a tell, and they do not move qualified sessions at this volume |
| No emoji rows, no thread emoji, no thread hooks | "🧵" is engagement bait wearing a costume |
| 300 characters on Bluesky. If it needs more, it is a three-post thread or a blog post. | Format discipline produces the clarity |
| Never speak as Jake, never first-person singular | The company did the thing, or nobody did |
| No claim without a baseline | The Analyst's first rule, applied to copy |

We say, we do not say:

| Not this | This |
|---|---|
| "Excited to announce our new AI marketing stack" | "Nine posts a week, drafted at 22:00, approved by one human at 08:00. Here is what that cost." |
| "We leverage AI to unlock growth" | "One published asset costs sixteen minutes of review. That is the whole budget." |
| "Our client saw 3x engagement" | "Week 2: fourteen qualified sessions from social. Baseline was zero." |
| "Coming soon" | Nothing. There is no post. |

Banned outright: excited, thrilled, leverage, unlock, game-changer, revolutionary, seamless, robust, cutting-edge, "in today's fast-paced landscape", and any sentence that begins with "We're proud to".

### 7.2 flambeee voice, derived and not invented

Taken from flambeee's own public writing, which is the only permitted source. Three real examples:

- "The Timer app had a quiet lie: type 7.5 minutes, press Start, and the clock ran 7 minutes while the field kept claiming 7.5, with no note anywhere."
- "Smallest visible fix we could ship."
- "It is the smallest playable answer to the biggest question on our roadmap."

What that voice does: names the defect in the first clause, uses concrete numbers, admits the embarrassment, refuses the adjective, and ends on what shipped. Dry, not cute. Specific, not clever.

Casing follows their own usage: `flambeee` in prose, `Flambeee` only at the start of a sentence, as their site and blog already do.

### 7.3 The failure this prevents

An agency that writes every client in the agency's voice is the most common way small agencies lose clients. Two voice documents, not one: `brand/voice.md` for Lightsword and `brand/voice-flambeee.md` for the client. The gate checks a draft against the voice doc for its own channel, and a Lightsword-voice sentence on flambeee's account is a gate failure, not a style note.

### 7.4 Format rules

| Item | Rule |
|---|---|
| Bluesky | 300 characters. Link in the post, not a reply chain. Alt text on every image, written by the Distribution Lead. |
| LinkedIn | 900 characters maximum. First line must stand alone, because that is all most people see. No "comment YES". |
| Images | Generated locally via ComfyUI or captured from the product. No stock. No faces of real people without a release. |
| Links | UTM-tagged: `utm_source`, `utm_medium=social`, `utm_campaign=<pillar>`, `utm_content=<asset-id>` |
| Replies | Human-sent for the first 60 days. Never a template. |

## 8. The 30-day calendar

**Schema.** `date | channel | pillar | asset-id | working title | type | source | owner`

`type` is one of `source` (a long-form asset that publishes to the blog and generates variants), `derived` (a social post cut from a source asset, format only), or `empty` (a deliberate blank with a reason).

`asset-id` follows `<client>-<channel>-<yyyymmdd>-<nn>`: `lt` for Lightsword, `fb` for flambeee.

### 8.1 Day by day

| Day | Date | What goes out | Channel | Pillar | Asset-id |
|---|---|---|---|---|---|
| 1 | Mon Nov 9 | **A00 The plan, in public**: what Lightsword is doing for 30 days, and what it will not do | LT blog + LT Bluesky | L3 | `lt-blog-20261109-01` |
| 2 | Tue Nov 10 | Derived from A00: one gate, one human, sixteen minutes | LT Bluesky + LinkedIn | L1 | `lt-bsky-20261110-01` |
| 3 | Wed Nov 11 | **A01 Four roles, one cron, one gate**: the staff behind a 22:00 company | LT blog + LT Bluesky | L3 | `lt-blog-20261111-01` |
| 4 | Thu Nov 12 | Derived from A01: the role that exists to disagree with the plan | LT Bluesky + LinkedIn | L2 | `lt-bsky-20261112-01` |
| 5 | Fri Nov 13 | **A02 The arcade with no login**: every game, one tap | FB long copy + FB Bluesky | F1 | `fb-blog-20261113-01` |
| 5 | Fri Nov 13 | Week 1 receipt: what the gate killed | LT Bluesky | L1 | `lt-bsky-20261113-01` |
| 6 | Sat Nov 14 | empty: weekend | none | — | — |
| 7 | Sun Nov 15 | Derived from A02: the games load in seconds, here is why that is the whole product | FB Bluesky | F1 | `fb-bsky-20261115-01` |
| 8 | Mon Nov 16 | **A03 The sixteen-minute post**: what one published asset actually costs | LT blog + LT Bluesky | L1 | `lt-blog-20261116-01` |
| 9 | Tue Nov 17 | Derived from A03: where the sixteen minutes go | LT Bluesky + LinkedIn | L1 | `lt-bsky-20261117-01` |
| 10 | Wed Nov 18 | **A04 Three claims we killed**: and the one that cost a night | LT blog + LT Bluesky | L2 | `lt-blog-20261118-01` |
| 11 | Thu Nov 19 | Derived from A04: the rule that lets a writer lose an argument with a script | LT Bluesky + LinkedIn | L2 | `lt-bsky-20261119-01` |
| 12 | Fri Nov 20 | **A05 The timer was lying about decimals**: why we ship the fix note first | FB long copy + FB Bluesky | F2 | `fb-blog-20261120-01` |
| 12 | Fri Nov 20 | Week 2 receipt: staged, blocked, shipped | LT Bluesky | L1 | `lt-bsky-20261120-01` |
| 13 | Sat Nov 21 | empty: weekend | none | — | — |
| 14 | Sun Nov 22 | Derived from A05: a bug note that admits the bug is the marketing | FB Bluesky | F2 | `fb-bsky-20261122-01` |
| 15 | Mon Nov 23 | **A06 One room, one mechanic**: what we cut from Echo Rounds | FB long copy + FB Bluesky | F3 | `fb-blog-20261123-01` |
| 16 | Tue Nov 24 | Derived from A06: scope cuts are the design | LT Bluesky + LinkedIn | L3 | `lt-bsky-20261124-01` |
| 17 | Wed Nov 25 | **A07 Three weeks in**: what the run log says about us | LT blog + LT Bluesky | L1 | `lt-blog-20261125-01` |
| 18 | Thu Nov 26 | empty: Thanksgiving | none | — | — |
| 19 | Fri Nov 27 | empty: deliberate. No filler on a dead Friday | none | — | — |
| 20 | Sat Nov 28 | empty: weekend | none | — | — |
| 21 | Sun Nov 29 | Derived from A06: one room, one mechanic, one trade-off | FB Bluesky | F3 | `fb-bsky-20261129-01` |
| 22 | Mon Nov 30 | **A08 Cadence math**: why nine posts and not thirty | LT blog + LT Bluesky | L3 | `lt-blog-20261130-01` |
| 23 | Tue Dec 1 | Derived from A08: the post we did not write | LT Bluesky + LinkedIn | L3 | `lt-bsky-20261201-01` |
| 24 | Wed Dec 2 | **A09 A new quest every UTC day**: how Cinder's daily works | FB long copy + FB Bluesky | F1 | `fb-blog-20261202-01` |
| 25 | Thu Dec 3 | Derived from A09: the cost of a daily anything | LT Bluesky + LinkedIn | L3 | `lt-bsky-20261203-01` |
| 26 | Fri Dec 4 | **A10 What thirty reply drafts taught us**: answering players without inventing policy | LT blog + LT Bluesky | L2 | `lt-blog-20261204-01` |
| 26 | Fri Dec 4 | Week 4 receipt: the reply that needed a position | LT Bluesky | L2 | `lt-bsky-20261204-01` |
| 27 | Sat Dec 5 | empty: weekend | none | — | — |
| 28 | Sun Dec 6 | Derived from A09: one quest, one UTC day, no account | FB Bluesky | F1 | `fb-bsky-20261206-01` |
| 29 | Mon Dec 7 | **A11 Day 30: what we're killing** | LT blog + LT Bluesky | L1 | `lt-blog-20261207-01` |
| 30 | Tue Dec 8 | Derived from A11: the three numbers, with denominators | LT Bluesky + LinkedIn | L1 | `lt-bsky-20261208-01` |

Twelve source assets, thirty-five social posts. Nine posts in a normal week, five in Thanksgiving week, three in the final stub week.

### 8.2 The twelve source assets

| Id | Date | Brand | Pillar | Title | Source it must cite |
|---|---|---|---|---|---|
| A00 | Nov 9 | LT | L3 | The plan, in public | `plans/social-media-plan.md`, this document |
| A01 | Nov 11 | LT | L3 | Four roles, one cron, one gate | `personas/00-index.md`, research brief §7 |
| A02 | Nov 13 | FB | F1 | The arcade with no login | flambeee.com, `README.md` |
| A03 | Nov 16 | LT | L1 | The sixteen-minute post | persona human-minutes table, week 1 run log |
| A04 | Nov 18 | LT | L2 | Three claims we killed | `queue/escalations/*`, gate failure records |
| A05 | Nov 20 | FB | F2 | The timer was lying about decimals | `BLOG.md` Session 50, v0.43.0 |
| A06 | Nov 23 | FB | F3 | One room, one mechanic | `BLOG.md` Session 47, Echo Rounds |
| A07 | Nov 25 | LT | L1 | Three weeks in | `metrics/*`, `published/manifest.ndjson` |
| A08 | Nov 30 | LT | L3 | Cadence math | this document, §5 |
| A09 | Dec 2 | FB | F1 | A new quest every UTC day | flambeee.com Cinder daily quest |
| A10 | Dec 4 | LT | L2 | What thirty reply drafts taught us | `queue/replies/*`, approval reason codes |
| A11 | Dec 7 | LT | L1 | Day 30: what we're killing | `reports/weekly/*`, day-30 review |

Eight Lightsword, four flambeee. The client gets a quarter of the volume in month one, which is correct while Lightsword's own brand has nothing behind it and the client's product already has a publishing habit to amplify.

Every source asset cites a document that exists in the repo or on the client's public site. A00 cites this plan, which is why this plan has to be right rather than merely plausible.

### 8.3 Deliberate blanks

| Date | Why |
|---|---|
| Sat Nov 14, 21, 28, Dec 5 | Nobody reads a B2B post on Saturday, and the nightly run needs one night without generation |
| Thu Nov 26 | Thanksgiving. A post that day is an admission that the calendar owns the company. |
| Fri Nov 27 | Dead Friday in a holiday week. Empty beats filler. |

Six blank rows, each with a reason. Month two is written after the day-30 review, not before it.

## 9. How flambeee is represented

This is the part most likely to be got wrong quietly, so it gets rules rather than intentions.

### 9.1 Two gates, recorded separately

On Lightsword's channels, Jake is the only gate. On flambeee's channels, flambeee's owner approves the copy and Jake publishes it. Today one person holds both roles. The records stay separate anyway, with a `client` key on every approval row, because the habit is the product.

A post that would need flambeee's owner to decide something is not a post yet. It goes to `queue/escalations/` as one line.

### 9.2 The permission ladder

| Stage | What Lightsword may say | Gate to advance |
|---|---|---|
| Week 1 to 4 | "Our first client is a small web-games studio." No name, no product, no numbers. | Written permission in `plans/scope-flambeee.md` |
| Day 30 to 45 | flambeee named, work described, no performance claims | A number from the Analyst with a baseline behind it |
| Day 45 onward | One case study, with real numbers and named methods | Analyst confirms the numbers moved and can show the denominator |

There is no stage where Lightsword implies a flambeee result it did not measure. A case study with invented results is the single most expensive mistake this company can make, and it is a mistake that cannot be undone by deleting the post.

### 9.3 What never gets said on flambeee's behalf

- A feature that has not shipped, in any tense. No teasers, no roadmap, no "soon". flambeee announces, Lightsword amplifies.
- A player count, a download figure, or a retention number without a source in flambeee's own docs.
- A reply about pricing, an outage, a complaint, or a person. Those escalate. A friendly answer that commits the client to something is worse than a slow one.
- Anything in Lightsword's voice. If a sentence could appear on Lightsword's account unchanged, it is probably wrong for flambeee's.

### 9.4 The account question, both branches

**Branch A, default.** The week 0 audit finds no flambeee Bluesky account, and Jake opens one. Lightsword drafts, Jake publishes for 60 days. The calendar runs as written.

**Branch B, fallback.** No flambeee account is opened in month one, either because a handle is squatted or because Jake will not create accounts before the first client signs. Then the four flambeee source assets still get written and publish on Lightsword's channels as unnamed client work under L1 and L2, and the flambeee Bluesky rows become Lightsword rows at the same slot. Nothing else in the plan changes.

The calendar is executable either way. Which branch is live gets recorded in `plans/scope-flambeee.md` in week 0, not decided at 22:20 on a Tuesday.

### 9.5 Attribution

Every flambeee asset links to the specific game or release, never to a generic homepage, and every product claim traces to flambeee.com, `README.md`, or `BLOG.md`. The Content Lead's source line is the citation, and the gate drops anything without one.

**One client fact to settle before week 1.** flambeee.com says "Seven games, one arcade" in the hero and "6 Games shipped" in its stats block. Both are the client's own words and they disagree, so no post carries a game count until flambeee says which is canonical. This is exactly the class of claim the gate exists to catch, and it is cheaper to ask once in week 0 than to publish a number and correct it.

## 10. Running it: the nightly fit

One asset, end to end. Times are America/Chicago.

| When | Role | Step | Artifact |
|---|---|---|---|
| T-1, 20:00 Sunday | Strategist | Week's rows and briefs written | `plans/calendar-30d.md`, `queue/briefs/` |
| T-1, 21:55 | Strategist | Pre-flight: row and brief exist, or escalate | pass, or `queue/escalations/` |
| T-1, 22:20 | Content Lead | Generate the asset plus its variants from the brief | `queue/drafts/<asset-id>.md` |
| T-1, 22:32 | Content Lead | Gate: claims, voice, sources | pass or fail mark on the file |
| T-1, 22:35 | Strategist | Adjudicate any failure: drop, re-brief, or escalate | `queue/escalations/` |
| T-1, 22:40 | Distribution | Stage per-platform posts as drafts | `queue/social/<asset-id>.json` |
| T, 08:00 | Jake | Approve or reject with a reason code | `approvals` row |
| T, 09:00 | Distribution or Jake | Publish, then append the manifest | `published/manifest.ndjson` |

**Phase 1 does not require Postiz.** Staged posts live as JSON in `queue/social/` and Jake publishes by hand, which is the phase 1 rule anyway. That keeps the plan unblocked while the scheduler is still being stood up, and Postiz becomes a convenience later rather than a dependency now.

**Failure behavior.** A missed approval is not an error and not a reason to publish. The post slips to the next slot, the manifest records the real timestamp, and the on-time rate takes the miss. A late post costs one data point. An unapproved one costs the company.

**Idempotency.** Every step keys on `asset-id` plus platform plus date, so a re-run cannot double-post or double-reply.

## 11. Measurement

Social contributes to one Tier 1 number and nothing else: qualified sessions from social, month over month. Branded search is the awareness proxy. Both need a baseline, and neither site has one.

| Metric | Tier | Definition |
|---|---|---|
| Qualified sessions from social | 1 | Sessions with a `utm_source` in the social set that reach a defined qualifying action |
| Branded search volume | 1 | Searches containing the brand name, from Search Console |
| On-time publish rate | 2 | Published in the scheduled slot, divided by planned |
| First-pass approval rate | 2 | Approved without a rejection, divided by submitted. Target above 80% by week 8 |
| Human minutes per published asset | 2 | Jake's measured time, divided by assets published. Target under 20 |
| Reply time | 2 | Hours from inbound to a sent human reply. Target under 24 |
| Gate failures per week | 3 | Count, by category. A trend, never a scoreboard |
| Published without approval | 3 | Zero. Stop-the-line. |

Never reported: follower count on its own, impressions, engagement rate without a denominator, or posts published. Those measure activity, and activity is not the product.

**Month one is a baseline, not a result.** The honest targets for these thirty days are process targets: nine posts a week shipped, no unapproved publishes, replies inside a day, and a baseline recorded before the first post. Any reach target printed now would be a number invented to look like a plan.

**The instrument gap is the first deliverable.** Neither `lightsword.org` nor `flambeee.com` has an analytics tag today. Until one exists, the UTM scheme measures nothing and the month produces content with no evidence. Installing it is week 0 work, ahead of the first post.

## 12. Blocked, and what runs anyway

| Blocker | State observed 2026-11-04 | Impact | Owner | Workaround in force |
|---|---|---|---|---|
| No analytics on either site | No tag found on `lightsword.org` or `flambeee.com` | No baseline, so no performance claim | Jake, host access | Publish and record. Do not claim results. |
| `lightsword.org` apex does not resolve | `www` answers, apex has no A record; NS at Porkbun, served by Caddy | A link to the bare domain fails | Jake, DNS | Use `www.` everywhere until fixed |
| No company site | The domain serves a Retro 4K and TetriNET download page, no nav, no blog, no `robots.txt`, no sitemap | Nowhere to publish a source asset | Jake, then default | Branch B: canonical post lives at the repo blob URL, replaced within 30 days. Keep the download page at a subpath, it has real inbound links. |
| No social accounts | Lightsword and flambeee Bluesky do not exist; no LinkedIn page | The calendar cannot start | Jake | None. This is a hard gate. |
| Postiz not running | No container, no listener | Staging has no scheduler | default, t_7070f858 | Stage JSON, publish by hand. Phase 1 needs no scheduler. |
| Bluesky custom handle needs DNS | `lightsword.org` and `flambeee.com` both need a TXT record | Cosmetic, not blocking | Jake | Use `.bsky.social` handles first |
| LinkedIn page API access | Unverified, may need app review | Manual posting 2/wk | Jake | Manual posting, 3 minutes |

The honest read: **the plan is blocked on Jake creating two Bluesky accounts and one analytics tag.** Everything else has a workaround. Without those three, month one is a document rather than a presence.

## 13. Acceptance

| Requirement | Where |
|---|---|
| Target platforms with rationale | §4, chosen and rejected, each with a reason and a revisit trigger |
| Posting cadence aligned to the 10pm workflow | §5, per-platform table plus the T-1 run of show in §10 |
| Content pillars and tone/voice | §6 and §7, three pillars per brand, each with a proof source |
| 30-day starter calendar | §8, thirty rows, twelve source assets, thirty-five posts, six deliberate blanks |
| flambeee representation | §9, two gates, permission ladder, banned claims, both account branches |
| Executable by the minimal AI staff | §10, every step has a role, a time, a path, and a failure behavior |

---

Written for task t_575b5333. Grounded in `docs/marketing-company-research.md` (t_ffe8efb5) and `personas/00-index.md` (t_fde1bfae). No flambeee prompt, persona, cron, or internal file was read or reused.
