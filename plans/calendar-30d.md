# Lightsword 30-day calendar — rows 2026-11-08..2026-11-29

Source of truth: `plans/growth-plan-30d-2026-11-08.md` §7 (2026-11-08), §7.4 and
§7.5 (daily rows for weeks 3-4, 2026-11-21).
`plans/social-media-plan.md` §8.1 is superseded for 2026-11-08..2026-12-08.
Schema: `date | channel | pillar | asset-id | working title | type | source | owner`.
`type` is `source`, `derived`, or `empty`. Empty rows are deliberate blanks with
a reason. Format, hook, and CTA for every row live in the plan §7.1.

**2026-11-21:** Lightsword Bluesky is daily at 19:00 America/Chicago from
2026-11-23 (`plans/posting-schedule.md`). 2026-11-21 and 2026-11-22 keep their
existing empty rows; the directive landed after those rows were written. The
client channel is unchanged: 3 staged drafts/week, client posts at 12:05.

The week-1 rows written 2026-11-04 (11-09..11-15) are replaced: the six social
posts behind them were published 11-06/11-07, and four of the eight drafts
contain Phase-1 copy that is no longer true. See plan Appendix B.

| date | channel | pillar | asset-id | working title | type | source | owner |
|---|---|---|---|---|---|---|---|
| 2026-11-08 | LT Bluesky | L1 | lt-bsky-20261108-01 | Pinned intro: what Lightsword is, what it costs, what it refuses (T01 card) | source | growth plan §7.1, §8 | Content Lead / Distribution Lead |
| 2026-11-09 | LT blog | L1 | lt-blog-20261109-02 | A00 v2 The plan, in public: what changed after the stall | source | growth plan §3, §4 | Content Lead |
| 2026-11-09 | LT Bluesky | L1 | lt-bsky-20261109-01 | Six posts, one follower, zero replies: the stall in numbers | derived | lt-blog-20261109-02 (A00 v2) | Content Lead |
| 2026-11-10 | LT Bluesky | L1 | lt-bsky-20261110-02 | The plan we are replacing it with (link to A00 v2) | derived | lt-blog-20261109-02 (A00 v2) | Content Lead |
| 2026-11-11 | LT Bluesky | L3 | lt-bsky-20261111-01 | Homepage correction: nothing auto-publishes stopped being true on 11-05 (T02 card if site fixed) | derived | audit §3.3 W2; growth plan §4 | Content Lead |
| 2026-11-12 | LT blog | L3 | lt-blog-20261112-01 | A01 v2 Four roles, one nightly run, one gate | source | personas/00-index.md; growth plan §2 | Content Lead |
| 2026-11-12 | LT Bluesky | L3 | lt-bsky-20261112-02 | The role that exists to disagree with the plan | derived | lt-blog-20261112-01 (A01 v2) | Content Lead |
| 2026-11-13 | LT Bluesky | L1 | lt-bsky-20261113-03 | Week 1 receipt: planned, shipped, killed, missed | derived | logs/nightly.ndjson; published/manifest.ndjson | Content Lead / Analyst |
| 2026-11-13 | FB Bluesky (staged) | F1 | fb-blog-20261113-01 | Wordfire: one word a day | derived | queue/drafts/fb-blog-20261113-01.md | Content Lead / Distribution Lead |
| 2026-11-13 | FB Bluesky (staged) | F1 | fb-bsky-20261113-02 | Afterglow: a memory maze you play in the dark | derived | queue/drafts/fb-bsky-20261115-01.md (re-slotted) | Content Lead / Distribution Lead |
| 2026-11-13 | FB Bluesky (staged) | F1 | fb-bsky-20261113-03 | Cinder: a new quest every UTC day | source | plans/client-brief-flambeee.md §1 | Content Lead / Distribution Lead |
| 2026-11-14 | none | — | — | empty: weekend | empty | growth plan §7.2 | Strategist |
| 2026-11-15 | none | — | — | empty: weekend; weekly planning 20:00, day-7 site rebaseline | empty | growth plan §7.2, §11 | Strategist |
| 2026-11-16 | LT blog | L1 | lt-blog-20261116-01 | A03 v2 What one published asset costs now | source | logs/nightly.ndjson; workflows/nightly-2200.md | Content Lead |
| 2026-11-16 | LT Bluesky | L1 | lt-bsky-20261116-01 | The old review number is retired | derived | lt-blog-20261116-01 (A03 v2) | Content Lead |
| 2026-11-17 | LT Bluesky | L2 | lt-bsky-20261117-01 | The 19-pixel tap target (T06 metric card) | source | audit §3.3 W11 | Content Lead |
| 2026-11-18 | LT Bluesky | L4 | lt-bsky-20261118-01 | No password, no takeover: how the client handoff works | source | plans/scope-flambeee.md §1, §3 | Content Lead |
| 2026-11-19 | LT blog | L3 | lt-blog-20261119-01 | A04 v2 The gate passed four drafts that were still wrong | source | queue/drafts (stale kit); audit W2; growth plan Appendix B | Content Lead |
| 2026-11-19 | LT Bluesky | L3 | lt-bsky-20261119-01 | A gate pass is not a fact check (T02 card) | derived | lt-blog-20261119-01 (A04 v2) | Content Lead |
| 2026-11-20 | LT Bluesky | L1 | lt-bsky-20261120-01 | Week 2 receipt and the provisional day-14 pillar read | derived | logs/nightly.ndjson; metrics/* | Content Lead / Analyst |
| 2026-11-20 | FB Bluesky (staged) | F2 | fb-bsky-20261120-01 | The timer that lied about 7.5 minutes | derived | flambeee BLOG.md Session 50 (v0.43.0) | Content Lead / Distribution Lead |
| 2026-11-20 | FB Bluesky (staged) | F1 | fb-bsky-20261120-02 | Six small browser utilities | source | flambeee.com/apps/ (public) | Content Lead / Distribution Lead |
| 2026-11-20 | FB Bluesky (staged) | F1 | fb-bsky-20261120-03 | Simon, with a colorblind mode | source | plans/client-brief-flambeee.md §2 | Content Lead / Distribution Lead |
| 2026-11-21 | none | — | — | empty: weekend | empty | growth plan §7.2 | Strategist |
| 2026-11-22 | none | — | — | empty: weekend; week 3 rows written 2026-11-21 | empty | growth plan §7.2; posting-schedule amendment | Strategist |
| 2026-11-23 | LT blog | L1 | lt-blog-20261123-01 | A07 Three weeks in: what the run log says about us | source | growth plan §7.4, §7.5; metrics/*; logs/nightly.ndjson | Content Lead |
| 2026-11-23 | LT Bluesky | L1 | lt-bsky-20261123-01 | Three weeks in: [n] planned, [n] live, [n] held | derived | lt-blog-20261123-01 (A07) | Content Lead |
| 2026-11-24 | LT Bluesky | L1 | lt-bsky-20261124-01 | The number that did not move | derived | growth plan §7.5; A07; metrics/2026-11-23.json vs metrics/2026-11-09.json | Content Lead |
| 2026-11-25 | LT Bluesky | L3 | lt-bsky-20261125-01 | Six followers is not a sample | source | growth plan §7.5; reports/campaign/2026-11-19-reach-final.md | Content Lead |
| 2026-11-26 | LT Bluesky | L1 | lt-bsky-20261126-01 | The run does not take holidays | source | growth plan §7.5; workflows/nightly-2200.md; cron b83aa855e26a | Content Lead |
| 2026-11-27 | LT Bluesky | L1 | lt-bsky-20261127-01 | Week 3 receipt: shipped, held, skipped | derived | growth plan §7.5; logs/nightly.ndjson; published/manifest.ndjson | Content Lead / Analyst |
| 2026-11-28 | LT Bluesky | L3 | lt-bsky-20261128-01 | The part of the plan that is not automated | source | growth plan §7.5; workflows/weekly-plan-sunday.md | Content Lead |
| 2026-11-29 | LT Bluesky | L2 | lt-bsky-20261129-01 | What the reply cap costs | source | growth plan §7.5; AGENTS.md rule 7; logs/bsky-actions.ndjson | Content Lead |

## Consumed assets — do not republish

Published 2026-11-06/11-07; already in `published/manifest.ndjson`. The old
calendar rows that pointed at them are replaced above.

| asset-id | platform | published | URL |
|---|---|---|---|
| lt-blog-20261109-01 | bsky | 2026-11-06T13:05:54Z | https://bsky.app/profile/lightsword.bsky.social/post/3mznh4w26sf23 |
| lt-bsky-20261110-01 | bsky | 2026-11-06T13:05:54Z | https://bsky.app/profile/lightsword.bsky.social/post/3mznh532pkw2s |
| lt-blog-20261111-01 | bsky | 2026-11-06T13:05:54Z | https://bsky.app/profile/lightsword.bsky.social/post/3mznh5a5ngo2s |
| lt-bsky-20261112-01 | bsky | 2026-11-06T13:05:54Z | https://bsky.app/profile/lightsword.bsky.social/post/3mznh5f4cu42g |
| lt-bsky-20261113-01 | bsky | 2026-11-07T11:09:03Z | https://bsky.app/profile/lightsword.bsky.social/post/3mzpr2veeor2k |
| lt-bsky-20261113-02 | bsky | 2026-11-07T11:22:29Z | https://bsky.app/profile/lightsword.bsky.social/post/3mzprsvy7yf2k |

## Notes

- FB rows are staging rows: `status: staged-awaiting-owner`. The client posts
  by default. During the §13 window (2026-11-13 08:00 → 2026-11-16 08:00 CT)
  the 72-hour campaign publishes through `workflows/bsky.py` with the
  owner-issued app password; outside it, the credential does not authorize a
  publish. Cadence amendment not required to draft or stage (scope §1, §12).
- No game count appears on any FB row except the canonical 8 games / 6 apps.
  **Corrected 2026-11-15:** that figure was the 2026-11-08 baseline and is now
  stale — v0.50.0 added SALTLINE on 2026-11-13, so the canonical count is
  **nine games / six apps** (`brand/claims-flambeee.md` row 2, re-verified
  11-13 against nine live `/games/*.html` pages). No FB copy uses 5, 7, or 8.
- LinkedIn is not a channel this month (audit §6). The two staged LinkedIn JSONs
  are dead and must not publish.
- The 11-13 and 11-20 FB rows are a Friday batch of three drafts each, for the
  client's following Mon/Wed/Fri 12:05 slots.
- **2026-11-13 to 2026-11-15 are governed by the 72-hour campaign**, not the
  rows above: `queue/campaign/fb-campaign-2026-11-13.json` is the source
  (12 slots, 4/day, first 12:05 Fri, last 19:00 Sun). The three 11-13 FB staged
  rows are superseded for this window and their JSONs are `status: superseded`.
  The 11-14 and 11-15 rows stay `empty`; do not stage extra FB posts on those
  days.
