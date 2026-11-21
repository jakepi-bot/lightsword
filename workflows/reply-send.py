#!/usr/bin/env python3
"""Send one reply from a gated queue/replies/*.md file.

    python3 workflows/reply-send.py queue/replies/fb-reply-20261116-01.md
    python3 workflows/reply-send.py queue/replies/....md --dry-run

Why this exists: a reply file carries frontmatter and a Sources block for the
gate, but only the text may reach Bluesky. Hand-copying that text into a
command is how a gated line and a sent line drift apart. This reads the file,
re-runs the gate, refuses on any failure, extracts the text, and sends through
workflows/bsky.py (the one posting path). It never sends more than one reply.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GATE = REPO / "workflows" / "gate.py"
BSKY = REPO / "workflows" / "bsky.py"
SOURCES_RE = re.compile(r"(?im)^#{0,6}\s*sources\s*:?\s*$")


def parse(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"REFUSED {path.name}: no frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise SystemExit(f"REFUSED {path.name}: unterminated frontmatter")
    meta = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            meta[k.strip().lower()] = v.strip()
    body = text[end + 4:]
    body = SOURCES_RE.split(body, maxsplit=1)[0]
    body = re.sub(r"^#.*$", "", body, flags=re.M)
    body = "\n".join(body.splitlines()).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    return meta, body


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    path = Path(args.file)
    if not path.is_file():
        raise SystemExit(f"REFUSED: no such reply file {args.file}")
    meta, text = parse(path)
    target = meta.get("target", "")
    if not target.startswith("at://"):
        raise SystemExit(f"REFUSED {path.name}: frontmatter has no AT-URI target")
    if not text:
        raise SystemExit(f"REFUSED {path.name}: empty reply text")

    gate = subprocess.run([sys.executable, str(GATE), str(path)],
                          capture_output=True, text=True)
    print(gate.stdout.strip())
    if gate.returncode != 0:
        raise SystemExit(f"REFUSED {path.name}: gate failed, nothing sent")
    if "<!-- gate: pass -->" not in path.read_text(encoding="utf-8"):
        raise SystemExit(f"REFUSED {path.name}: no gate pass mark, nothing sent")

    asset_id = meta.get("asset-id") or path.stem
    id_key = f"{asset_id}+bsky+{datetime.now():%Y-%m-%d}"
    scratch = Path.home() / ".hermes" / "profiles" / "lightsword" / "cache" / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, dir=str(scratch)) as fh:
        fh.write(text + "\n")
        tmp = fh.name
    cmd = [sys.executable, str(BSKY), "--account", "fb", "reply",
           "--to", target, "--text-file", tmp, "--id-key", id_key]
    if args.dry_run:
        cmd.append("--dry-run")
    print(f"TEXT ({len(text)} chars): {text}")
    try:
        sent = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        Path(tmp).unlink(missing_ok=True)
    print(sent.stdout.strip())
    if sent.returncode != 0:
        print(sent.stderr.strip(), file=sys.stderr)
        return sent.returncode
    if sent.stdout.startswith("OK reply"):
        line = {"ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "asset_id": asset_id,
                "target": target, "handle": meta.get("target-handle"),
                "text": text, "result": sent.stdout.splitlines()[0]}
        log = REPO / "logs" / "replies.ndjson"
        log.parent.mkdir(exist_ok=True)
        with log.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
