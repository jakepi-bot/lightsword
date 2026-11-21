# Claims list — flambeee

**Version:** 1.0 · **Date:** 2026-11-08 · **Due:** 2026-11-14 · **Owner:** Content Lead; review Strategist
**2026-11-12 campaign additions:** rows 23-26 were added from public pages for the 72-hour campaign (Timer, Simon board, Echo Rounds, Typewreck).
**2026-11-13 launch-day re-verification:** v0.50.0 shipped at 09:24Z with SALTLINE, the ninth game; the client homepage now says "Nine games, still one file each". Row 2 and rows 19-20 updated to 9 games / v0.50.0 / 55 releases. The three campaign posts that carried a count were re-gated after the edit.
**2026-11-15 correction:** the style-ban row still said "8 games / 6 apps", the 2026-11-08 baseline. Corrected to nine games / six apps (nine live `/games/*.html` pages verified on the homepage graph tonight). Decision: `queue/escalations/2026-11-15-claims-count-rule.md`.
**2026-11-18 release re-verification (nightly):** v0.52.0 shipped 2026-11-18T08:59Z with Empty Hands, the tenth game. Public homepage now links ten `/games/*.html` pages including `empty-hands.html`; BLOG.md Session 65 calls it "the tenth game". Rows 2, 19, 20 and the style-ban count row updated to ten games / six apps / v0.52.0 / 57 releases. No LT or FB asset carried a count tonight; the 11-20 FB batch carries none by brief.
**2026-11-20 release re-verification (nightly):** v0.53.0 shipped 2026-11-19T09:02Z with a Cinder local play counter: one line under the status bar, one `localStorage` key (`flambeee-cinder-plays`), no network call. Rows 8, 19 and 20 updated to v0.53.0 / 58 releases. No 11-20 asset carries a release count; the FB batch carries none by brief.
**2026-11-20 22:00 re-verification (nightly):** v0.54.0 shipped 2026-11-20T10:04Z ("Detail-view plays rows" for Cinder, Afterglow, Typewreck). No new game or app: ten games / six apps unchanged, all ten `/games/*.html` pages HTTP 200 on the live homepage graph. Rows 19 and 20 updated to v0.54.0 / 59 releases (GitHub releases API returned 59). The release body says the site never writes localStorage and the plays helper is read-only, so row 8 stands. No asset tonight carries a release count.
**2026-11-21 release re-verification (nightly):** v0.55.0 shipped 2026-11-21T08:57Z ("Empty Hands BUST copy and instrument truthfulness"; Empty Hands BUST-title fix and Ctrl/Cmd/Alt input guard, plus tooling). No new game or app: ten games / six apps unchanged; homepage copy reads "Ten games, one arcade"; all ten `/games/*.html` pages HTTP 200. Rows 19 and 20 updated to v0.55.0 / 60 releases (GitHub releases API, paginated count). The release body says no new storage keys, no network calls, no identity, no PII, so row 8 stands. No asset tonight carries a release count (empty weekend row).
**Source of truth:** `plans/client-brief-flambeee.md` v1.0 and the public surface
checked 2026-11-08. A claim not in this file does not go in copy.
**Verification:** every public URL cited here returned HTTP 200 on 2026-11-08;
counts were re-derived from the live surface. No Set-Cookie header and no
analytics/tracker script were found on the homepage or the 14 game/app pages.
**Expiry rule:** a release, a site copy change, or a client correction expires
the affected rows immediately. Recheck the whole file every Friday.

## 1. Canonical facts (usable today)

| # | Claim (use this wording) | Source | Verified | Recheck | Status |
|---|---|---|---|---|---|
| 1 | Flambeee is a small software company with two divisions: Flambeee Games and Flambeee Apps. | client brief §1 | 2026-11-08 | 2026-12-08 | usable |
| 2 | Ten free browser games: Wordfire, Minesweeper, Simon, 2048, Cinder, Afterglow, Echo Rounds, Typewreck, Saltline, Empty Hands. | client brief §1 (count rule); 10 `/games/*.html` pages HTTP 200 on the live homepage graph 2026-11-18; BLOG.md Session 65; v0.52.0 | 2026-11-18 | next release | usable — use ten games / six apps |
| 3 | Six small browser apps: Day Pad, Timer, Tally, Dice, Coin Flip, Convert. | client brief §1; 6 `/apps/*.html` pages HTTP 200 | 2026-11-08 | next release | usable |
| 4 | Everything runs in a modern browser; there is nothing to install. | client brief §1; flambeee.com (HTTP 200) | 2026-11-08 | 2026-12-08 | usable |
| 5 | No account and no sign-up. | client brief §1; flambeee.com | 2026-11-08 | 2026-12-08 | usable |
| 6 | No ads. | client brief §1; flambeee.com | 2026-11-08 | 2026-12-08 | usable |
| 7 | No cookies, trackers, or PII. | client brief §1; flambeee.com | 2026-11-08 | 2026-12-08 | usable |
| 8 | Progress and play counts stay in your browser's localStorage; Afterglow's and Cinder's play counters make no network call. | client brief §1, §3; v0.47.0 release body; v0.53.0 release body (GitHub API) | 2026-11-20 | next release | usable |
| 9 | The PWA is optional; the precached shell works offline after the first load. | client brief §1, §3 | 2026-11-08 | next release | usable |
| 10 | Wordfire gives you one word a day; guess the 5-letter word and keep your streak. | flambeee.com; public README | 2026-11-08 | next release | usable |
| 11 | Cinder is a BBS-style text RPG with a new quest every UTC day. | flambeee.com/games/cinder.html; client brief §2 | 2026-11-08 | next release | usable |
| 12 | Afterglow lights the board, goes dark, and takes moves from memory. | flambeee.com; client brief §3 | 2026-11-08 | next release | usable |
| 13 | Echo Rounds is fire light in a dark room; it is keyboard-only. | flambeee.com; client brief §1-§2 | 2026-11-08 | next release | usable — never feature it in mobile creative |
| 14 | Typewreck turns pasted text into a deterministic destructible wall. | client brief §3; `/games/typewreck.html` HTTP 200 | 2026-11-08 | next release | usable |
| 15 | Simon has a colorblind mode; Wordfire has a colorblind mode. | client brief §2 | 2026-11-08 | next release | usable — no WCAG claim |
| 16 | Minesweeper's first click is safe; mobile uses long-press to flag. | public README | 2026-11-08 | next release | usable |
| 17 | 2048 merges tiles; reach 2048 and chase a new high score. | flambeee.com | 2026-11-08 | next release | usable |
| 18 | Day Pad is a UTC-day countdown plus one saveable line; the line stays in the browser. | `/apps/` page (HTTP 200); client brief §1 | 2026-11-08 | next release | usable |
| 19 | The current release is v0.55.0, published 2026-11-21. | GitHub releases API | 2026-11-21 | next release | usable |
| 20 | 60 releases to date. | GitHub releases API, 2026-11-21 | 2026-11-21 | next release | usable only with "client count" attribution |
| 21 | Free; there is no paywall. | client brief §1; flambeee.com | 2026-11-08 | 2026-12-08 | usable |
| 22 | No analytics, no email list, no aggregate play or traffic number exists. | client brief §1, §6 | 2026-11-08 | 2026-12-08 | usable as a limitation, never as a growth claim |
| 23 | Timer v0.43.0 fixed a display bug: typing 7.5 minutes ran the clock for 7 minutes while the field still said 7.5; the field now corrects to the value the clock actually uses. | public `BLOG.md`, section "v0.43.0: Timer stops lying about decimals" (https://github.com/jakepi-bot/flambeee/blob/main/BLOG.md) | 2026-11-12 | next release | usable |
| 24 | Simon's board is four colored buttons with shape symbols: circle, triangle, square, diamond. | `/games/simon.html` screenshot (checked 2026-11-12); public README "Colorblind-friendly with shape symbols" | 2026-11-12 | next release | usable |
| 25 | Echo Rounds is one dark room with four echo cells and 16 shots; shots are the only light, and every shot gives you away. | `/games/echo-rounds.html` (checked 2026-11-12) | 2026-11-12 | next release | usable — keyboard-only, never mobile creative |
| 26 | Typewreck turns pasted text into a fortress wrecked by piercing shots; the same text produces the same wall. | `/games/typewreck.html` (checked 2026-11-12); claim 14 | 2026-11-12 | next release | usable |

Status values: `usable`, `needs check`, `banned` (banned rows live in §2). A
qualified status such as "usable only with client count" means the wording must
carry the stated qualification.

## 2. Banned claims and words (do not use)

The first table copies the off-limits claims from `plans/client-brief-flambeee.md`
§3 verbatim, one row per semicolon group. The second table adds the style bans
that apply to flambeee copy.

| Banned (verbatim, brief §3) | Why |
|---|---|
| controller support, FPS, native/Steam/app-store, multiplayer, leaderboards, accounts, cloud saves, cross-device sync | Not features; the FPS/gamepad gate is open. |
| player counts, play totals, retention, traffic, "growing", "viral" | No measurement exists; the client forbids the claim. |
| revenue, ads, pricing, "free forever", paid tier | Not sourced. "Ads" here means ad revenue or an ad product; the absence of ads is claim 6 and is usable. "Free forever" is a promise the client has not made. |
| roadmap, "soon", "coming", unshipped features | Claim creep; social plan §9.3. |
| "open source" or any license claim until the MIT/GPL contradiction is fixed | README says MIT; LICENSE is GPL-3.0. Resolve before claiming either. |
| "Seven games" and "new game every Tuesday and Friday" (both stale) | Public homepage and README are stale; the client ruled 8 games / 6 apps on 2026-11-08. The build days are Mon/Wed/Fri and the 3-posts-a-week proposal is not approved. |
| "original" for Minesweeper/Simon/2048 | Classic games; only the implementation is original. |
| WCAG/ADA, COPPA/GDPR/CCPA, "secure", "anonymous" | No audit or legal basis. |
| community size or "community-driven" | No measurement; no community data. |
| "fastest" without measurement | Speed claim needs a number and a method. |
| "AI-powered" or internal team/tooling references | Not a product claim. |

| Additional style bans | Why |
|---|---|
| "five games", "seven games", "eight games", "nine games", or any count except ten games / six apps — the count rule is ten games / six apps; 5, 7, 8 and 9 are stale (9 was the count before v0.52.0 shipped Empty Hands on 2026-11-18) | Corrected 2026-11-18 by the nightly (Content Lead re-verification, release-day rule); ten `/games/*.html` pages verified on the live homepage graph. Prior correction 2026-11-15: `queue/escalations/2026-11-15-claims-count-rule.md`. |
| "players love it" | No measurement; no community data. |
| "Addictive", "immersive", "epic", "world-class", "seamless", "leverage", "synergy", "best-in-class", "revolutionary", "unlock", "thrilled", "excited" | flambeee voice and the Lightsword gate both reject these. |
| Em dashes | flambeee voice calls for plain punctuation. |

## 3. Maintenance

- Recheck every row on the Friday after a release, and immediately after any
  client copy correction.
- A row that cannot be re-verified moves to `needs check`; it does not stay
  `usable` by inertia.
- New claims enter only with a source and a recheck date. Unknown beats
  invented.
