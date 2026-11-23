# Daily engagement shift — spec

**Status:** active, 2026-11-23.
**Program:** `plans/engagement-program.md` (the why and the rules).
**Registry:** `plans/clients.json`. **Schedule:** `plans/posting-schedule.json`.
**Cron job:** `913c13d1ec71`, daily 19:10 America/Chicago.
**Roles:** Distribution Lead runs it; Analyst owns the snapshot; Strategist
decides anything position class.

This spec is short because the rules already live in the program document and
the per-client playbook. It exists so the job prompt can say "follow
`workflows/engagement-shift.md`" instead of restating them, and so a run that
behaves differently from this file is a bug rather than a judgement call.

---

## 0. Before anything

```bash
git pull --ff-only origin main          # merged plans arrive this way
date                                     # every date comes from here
python3 workflows/schedule-check.py      # engagement state per account, registry state
```

Never commit, never push. Working directory is this clone.

## 1. Who is engaged today

Read `plans/schedule-check.py`'s engagement lines, which are derived from
`plans/posting-schedule.json` + `plans/clients.json` + the window file:

- `engage run` → the account is engaged this shift.
- `engage OFF` → the account is not engaged. **Report the reason, do not send.**
  A blocked client is a finding, not a problem to solve: the reason is consent,
  and this run cannot grant it.

An account with no entry at all is not engaged. Absence is not permission.

## 2. The snapshot (always, for every account)

```bash
python3 workflows/reach-metrics.py --account lt
python3 workflows/reach-metrics.py --client flambeee
```

Appends one NDJSON line per account to `metrics/<account>/reach.ndjson`, covering
the period since the previous snapshot. Run it even when the account is blocked:
followers are worth a continuous record and reading is not writing.

If it errors, record `unavailable` and the reason. Do not estimate a number.

## 3. The reply shift (only for `engage run` accounts)

For each engaged account, in registry order, until that account's daily target
(`engagement.replies_per_day`, default 3) or the code cap stops the run:

1. `python3 workflows/bsky.py --account <key> limits` — if `replies_24h` is at
   or above the account's target, this account is done; say so.
2. Discover targets with at least four searches:
   `python3 workflows/bsky.py --account <key> search -q "<query>" --limit 10 --sort top --since <30h ago, ISO>`
   Query shapes: what the client's products actually answer.
3. Apply the six eligibility tests in `plans/engagement-program.md` §5. Fewer
   than the target qualifies → send fewer and say which test failed. Never
   invent a target and never reply to a random post.
4. Write `queue/replies/<account>-<YYYYMMDD>-<NN>.md` with the playbook's
   frontmatter and `Sources:` section, using a pre-approved snippet whose first
   clause names what the person actually asked about.
5. Send with `python3 workflows/reply-send.py <file>.md`. That script re-runs
   the gate and refuses on failure — never copy the text into `bsky.py` by hand.
6. Space sends ≥10 minutes apart. If a call refuses, stop that account.

Anything in the position class is **not sent**: write
`queue/escalations/YYYY-MM-DD-<slug>.md` with the stranger's text verbatim and
let the Strategist decide. Security, legal, self-harm, doxxing and press
deadlines also say URGENT in the final line.

## 4. Logging

- One `queue/replies/*.md` per reply, with the exact text and its sources.
- One line per action in `logs/replies.ndjson` (`result: posted | held`).
- One line in the shift log: `reports/engagement/YYYY-MM-DD.md` — accounts
  engaged, replies sent with URIs, escalations written, and every blocked
  account with its reason.
- The final response is at most five lines, and the same lines are written to
  `reports/engagement/YYYY-MM-DD.txt` and delivered with
  `python3 workflows/notify.py --file reports/engagement/YYYY-MM-DD.txt --kind engagement-shift`.
  This profile's gateway delivery is `local`; `notify.py` is how Jake actually
  receives it (see `docs/discord-delivery.md`). If it prints ERROR, add the
  reason to the shift log and say so in the final response; one retry, never more.

## 5. Done means

- Every account in the schedule has a snapshot line for today.
- Zero replies sent to a blocked account.
- Zero replies over a cap, or without a snippet and a sources block, or in the
  position class.
- Every blocked account named in the shift log with its reason.
- Nothing invented. If the shift did nothing, the log says why.
