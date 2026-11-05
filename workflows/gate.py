#!/usr/bin/env python3
"""Mechanical compliance/claims gate for Lightsword drafts and replies.

Part one of the two-part gate (workflows/nightly-2200.md): this script decides
pass or fail, deterministically and the same way every night. Part two is the
Strategist adjudicating failures. The Content Lead runs this script and may not
edit its output or waive a result.

Usage:
    python3 workflows/gate.py FILE [FILE...]

Exit codes: 0 = all pass, 1 = at least one fail, 2 = usage/missing file.
Each checked file gets a gate mark appended (replaced on re-run):
    <!-- gate: pass -->
    <!-- gate: fail:code1,code2 -->
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Frontmatter every draft must carry (persona 20-content-lead.md, definition of done).
REQUIRED_DRAFT_KEYS = ("asset-id", "client", "channel", "pillar", "brief", "target-query", "word-count")

# Banned outright: social plan §7.1.
BANNED_WORDS = (
    "excited",
    "thrilled",
    "leverage",
    "unlock",
    "game-changer",
    "revolutionary",
    "seamless",
    "robust",
    "cutting-edge",
    "fast-paced landscape",
    "we're proud to",
    "we are proud to",
)

# Claim creep: social plan §9.3 — no teasers, no roadmap, no "soon".
CLAIM_CREEP = (
    "coming soon",
    "will launch",
    "will ship",
    "in the works",
    "stay tuned",
    "on the roadmap",
    "on our roadmap",
    "in a future release",
)

GATE_MARK_RE = re.compile(r"^<!-- gate: (?:pass|fail[^>]*) -->\s*$", re.M)


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, _, value = line.partition(":")
            meta[key.strip().lower()] = value.strip()
    return meta


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    meta = parse_frontmatter(text)
    if meta is None:
        return None, text
    end = text.find("\n---", 3)
    return meta, text[end + 4:] if end != -1 else text


def has_sources_section(body: str) -> bool:
    return bool(re.search(r"(?im)^(#{1,6}\s*)?sources?\s*:?\s*$", body) or re.search(r"(?im)^sources?\s*:", body))


def source_entry_count(body: str) -> int:
    match = re.search(r"(?ims)^(?:#{1,6}\s*)?sources?\s*:?\s*\n(.*?)(?=^#|\Z)", body)
    if match:
        entries = [ln for ln in match.group(1).splitlines() if ln.strip().startswith(("-", "*", "http")) or ln.strip()]
        return len([e for e in entries if e.strip()])
    inline = re.findall(r"(?im)^sources?\s*:\s*(.+)$", body)
    return sum(1 for ln in inline if ln.strip())


def check_draft(body: str, meta: dict | None, path: str) -> list[str]:
    codes: list[str] = []
    if meta is None:
        codes.append("no-frontmatter")
    else:
        missing = [k for k in REQUIRED_DRAFT_KEYS if not meta.get(k)]
        if missing:
            codes.append("missing-keys:" + ",".join(missing))
    words = len(re.findall(r"[A-Za-z0-9']+", body))
    if words < 40:
        codes.append("too-short")
    if not has_sources_section(body):
        codes.append("no-sources")
    elif source_entry_count(body) < 1:
        codes.append("empty-sources")
    codes.extend(scan_text(body))
    return codes


def check_reply(body: str, _meta: dict | None, _path: str) -> list[str]:
    codes: list[str] = []
    words = len(re.findall(r"[A-Za-z0-9']+", body))
    if words < 10:
        codes.append("too-short")
    # A reply carrying any digit must carry a source (zero unsourced numbers).
    if re.search(r"\d", body) and not (has_sources_section(body) and source_entry_count(body) >= 1):
        codes.append("unsourced-number")
    codes.extend(scan_text(body))
    return codes


def scan_text(body: str) -> list[str]:
    codes: list[str] = []
    lower = body.lower()
    hits = [w for w in BANNED_WORDS if re.search(rf"(?<![\w-]){re.escape(w)}(?![\w-])", lower)]
    if hits:
        codes.append("banned-word:" + ",".join(hits))
    creep = [p for p in CLAIM_CREEP if p in lower]
    if creep:
        codes.append("claim-creep:" + ",".join(c.replace(" ", "-") for c in creep))
    return codes


def write_mark(path: Path, codes: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    text = GATE_MARK_RE.sub("", text).rstrip("\n")
    mark = "<!-- gate: pass -->" if not codes else "<!-- gate: fail:" + ",".join(codes) + " -->"
    path.write_text(text + "\n\n" + mark + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: gate.py FILE [FILE...]", file=sys.stderr)
        return 2
    failed = 0
    for arg in argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"ERROR missing file: {arg}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8")
        meta, body = split_frontmatter(text)
        is_reply = "replies" in path.parts
        codes = check_reply(body, meta, str(path)) if is_reply else check_draft(body, meta, str(path))
        write_mark(path, codes)
        if codes:
            failed += 1
            print(f"FAIL {arg} :: {','.join(codes)}")
        else:
            print(f"PASS {arg}")
    total = len(argv) - 1
    print(f"GATE {'FAIL' if failed else 'PASS'} {total - failed}/{total}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
