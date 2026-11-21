# Campaign: reach first, 72 hours

**Campaign id** `flambeee-reach-2026-11-16`
**Window** 2026-11-16 07:10 → 2026-11-19 07:10 America/Chicago (13:10Z → 13:10Z)
**Account** `@flambeee.bsky.social`
**Authority** `plans/scope-flambeee.md` §14 (Jake, kanban `t_06c24183`, 2026-11-16)
**Owner** Strategist. Content Lead writes, Distribution Lead sends, Analyst measures.

## 1. What the last campaign proved

`reports/campaign/2026-11-16-final.md`: 12/12 posts shipped on time, 8/8 with alt
text, gate 12/12 pass — and followers stayed at 4 with **0 engagement actions
from anyone**, including on the client's own SALTLINE launch post. The delivery
layer works. Broadcasting into a four-follower feed does not, and a second
broadcast would produce the same number. Copy, format and slot were not the
constraint; reach was.

## 2. Objective

Move the account from broadcast to conversation: put flambeee in front of people
who are already asking for a game, a recommendation, or a browser alternative,
and let a specific answer do the work. One sentence: **show up in ten real
conversations and be useful, instead of posting twelve ads into an empty feed.**

## 3. Mechanism

| Lever | Rule |
|---|---|
| Replies | 3 per day, maximum 5 per rolling 24h, 10+ minutes apart, max 2 per thread (AGENTS.md §7, enforced in `workflows/bsky.py`) |
| Target selection | A stranger asking for a game, a recommendation, or a no-install/no-account alternative, in the last 30 hours, in English, with a readable thread |
| Reply content | One specific game or app, one link, no pitch paragraph, flambeee voice (dry, exact, no hype) |
| Posts | 1 per day at 15:10 CT, image + alt where it earns it. Not 4 per day |
| Profile | One pinned "start here" post, so a reply-driven profile visit converts |
| Follows | **Not authorized in this window.** §14 names posting and replying only. Recorded as the largest unspent lever, not done |

## 4. KPIs

Baseline measured 2026-11-16 13:00Z: 4 followers, 58 posts, 0 inbound actions in
the previous 72 hours.

| # | KPI | Baseline | Target | How it is counted |
|---|---|---|---|---|
| K1 | Campaign posts live at their slots | 0 | 3/3, gate pass, alt on image posts | `published/manifest.ndjson` + repo read |
| K2 | Replies sent to strangers | 0 | 9 (3/day), 0 policy breaks | `logs/bsky-actions.ndjson` |
| K3 | Followers | 4 | 7 (+3) | public AppView `followersCount` |
| K4 | Inbound actions from other accounts | 0 | ≥6, incl. ≥1 stranger reply | notification list + conversation reads |

Impressions, profile visits, site clicks and signups are **unavailable** (no
analytics tag, no instrument on flambeee.com). They are recorded as unavailable,
never as zero and never estimated.

## 5. Daily schedule (America/Chicago)

| Time | Role | Work |
|---|---|---|
| 09:10 | Distribution | Reply shift A: 2 replies from the day's target list |
| 15:10 | Content/Distribution | 1 scheduled post from `queue/outbox/` |
| 19:10 | Distribution + Analyst | Reply shift B: 1 reply, then the day's snapshot |

Three replies a day is deliberately under the cap of five. The cap exists
because a burst reads as spam; the campaign should not spend its whole budget
because it can.

## 6. Target list rules

A reply target must satisfy all five:

1. Posted in the last 30 hours.
2. A real person or small account, not a brand ad, not a repost bot.
3. The post asks for something: a recommendation, a game to play, an
   alternative to ads/installs/accounts, or a "what are you playing" thread.
4. One of the nine games or six apps genuinely answers it.
5. The reply can name the specific thing in the first clause.

No reply to a complaint, a price question, a bug report, a person, or a thread
already carrying two of our replies. Those are position class and go to the
Strategist (`plans/reply-playbook-flambeee.md` §7).

## 7. Fail-closed

- Window is enforced in code (`check_window` in `workflows/bsky.py`), not in a
  prompt. Outside the window every client-account write refuses.
- A missing target list or an empty search result is a zero-reply day, logged.
  It never becomes an invented target or a reply to a random post.
- Every reply is gated (`workflows/gate.py`) before it is sent. A gate failure
  is dropped, not reworded by the sender.
- Daily snapshot appends to `metrics/campaign/2026-11-19-reach.ndjson` (one JSON
  object per line); the final report is
  `reports/campaign/2026-11-19-reach-final.md`. The daily narrative log is
  `reports/campaign/2026-11-19-reach-log.md`.

## 8. Sources for every claim used

`brand/claims-flambeee.md` v1.0 rows 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 17, 25;
client homepage v0.50.0 ("Nine games, still one file each"). No new claim is
introduced by this campaign.
