# Posting schedule — daily campaign at the best-engagement slot

**Status:** active, 2026-11-21.
**Authority:** kanban `t_3e006185` (root `t_27e05413`), *Update Lightsword campaign
schedule to daily*; operator comment 2026-11-21: "It should write when is best for
engagement."
**Machine-readable copy:** `plans/posting-schedule.json`.
**Verifier:** `python3 workflows/schedule-check.py` (also runs in the nightly
pre-flight).

## 1. The schedule

| Channel | Cadence | Slot (America/Chicago) | Who publishes | State |
|---|---|---|---|---|
| Lightsword Bluesky (`@lightsword.bsky.social`) | **daily, 7 days** | **19:00** | Nightly arms at 22:00 T-1; the 5-minute outbox tick publishes at 19:00 | **active** |
| Lightsword blog | 2 articles/week (Mon + one weekday) | link post at 19:00 | Nightly writes the page at 22:40 T-1; the 18:45 link check swaps in the brief's `text_fallback` or holds the item unless the live URL is 200 | active |
| flambeee Bluesky (`@flambeee.bsky.social`) | 3 drafts/week, staged | client's 12:05 | Client owner by default; the bot publishes only inside a written window | **blocked — §14 window closed 2026-11-19 07:10** |
| **Engagement (replies to strangers)** | **daily, every day, per account** | **19:10** (job `a9aa000ba1f3`) | `workflows/engagement-shift.md` | **LT active; flambeee blocked on consent** |

Engagement is a separate clock from content: it runs every day whether or not the
calendar has a row (`plans/engagement-program.md`, Jake directive 2026-11-23).
The bot's own account has no third-party consent to obtain, so its shift runs
from today. flambeee's does not, and the reason is in `plans/clients.json`.

The daily campaign is `lightsword-daily-2026-11-21` on the Lightsword account;
its first publish is **2026-11-23 19:00 CT**. The client account keeps its
existing staging cadence and its own publishing rhythm: a client write needs a
new written window (`plans/scope-flambeee.md` §14; `state/flambeee-window.json`),
and the bot cannot waive that. `workflows/bsky.py check_window` refuses every
client write outside the window, by design.

## 2. Why 19:00

The honest answer: nobody knows the best hour for these two accounts. Our own
data cannot answer it. `@lightsword` has 15 measured originals and 3
interactions in total, and every planned post in week 2 shipped at the same
09:00 slot. The numbers below are from
`metrics/2026-11-21-posting-times.json` (public AppView read, 2026-11-21):

| LT slot | Originals | Interactions | Note |
|---|---|---|---|
| 05:00 | 2 | 0 | the 11-06/07 publish batch |
| 07:00 | 3 | 0 | intro and profile posts |
| 08:00 | 1 | 2 | the 11-08 intro set |
| 09:00 | 5 | 0 | the slot this change replaces |
| 19:00 | 1 | 0 | the 11-15 quote post |
| 22:00 | 3 | 1 | week-1 nightly posts |

Total: 15 originals, 3 interactions. No hour has more than five posts, so the
table cannot rank a slot. The published studies disagree with each other and two
of them are explicit that the effect disappears when an account is compared
against itself:

| Source | Sample | Finding |
|---|---|---|
| [Buffer](https://buffer.com/resources/best-time-to-post-on-bluesky/) | >3,000,000 Bluesky posts | Weekday peak 6–9 pm local; Saturday 5 pm; weekday 10 am–1 pm quietest |
| [SocialPilot](https://www.socialpilot.co/fr/insights/best-time-to-post-on-bluesky) | >1,000,000 posts, 5,000+ accounts | Weekday mornings beat weekends |
| [PostDaily](https://www.postdaily.app/blog/best-time-to-post-on-bluesky) | 8,373 posts, 344 accounts, within-account | No meaningful effect of posting time |
| [BskySuite](https://bskysuite.com/blog/bluesky-best-time-to-post/) | 27,755 posts, 491 accounts, within-account | Quiet vs busy hours 1.00× — a coin flip |

19:00 is chosen because it is the one window the largest study and the
cross-study summary agree on (weekday 6–9 pm local). Weekends at 19:00 are
slightly later than Buffer's 4–7 pm weekend window; a single daily slot is a
deliberate simplification, and the day-30 review can split the weekend slot if
the data ever supports one. Our own data cannot confirm 19:00 either: the LT
account has no 19:00 signal, and the client account's two 19:00–19:30 campaign
posts carry 2 interactions between them. It is a prior, not a finding. The
schedule is not defended as "the best time"; it is the least-bad prior available,
and it is the slot we will measure.

Two operational reasons also point at 19:00:

1. A 19:00 post gives the 22:00 nightly three hours of engagement to read before
   it writes the digest and generates the next day's asset.
2. The nightly stays at 22:00. Moving the nightly to the slot would publish and
   analyze in the same minute, and it would lose the day's reply and metric work.

## 3. How it runs

No new cron job. The chain is the one already registered:

| Time (CT) | What happens | Where |
|---|---|---|
| T-1 22:00 | Nightly generates T's asset from the calendar row and brief, runs the gate, arms `queue/outbox/<id>.json` with `publish_at = T 19:00:00-06:00` | job `b83aa855e26a` |
| T 18:45 | Link check on the armed item: 200, or swap to `text_fallback`, or `held-link-dead` + DM | job `e180ec9bc2cd` |
| T 19:00 | The 5-minute outbox tick publishes the armed item, one audit line per send | job `84e5289134f4` |
| T 22:00 | Nightly reads the result, writes the digest, repeats for T+1 | job `b83aa855e26a` |
| Sun 20:00 | Weekly planning writes the coming week's rows and briefs | job `2b4e865f7401` |

If the arm fails or the slot has already passed, the existing rule applies:
publish immediately through `workflows/bsky.py post` and record one WARNING
line. The tick is idempotent; a re-run never duplicates a post.

**Verify it:**

```bash
cd ~/.hermes/lightsword/lightsword
python3 workflows/schedule-check.py
```

Expected on 2026-11-21: `PASS`, all four jobs `ok`, and
`next publish 2026-11-23T19:00:00-06:00 (lt-bsky-20261123-01)`. A closed client
window is a warning, not a failure: the client channel is staged, not published.

## 4. Content supply

A daily slot does not create an asset. The calendar still decides what ships.

- The Sunday planning job writes a row for every date in the coming week and a
  brief for every non-empty row.
- A day with no grounded asset stays `type: empty` with a reason and the nightly
  records a planned skip. Empty is not a failure; filler is.
- Weeks 3 and 4 now carry daily rows (`plans/growth-plan-30d-2026-11-08.md`
  §7.4–§7.5), derived from A07, A08 and A10 and the repo's own run logs. The first
  daily post is **2026-11-23 19:00**; 2026-11-21 and 2026-11-22 keep their
  existing empty rows because the directive landed after those rows were
  written.
- Daily adds six Lightsword posts to the 30-day plan (27 instead of 21
  Lightsword posts; 39 social posts instead of 35). The extra six are grounded
  in `logs/nightly.ndjson`, `metrics/*`, `published/manifest.ndjson` and
  `AGENTS.md` rule 7; no new product claim is introduced.
- The nightly's three-asset cap still binds. When a Friday flambeee batch and
  the daily Lightsword post land on the same run, the Lightsword post goes
  first; the client batch can roll to Saturday and still stage before the
  client's Monday 12:05 slot.

## 5. Measurement and review

Every post already carries its slot: `slot` in `queue/social/*.json` and
`publish_at` in `queue/outbox/*.json`. The Analyst's per-post table in
`metrics/YYYY-MM-DD.json` carries the public `indexedAt` and the four action
counts, so slot joins to engagement without a new instrument.

- Review after **14 daily Lightsword posts**, in the day-30 report on
  **2026-12-08**.
- Report interactions per original post by publish hour, with the post count
  for each hour. Do not call a winner below five posts in that hour; write
  `insufficient sample` instead.
- If a slot shows a repeatable difference, move the schedule with the numbers
  attached. If it does not, keep 19:00 for stability and say so — do not claim
  a best time the data does not support.
- Impressions, profile visits, clicks and signups stay `unavailable`: no
  analytics tag and no view count in the public API. Never report them as zero
  and never estimate them.

## 6. Dependencies and open items

1. **Client consent (hard dependency).** `@flambeee` writes are refused by
   `check_window`. §14 closed 2026-11-19 07:10: "draft-only resumes unless
   extended in writing." A daily client campaign needs a new written window in
   `plans/scope-flambeee.md` plus `state/flambeee-window.json`. Third-party
   consent is not a gate the bot can waive. Until then the client channel stays
   `staged-awaiting-owner` and the owner posts.
2. **Calendar rows.** The Sunday 20:00 job owns them. If it does not write a
   row or a brief, the nightly pre-flight halts phases 3–7 and escalates; the
   schedule never invents an asset.
3. **Publisher and checks.** The outbox tick (`84e5289134f4`) is the publisher.
   The 18:45 link check (`e180ec9bc2cd`) guards any link post. The
   `schedule-check.py` verifier fails if either job is disabled or has no next
   run.
4. **Content inventory.** Daily is six more Lightsword posts than the 30-day
   plan carried. If the Sunday run cannot ground a day from the plan's sources,
   the day is `empty`; daily cadence is not a license to invent.

## 7. Change log

- **2026-11-21:** created. Lightsword Bluesky moves from 5 posts/week Mon–Fri at
  09:00 to daily at 19:00. The campaign's own final report
  (`reports/campaign/2026-11-19-reach-final.md`, recommendation 5) said "drop
  the daily post cadence"; the operator directive in `t_3e006185` supersedes
  it, and the reason is recorded here. No client window was added.
- **2026-11-21 (later):** added the 18:45 `Lightsword blog link check`
  (`e180ec9bc2cd`). A link post's staged asset may carry `text_fallback` (the
  brief's no-link CTA); the check swaps it in when a URL is not 200 and
  otherwise holds the item (`held-link-dead`). This gives the "verify at 18:45"
  line a scheduled job; before this it had none.
