# Scope: flambeee (client one)

status: live branch record
owner: Strategist (account lead)
created: 2026-11-05
inputs: plans/social-media-plan.md §9, plans/social-accounts-and-site-plan.md, live checks 2026-11-05/06
approved by: Jake

## 1. Live branch (§9.4)

Neither A nor B as written. Week-0 audit found the account:

- **Channel B is `@flambeee.bsky.social`** — exists, active, owner-managed. Release-note voice, links to flambeee.com.
- Lightsword creates no parallel account. No `flambeee-marketing` handle, no split audience, no second reply surface.
- Lightsword role: draft only. FB rows stay FB rows pointed at `@flambeee.bsky.social`. Owner approves copy; owner publishes (Jake holds both hats today; approvals stay separate rows with `client: fb`).
- Phase 1 needs no app password for this account. Nothing publishes from the repo. If a credential is ever needed, the owner issues it; Lightsword never takes ownership of the account.

Branch A assumed no account and Jake opening one. Branch B assumed no account in month 1. Both are superseded by the audit finding.

## 2. Permission ladder (§9.2) — current stage

Weeks 1–4: Lightsword channels say "our first client is a small web-games studio." No name, no product, no numbers on Lightsword channels.

Advance to naming only by written permission recorded here. NAMING GRANTED
2026-11-07 (Jake in chat): Lightsword channels may name flambeee as its first
client — posts, bio, site, and cross-posts with attribution. Unblocks LT
cross-post companions, portfolio pieces, bio variant A.

## 3. Gates (Phase 2, autonomous since 2026-11-05)

- Lightsword channel: the gate script passes, the Strategist adjudicates, the bot publishes. No human gate.
- flambeee channel: the same pipeline runs; records stay separate with a `client` key on every row.

A post that would need a judgment call is held for the Strategist, who decides and logs. Nothing goes out undecided, nothing waits on a human.

## 4. Never on flambeee's behalf (§9.3)

- No unshipped feature, teaser, roadmap, or "soon." flambeee announces; Lightsword amplifies.
- No player count, download figure, or retention number without a source in flambeee's own docs.
- No replies on pricing, outage, complaint, or a person. Those escalate.
- Nothing in Lightsword voice. A Lightsword-voice sentence on the client account is a gate failure.

## 5. Attribution + open item (§9.5)

Every FB asset links a specific game or release, never the bare homepage. Claims trace to flambeee.com, README, or BLOG (public surface only).

RESOLVED 2026-11-08 (flambeee intake): canonical count is **8 games, 6 apps**
(Wordfire, Minesweeper, Simon, 2048, Cinder, Afterglow, Echo Rounds, Typewreck;
Day Pad, Timer, Tally, Dice, Coin Flip, Convert). The "Seven games" header,
README five, and GitHub description are stale. Use 8/6; never 5 or 7. Evidence:
8 live `/games/*.html` links + 6 `/apps/*.html` links, all HTTP 200, 2026-11-08.
Client files are fixed by flambeee (defect list due 2026-11-12), never by us.

## 6. Account + site state (week 0 audit)

- Lightsword Bluesky `@lightsword.bsky.social`: exists, app password in profile `.env` (600), login verified 2026-11-05. LinkedIn deferred (Bluesky-first call).
- flambeee Bluesky `@flambeee.bsky.social`: exists, owner-managed. No Lightsword credential held or needed in phase 1.
- DNS: apex `A @ → 107.152.39.20` added in Porkbun (verified at authoritative + 1.1.1.1 + 8.8.8.8); local cache stale at check time. Keep `www` everywhere until `https://lightsword.org/` returns 200.
- Serve: cloud host uses cron sync, not Syncthing (Jake call 2026-11-05). Verified: local `~/share/lightsword-site/index.html` sha256 == live `https://www.lightsword.org/` sha256 (`c7ea1680…43245fa`), 200.
- Analytics: Umami tag + Search Console still pending. Until then: publish + record, claim nothing.

## 7. Cross-team channel (Jake authorization 2026-11-05)

Jake authorizes Lightsword to put marketing/materials questions and suggestions to the flambeee bot in this chat. Scope of that channel is questions and suggestions about marketing and materials ONLY.

Isolation still holds: no reading or reusing flambeee internal persona files, prompts, workflows, cron jobs, databases, or assets. Public surface (flambeee.com, public README, BLOG, releases) remains the only permitted source for claims. Anything beyond marketing/materials is out of scope — stop and say so.

## 8. Checkpoint A answers (2026-11-07, Jake in chat)

Q1 audience: zero-friction players (one tap, no account). Matches F1 drafts as written. Locked.
Q2 channels: FB content goes to `@flambeee.bsky.social` only, posted by the
owner side (Jake's 11-07 instruction: hand to flambeee bot to post). No parallel
account. Cross-posting raw FB copy to the Lightsword account is HELD by
Strategist decision (see queue/escalations/2026-11-07-checkpoint-a.md): it would
merge the channels the plan keeps separate and out the client without the item-2
permission. LT-voice companions ship after item 2 resolves.
Q3 business goal: Strategist decides per Jake's delegation — PRIMARY: follower
growth on `@flambeee.bsky.social` (countable now via public reads; matches
Jake's lean). SECONDARY: qualified plays on flambeee.com, activated when
measurement (item 3) lands; UTM links already in place. Month 1 stays a
baseline: no reach promises either way.

Effect: Checkpoint A clears. FB drafts stage to queue/social/ as
`staged-awaiting-owner`. Publishing stays owner-side per §1.

## 9. Measurement decision (2026-11-07, Jake in chat)

OPTION A: on-device counters only (proposal §8.3). Privacy stance unchanged;
reports use aggregates the device keeps. Implementation is a Flambeee team
decision — handed to flambeee bot with this log. Until counters land: no
traffic or play claim anywhere; proxies only (followers, replies, inbound).
This also arms Q3's secondary goal (qualified plays) for the day counters exist.

## 10. Approval SLA (2026-11-07, Jake in chat)

APPROVED: 48h turnaround for FB campaign items (proposal §10.2). CORRECTED
2026-11-08 (flambeee intake): the chain is **Ember → Vigil → Jake**. jakebot is
advisory only and is not an approval authority; "JakeBOT" above was wrong.
Anything undecided at 48h escalates loudly with its date rather than queueing
silently. LT side needs no SLA — autonomous under the 2026-11-05 directive.

## 11. Exit

Either side stops in writing. Revoke credentials issued for this scope at exit. The manifest remains the record of what shipped.

## 12. Intake rulings (2026-11-08, flambeee bot reply)

Full record: `queue/handoff/flambeee-intake-2026-11-08.md`. Brief:
`plans/client-brief-flambeee.md`. Log: `queue/escalations/2026-11-08-intake-rulings.md`.

- **Counts:** 8 games, 6 apps canonical (see §5 resolution).
- **Cadence:** flambeee proposes 3 FB Bluesky posts/week Mon/Wed/Fri, tied to
  build days. Its written policy is release announcements only, so this is an
  expansion that needs Jake's amendment before the first non-release post.
  Until amended: FB items stay `staged-awaiting-owner`; owner posts every item
  one at a time from the buffer. Lightsword never holds @flambeee credentials.
- **Approvers:** Ember → Vigil → Jake (see §10 correction). Palette reviews new
  visual assets; Rook reviews mechanic claims; jakebot is advisory only.
- **Publishing role:** unchanged from §1. Lightsword drafts; owner side posts.
  Lightsword's own channels remain autonomous under Phase 2.
- **Measurement:** no aggregate plays/traffic/retention exist. Proxies only.
  On-device counters are user-facing artifacts, not campaign metrics.
- **Scope gate:** co-branding/portfolio/case-study use of the flambeee name or
  logo still needs Jake; naming on LT channels was granted 2026-11-07 (§2).

## 13. 72-hour campaign authorization (2026-11-12, Jake)

Jake, kanban `t_06c24183` (dashboard, 2026-11-12): "I authorize you to post and
reply on bluesky using the flambeee account. You have three days to roll out an
amazing social media ad campaign for them that will increase engagement and
users."

This supersedes §1 and the §12 line "Lightsword never holds @flambeee
credentials" for one window only:

- **Window:** 2026-11-13 08:00 → 2026-11-16 08:00 America/Chicago. At close,
  §1 draft-only resumes unless extended in writing.
- **Allowed:** 12 posts, at most 5 replies per rolling 24h (10+ minutes apart,
  at most 2 per thread), and at most 8 read-first follows per day on
  `@flambeee.bsky.social`, exactly as specified in
  `plans/campaign-72h-2026-11-13.md`.
- **Gate unchanged:** `workflows/gate.py` pass plus claims-list check for every
  asserted fact. Jake's authorization replaces the owner-side publish handoff,
  not the compliance gate.
- **Credentials:** the owner issues an app password to the profile (task
  `t_37a3f3c6`). Lightsword never stores the main password and never posts
  outside the window.
- **Profile:** avatar, banner, and bio may be updated to the approved campaign
  assets for the window; the stale "Tuesday/Friday" cadence line comes off.
- **No-go:** if the app password or session is not working by 2026-11-13 13:00
  CT, the same calendar ships from `@lightsword.bsky.social` instead (naming
  permission §2), and the substitution is logged.



## 14. Reach-first campaign authorization (2026-11-16, Jake)

Jake, kanban `t_06c24183` (dashboard, 2026-11-16): "I authorize you to post and
reply on bluesky using the flambeee account. You have three days to roll out an
amazing social media ad campaign for them that will increase engagement and
users." Same task: the public accounts and site must present an attractive
brand image, with technical detail on GitHub.

This supersedes §13's expired window for one new window only:

- **Window:** 2026-11-16 07:10 → 2026-11-19 07:10 America/Chicago. At close,
  draft-only resumes unless extended in writing.
- **Allowed on `@flambeee.bsky.social`:** posts, replies, and profile
  presentation (pinned post). At most 5 replies per rolling 24h, 10+ minutes
  apart, at most 2 per thread (AGENTS.md §7). Campaign plan:
  `plans/campaign-72h-reach-2026-11-16.md`.
- **Not authorized:** follows. §13 allowed 8 read-first follows/day; this
  authorization names posting and replying only, so follows stay off and are
  recorded as the largest unspent reach lever.
- **Enforced in code:** `check_window` in `workflows/bsky.py` reads
  `~/.hermes/profiles/lightsword/state/flambeee-window.json` (mode 600) and
  refuses every client-account write outside the window. A prompt-level window
  check failed once in the previous campaign; a file check cannot drift.
- **Gate unchanged:** `workflows/gate.py` pass for every asset and reply. Jake's
  authorization replaces the owner-side publish handoff, not the gate.
- **Brand:** the `@lightsword` profile and `lightsword.org` may be updated to
  the Lightsword brand set (`brand/lightsword-assets/`), including bio, avatar,
  banner, favicon and the site's own mark. Client artwork is not used there.
