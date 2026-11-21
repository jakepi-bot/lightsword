#!/usr/bin/env python3
"""Cron entry point for the Bluesky outbox (Hermes `no_agent` job).

Prints nothing when nothing is due, so the 5-minute tick stays quiet.

Anything the tick prints — a `PUBLISHED` line with the Bluesky URI, or a
`WARNING` for an expired slot, a missing credential, a refused item — is
captured and posted to Jake's Discord through `workflows/notify.py
--kind outbox-tick`, which chunks long output and records the message id in
`logs/notify.ndjson`. The cron job itself is `deliver: local`: the gateway's
shared Discord bot route for Jake's DM belongs to the flambeee profile, so a
`discord:` target here fails closed (`docs/discord-delivery.md`). The captured
text is echoed to stdout afterwards, so the job's own output file keeps the
audit trail even when the Discord send fails.

The publish path is untouched: `bsky.main(["tick"])` does the same work in the
same order; only where its lines go is different.

Exit codes: 0 for a clean tick and for blocked/expired items (the message is
the signal; a nonzero exit would surface as a job failure instead of a notice).
A genuine crash still exits nonzero, which is what we want to hear about; the
lines it printed before the crash are still delivered. A failed Discord send
exits 1 once the tick's own work is done, so the failed run stays visible in
`hermes cron runs` and the log, and it is not mistaken for a quiet tick.
"""

import io
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bsky  # noqa: E402  (path set above; workflows/ is not a package)
import notify  # noqa: E402

TICK_EXIT_OK = (0, 3)
NOTIFY_KIND = "outbox-tick"


def run_tick() -> tuple[int, str]:
    """Run one tick with stdout+stderr captured; return (exit code, output)."""
    buf = io.StringIO()
    real_out, real_err = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = buf
    try:
        code = bsky.main(["tick"])
    except SystemExit as exc:  # argparse errors etc.
        code = int(exc.code or 0)
    except Exception:  # a crash: keep what was printed, still fail the run
        code = 1
        traceback.print_exc(file=buf)      # delivered with the output
        traceback.print_exc(file=real_err)  # and recorded for the scheduler
    finally:
        sys.stdout, sys.stderr = real_out, real_err
    return (0 if code in TICK_EXIT_OK else code), buf.getvalue().strip()


def deliver(output: str) -> int:
    """Post the tick's output to Jake's DM; return notify.py's exit code."""
    try:
        return notify.main(["--text", output, "--kind", NOTIFY_KIND])
    except SystemExit as exc:
        return int(exc.code or 0)
    except Exception as exc:  # notify.py must never take the tick down
        print(f"WARNING notify.py crashed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    code, output = run_tick()
    if not output:
        sys.exit(code)
    print(output, flush=True)  # the job's output file keeps the trail
    if deliver(output) != 0:
        print(
            "WARNING outbox-tick output did not reach Discord; "
            "see logs/notify.ndjson",
            file=sys.stderr,
        )
        sys.exit(code or 1)
    sys.exit(code)
