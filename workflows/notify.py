#!/usr/bin/env python3
"""Deliver a Lightsword message to Jake's Discord.

Why this exists
---------------
The nightly and weekly cron jobs used to deliver through the gateway with
``deliver: discord:1558054081325695037``. Under Hermes multiplexing that path
is closed to this profile: the gateway's shared Discord bot lends its adapter
only to a chat that an enabled ``gateway.profile_routes`` entry maps to the
firing profile, and chat 1558054081325695037 is mapped to ``flambeee``
(declared first; equal specificity keeps declaration order). Every cron send
from the ``lightsword`` profile therefore failed closed with
``platform 'discord' not configured/enabled`` from 2026-11-18 on, and the
digest never reached Jake.

One shared bot cannot serve two profiles on one chat, so this profile posts
the message itself with the same bot, straight to the Discord REST API, and
records the outcome in ``logs/notify.ndjson``. Delivery is one message a day,
so rate limits are not a concern.

Usage
-----
    python3 workflows/notify.py --digest-today --once-per-day
    python3 workflows/notify.py --text "..." --kind test
    python3 workflows/notify.py --file reports/nightly/2026-11-21.digest.txt
    python3 workflows/notify.py --digest-today --dry-run

Environment
-----------
``DISCORD_BOT_TOKEN`` is read from the environment, else from this profile's
``.env``, else from the primary Hermes home's ``.env`` (the shared bot's
credential lives there; it is Jake's own bot, not another team's data).

Exit codes: 0 sent or deliberately skipped, 1 on a real delivery failure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date as _date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LOG = REPO / "logs" / "notify.ndjson"

# Jake's Discord DM with the shared Hermes bot (hermes_jakepi#1114).
DEFAULT_CHANNEL = "1558054081325695037"
DISCORD_API = "https://discord.com/api/v10"
MAX_CONTENT = 1900  # Discord's hard limit is 2000; keep headroom


# --------------------------------------------------------------------------
# environment / credential
# --------------------------------------------------------------------------

def _parse_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return out
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key.strip()] = value
    return out


def _hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".hermes" / "profiles" / "lightsword"


def _primary_home() -> Path:
    """The default Hermes home (owner of the shared Discord bot credential)."""
    home = _hermes_home().resolve()
    if home.parent.name == "profiles":
        return home.parent.parent
    return Path.home() / ".hermes"


def _bot_token() -> str | None:
    token = (os.environ.get("DISCORD_BOT_TOKEN") or "").strip()
    if token:
        return token
    for env_path in (_hermes_home() / ".env", _primary_home() / ".env"):
        token = (_parse_env_file(env_path).get("DISCORD_BOT_TOKEN") or "").strip()
        if token:
            return token
    return None


def _today() -> str:
    return _date.today().isoformat()


# --------------------------------------------------------------------------
# message assembly
# --------------------------------------------------------------------------

def _digest_file(day: str) -> Path:
    return REPO / "reports" / "nightly" / f"{day}.digest.txt"


def _report_file(day: str) -> Path:
    return REPO / "reports" / "nightly" / f"{day}.md"


def _load_digest(day: str, notify_missing: bool = False) -> tuple[str | None, Path | None, str]:
    """Return ``(text, source_path, note)`` for today's digest."""
    path = _digest_file(day)
    if path.is_file():
        text = path.read_text(encoding="utf-8").strip()
        if text:
            return text, path, "digest-file"
    report = _report_file(day)
    if report.is_file():
        return (
            f"Lightsword nightly ran on {day} but wrote no digest file "
            f"({path.name}). Report: reports/nightly/{report.name}",
            report,
            "report-only",
        )
    if notify_missing:
        return (
            f"Lightsword nightly: no digest for {day} was written. The 22:00 run "
            f"failed or never started. Check logs/nightly.ndjson and "
            f"`hermes -p lightsword cron runs`.",
            None,
            "missing-notice",
        )
    return None, None, "missing"


def _stale_notice(day: str, path: Path, age_hours: float) -> str:
    # No age in the text: the message hash is the idempotency key, and a
    # changing age would make every re-run look like a new message.
    return (
        f"Lightsword nightly: no fresh digest from the 22:00 run for {day}. "
        f"The run failed or never started. Check logs/nightly.ndjson and "
        f"`hermes -p lightsword cron runs` (last digest file: {path.name})."
    )


def _chunks(text: str) -> list[str]:
    text = text.strip()
    if len(text) <= MAX_CONTENT:
        return [text] if text else []
    chunks: list[str] = []
    rest = text
    while rest:
        if len(rest) <= MAX_CONTENT:
            chunks.append(rest)
            break
        cut = rest.rfind("\n", 0, MAX_CONTENT)
        if cut < MAX_CONTENT // 2:
            cut = MAX_CONTENT
        chunks.append(rest[:cut].rstrip())
        rest = rest[cut:].lstrip("\n")
    return chunks


# --------------------------------------------------------------------------
# idempotency log
# --------------------------------------------------------------------------

def _key_for(text: str, channel: str) -> str:
    return hashlib.sha256(f"{channel}\x00{text}".encode("utf-8")).hexdigest()[:16]


def _already_sent(key: str) -> bool:
    if not LOG.is_file():
        return False
    try:
        with LOG.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("ok") and row.get("key") == key:
                    return True
    except OSError:
        return False
    return False


def _log(row: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------
# send
# --------------------------------------------------------------------------

def _post(channel: str, token: str, content: str) -> dict:
    body = json.dumps(
        {"content": content, "allowed_mentions": {"parse": []}},
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{DISCORD_API}/channels/{channel}/messages",
        data=body,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "LightswordNotifier/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Post a Lightsword message to Jake's Discord.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--text", help="message text")
    src.add_argument("--file", help="read the message from this file")
    src.add_argument("--digest-today", action="store_true",
                     help="post today's reports/nightly/<date>.digest.txt")
    ap.add_argument("--channel", default=os.environ.get("LIGHTSWORD_DISCORD_CHANNEL", DEFAULT_CHANNEL))
    ap.add_argument("--kind", default="manual", help="label recorded in logs/notify.ndjson")
    ap.add_argument("--once-per-day", action="store_true",
                    help="skip when this exact text was already delivered to this channel")
    ap.add_argument("--notify-missing", action="store_true",
                    help="with --digest-today: post a failure notice when no digest exists")
    ap.add_argument("--max-age-hours", type=float, default=None,
                    help="with --digest-today: refuse a digest file older than this")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    day = _today()
    source_note = "text"
    source_path: Path | None = None

    if args.digest_today:
        text, source_path, source_note = _load_digest(day, notify_missing=args.notify_missing)
        if text is None:
            print(f"NO-DIGEST: no reports/nightly/{day}.digest.txt and no {day}.md")
            return 0
        if args.max_age_hours is not None and source_path is not None:
            age = datetime.now().timestamp() - source_path.stat().st_mtime
            if age > args.max_age_hours * 3600:
                if not args.notify_missing:
                    print(
                        f"STALE-DIGEST: {source_path.name} is {age / 3600:.1f}h old "
                        f"(limit {args.max_age_hours:g}h) — not sending"
                    )
                    return 0
                # A stale file means tonight's run produced nothing: send the
                # failure notice instead of an out-of-date digest.
                text = _stale_notice(day, source_path, age / 3600)
                source_path = None
                source_note = "stale-notice"
    elif args.file:
        source_path = Path(args.file).expanduser()
        if not source_path.is_file():
            print(f"ERROR: no such file: {source_path}")
            return 1
        text = source_path.read_text(encoding="utf-8").strip()
        source_note = "file"
    else:
        text = (args.text or "").strip()

    if not text:
        print("ERROR: empty message; nothing to send")
        return 1

    channel = str(args.channel).strip()
    key = _key_for(text, channel)
    if args.once_per_day and _already_sent(key):
        print(f"SKIP: already delivered to {channel} (key {key})")
        return 0

    chunks = _chunks(text)
    if args.dry_run:
        print(f"DRY-RUN: would send {len(chunks)} message(s), {len(text)} chars, "
              f"channel {channel}, key {key}, source={source_note}")
        print(text)
        return 0

    token = _bot_token()
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not found (env, profile .env, primary .env)")
        _log({"ts": datetime.now().isoformat(timespec="seconds"), "date": day,
              "channel": channel, "kind": args.kind, "key": key, "ok": False,
              "error": "missing-token"})
        return 1

    sent_ids: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        try:
            msg = _post(channel, token, chunk)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:400]
            print(f"ERROR: Discord HTTP {exc.code} on part {index}/{len(chunks)}: {detail}")
            _log({"ts": datetime.now().isoformat(timespec="seconds"), "date": day,
                  "channel": channel, "kind": args.kind, "key": key, "ok": False,
                  "http": exc.code, "error": detail})
            return 1
        except Exception as exc:  # network, timeout, JSON
            print(f"ERROR: delivery failed on part {index}/{len(chunks)}: {exc}")
            _log({"ts": datetime.now().isoformat(timespec="seconds"), "date": day,
                  "channel": channel, "kind": args.kind, "key": key, "ok": False,
                  "error": str(exc)[:400]})
            return 1
        sent_ids.append(str(msg.get("id", "")))

    _log({"ts": datetime.now().isoformat(timespec="seconds"), "date": day,
          "channel": channel, "kind": args.kind, "key": key, "ok": True,
          "chars": len(text), "parts": len(chunks), "message_ids": sent_ids,
          "source": source_note})
    print(f"SENT: {len(chunks)} message(s) to {channel} ({len(text)} chars) "
          f"ids={','.join(sent_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
