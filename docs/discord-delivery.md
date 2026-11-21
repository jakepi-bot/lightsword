# Discord delivery for the `lightsword` profile

**Status:** fixed 2026-11-21. The nightly digest and the Bluesky outbox tick's
event lines reach Jake's Discord DM again.
**Symptom it fixes:** every cron run from this profile ended with
`last_status: delivery_failed`, `last_delivery_error: platform 'discord' not
configured/enabled`, and the message never arrived. The run itself was healthy;
the delivery was not.

## What was wrong

The gateway is one multiplexed process (`hermes-gateway.service`, primary home
`~/.hermes`) that runs the cron stores of every profile. It owns one Discord
bot (`hermes_jakepi#1114`). A profile without its own bot token — this one —
may borrow that adapter **only** for a chat that an enabled
`gateway.profile_routes` entry maps to that profile
(`website/docs/user-guide/multi-profile-gateways.md`: "a chat, topic or thread
whose most specific route names another profile is never sent through the
shared bot").

The primary config had two routes on the same chat — Jake's DM,
`1558054081325695037`:

```yaml
gateway:
  profile_routes:
    - name: flambeee-ops-cron       # declared first
      platform: discord
      guild_id: flambeee-cron-delivery-only
      chat_id: '1558054081325695037'
      profile: flambeee
    - name: lightsword-cron-delivery
      platform: discord
      guild_id: lightsword-cron-delivery-only
      chat_id: '1558054081325695037'
      profile: lightsword
```

Neither route can match an inbound DM (their `guild_id` is a synthetic string),
so they exist only to authorize cron sends. But the cron resolver compares a
send against *dispatch*: both routes match the target, both carry the same
specificity (`guild_id` 2 + `chat_id` 4), and equal scores keep declaration
order. `flambeee` therefore wins the chat, and the `lightsword` lookup returns
nothing — fail closed, `platform 'discord' not configured/enabled`.

Verified 2026-11-21 with the live config:

```
this profile's routes:  ['lightsword-cron-delivery']
dispatch routes:        ['flambeee-ops-cron', 'lightsword-cron-delivery']
get(discord, 1558054081325695037) -> None      # lightsword: shadowed
get(discord, 1558054081325695037) -> adapter   # flambeee: authorized
```

One chat belongs to one profile. Two profiles cannot both deliver to Jake's DM
through the shared bot; Hermes' own answer for that is a second bot token, which
only Jake can create. Do not "fix" this by deleting or reordering the
`flambeee` route: that would break another team's delivery.

## What the fix is

`workflows/notify.py` posts the message with the same bot straight to the
Discord REST API (`POST /channels/<id>/messages`), so the destination stays
exactly what it always was: Jake's DM. The cron job's own delivery is set to
`local` (`deliver: local`, `failure_deliver: local`) so a healthy run is not
reported as a delivery failure.

Path of a nightly digest:

1. Phase 8 writes `reports/nightly/<today>.md` and the five digest lines to
   `reports/nightly/<today>.digest.txt`.
2. Phase 8b runs `python3 workflows/notify.py --digest-today --kind nightly`.
   One Discord message, outcome appended to `logs/notify.ndjson`.
3. The `Lightsword digest delivery (22:10 fallback)` job
   (`d0081085f205`, script-only, `scripts/digest-deliver.py`) re-sends the
   digest only if step 2 did not happen or failed (idempotent on the message
   hash), and posts a failure notice when the nightly wrote nothing at all.

The weekly planning job uses the same script with
`--file reports/weekly/<today>.digest.txt --kind weekly`.

The Bluesky outbox tick (`84e5289134f4`, every 5 minutes) uses the same route
for its event lines. `workflows/bsky-tick.py` runs `bsky.main(["tick"])` with
stdout and stderr captured, echoes the captured text to its own output file,
and — only when it is non-empty — posts it with
`notify.py --text <output> --kind outbox-tick`. A normal tick prints nothing
and sends nothing. The publishing path (`workflows/bsky.py tick`) is unchanged;
only the destination of its `PUBLISHED` / `WARNING` lines moved from the
gateway to `notify.py`.

## Credential

`notify.py` reads `DISCORD_BOT_TOKEN` from the environment, else this profile's
`.env`, else the primary home's `.env` (`~/.hermes/.env`). One copy of the
token, one owner; nothing is copied into this repo or this profile.

## Verifying it

```bash
cd ~/.hermes/lightsword/lightsword
python3 workflows/notify.py --text "test" --dry-run           # no send
python3 workflows/notify.py --text "test" --kind delivery-test
tail -1 logs/notify.ndjson                                    # ok: true, message id
hermes -p lightsword cron runs b83aa855e26a                   # delivery_outcome: success
```

To exercise the tick path without publishing anything, drop a temporary outbox
item in the past (it is marked `expired`, never posted), fire the job once, and
remove the item:

```bash
printf '%s\n' '{"id":"zz-tick-test","account":"lt","publish_at":"2026-01-01T09:00:00-06:00","text":"TEST — never published.","images":[],"alts":[],"idempotency_key":"zz-tick-test","status":"queued","attempts":0}' \
  > queue/outbox/zz-tick-test.json
hermes -p lightsword cron run 84e5289134f4
tail -1 logs/notify.ndjson        # kind: outbox-tick, ok: true, message_ids
rm queue/outbox/zz-tick-test.json
```

Do not point a `discord:...` target back at this profile's cron jobs without
first giving it its own bot: the route gate will reject it again.

## Related

- `workflows/nightly-2200.md` — phase 8/8b, the logging contract.
- `workflows/weekly-plan-sunday.md` — the weekly variant.
- `workflows/bsky-tick.py` — the outbox tick wrapper (`--kind outbox-tick`).
- `logs/notify.ndjson` — every send, success or failure, with the Discord
  message id.
