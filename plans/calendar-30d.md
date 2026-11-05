# Lightsword 30-day calendar — week 1 rows (2026-11-09..2026-11-15)

Source of truth: `plans/social-media-plan.md` §8.1. Schema (§8):
`date | channel | pillar | asset-id | working title | type | source | owner`.
`type` is `source`, `derived`, or `empty`. Window 2026-11-09..2026-12-08.
Fri Nov 13 carries two plan entries (A02 plus the week-1 receipt), so seven
dates are covered by eight content/empty rows, not seven.

| date | channel | pillar | asset-id | working title | type | source | owner |
|---|---|---|---|---|---|---|---|
| 2026-11-09 | LT blog + LT Bluesky | L3 | lt-blog-20261109-01 | A00 The plan, in public | source | plans/social-media-plan.md | Content Lead |
| 2026-11-10 | LT Bluesky + LinkedIn | L1 | lt-bsky-20261110-01 | Derived from A00: one gate, one human, sixteen minutes | derived | lt-blog-20261109-01 (A00) | Content Lead |
| 2026-11-11 | LT blog + LT Bluesky | L3 | lt-blog-20261111-01 | A01 Four roles, one cron, one gate | source | personas/00-index.md; docs/marketing-company-research.md §7 | Content Lead |
| 2026-11-12 | LT Bluesky + LinkedIn | L2 | lt-bsky-20261112-01 | Derived from A01: the role that exists to disagree with the plan | derived | lt-blog-20261111-01 (A01) | Content Lead |
| 2026-11-13 | FB long copy + FB Bluesky | F1 | fb-blog-20261113-01 | A02 The arcade with no login | source | flambeee.com; flambeee README (public surface only) | Content Lead |
| 2026-11-13 | LT Bluesky | L1 | lt-bsky-20261113-01 | Week 1 receipt: what the gate killed | derived | logs/nightly.ndjson + published/manifest.ndjson (week 1 actuals) | Content Lead |
| 2026-11-14 | none | — | — | empty: weekend | empty | social plan §8.3 (no B2B Saturday post; run rests) | Strategist |
| 2026-11-15 | FB Bluesky | F1 | fb-bsky-20261115-01 | Derived from A02: the games load in seconds | derived | fb-blog-20261113-01 (A02) | Content Lead |

Notes: FB rows execute per `plans/scope-flambeee.md` §9.4 branch (week-0 item,
file not yet written — Jake to record). No game count appears on any FB row
(plan §9.5: hero vs stats block disagree, banned until flambeee rules).
