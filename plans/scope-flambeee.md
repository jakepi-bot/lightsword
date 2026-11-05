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

Advance to naming only by written permission recorded here. No permission granted yet.

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

Open: game count stays out of all copy (hero vs stats block disagree) until flambeee rules which is canonical.

## 6. Account + site state (week 0 audit)

- Lightsword Bluesky `@lightsword.bsky.social`: exists, app password in profile `.env` (600), login verified 2026-11-05. LinkedIn deferred (Bluesky-first call).
- flambeee Bluesky `@flambeee.bsky.social`: exists, owner-managed. No Lightsword credential held or needed in phase 1.
- DNS: apex `A @ → 107.152.39.20` added in Porkbun (verified at authoritative + 1.1.1.1 + 8.8.8.8); local cache stale at check time. Keep `www` everywhere until `https://lightsword.org/` returns 200.
- Serve: cloud host uses cron sync, not Syncthing (Jake call 2026-11-05). Verified: local `~/share/lightsword-site/index.html` sha256 == live `https://www.lightsword.org/` sha256 (`c7ea1680…43245fa`), 200.
- Analytics: Umami tag + Search Console still pending. Until then: publish + record, claim nothing.

## 7. Cross-team channel (Jake authorization 2026-11-05)

Jake authorizes Lightsword to put marketing/materials questions and suggestions to the flambeee bot in this chat. Scope of that channel is questions and suggestions about marketing and materials ONLY.

Isolation still holds: no reading or reusing flambeee internal persona files, prompts, workflows, cron jobs, databases, or assets. Public surface (flambeee.com, public README, BLOG, releases) remains the only permitted source for claims. Anything beyond marketing/materials is out of scope — stop and say so.

## 8. Exit

Either side stops in writing. Revoke credentials issued for this scope at exit. The manifest remains the record of what shipped.
