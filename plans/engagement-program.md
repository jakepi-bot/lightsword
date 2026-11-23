# Standing engagement program

**Status:** active, written 2026-11-23.
**Authority:** Jake directive 2026-11-23 — "the actions we did during our 3-day
campaign of driving engagement for our client worked great, we should do this
activity everyday for every client, not just when we call for a new campaign."
**Supersedes:** the campaign-only framing in `plans/campaign-72h-reach-2026-11-16.md`
§5 and §7. The levers, caps and target rules from that campaign carry over
unchanged; what changes is that they no longer need a campaign to run.
**Machine-readable per-client state:** `plans/clients.json`.
**Still binding:** `plans/reply-playbook-flambeee.md` (the snippets and the class
rules), `plans/scope-flambeee.md` (client permission), `AGENTS.md` rules 7–10.

---

## 1. What becomes daily

The 72-hour reach campaign ran three levers for three days. All three are now a
standing daily activity, on every client account, every day of the week:

| Lever | Daily amount | Why it is the one that matters |
|---|---|---|
| **Replies to strangers** | 3 per account, max 5 per rolling 24h, ≥10 min apart, ≤2 per thread | A broadcast post reaches the followers an account already has. A reply reaches a reader who was already asking. This is the only lever that adds new people. |
| **Original post** | 1 per account, at that account's slot | Keeps the profile current for the visit a reply earns. One, not four. |
| **Snapshot** | 1 per account per day | Without it nobody can tell whether the activity is working. |

The pinned "start here" post is maintenance, not daily work: check it weekly and
refresh it when the facts on it change.

**Follows are still not authorized** by any client scope. They stay on the
unspent-levers list. A standing program is not a permission.

## 2. The structural change: engagement no longer waits for a campaign

Before this, engagement work lived inside campaign plans, and the nightly run
skipped phases 3–7 whenever tomorrow's calendar row was `type: empty` — a
deliberate blank day. The calendar is about **original content**, and blank days
are healthy: an account does not need a post every day. But a blank calendar day
was silently turning into a zero-engagement day too, which is why engagement
only happened in bursts around campaigns.

From now on the two are separate clocks:

| Clock | Driven by | Runs on |
|---|---|---|
| **Campaign content** | `plans/calendar-30d.md` rows + `queue/briefs/` | Any day with a non-empty row |
| **Engagement** | `plans/clients.json` + `plans/posting-schedule.json` | **Every day, regardless of the calendar** |

An `empty` calendar row skips content generation. It never skips the engagement
shift. A missing calendar file does not skip it either — the halt rule for
content (phases 3–7) does not reach the engagement phase (phase 3b).

## 3. Why repeating the same lever daily is safe

Three things make the daily version safe where an ad-hoc daily version would not
be:

1. **The copy is pre-approved, not written fresh.** `plans/reply-playbook-flambeee.md`
   §6 carries ten approved snippets. A daily shift selects a snippet whose first
   clause names what the stranger actually asked about. It does not compose new
   sentences about the product, because composing new sentences is how a sourced
   claim turns into an invented one.
2. **Every reply still passes the gate.** `workflows/gate.py` runs on the reply
   file; `workflows/reply-send.py` re-runs it and refuses on any failure. The
   gate does not become optional because the reply is routine.
3. **The caps are in code.** `guard_reply` in `workflows/bsky.py` enforces
   5-per-24h, 10-minute spacing and 2-per-thread. A busy day cannot spend a
   week's budget in an hour, and a retry cannot resend.

What the daily version does **not** do: invent new claims, answer anything in
the position class, or infer a product feature from a game page. Those rules do
not relax with frequency. If anything they tighten, because volume is what turns
one wrong reply into a pattern.

## 4. The daily shift

Times are America/Chicago. A shift that has no eligible target is a zero-reply
day: it is logged as `0 of 3, no eligible target`, and it never becomes a reply
to a random post.

| Time | Role | Work | Artifact |
|---|---|---|---|
| 09:10 | Distribution | Reply shift A — discover targets, send up to 2 | `queue/replies/`, `logs/replies.ndjson` |
| 15:10 | Distribution | The day's original post (internal accounts; a client account only inside a written window) | `queue/outbox/`, `published/manifest.ndjson` |
| 19:10 | Distribution + Analyst | Reply shift B — up to 1 more, then the day's snapshot | `queue/replies/`, per-client metrics NDJSON |

Inside the 14:00–20:00 CT reply window, a reply to an inbound question goes out
within 2 hours. Outside it, the reply waits for the next window: a 2 a.m. reply
reads as a bot working through a list.

**A client account's shift additionally requires an open written window.** See
§6. Discovery and drafting may happen for a client without a window; the send
refuses. That is the point of `check_window`.

## 5. Target selection (unchanged from the campaign, restated as the standard)

A target is eligible only if all six hold:

1. Posted in the last 30 hours.
2. A real person or small account — not a brand ad, not a repost bot, not an
   account that only broadcasts.
3. The post asks for something: a recommendation, a game to play, an
   alternative to ads/installs/accounts, or a "what are you playing" thread.
4. One of the client's shipped things genuinely answers it.
5. The reply can name that specific thing in its first clause.
6. The reply traces to a claims row or a pre-approved snippet — no new claim.

**Never reply to:** a complaint, a price question, a bug report, a named person,
or a thread already carrying two of our replies. Those are position class and go
to the Strategist, who decides and logs. The class rules are
`plans/reply-playbook-flambeee.md` §7.

## 6. Per-client requirements

`plans/clients.json` is the registry. A client is engaged **only** when all of
these are true; otherwise the shift is recorded as blocked with the exact
reason, and nothing is sent.

| Requirement | Where it lives | If it is missing |
|---|---|---|
| A scope file granting the activity | `plans/<client> scope>.md` | Blocked. Engagement is not a default. |
| A claims file for every fact the snippets assert | `brand/claims-<client>.md` | Blocked. No sourced claim, no reply. |
| The client's own voice | `brand/voice-<client>.md` | Blocked. A Lightsword-voice sentence on a client account is a gate failure. |
| A reply playbook with pre-approved snippets | `plans/reply-playbook-<client>.md` | Blocked. Discovery without approved copy produces invented copy. |
| An open written window, where the scope requires one | `state/<client>-window.json` | Blocked. `check_window` refuses the write. |
| An app password in the profile `.env` | `.env` | Blocked. Reported, never guessed. |

### flambeee — blocked today

flambeee is the only client and it is **blocked on consent, not on tooling**.
`plans/scope-flambeee.md` §14 authorized bot posting and replying for a single
window, 2026-11-16 07:10 → 2026-11-19 07:10 CT, and it closed. `state/flambeee-window.json`
carries that closed range, and `check_window` in `workflows/bsky.py` refuses
every client write outside a written window — by design, because a client's
consent is not a gate this company can waive on its own.

Consequence: from today the program runs discovery and drafting for flambeee
every day and sends nothing, and the nightly digest says so in one line. **It
starts sending the day Jake records a standing window in writing** — a
`{"start", "end", "authority"}` file at `state/flambeee-window.json` plus the
matching entry in `plans/scope-flambeee.md`. No code change is needed on that
day.

## 7. Fail-closed rules

- **No eligible target is a zero-reply day**, logged as such. Never a random
  target, never a recycled one, never a reply to our own thread.
- **A gate failure is dropped.** The sender never rewords it. Only the
  Strategist adjudicates, and a daily shift generates no new brief, so a drop is
  a drop.
- **A closed or missing window is a blocked client shift**, logged with the
  reason. Not a run failure, not a silent skip.
- **Caps bind before targets do.** If the rolling 24h count is already 5, the
  shift is over; the remaining work rolls to tomorrow, loudly.
- **Idempotency.** One reply per target per account, ever. `bsky.py` keys on
  asset-id + platform + date; a re-run must not double-send. `published-duplicate`
  is a warning in the digest, never a silent terminal state — the 2026-11-17
  suppressed post in the reach campaign is the reason that rule exists.
- **Unknown beats invented.** A missing number, date or feature is left out and
  escalated. A blank line is cheaper than a retraction.

## 8. What gets measured

Per account, per day, appended to one NDJSON line:

`workflows/reach-metrics.py --client <slug>` → `metrics/<client>/reach.ndjson`

| Countable | Not countable |
|---|---|
| Followers, follows, posts | Impressions |
| Likes, reposts, replies, quotes, mentions (notification list) | Profile visits (not in the AT Protocol) |
| Replies we sent, on which targets | Site clicks (no analytics tag on either site) |
| | Signups, play counts |

The uncountable list is recorded as `unavailable` with a reason. It is never
zero and never estimated.

### Baseline, recorded honestly

Measured at the close of the reach campaign, 2026-11-19 13:30Z
(`reports/campaign/2026-11-19-reach-final.md`):

| | Before campaign | After 72h |
|---|---|---|
| Followers | 4 | 6 |
| Inbound actions from other accounts | 0 | 1 (a single follow) |
| Likes / reposts / replies / quotes on campaign assets | 0 | 0 |

The campaign's own four KPIs came back 0 of 4 met. That is the number this
program starts from, and the operator's judgement that the activity is worth
making daily is the reason it continues anyway — engagement is a compounding
input, and three days is not enough runway to judge it. Both facts belong in the
record: the directive, and what the instrument actually said.

**Review:** after 30 days of daily shifts (or 14 if the client window opens
later than that), the Analyst writes
`reports/weekly/<date>-engagement-review.md` comparing followers, inbound
actions per reply sent, and replies per eligible target found. The decision it
forces is: keep, change the levers, or stop. A program that cannot show a
direction after 30 days does not get to keep spending the account's credibility.

## 9. Adding a client

Adding a client to the program is four files and one registry entry, in this
order — and the registry entry comes last, because the run reads the registry as
permission to act:

1. `plans/scope-<client>.md` — written authority naming the account and the
   activity. No scope, no engagement.
2. `brand/claims-<client>.md` — every fact the snippets are allowed to assert,
   each with a public source. No claims, no snippets.
3. `brand/voice-<client>.md` — the client's voice, derived from its own public
   writing.
4. `plans/reply-playbook-<client>.md` — the class rules and the pre-approved
   snippets, copied from the flambeee playbook's structure, filled with the new
   client's claims.
5. `plans/clients.json` — the registry entry, with `"status"` set to what is
   actually true. A client whose window is not open goes in as `blocked` with
   the reason, so the digest reports it instead of the run discovering it.

The nightly picks up the new client from the registry on its next run. Nothing
else needs editing.

---

*Written 2026-11-23 for Jake's directive of the same date. If this file and a
client's scope file disagree about whether the bot may act, the scope file wins.
If this file and `brand/claims-<client>.md` disagree about a fact, the claims
file wins.*
