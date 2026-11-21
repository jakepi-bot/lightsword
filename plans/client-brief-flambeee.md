# Client brief — flambeee

**Version:** 1.0 · **Date:** 2026-11-08 · **Owner:** Strategist (account lead) · **Status:** active
**Sources:** flambeee bot intake reply, 2026-11-08 07:20 CST (verbatim: `queue/handoff/flambeee-intake-2026-11-08.md`); public-surface checks 2026-11-08 (`flambeee.com`, public README/BLOG/releases); `plans/scope-flambeee.md`.
**Rule for every asset:** if a line here is not sourced, it does not go in copy. Unknown beats invented.

---

## 1. Product summary

flambeee is a small software company with two live divisions: **Flambeee Games**, eight free browser games, and **Flambeee Apps**, six small browser utilities. Everything is a dependency-free web page: no install, no account, no ads, no paywall, no cookie banner; progress stays in the browser. Current release **v0.47.0 (2026-11-08)**; 52 releases and 49 blog posts to date (client count).

| Fact | Canonical value | Proof |
|---|---|---|
| Games | **8**: Wordfire, Minesweeper, Simon, 2048, Cinder, Afterglow, Echo Rounds, Typewreck | Client ruling 11-08; 8 live `/games/*.html` links, all HTTP 200, checked 11-08 |
| Apps | **6**: Day Pad, Timer, Tally, Dice, Coin Flip, Convert | Client ruling; 6 live `/apps/*.html` links |
| Count rule | **Use 8 games / 6 apps. Never 5 or 7.** | Site header "Seven games", README five, and GitHub description are stale |
| Friction | Free; no ads, no cookies, no trackers, no PII | Client; site/README |
| Platform | Modern browser, mobile-first; PWA optional; Echo Rounds is keyboard-only | Client |
| Status | v0.47.0 released 2026-11-08; release chain complete | GitHub releases API; client |

**Player sentence (client-approved):** "Pick a game and play in your browser. Nothing to install, no account, no ads."

> The 2026-11-05 proposal is stale on version (v0.44.0), release count (49), blog posts (46), and Bluesky posts (38). Use this brief.

## 2. Audience

| Segment | Definition | Copy consequence |
|---|---|---|
| **Primary** | Casual mobile break players: thumb-sized, two-minute, no-signup play | Lead with play-now, one tap, no account |
| **Secondary** | Daily word/puzzle players (Wordfire daily, Cinder daily quest, Afterglow daily seed) | Only retention loop; daily/streak language; no push or notification claims |
| **Not the audience** | Competitive/esports; multiplayer, leaderboards, accounts, cloud saves, cross-device sync; console/AAA/native; retro/BBS nostalgia as a segment; developer/open-source browsers; under-13 | Never target or imply these |

English only, no localization; daily resets are UTC. Desktop works; **Echo Rounds is not mobile-playable** — never feature it in mobile creative. General audience, no accounts, no PII; do not target children. Colorblind modes exist in Wordfire and Simon; there is no WCAG audit or conformance claim.

## 3. Positioning

**Positioning statement (Lightsword, derived):** For casual mobile break players who want two minutes of play without a signup, flambeee is the free browser arcade that opens in one tap and asks for nothing — no install, no account, no ads, no tracking. Eight games and six small apps, playable in the browser, with progress kept on your own device.

**Three differentiators, true today:**
1. **Zero friction** — all 8 games and 6 apps are free and run in the browser; no install, account, ads, paywall, or cookie banner. The PWA installs and the precached shell works offline after first load.
2. **Privacy by architecture** — no analytics, trackers, cookies, or PII; progress and play counts live only in the browser's localStorage. This is also why no traffic or aggregate-play number can be reported.
3. **Original mechanics that shipped** — Afterglow separates the information window from the input window (board lights, then goes dark and accepts moves only from memory); Typewreck turns any pasted text into a deterministic destructible wall.

| Competitor | The one true advantage to use |
|---|---|
| NYT Games | No account or subscription; Wordfire is free and immediate |
| Poki | No ads and no cookie banner |
| CrazyGames | No ads and no install prompts |
| itch.io | No store page or download step; click and play |
| minesweeper.online | No account or leaderboard requirement, plus 8 other games; first-click-safe, mobile long-press flag |

Use these as "where flambeee is different today", never as blanket "better than". **No paid promotion using the Minesweeper, Simon, or 2048 names without a legal read.**

**Off-limits claims:** controller support, FPS, native/Steam/app-store, multiplayer, leaderboards, accounts, cloud saves, cross-device sync; player counts, play totals, retention, traffic, "growing", "viral"; revenue, ads, pricing, "free forever", paid tier; roadmap, "soon", "coming", unshipped features; "open source" or any license claim until the MIT/GPL contradiction is fixed; "Seven games" and "new game every Tuesday and Friday" (both stale); "original" for Minesweeper/Simon/2048; WCAG/ADA, COPPA/GDPR/CCPA, "secure", "anonymous"; community size or "community-driven"; "fastest" without measurement; "AI-powered" or internal team/tooling references.

## 4. Voice and tone

**flambeee voice (client ruling; derived from its own writing):**
1. Direct, technically precise, no filler. Dry humor. Exact with numbers and names. No buzzwords.
2. Plain punctuation, **no em dashes**. At most one emoji where it genuinely fits; no heavy emoji.
3. Short sentences. Specific over adjectives.
4. Never overclaim. If a number is not measured, do not use it. State the limitation as plainly as the claim.
5. **"flambeee" lowercase** for the wordmark/product; **"Flambeee"** for the company. Flame mark and navy/flame palette, no substitutions.
6. Release-note voice on @flambeee: **yes for tone and honesty, no for format**. Release posts are one short paragraph, 300 graphemes max, and must include `https://flambeee.com`. Marketing may be longer, but it must sound like the same person.

**Use:** play, browser, free, no account, no install, no ads, no tracking, on your device, small, sharp, pick one and go, daily, streak, memory, paste, wreck.
**Avoid:** revolutionary, immersive, epic, world-class, seamless, leverage, synergy, best-in-class, addictive, viral, soon, coming soon, AI-powered, free forever, unlimited, secure, anonymous, GDPR compliant, WCAG compliant, community-driven, players love it.

**Brand assets (client-supplied):**
- **Logo:** public repo `brand/logo/` — PNG 16/32/64/128/256/512, 400px avatar, 1200px and 1500px banner PNGs plus SVG banner, logo-icon SVG, PWA icon SVG, favicon. Use SVG masters; do not recolor, crop, or distort.
- **Palette:** `#0f1428` page background, `#1a1a2e` surface, `#e94560` flame accent, `#ff5a75` secondary, `#ffb74d` amber, `#eef2ff` text, `#9aa7d8` dim, `#2a3a6e` border, 14px radius. Dark theme only.
- **Font:** system sans stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`); no custom webfont.
- **Screenshots:** `website/assets/` has six game shots (Wordfire, Minesweeper, Simon, 2048, Cinder, Afterglow); missing Echo Rounds and Typewreck; no app screenshots. Release cards in `brand/release/` are stale.
- **Permission:** logos and existing screenshots may be used in flambeee-owned materials. New assets need Palette review. Co-branding, portfolio, or case-study use needs Jake. There is no public brand page or press kit.

Lightsword house voice is separate and never appears on the client account. A Lightsword-voice sentence on the flambeee channel is a gate failure, not a style note.

## 5. Channels and publishing

| Channel | Role | Owner / publisher | Cadence | Lightsword rights |
|---|---|---|---|---|
| flambeee.com | Owned primary surface | Ember (copy); Jake syncs ~11:00 CST; no analytics | Continuous | Suggestions only |
| @flambeee.bsky.social | Only social channel; bot-labeled; 4 followers / 41 posts (11-08) | Ember drafts, Vigil clears, noon cron posts 12:05 CST; Jake holds credentials | Written policy: release announcements only | **Drafts to staged buffer only. No credentials. Owner posts every item, one at a time.** |
| GitHub releases + README | Public release record, developer/SEO surface; 0 stars | Release owner; README/BLOG Ember | Per release (52 so far) | Read-only; file copy defects as text |
| BLOG.md | Long-form, GitHub-hosted | Ember | Per release | Read-only |
| Lightsword channels | Lightsword's own audience | Lightsword (Phase 2 autonomous) | LT cadence; separate voice | Publish after gate + Strategist |

**Cadence note.** The client proposes 3 posts/week on @flambeee (Mon/Wed/Fri, tied to build days). That is an expansion of its written release-only policy and needs Jake's amendment before the first non-release post. Until it lands, FB items stay staged-awaiting-owner and only release posts go out. The existing 2/week Fri/Sun plan is superseded by this proposal once amended; the staged 11-15 (Sunday) item is re-slotted to Mon 11-16 / Wed 11-18 by the 11-08 weekly planning run.

**Deadlines and operating rhythm (client):**
- No launches, events, embargoes, or blackout dates are documented through 2027-02-06.
- One dated milestone: **2026-12-07** — Typewreck Game-of-the-Week revisit gate (3+ external signals or 20+ local plays). A decision date, not a launch; marketing can influence it.
- Operational: site sync ~11:00 CST; Bluesky post 12:05 CST daily; copy staged before noon. Build days are Mon/Wed/Fri; legacy maintenance Tue/Thu/Sat/Sun (written cadence policy sits in an open PR).
- No FPS date (gamepad gate open), no app launch date, no v1.0 date.

## 6. 30-day deliverables (2026-11-08 → 2026-12-08)

**Baseline (2026-11-08, client + public API):** 4 Bluesky followers / 41 posts / 0-1 likes / 0 reposts / 0 replies; 0 GitHub stars and forks; 26 repo views and 1 unique in 14 days; 52 releases, 49 blog posts; 2 external humans lifetime; no site analytics; no email list.

| # | Deliverable | Lightsword owner | Client counter-owner | Due |
|---|---|---|---|---|
| 1 | Claims list (`brand/claims-flambeee.md`): every usable claim, its source, its expiry | Content Lead; Strategist review | Vigil PASS | **Sat 2026-11-14** |
| 2 | Voice sheet (`brand/voice-flambeee.md`): rules, use/avoid, worked examples | Content Lead | Ember sign-off | **Sat 2026-11-14** |
| 3 | 12 staged FB Bluesky drafts, 3/week Mon/Wed/Fri, one at a time (A02 11-13 already staged; 11-15 re-slots) | Content Lead → Distribution Lead | Ember (copy), Vigil (claims); owner posts | Batches **11-13, 11-20, 11-27, 12-04** |
| 4 | 2 launch posts on Lightsword's own account for the next two new-game days | Content Lead → Distribution Lead (LT) | — | Within 24h of each release; first checkpoint **Fri 2026-11-13** |
| 5 | Copy defect list to Ember: "Seven games" header, Bluesky bio cadence, README license, GitHub description | Strategist | Ember | **Thu 2026-11-12** |
| 6 | Asset gap list + requests: Echo Rounds/Typewreck screenshots, release cards for Cinder/Echo Rounds/Typewreck, app screenshots | Content Lead | Palette | **Sat 2026-11-21** |
| 7 | Weekly proxy-metric report: followers, stars, external humans, third-party links — no dashboard | Analyst | — | Fridays **11-13, 11-20, 11-27, 12-04** |
| 8 | Typewreck Game-of-the-Week campaign window (3+ external signals or 20+ local plays) | Content Lead; Strategist | Ember | **Mon 2026-12-07** |
| 9 | Day-30 review: plan vs actuals, keep/kill input for the primary segment | Analyst + Strategist | Ember/Jake | **Tue 2026-12-08** |

**30-day targets (client-proposed, adopted):** Bluesky 4 → 40 followers; GitHub stars 0 → 10; 5 new external humans (reply, issue, or DM) against a lifetime baseline of 2; 1 third-party link or mention. **No targets for plays, sessions, or traffic.**

## 7. 90-day deliverables (by 2027-02-06)

| Deliverable | Owner |
|---|---|
| 36 posts delivered and posted (or the agreed cadence) | Content Lead / Distribution Lead |
| 3 campaigns tied to actual ships | Strategist + Content Lead |
| 6 new visual assets (Palette review for any new asset) | Content Lead |
| 2 third-party placements | Strategist |
| Written segment read with real numbers | Analyst |
| Keep-or-kill recommendation on the primary segment | Analyst + Strategist |
| 90-day report: channel performance + measurement recommendation | Analyst |

**90-day targets (client-proposed, adopted):** Bluesky 150 followers; GitHub 25 stars; 15 distinct external humans; 3 third-party links; one written segment read; keep/kill call. No play, traffic, or retention targets.

## 8. Approval and compliance

**Chain (corrected 2026-11-08; scope §10 said "JakeBOT" — jakebot is advisory only):**

| Step | Who | Scope | SLA |
|---|---|---|---|
| 1 | **Ember** | Copy owner; edits and owns the channel | 1 business day (proposed) |
| 2 | **Vigil** | PASS on external copy; under the proposed model, only copy that makes a claim not on the approved claims list | Within the 48h campaign window |
| 3 | **Jake** | Positioning, commitments, legal, credentials | Final call |
| — | Palette | New visual assets | Per asset |
| — | Rook | Mechanic claims | Per claim |

**48h SLA** applies to planned campaign items; release posts stay on the daily noon pipeline. Anything undecided at 48h escalates loudly with its date. **Lightsword internal gate:** `workflows/gate.py` pass + Strategist adjudication; LT channels publish autonomously, FB stays draft-only.

**Forbidden claim classes:** privacy ("anonymous", "secure", "GDPR/CCPA compliant"; "no analytics, no trackers, no cookies" is true); play counts (no aggregate numbers, player counts, retention); pricing (everything is free; no "free forever", paid tier, or ads); competitor comparisons (only named true claims; legal read before paid promotion using Minesweeper/Simon/2048); age (no child-directed marketing, no COPPA claim); accessibility (colorblind modes and keyboard support are true per title; no WCAG/ADA conformance); roadmap (no unshipped features or "soon"); license (no MIT/GPL/open-source claim until fixed).

**Legal constraints:** no privacy policy, no terms page, no registered entity, no press contact; license contradiction (GPL-3.0 in LICENSE, MIT in README); trademark risk on Minesweeper, Simon, 2048; @flambeee carries a self-applied "bot" label — do not present it as human-run; no age gate — do not target under-13; no team mixing (never reference other bots, teams, or internal tooling in public copy).

## 9. Assumptions (stated so work does not stall)

1. **Working agreement.** No Lightsword deliverables are recorded in Flambeee's team files. The 2026-11-05 scope plus this reply's 30/90-day list form the agreement; nothing else is promised.
2. **Launch date.** No single launch date or v1.0 exists. "Launched" means the continuous release chain; current status is v0.47.0 (2026-11-08). No "launch" claim is made.
3. **Cadence.** 3/week Mon/Wed/Fri is a proposal, not policy. Non-release FB posts stay staged until Jake amends the written release-only policy. Fallback schedule: first full week 11-16, giving 10 of 12 posts in-window; all 12 land by 12-04 if the amendment arrives by 11-12.
4. **Counts.** 8 games / 6 apps is canonical. 5 and 7 are banned. The stale header, bio, README, and GitHub description are flambeee's fixes; Lightsword files them as text and never edits client files.
5. **Measurement.** No aggregate plays, traffic, or retention exist. Reports use proxies only (followers, stars, external humans, links, inbound). On-device counters (Typewreck v0.45.0, Afterglow v0.46.0; Cinder owed #215) are user-facing artifacts, not campaign metrics.
6. **Assets.** Logos and existing screenshots may be pulled from the public repo for flambeee-owned materials. Co-branding, portfolio, or case-study use of the flambeee name/logo needs Jake; until then it is not used on Lightsword channels.
7. **Echo Rounds.** Keyboard-only prototype; excluded from mobile creative, used desktop-only as a secondary asset.
8. **Apps.** Secondary to games; games lead every asset, apps appear only as proof of the "small useful tools" claim.
9. **Campaign dates.** None exist client-side. Lightsword proposes ship-linked dates; the only dated milestone is the 12-07 Typewreck GOTW revisit gate.
10. **Competitors.** Names are used descriptively, never in paid promotion without a legal read.
11. **Legal prerequisites.** No privacy policy, terms, entity, or press contact. No legal/compliance claims, no data-collection CTA, and no paid spend until Jake resolves them.
12. **License.** MIT in README vs GPL-3.0 in LICENSE is unresolved; no license or open-source claim is made.
13. **Age.** General audience, no accounts/PII, but no COPPA review. No under-13 targeting, no child-directed creative.
14. **Approval.** The corrected chain is Ember → Vigil → Jake; jakebot is advisory only. 48h applies to campaign items; release posts stay on the noon pipeline.

## 10. Open decisions for Jake

1. **Cadence amendment** — release-only → 3/week Mon/Wed/Fri non-release posts on @flambeee. Needed before the first non-release post; target **2026-11-12**.
2. **Co-branding/portfolio use** of the flambeee name and logo on Lightsword channels — needed before any LT portfolio piece; target **2026-11-14**. (Naming on LT channels was granted 2026-11-07; this is logo/mark usage.)
3. **Campaign date sign-off** — confirm the 11-30 → 12-07 Typewreck GOTW window, or supply a different date. No date exists client-side.
4. **Paid promotion** — blocked while there is no entity, privacy policy, or terms; any paid spend is a Jake decision.

---

## Appendix A — Questionnaire coverage

| Q | Item | Where answered |
|---|---|---|
| 1 | Product and one-sentence promise | §1 |
| 2 | Launch date, status, canonical count, apps in scope | §1; Assumption 2 (no single launch date) |
| 3 | Audience segments, non-audience, constraints | §2 |
| 4 | Competitor set and true advantage | §3 |
| 5 | Differentiators and off-limits claims | §3 |
| 6 | Brand voice and tone rules | §4 |
| 7 | Brand guidelines and assets | §4 (brand assets); Assumption 6 |
| 8 | Priority channels, ownership, cadence | §5 |
| 9 | Success metrics, measurable today | §5 (baseline), §6, §7; Assumption 5 |
| 10 | Hard deadlines | §5 (deadlines); Assumption 9 |
| 11 | Compliance and approval | §8; Assumption 14 |
| 12 | 30-day and 90-day deliverables | §6, §7 |
| 13 | Anything else | §8 (legal), Assumptions 4/7/12/13, §10 |

## Appendix B — Verification log (2026-11-08)

- flambeee.com: header text "Seven games" over **8 game links**, all `/games/*.html` HTTP 200 (Wordfire, Minesweeper, Simon, 2048, Cinder, Afterglow, Echo Rounds, Typewreck).
- Apps: **6 app links** (Day Pad at `/apps/index.html`, Timer, Tally, Dice, Coin Flip at `/apps/coin.html`, Convert), all HTTP 200.
- GitHub: v0.47.0 release published 2026-11-08T08:58Z; 52 releases (Link header); 0 stars/forks; description still lists five games; LICENSE is GPL-3.0 while README says MIT.
- Bluesky public API: @flambeee.bsky.social 4 followers, 41 posts, self-applied "bot" label; bio still says "New game every Tuesday and Friday".
- Brand: `brand/logo/` contains 13 files (16-512px PNGs, 400px avatar, 1200/1500px banners, SVG banner, logo icon, PWA icon, favicon).

