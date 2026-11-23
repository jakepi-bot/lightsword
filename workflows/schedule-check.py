#!/usr/bin/env python3
"""Check the Lightsword posting schedule against the live cron and calendar.

Read-only. Used by the nightly pre-flight and runnable by hand:

    python3 workflows/schedule-check.py
    python3 workflows/schedule-check.py --json

Exit codes:
    0 = the schedule is loadable and every required cron job is enabled
    1 = a required job is missing/disabled, or the config/calendar is unreadable
    2 = usage error

Warnings (missing future rows, missing briefs, a closed client window) do not
fail the check: the Sunday planning job owns future rows and the client window
is a written-consent dependency, not a scheduler fault.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
DEFAULT_PROFILE = Path.home() / ".hermes" / "profiles" / "lightsword"
TZ = ZoneInfo("America/Chicago")
DAY_KEYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
CAL_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|")


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("cadence") != "daily":
        raise ValueError(f"{path}: cadence is {data.get('cadence')!r}, expected 'daily'")
    if not data.get("channels"):
        raise ValueError(f"{path}: no channels")
    for key, ch in data["channels"].items():
        hh, mm = ch["publish_time"].split(":")
        if not (0 <= int(hh) <= 23 and 0 <= int(mm) <= 59):
            raise ValueError(f"{path}: channel {key} has invalid publish_time")
        if not set(ch.get("days", [])) <= set(DAY_KEYS):
            raise ValueError(f"{path}: channel {key} has an unknown day")
    return data


def load_jobs(profile: Path) -> dict:
    path = profile / "cron" / "jobs.json"
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    jobs = data.get("jobs", data) if isinstance(data, dict) else data
    return {j.get("id"): j for j in jobs}


def read_calendar(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not CAL_ROW.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        rows.append({
            "date": cells[0],
            "channel": cells[1],
            "pillar": cells[2],
            "asset_id": cells[3],
            "title": cells[4],
            "type": cells[5],
            "source": cells[6],
            "owner": cells[7],
        })
    return rows


def parse_hhmm(value: str) -> tuple[int, int]:
    hh, mm = value.split(":")
    return int(hh), int(mm)


def next_slot(now: datetime, channel: dict, config: dict) -> datetime:
    """The next configured clock slot, whether or not a row is planned."""
    hh, mm = parse_hhmm(channel["publish_time"])
    for offset in range(0, 8):
        day = (now + timedelta(days=offset)).date()
        if DAY_KEYS[day.weekday()] not in channel.get("days", DAY_KEYS):
            continue
        candidate = datetime(day.year, day.month, day.day, hh, mm, tzinfo=TZ)
        if candidate > now:
            return candidate
    raise ValueError("no slot in the next 8 days")


def next_planned(now: datetime, rows: list[dict], channel: dict) -> dict | None:
    ch_name = channel.get("calendar_channel")
    hh, mm = parse_hhmm(channel["publish_time"])
    today = now.date().isoformat()
    for row in sorted(rows, key=lambda r: r["date"]):
        if row["date"] < today or row["channel"] != ch_name:
            continue
        if row["type"] == "empty":
            continue
        slot_dt = datetime.fromisoformat(row["date"]).replace(hour=hh, minute=mm, tzinfo=TZ)
        if slot_dt <= now:
            continue
        return row
    return None


def window_state(path: Path, now: datetime) -> dict:
    if not path.exists():
        return {"state": "missing", "path": str(path), "detail": "no window file; client writes refused"}
    data = json.loads(path.read_text(encoding="utf-8"))
    start = datetime.fromisoformat(data["start"])
    end = datetime.fromisoformat(data["end"])
    if now < start:
        return {"state": "before", "start": data["start"], "end": data["end"], "authority": data.get("authority")}
    if now > end:
        return {"state": "closed", "start": data["start"], "end": data["end"], "authority": data.get("authority")}
    return {"state": "open", "start": data["start"], "end": data["end"], "authority": data.get("authority")}


def brief_status(repo: Path, date: str) -> str:
    hits = sorted(glob.glob(str(repo / "queue" / "briefs" / f"{date}-*.md")))
    return hits[0] if hits else "missing"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=str(REPO / "plans" / "posting-schedule.json"))
    ap.add_argument("--calendar", default=str(REPO / "plans" / "calendar-30d.md"))
    ap.add_argument("--profile", default=str(DEFAULT_PROFILE))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv[1:])

    now = datetime.now(TZ)
    warnings: list[str] = []
    errors: list[str] = []
    report: dict = {"checked_at": now.isoformat(), "config": args.config}

    try:
        config = load_config(Path(args.config))
        report["cadence"] = config["cadence"]
        report["timezone"] = config.get("timezone")
    except Exception as exc:  # noqa: BLE001 - a broken config must fail closed
        print(f"FAIL config: {exc}", file=sys.stderr)
        return 1

    try:
        jobs = load_jobs(Path(args.profile))
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL cron jobs: {exc}", file=sys.stderr)
        return 1

    report["jobs"] = {}
    for label, job_id in config.get("jobs", {}).items():
        job = jobs.get(job_id)
        if not job:
            errors.append(f"job {label} ({job_id}) missing")
            report["jobs"][label] = {"id": job_id, "state": "missing"}
            continue
        state = {
            "id": job_id,
            "name": job.get("name"),
            "enabled": bool(job.get("enabled")),
            "schedule": (job.get("schedule") or {}).get("expr"),
            "next_run_at": job.get("next_run_at"),
            "last_status": job.get("last_status"),
        }
        report["jobs"][label] = state
        if not state["enabled"]:
            errors.append(f"job {label} ({job_id}) is disabled")
        if not state["next_run_at"]:
            warnings.append(f"job {label} ({job_id}) has no next_run_at")

    try:
        rows = read_calendar(Path(args.calendar))
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL calendar: {exc}", file=sys.stderr)
        return 1

    report["channels"] = {}
    for key, channel in config["channels"].items():
        slot = next_slot(now, channel, config)
        planned = next_planned(now, rows, channel)
        info = {
            "handle": channel.get("handle"),
            "cadence": channel.get("cadence"),
            "publish_time": channel.get("publish_time"),
            "days": channel.get("days"),
            "next_slot": slot.isoformat(),
            "requires_window": bool(channel.get("requires_window")),
            "next_planned": None,
            "window": None,
            "engagement": None,
        }
        if planned:
            brief = brief_status(REPO, planned["date"])
            hh, mm = parse_hhmm(channel["publish_time"])
            publish_dt = datetime.fromisoformat(planned["date"]).replace(hour=hh, minute=mm, tzinfo=TZ)
            info["next_publish"] = publish_dt.isoformat()
            info["next_planned"] = {
                "date": planned["date"],
                "asset_id": planned["asset_id"],
                "title": planned["title"],
                "type": planned["type"],
                "brief": brief,
            }
            if brief == "missing":
                warnings.append(f"{key}: no brief for planned row {planned['date']} {planned['asset_id']}")
        else:
            warnings.append(f"{key}: no non-empty calendar row in the next week")
        if channel.get("requires_window"):
            win = window_state(Path(os.path.expanduser(channel["window_file"])), now)
            info["window"] = win
            if win["state"] != "open":
                warnings.append(f"{key}: client window {win['state']} — publishing blocked, staging only")

        # Engagement is its own clock (plans/engagement-program.md). A missing or
        # malformed engagement block disables that account's shift rather than
        # failing the schedule: content work must not halt because a side clock
        # is misconfigured. The reason is reported either way.
        eng = channel.get("engagement")
        if not isinstance(eng, dict) or "enabled" not in eng:
            info["engagement"] = {"runnable": False, "reason": "no engagement block on this channel"}
            warnings.append(f"{key}: no engagement block — the daily shift is off for this account")
        elif not eng.get("enabled"):
            info["engagement"] = {"runnable": False, "reason": "engagement disabled"}
        else:
            status = eng.get("status")
            # Replies are only ever sent from a pre-approved playbook. An account
            # with no playbook is engaged for posting and snapshotting only; it
            # never gets an improvised reply (plans/engagement-program.md §3).
            playbook = eng.get("playbook")
            playbook_ok = bool(playbook) and (REPO / playbook).exists()
            window_ok = True
            if eng.get("requires_window"):
                win_path = Path(os.path.expanduser(channel.get("window_file", "")))
                win = window_state(win_path, now)
                window_ok = win["state"] == "open"
                if not window_ok:
                    info.setdefault("window", win)
            runnable = status == "active" and window_ok and playbook_ok
            reason = None
            if status != "active":
                reason = eng.get("status_reason") or f"engagement status is {status!r}"
                warnings.append(f"{key}: engagement {status} — {reason}")
            elif not window_ok:
                reason = "a client write needs an open written window"
                warnings.append(f"{key}: engagement blocked — {reason}")
            elif not playbook_ok:
                reason = f"no reply playbook at {playbook or '(unset)'} — replies are not improvised"
                warnings.append(f"{key}: engagement blocked — {reason}")
            info["engagement"] = {
                "runnable": runnable,
                "status": status,
                "replies_per_day": eng.get("replies_per_day"),
                "posts_per_day": eng.get("posts_per_day"),
                "requires_window": bool(eng.get("requires_window")),
                "playbook": playbook,
                "reason": reason,
            }
        report["channels"][key] = info

    # The registry is read as permission to act: a client listed here with a
    # status that is not 'active' must never be engaged, and a client in the
    # registry with no matching channel is a configuration gap.
    registry_path = REPO / "plans" / "clients.json"
    registry = {}
    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8")).get("clients", {})
        except (ValueError, OSError) as exc:  # noqa: BLE001
            warnings.append(f"clients registry unreadable ({exc}) — no client account is engaged")
            registry = {}
    else:
        warnings.append("no plans/clients.json — no client account is engaged")
    for slug, client in registry.items():
        key = client.get("account_key")
        ch_info = report["channels"].get(key) or {}
        eng_info = ch_info.get("engagement") or {}
        if key not in config["channels"]:
            warnings.append(f"client {slug}: account_key {key!r} has no channel in the posting schedule")
        elif client.get("status") != "active" and not eng_info.get("reason"):
            # The channel block already reports a blocked or paused shift with its
            # reason; this only catches a registry that disagrees with the schedule.
            warnings.append(f"client {slug}: registry status {client.get('status')!r} — not engaged")
    report["clients"] = {
        slug: {
            "account_key": c.get("account_key"),
            "status": c.get("status"),
            "reason": c.get("status_reason"),
        }
        for slug, c in registry.items()
    }

    # Rows for the next seven days: the weekly job's contract.
    today = now.date()
    missing_dates = []
    upcoming = []
    for offset in range(0, 8):
        date = (today + timedelta(days=offset)).isoformat()
        day_rows = [r for r in rows if r["date"] == date]
        if not day_rows:
            missing_dates.append(date)
        for row in day_rows:
            if row["type"] == "empty":
                continue
            brief = brief_status(REPO, row["date"])
            upcoming.append({"date": row["date"], "channel": row["channel"],
                             "asset_id": row["asset_id"], "type": row["type"],
                             "brief": brief})
            if brief == "missing":
                warnings.append(f"no brief yet: {row['date']} {row['asset_id']} ({row['channel']})")
    report["upcoming_rows"] = upcoming
    report["missing_calendar_dates"] = missing_dates
    if missing_dates:
        warnings.append("calendar has no row for: " + ", ".join(missing_dates))

    report["warnings"] = warnings
    report["errors"] = errors
    report["ok"] = not errors

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"SCHEDULE CHECK {now.isoformat()}")
        print(f"config   : {args.config} (cadence={config['cadence']}, tz={config.get('timezone')})")
        for label, job in report["jobs"].items():
            flag = "ok" if job.get("enabled") else "FAIL"
            print(f"job      : {label:16} {job.get('id')} {flag:4} next={job.get('next_run_at')} last={job.get('last_status')}")
        for key, ch in report["channels"].items():
            print(f"channel  : {key:2} {ch['handle']} {ch['cadence']} {ch['publish_time']} {config.get('timezone')}")
            print(f"           next clock slot {ch['next_slot']}")
            if ch["next_planned"]:
                p = ch["next_planned"]
                print(f"           next publish {ch.get('next_publish')}  ({p['asset_id']})")
                print(f"           next row  {p['date']} {p['asset_id']} ({p['type']}) brief={p['brief']}")
            else:
                print("           next publish none — no non-empty row in the next week")
            if ch["window"]:
                print(f"           window    {ch['window']['state']} {ch['window'].get('start')} -> {ch['window'].get('end')}")
            eng = ch.get("engagement") or {}
            if eng:
                flag = "run" if eng.get("runnable") else "OFF"
                detail = f" ({eng['reason']})" if eng.get("reason") else ""
                print(f"           engage    {flag:3} {eng.get('replies_per_day')} replies + {eng.get('posts_per_day')} post/day{detail}")
        if report.get("clients"):
            for slug, client in report["clients"].items():
                print(f"client   : {slug:16} account={client['account_key']} status={client['status']}")
        if missing_dates:
            print("calendar : missing rows for " + ", ".join(missing_dates))
        for warning in warnings:
            print(f"WARN     : {warning}")
        for error in errors:
            print(f"ERROR    : {error}")
        print(f"result   : {'PASS' if report['ok'] else 'FAIL'} ({len(warnings)} warning(s), {len(errors)} error(s))")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
