# 72-hour campaign copy and calendar — flambeee, "Pick one and play"

**Version** 1.2 · **Issued** 2026-11-12 · **Owner** Content Lead (copy), Strategist (calendar) · **Status** running (window open; #12 amended 2026-11-14)

**v1.1, 2026-11-13 06:45 CT:** v0.50.0 shipped SALTLINE at 09:24Z, the ninth game; the client homepage says "Nine games, still one file each". Posts #01, #12 and reply snippet R3 were changed 8 -> 9, the link card was re-rendered with "Nine games.", and all 12 drafts were re-gated (12/12 pass). Strategist decide-and-log in `queue/escalations/2026-11-13-campaign-go-no-go.md`.

**v1.2, 2026-11-14 12:20 CT:** the brief's 28-hour rule fired (followers 4 < 6 at 12:00 CT). Post #12's lead game moved 2048 -> Cinder, the account's top-engagement game by measured actions. Text, link and sources below are updated; slot, asset, alt text, UTM and idempotency key are unchanged. Gate re-run: PASS. Strategist decide-and-log in `queue/escalations/2026-11-14-28h-rule.md`.

**Campaign brief:** `plans/campaign-72h-2026-11-13.md`. This document turns that brief into words and slots. It does not change the objective, the audience, the KPIs, or the voice.

**Window:** Fri 2026-11-13 08:00 → Mon 2026-11-16 08:00 America/Chicago (14:00Z → 14:00Z).

**Account:** `@flambeee.bsky.social`. Fallback per brief §7: `@lightsword.bsky.social` if the session is not working by 2026-11-13 13:00 CT.

**Authority:** Jake, kanban `t_06c24183`, 2026-11-12; recorded in `plans/scope-flambeee.md` §13. The compliance gate is not waived.

**Gate:** 12 drafts in `queue/drafts/fb-camp-20261113-01.md` … `-12.md`, each with `<!-- gate: pass -->`. A post without a gate pass does not publish.

---

## 1. The campaign at a glance

| Item | Value |
|---|---|
| Objective | 12 posts in 72 hours on `@flambeee.bsky.social` that put "pick one and play" in front of casual mobile players. |
| K1 | 12/12 posts live; manifest and post URIs. |
| K2 | Followers 4 → 9 by Mon 08:00 CT; AppView `getProfile`. |
| K3 | ≥10 engagement actions and ≥2 replies from strangers across the 12 posts; AppView per post. |
| Audience | Primary: casual mobile break players. Secondary: daily word and puzzle players. |
| One message | "Pick a game and play in your browser. Nothing to install, no account, no ads." (client-approved) |
| Voice | Direct, dry, precise, exact. No hashtags, no em dashes, no hype, never a Lightsword-voice sentence. |

Not KPIs: profile visits (no Bluesky endpoint), site clicks, signups, play counts (no analytics or aggregate counter at flambeee.com). Report each as `unavailable (no instrument)`, never 0, never estimated.

---

## 2. Calendar

All 12 top-level posts. `#08` also carries one reply; it is not a separate slot. Times are exact; the CT column is for the operator, the UTC column is the contract. K1 (12/12 live) applies to every row; the KPI column names the secondary target the post is shaped for.

| # | UTC | America/Chicago | Format | Pillar | KPI | Asset | Post |
|---|---|---|---|---|---|---|---|
| 01 | 2026-11-13T18:05:00Z | Fri 2026-11-13 12:05 | image | F1 | K2 followers | `flambeee-ad-claim-1080x1080.png` | Hook: no installs, no accounts, no ads |
| 02 | 2026-11-13T21:30:00Z | Fri 2026-11-13 15:30 | image | F1 | K3 engagement | `game-wordfire.png` | Wordfire: one word a day |
| 03 | 2026-11-14T00:00:00Z | Fri 2026-11-13 18:00 | image | F1 | K3 engagement | `game-2048.png` | 2048: merge the tiles |
| 04 | 2026-11-14T02:00:00Z | Fri 2026-11-13 20:00 | text | F2 | K3 engagement | none | Story: the Timer stopped lying about decimals |
| 05 | 2026-11-14T15:00:00Z | Sat 2026-11-14 09:00 | image | F1 | K3 engagement | `game-simon.png` | Simon: colorblind mode |
| 06 | 2026-11-14T18:05:00Z | Sat 2026-11-14 12:05 | image | F1 | K3 engagement | `flambeee-ad-game-spotlight-1080x1080.png` | Afterglow: play it from memory |
| 07 | 2026-11-14T22:00:00Z | Sat 2026-11-14 16:00 | image | F1 | K3 engagement | `game-minesweeper.png` | Minesweeper: the first click is safe |
| 08 | 2026-11-15T01:30:00Z | Sat 2026-11-14 19:30 | thread | F3 | K3 engagement | none | Thread: Echo Rounds, one room, one mechanic |
| 09 | 2026-11-15T15:00:00Z | Sun 2026-11-15 09:00 | text | F1 | K2 followers | none | Apps: six small browser tools |
| 10 | 2026-11-15T18:05:00Z | Sun 2026-11-15 12:05 | image | F1 | K3 engagement | `game-cinder.png` | Cinder: a new quest every UTC day |
| 11 | 2026-11-15T22:00:00Z | Sun 2026-11-15 16:00 | text | F3 | K3 engagement | none | Typewreck: paste text, wreck the wall |
| 12 | 2026-11-16T01:00:00Z | Sun 2026-11-15 19:00 | image | F1 | K2 followers | `flambeee-ad-link-card-1200x628.png` | CTA: pick one and play |
| 08b | 2026-11-15T01:31:00Z | Sat 2026-11-14 19:31 | reply | F3 | K3 engagement | none | Thread part 2, reply to #08 |

**Slot rule.** The brief fixes four slots per day. This document fills all twelve. If a slot is missed, publish it late the same CT day; never skip it, never double-post it, never move it to the next day.

---

## 3. The posts

Each block is the exact publish text and the exact asset. Character counts are measured on the string that ships, including the URL.

### 01 · Fri 2026-11-13 12:05 CT · 2026-11-13T18:05:00Z · image · F1 · K2 followers

**New copy.**

**Post text** (155 chars). Copy exactly, no leading or trailing spaces:

```text
Nine browser games and six small apps, all free. No installs. No accounts. No ads. Pick one and play. For the next three days, one thing to play at a time.
```

**Asset:** `brand/flambeee-assets/exports/flambeee-ad-claim-1080x1080.png`

**Alt text:** flambeee ad: the words no installs. no accounts. no ads. in large white and coral type on navy.

**Sources:**

- Campaign brief §3: the one message, "Pick a game and play in your browser. Nothing to install, no account, no ads." `plans/campaign-72h-2026-11-13.md`.
- 9 games / 6 apps: `brand/claims-flambeee.md` rows 2 and 3; client brief §1; client homepage v0.50.0.
- No install, no account, no ads: claims rows 4, 5, 6.
- Image and alt text: `brand/flambeee-assets/manifest.json` (adClaim), file `exports/flambeee-ad-claim-1080x1080.png`, rendered 2026-11-12.


---

### 02 · Fri 2026-11-13 15:30 CT · 2026-11-13T21:30:00Z · image · F1 · K3 engagement

**Reuse:** queue/social/2026-11-13-fb-bsky-1.json (gate: pass, 189 chars). Text unchanged; only the slot moved.

**Post text** (189 chars). Copy exactly, no leading or trailing spaces:

```text
Wordfire gives you one word a day. No install, no account. Try it: https://flambeee.com/games/wordfire.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-blog-20261113-01
```

**Asset:** `brand/flambeee-assets/assets/game-wordfire.png`

**Alt text:** A Wordfire puzzle on a dark background: a 5x4 grid of tiles. The top row spells CRANE and the second row spells BLIND in white letters; the bottom two rows are empty.

**Sources:**

- Reused verbatim from `queue/social/2026-11-13-fb-bsky-1.json` (gate: pass, 189 chars, 2026-11-08). Slotted to the campaign's Fri 15:30 CT slot.
- Wordfire one word a day, five letters, streak: claims row 10; `plans/client-brief-flambeee.md` §1.
- No install, no account: claims rows 4 and 5.
- Image: `brand/flambeee-assets/assets/game-wordfire.png` (client screenshot, public repo, 648x486).


---

### 03 · Fri 2026-11-13 18:00 CT · 2026-11-14T00:00:00Z · image · F1 · K3 engagement

**New copy.**

**Post text** (224 chars). Copy exactly, no leading or trailing spaces:

```text
2048 in the browser: merge the tiles, reach 2048, chase a new high score. No install, no account, no ads: https://flambeee.com/games/2048.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-camp-20261113-03
```

**Asset:** `brand/flambeee-assets/assets/game-2048.png`

**Alt text:** A 2048 screenshot: a 4x4 grid of numbered tiles on a dark background, with 2, 4, 8, and 16 tiles in gray and amber. The board is full.

**Sources:**

- 2048 merges tiles, reach 2048, new high score: claims row 17.
- Game page HTTP 200: https://flambeee.com/games/2048.html (checked 2026-11-12).
- No install, no account, no ads: claims rows 4, 5, 6.
- Image: `brand/flambeee-assets/assets/game-2048.png` (client screenshot, 856x856).


---

### 04 · Fri 2026-11-13 20:00 CT · 2026-11-14T02:00:00Z · text · F2 · K3 engagement

**New copy.**

**Post text** (272 chars). Copy exactly, no leading or trailing spaces:

```text
The Timer app used to run 7 minutes while the field said 7.5. The fix shipped in v0.43.0: the clock now counts the seconds it says it counts. No account: https://flambeee.com/apps/timer.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-camp-20261113-04
```

**Asset:** none. Text-only post.

**Alt text:** none (text-only).

**Sources:**

- Timer display bug and v0.43.0 fix: `brand/claims-flambeee.md` row 23; public `BLOG.md`, section "v0.43.0: Timer stops lying about decimals" (https://github.com/jakepi-bot/flambeee/blob/main/BLOG.md, checked 2026-11-12).
- No account: claims row 5.
- Timer page HTTP 200: https://flambeee.com/apps/timer.html (checked 2026-11-12).


---

### 05 · Sat 2026-11-14 09:00 CT · 2026-11-14T15:00:00Z · image · F1 · K3 engagement

**New copy.**

**Post text** (229 chars). Copy exactly, no leading or trailing spaces:

```text
Simon, with a colorblind mode. Four colors and four shapes, one sequence to remember. No install, no account: https://flambeee.com/games/simon.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-camp-20261113-05
```

**Asset:** `brand/flambeee-assets/assets/game-simon.png`

**Alt text:** A Simon game board: four rounded buttons in a 2x2 grid on dark blue. The top-left green circle and bottom-left yellow square are lit; the top-right dark red triangle and bottom-right dark blue diamond are unlit.

**Sources:**

- Colorblind mode with shape symbols: claims row 15; public README "Colorblind mode with shape symbols" (https://github.com/jakepi-bot/flambeee/blob/main/README.md, checked 2026-11-12).
- Four colors and four shapes: claims row 24 (Simon board screenshot; public README shape symbols).
- No install, no account: claims rows 4 and 5.
- Image: `brand/flambeee-assets/assets/game-simon.png` (client screenshot, 652x652).


---

### 06 · Sat 2026-11-14 12:05 CT · 2026-11-14T18:05:00Z · image · F1 · K3 engagement

**Reuse:** queue/social/2026-11-13-fb-bsky-2.json (gate: pass, 202 chars). Text unchanged; only the slot moved.

**Post text** (202 chars). Copy exactly, no leading or trailing spaces:

```text
Afterglow is a memory maze played in the dark. No install, no account. Try it: https://flambeee.com/games/afterglow.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-bsky-20261113-02
```

**Asset:** `brand/flambeee-assets/exports/flambeee-ad-game-spotlight-1080x1080.png`

**Alt text:** Afterglow ad: a dark grid puzzle screenshot above the line See the board. Then the lights go out.

**Sources:**

- Reused verbatim from `queue/social/2026-11-13-fb-bsky-2.json` (gate: pass, 202 chars, 2026-11-08). Slotted to the campaign's Sat 12:05 CT slot.
- Afterglow lights the board, goes dark, moves from memory: claims row 12; client brief §3.
- No install, no account: claims rows 4 and 5.
- Image and alt text: `brand/flambeee-assets/manifest.json` (adSpotlight), file `exports/flambeee-ad-game-spotlight-1080x1080.png`, rendered 2026-11-12.


---

### 07 · Sat 2026-11-14 16:00 CT · 2026-11-14T22:00:00Z · image · F1 · K3 engagement

**New copy.**

**Post text** (233 chars). Copy exactly, no leading or trailing spaces:

```text
Minesweeper's first click is always safe, and on a phone a long-press flags a tile. No account, no install: https://flambeee.com/games/minesweeper.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-camp-20261113-07
```

**Asset:** `brand/flambeee-assets/assets/game-minesweeper.png`

**Alt text:** A Minesweeper board on a dark background: an 8x8 grid of blue tiles. The top three rows are partly revealed, showing dark tiles with the numbers 1 and 2; the bottom five rows are covered.

**Sources:**

- First click is always safe; mobile long-press to flag: claims row 16; public README.
- Game page HTTP 200: https://flambeee.com/games/minesweeper.html (checked 2026-11-12).
- No account, no install: claims rows 4 and 5.
- Image: `brand/flambeee-assets/assets/game-minesweeper.png` (client screenshot, 792x792).


---

### 08 · Sat 2026-11-14 19:30 CT · 2026-11-15T01:30:00Z · thread · F3 · K3 engagement

**New copy.**

**Post text** (122 chars). Copy exactly, no leading or trailing spaces:

```text
Echo Rounds is one dark room, four echo cells, sixteen shots. The shots are the only light, and every shot gives you away.
```

**Thread part 2** (242 chars), reply to part 1 at 2026-11-15T01:31:00Z (about 60 seconds later; not a separate calendar slot):

```text
One room, one mechanic, one trade-off per shot. Keyboard and mouse, so it is a desktop game. No install, no account: https://flambeee.com/games/echo-rounds.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-camp-20261113-08
```

**Asset:** none. Text-only post.

**Alt text:** none (text-only).

**Sources:**

- One dark room, four echo cells, 16 shots, shots are the only light, every shot gives you away: claims row 25; https://flambeee.com/games/echo-rounds.html (checked 2026-11-12).
- Keyboard-only, not mobile-playable: claims row 13; client brief §1-§2.
- One room, one mechanic, one trade-off per shot: `plans/social-media-plan.md` §6.2 (F3).
- No install, no account: claims rows 4 and 5.


---

### 09 · Sun 2026-11-15 09:00 CT · 2026-11-15T15:00:00Z · text · F1 · K2 followers

**New copy.**

**Post text** (245 chars). Copy exactly, no leading or trailing spaces:

```text
Six small browser tools: Day Pad, Timer, Tally, Dice, Coin Flip, Convert. No account, no install, no ads. Open one and use it: https://flambeee.com/apps/index.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-camp-20261113-09
```

**Asset:** none. Text-only post.

**Alt text:** none (text-only).

**Sources:**

- Six apps, names: claims row 3; client brief §1.
- Apps page HTTP 200: https://flambeee.com/apps/index.html (Day Pad, plus the app list, checked 2026-11-12).
- No account, no install, no ads: claims rows 4, 5, 6.


---

### 10 · Sun 2026-11-15 12:05 CT · 2026-11-15T18:05:00Z · image · F1 · K3 engagement

**Reuse:** queue/social/2026-11-13-fb-bsky-3.json (gate: pass, 196 chars). Text unchanged; only the slot moved.

**Post text** (196 chars). Copy exactly, no leading or trailing spaces:

```text
Cinder gives you a new quest every UTC day. No install, no account. Try it: https://flambeee.com/games/cinder.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-bsky-20261113-03
```

**Asset:** `brand/flambeee-assets/assets/game-cinder.png`

**Alt text:** A Cinder screenshot: a retro text RPG on a dark background with green, yellow, and orange text. The title CINDER sits above a status bar reading FlambeeeHero, Lv.1, HP 10/10, ATK 3, DEF 2, Gold 20. The Town Square menu lists Wilderness, Weapon Shop, Armor Shop, Bank, Inn, Trainer, and Tavern.

**Sources:**

- Reused verbatim from `queue/social/2026-11-13-fb-bsky-3.json` (gate: pass, 196 chars, 2026-11-08). Slotted to the campaign's Sun 12:05 CT slot.
- Cinder is a BBS-style text RPG with a new quest every UTC day: claims row 11; client brief §1.
- No install, no account: claims rows 4 and 5.
- Image: `brand/flambeee-assets/assets/game-cinder.png` (client screenshot, 1024x768).


---

### 11 · Sun 2026-11-15 16:00 CT · 2026-11-15T22:00:00Z · text · F3 · K3 engagement

**New copy.**

**Post text** (273 chars). Copy exactly, no leading or trailing spaces:

```text
What happens when you paste a page of text into Typewreck? It becomes a fortress you can wreck with piercing shots. Same text, same wall. No account: https://flambeee.com/games/typewreck.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-camp-20261113-11
```

**Asset:** none. Text-only post.

**Alt text:** none (text-only).

**Sources:**

- Paste text, fortress, piercing shots, deterministic wall: claims row 26; https://flambeee.com/games/typewreck.html (checked 2026-11-12).
- Deterministic destructible wall: claims row 14; client brief §3.
- No account: claims row 5.


---

### 12 · Sun 2026-11-15 19:00 CT · 2026-11-16T01:00:00Z · image · F1 · K2 followers

**New copy. v1.2 (28-hour rule): lead game is Cinder, not 2048.**

**Post text** (276 chars). Copy exactly, no leading or trailing spaces:

```text
Nine games, six apps, one browser tab. Pick one and play. Start with Cinder if you want a reason to open it again tomorrow. No install, no account, no ads: https://flambeee.com/games/cinder.html?utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=fb-camp-20261113-12
```

**Asset:** `brand/flambeee-assets/exports/flambeee-ad-link-card-1200x628.png`

**Alt text:** flambeee link card: four game screenshots beside the line Nine games. No installs. No ads.

**Sources:**

- 9 games / 6 apps: claims rows 2 and 3; client brief §1; client homepage v0.50.0.
- No install, no account, no ads: claims rows 4, 5, 6.
- "a reason to open it again tomorrow": claims row 11 (Cinder, a new quest every UTC day); https://flambeee.com/games/cinder.html HTTP 200, "UTC day" present (checked 2026-11-14).
- Cinder as lead game: `app.bsky.feed.getAuthorFeed` pull 2026-11-14 12:12 CT; Cinder posts 1 like + 2 reposts + 1 reply; best single post 2026-08-30 launch. `queue/escalations/2026-11-14-28h-rule.md` §2.
- Image and alt text: `brand/flambeee-assets/manifest.json` (adLink), file `exports/flambeee-ad-link-card-1200x628.png`, rendered 2026-11-13 (pack v1.1).


---

## 4. Coverage audit

The brief's window is 72 hours. "Covered" here means four posts on each of the three campaign days, with the first post after the window opens and the last post before it closes. It does not mean an hourly heartbeat: the audience is US Central and asleep between 02:00Z and 15:00Z, and a post at 03:00 CT would be bot noise, not reach.

| Campaign day | Date (CT) | Posts | First UTC | Last UTC | Span |
|---|---|---|---|---|---|
| Day 1 | Fri 2026-11-13 | 4 | 18:05Z | 02:00Z (Sat) | 7h55m |
| Day 2 | Sat 2026-11-14 | 4 | 15:00Z | 01:30Z (Sun) | 10h30m |
| Day 3 | Sun 2026-11-15 | 4 | 15:00Z | 01:00Z (Mon) | 10h00m |
| **Total** | **3 days** | **12** | **18:05Z Fri** | **01:00Z Mon** | **12/12 slots filled** |

- Window opens 2026-11-13T14:00:00Z. First post is 4h05m later, after the 11:00 CT GO/NO-GO and the 12:05 CT first slot.
- Window closes 2026-11-16T14:00:00Z. Last post is 13h before the close, so a missed final slot still has a same-day late window.
- Every calendar day in the window has four posts. There is no empty day and no unfilled slot.
- The three overnight gaps are deliberate quiet hours, not omissions. A 24-hour heartbeat would post to an empty room and burn the account's credibility.

---

## 5. Hashtag and alt-text conventions

1. **No hashtags in this campaign. Zero of twelve.** The flambeee voice sheet and the campaign brief both ban them. Reach is not a reason to add one; the account has four followers and no hashtag history.
2. **Never hashtag a trademarked game name.** Minesweeper, Simon, and 2048 are third-party marks; no `#minesweeper`, `#simon`, or `#2048`, even if a future campaign reverses the no-hashtag rule. The same rule applies to the bare names in paid promotion without a legal read.
3. **Alt text on every image post, written before the post is scheduled.** This campaign has eight image posts (`#01`, `#02`, `#03`, `#05`, `#06`, `#07`, `#10`, `#12`). The alt text is in the post block and in the draft file; it is not optional and it is not written after publishing.
4. **Alt text describes what is visible, not what the post wants.** Name the game screen or card, the layout, and any on-image text verbatim. No marketing adjectives, no "image of", no emoji. Keep it under 300 characters where the image allows.
5. **One source for alt text.** For designer assets, use the `alt` line in `brand/flambeee-assets/manifest.json` verbatim. For client screenshots, use the alt text in this document and in the draft file. If an image changes, both change together. Text-only posts get an empty alt field, never the words "no image".

---

## 6. Execution rules

1. **Publish in UTC order.** The CT times are for the operator; the UTC timestamps are the contract. Do not reorder a slot because a later post looks stronger.
2. **Use the exact text.** No edits after gate pass. If a fact expires (a release, a site change, a client correction), pull the post, re-verify the claim, re-run the gate, and only then publish late.
3. **Use the exact asset and alt text.** Do not substitute a different screenshot, crop the designer card, or add text to an image. The designer files are final renders; changing them breaks the alt text.
4. **Links stay as written.** Every URL carries `utm_source=bsky&utm_medium=social&utm_campaign=F1&utm_content=<asset-id>`. Do not shorten, strip, or swap a specific game link for the homepage. The one post with no link is `#01`, deliberately: it asks for the follow, and the first game link is `#02` three hours later.
5. **The thread is one top-level post plus one reply.** `#08` publishes part 1 at 01:30Z; part 2 is a reply to part 1 at 01:31Z. K1 counts top-level posts, so the thread is 1 of 12, not 2 of 12.
6. **Idempotency.** Key every publish on `asset-id + bsky + date` (`fb-camp-20261113-01+bsky+2026-11-13`, and so on). A re-run updates in place; it never double-posts.
7. **Client rows stage, then publish under the §13 authorization.** The three reused posts already exist as `staged-awaiting-owner` JSON. For this window, Jake's §13 authorization replaces the owner handoff; the launch worker publishes all twelve after the gate pass and writes the manifest. The old release-only cadence does not apply to this window.
8. **Reply window.** Replies run 14:00-20:00 CT, max 5 per rolling 24 hours, at least 10 minutes apart, at most 2 per thread. Use `plans/reply-playbook-flambeee.md`.
9. **No-go fallback.** If the `@flambeee` session is not working by 2026-11-13 13:00 CT, the brief's fallback runs the same calendar from `@lightsword.bsky.social`. That is a channel-voice change: the Strategist must decide and log whether the flambeee-voice copy runs on the Lightsword account or the day is held. Do not silently swap accounts.

---

## 7. Conflicts and handoffs

### 7.1 The three staged 11-13 JSONs are the highest-risk collision

`queue/social/2026-11-13-fb-bsky-1.json`, `-2.json`, and `-3.json` all carry `date: 2026-11-13` and `slot: 12:05 America/Chicago`. They are a Friday batch of three drafts, but as filed they would fire three times at 12:05 on Friday if a scheduler reads the date and slot literally.

This calendar uses their text as posts `#02` (Wordfire, Fri 15:30), `#06` (Afterglow, Sat 12:05), and `#10` (Cinder, Sun 12:05). Before launch:

1. Set the old three JSONs to `status: superseded` (or `do_not_publish`) so no scheduler can fire them at 12:05 Friday.
2. Create the campaign JSONs from `queue/campaign/fb-campaign-2026-11-13.json` with the campaign slots and `status: ready-to-publish`.
3. If the launch worker prefers to keep the original files, re-date `-1` to 11-13 15:30, `-2` to 11-14 12:05, and `-3` to 11-15 12:05, and change their `slot` fields to the campaign UTC times. Do not leave all three at 11-13 12:05.

### 7.2 The 30-day calendar

`plans/calendar-30d.md` has three `FB Bluesky (staged)` rows on 2026-11-13 pointing at the same three drafts. This campaign calendar supersedes those FB rows for 2026-11-13 through 2026-11-15. The launch worker should add a note to the 30-day calendar or treat the campaign JSON as the source for the window, so the nightly does not try to stage a fourth 11-13 FB post.

### 7.3 Claims re-verification is a launch-day task, not a copy task

`brand/claims-flambeee.md` was re-verified on 2026-11-13: v0.50.0 / 55 releases, nine games including SALTLINE. This copy avoids release and version counts entirely except the historical Timer line (`v0.43.0`), which is sourced to claims row 23 and the public BLOG and remains true. The count rows are now nine games / six apps; the three posts and one reply snippet that carried a count were re-gated at 12/12 on 2026-11-13.

### 7.4 Asset pack dependency is satisfied

`brand/flambeee-assets/manifest.json` v1.0 (2026-11-12) contains the three ad renders used here: `flambeee-ad-claim-1080x1080.png`, `flambeee-ad-game-spotlight-1080x1080.png`, `flambeee-ad-link-card-1200x628.png`. All three were rendered and checked at the exact dimensions; the alt lines above come from that manifest. The avatar (`flambeee-avatar-bluesky-1000x1000.png`) and Bluesky banner (`flambeee-banner-bluesky-3000x1000.png`) are the profile assets for the launch checklist. The bio string is brief §5 as amended on 2026-11-13: 'Nine free browser games and six small apps. No install, no account, no ads. Progress stays on your device. flambeee.com'; the profile was updated from the 8-game string after SALTLINE shipped.

### 7.5 The Day-3 Lightsword quote-post is not one of the 12

The brief's Day 3 10:00 CT item is a Lightsword-account quote-post of the top campaign post. It is not in this calendar and not in the 12-post count. If the launch worker runs it, it needs a separate Lightsword-voice draft, its own gate pass, and its own idempotency key. Do not post flambeee-voice copy on `@lightsword.bsky.social`.

### 7.6 Credential and authority

`t_37a3f3c6` owns the app password and session test. `plans/scope-flambeee.md` §13 owns the window authority. Neither is assumed here: if the session test fails, the brief's fallback applies and the Strategist logs the substitution.

---

## 8. Definition of done for this deliverable

- [x] 12 top-level posts, 4 per campaign day, all inside the 72-hour window.
- [x] Every post ≤300 characters including its URL. Longest: #11 at 273; #04 at 272.
- [x] 9 new posts and the 3 gate-passed 11-13 drafts reused with their text unchanged.
- [x] Every post lands on a specific game or app page, except #01 (the follow-first hook); #08 carries its link in the thread reply.
- [x] 8 image posts, each with an existing asset file and alt text; 4 text/thread posts with no asset.
- [x] Every image post's alt text is written in the post block and in its draft file.
- [x] A mini-thread (2 posts), a question post (#11), a one-liner (#07), demos, a story, and a CTA.
- [x] 12 drafts, each with frontmatter, sources, and a gate pass.
- [x] Reply playbook at `plans/reply-playbook-flambeee.md` with 10 pre-approved snippets, the hard rules, and the escalation template.
- [x] Machine-readable schedule at `queue/campaign/fb-campaign-2026-11-13.json`.

---

## 9. Source ledger

| Claim used in copy | Source | Post(s) |
|---|---|---|
| 9 games, 6 apps | `plans/client-brief-flambeee.md` §1; `brand/claims-flambeee.md` rows 2-3; client homepage v0.50.0 | 1, 9, 12 |
| No install, no account, no ads | claims rows 4-6 | 1, 3, 5, 7, 9, 12 |
| Wordfire: one word a day, five letters, streak | claims row 10 | 2 |
| 2048: merge tiles, reach 2048, high score | claims row 17 | 3, 12 |
| Timer 7.5 / 7 minutes defect, fixed in v0.43.0 | claims row 23; public `BLOG.md`, `v0.43.0: Timer stops lying about decimals` | 4 |
| Simon: colorblind mode, four colors and four shapes | claims rows 15 and 24; public README | 5 |
| Afterglow: board lights, goes dark, moves from memory | claims row 12 | 6 |
| Minesweeper: first click safe, long-press flag | claims row 16; public README | 7 |
| Echo Rounds: one dark room, four echo cells, 16 shots, shots are the only light | claims row 25; `https://flambeee.com/games/echo-rounds.html` | 8 |
| Six apps and their names | claims row 3 | 9 |
| Cinder: BBS-style text RPG, new quest every UTC day | claims row 11 | 10 |
| Typewreck: paste text, fortress, piercing shots, deterministic | claims row 26; `https://flambeee.com/games/typewreck.html` | 11 |
| Designer ad copy and alt text | `brand/flambeee-assets/manifest.json` | 1, 6, 12 |

---

*Written 2026-11-12 for kanban `t_e903944b`. The strategy is `plans/campaign-72h-2026-11-13.md`; this document is the words and the slots.*
