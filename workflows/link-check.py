#!/usr/bin/env python3
"""Check the links in an armed post before its slot, at 18:45 America/Chicago.

The 19:00 Lightsword post may link to a blog page that the nightly wrote at
22:40 the night before. The site is published by a separate sync; if that sync
has not landed, the link would 404. `workflows/nightly-2200.md` says the post
then ships the brief's text-only fallback, and the link moves to the next slot.

This script is the scheduled check. It is read-only with respect to the
calendar and the gate; it may change exactly one thing in the outbox, and only
in the two ways the spec allows:

* the armed item carries `text_fallback` (the brief's prepared no-link copy,
  copied there by `bsky.py arm` from the gate-passed staged asset) and a URL in
  its text does not return 200 -> the item's `text` is replaced by the
  fallback, `use_fallback` is set, and the change is logged;
* there is no fallback -> the item is set to `held-link-dead`, which the
  5-minute tick does not publish (it only publishes `queued`/`retry`), and the
  problem is sent to Jake's DM.

It also warns when a non-empty Lightsword calendar row is due today and nothing
is armed for its slot: the nightly arms at 22:00 T-1, so by 18:45 the item must
exist.

Usage:
    python3 workflows/link-check.py
    python3 workflows/link-check.py --now 2026-11-22T18:45:00-06:00 --no-notify
    python3 workflows/link-check.py --outbox /tmp/outbox --dry-run

Exit codes: 0 = checked (pass, skip, swap, or hold are all reported, not job
failures), 1 = a real delivery failure or a crash. Quiet when there is nothing
due and nothing to warn about.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bsky  # noqa: E402  (workflows/ is not a package)
import notify  # noqa: E402

TZ = ZoneInfo("America/Chicago")
CAL_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|")
URL_RE = re.compile(r"https?://[^\s<>\"']+")
TRIM = ".,;:!?)]}'\"\u201d"
UA = "lightsword-link-check/1.0 (+https://lightsword.org)"
AUDIT = REPO / "logs" / "link-check.ndjson"


def trim_url(url: str) -> str:
    return url.rstrip(TRIM)


def extract_urls(text: str) -> list[str]:
    seen, out = set(), []
    for raw in URL_RE.findall(text or ""):
        url = trim_url(raw)
        if url and url not in seen:
            seen.add(url)
            out.append(url)
    return out


def check_url(url: str, timeout: float = 15.0) -> dict:
    """GET the URL, following redirects. Any 2xx is live."""
    started = time.monotonic()
    result: dict = {"url": url, "ok": False, "status": None, "final_url": None}
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result["status"] = resp.status
            result["final_url"] = resp.geturl()
            result["ok"] = 200 <= resp.status < 300
    except urllib.error.HTTPError as exc:
        result["status"] = exc.code
    except Exception as exc:  # noqa: BLE001 - DNS, TLS, timeout, refused
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["ms"] = int((time.monotonic() - started) * 1000)
    return result


def load_calendar_rows(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not CAL_ROW.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        rows.append({"date": cells[0], "channel": cells[1], "asset_id": cells[3], "type": cells[5]})
    return rows


def load_items(outbox: Path) -> list[tuple[Path, dict]]:
    items = []
    for path in sorted(outbox.glob("*.json")):
        try:
            items.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError):
            continue
    return items


def save_item(path: Path, item: dict) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(item, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def audit(entry: dict) -> None:
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def send(message: str, dry_run: bool) -> int:
    if dry_run:
        print(f"DRY-RUN notify: {message}")
        return 0
    try:
        return notify.main(["--text", message, "--kind", "link-check"])
    except SystemExit as exc:
        return int(exc.code or 0)
    except Exception as exc:  # noqa: BLE001 - never let delivery crash the check
        print(f"WARNING notify.py crashed: {exc}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--now", help="ISO-8601 instant to evaluate (default: now)")
    ap.add_argument("--config", default=str(REPO / "plans" / "posting-schedule.json"))
    ap.add_argument("--calendar", default=str(REPO / "plans" / "calendar-30d.md"))
    ap.add_argument("--outbox", default=str(REPO / "queue" / "outbox"))
    ap.add_argument("--lead-minutes", type=int, default=240,
                    help="check items whose slot is at most this far away (default 240)")
    ap.add_argument("--dry-run", action="store_true", help="report, change nothing, send nothing")
    ap.add_argument("--no-notify", action="store_true", help="never send to Discord")
    args = ap.parse_args(argv)

    now = bsky.parse_iso(args.now, "--now") if args.now else datetime.now(TZ)
    if now.tzinfo is None:
        now = now.replace(tzinfo=TZ)
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    lt = config["channels"]["lt"]
    hh, mm = (int(x) for x in lt["publish_time"].split(":"))
    outbox = Path(args.outbox)

    horizon = now + timedelta(minutes=args.lead_minutes)
    floor = now - timedelta(minutes=5)
    candidates = []
    for path, item in load_items(outbox):
        if item.get("status") not in ("queued", "retry"):
            continue
        try:
            when = bsky.parse_iso(item["publish_at"], f"{path.name} publish_at")
        except Exception:  # noqa: BLE001 - a malformed item is the tick's problem
            continue
        if floor <= when <= horizon:
            candidates.append((path, item, when))

    problems: list[str] = []
    checked_items = 0
    checked_urls = 0
    changes = 0

    for path, item, when in candidates:
        urls = extract_urls(item.get("text", ""))
        if not urls:
            continue
        checked_items += 1
        results = [check_url(url) for url in urls]
        checked_urls += len(results)
        bad = [r for r in results if not r["ok"]]
        note = {
            "ts": datetime.now(TZ).isoformat(),
            "item": item.get("id"),
            "publish_at": item.get("publish_at"),
            "action": "checked",
            "urls": results,
        }
        if not bad:
            audit(note)
            continue
        detail = ", ".join(f"{r['url']} -> {r.get('status') or r.get('error')}" for r in bad)
        fallback = (item.get("text_fallback") or "").strip()
        if fallback:
            try:
                bsky.validate_text(fallback, f"{item.get('id')} text_fallback")
            except bsky.Refused as exc:
                fallback = ""
                detail += f"; text_fallback also invalid ({exc})"
        if fallback:
            item["text"] = fallback
            item["use_fallback"] = True
            item["link_check"] = {"ts": note["ts"], "ok": False, "urls": results,
                                  "action": "swapped-fallback"}
            if not args.dry_run:
                save_item(path, item)
                changes += 1
            note.update({"action": "swapped-fallback", "detail": detail})
            audit(note)
            problems.append(
                f"SWAPPED {item.get('id')} to its text-only fallback: {detail}. "
                f"It still publishes at {item.get('publish_at')}.")
        else:
            item["status"] = "held-link-dead"
            item["last_error"] = f"link check failed at {note['ts']}: {detail}"
            item["link_check"] = {"ts": note["ts"], "ok": False, "urls": results,
                                  "action": "held"}
            if not args.dry_run:
                save_item(path, item)
                changes += 1
            note.update({"action": "held", "detail": detail})
            audit(note)
            problems.append(
                f"HELD {item.get('id')} (slot {item.get('publish_at')}): {detail}. "
                "No text-only fallback was staged, so it will not publish; "
                "the site sync or a re-brief is needed.")

    # A non-empty row due today with nothing armed at 18:45 is a broken chain,
    # not a quiet day. 11-21/11-22 carry deliberate `empty` rows and stay silent.
    today = now.date().isoformat()
    try:
        rows = [r for r in load_calendar_rows(Path(args.calendar))
                if r["date"] == today and r["channel"] == lt.get("calendar_channel")
                and r["type"] != "empty"]
    except OSError:
        rows = []
    if rows and not candidates:
        problems.append(
            f"NOT ARMED: {len(rows)} Lightsword row(s) due {today} but no queued "
            f"outbox item for the {lt['publish_time']} slot.")

    for problem in problems:
        print(f"WARNING {problem}")

    stamp = now.isoformat()
    summary = {"ts": stamp, "run": "link-check", "items": checked_items,
               "urls": checked_urls, "changes": changes, "problems": len(problems)}
    if problems:
        header = f"Lightsword link check {stamp}: {len(problems)} problem(s)."
        code = 0 if args.no_notify else send(header + "\n\n" + "\n".join(problems), args.dry_run)
        print(f"LINK-CHECK ISSUE {stamp} items={checked_items} urls={checked_urls} "
              f"changes={changes}")
    elif not rows and not checked_items:
        print(f"LINK-CHECK SKIP {stamp} — no non-empty Lightsword row today.")
        code = 0
    else:
        print(f"LINK-CHECK PASS {stamp} items={checked_items} urls={checked_urls} "
              f"changes={changes}")
        code = 0
    if not args.dry_run:
        audit(summary)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
