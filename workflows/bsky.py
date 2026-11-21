#!/usr/bin/env python3
"""Lightsword Bluesky client — AT Protocol, app.bsky.feed.post.

One small stdlib-only client used by every Lightsword posting path: manual
posts, replies, thread chains, and the queue-driven scheduler. It exists so
that publishing is a documented command with an audit line, not an ad-hoc
script per asset.

Design rules (why the code looks like this):

  * Credentials live in the Hermes profile .env (mode 600), never in argv,
    never in the repo, never in a log line. `--account` picks the prefix.
  * Sessions are cached per account under <profile>/state/ because
    com.atproto.server.createSession is capped at 10 calls / 24 h per IP.
    A naive "one createSession per script run" client locks itself out on
    day one. The cache holds the refresh token and is chmod 600.
  * Every action appends one NDJSON line to logs/bsky-actions.ndjson with
    timestamp, account, action, text, URI and outcome. Rate limits are
    enforced by reading that same log, so the log is the single source of
    truth for "what did we already send".
  * Fail closed. A missing credential, an unknown account, a naive
    timestamp, or a text over 300 graphemes is a refusal with exit code 2,
    not a best-effort attempt.

Usage:
    python3 workflows/bsky.py --account lt probe
    python3 workflows/bsky.py --account fb post --text-file draft.txt \\
        --image brand/visual/exports/announcement-1200x1200.png \\
        --alt "Lightsword announcement card. Heading: ..." --id-key demo-1
    python3 workflows/bsky.py --account fb reply --to at://did:plc:.../app.bsky.feed.post/3k... \\
        --text "Thanks — it runs in the browser, nothing to install."
    python3 workflows/bsky.py --account fb delete --uri at://.../app.bsky.feed.post/3k... --why "internal test"
    python3 workflows/bsky.py --account fb mentions --limit 25
    python3 workflows/bsky.py tick --dry-run
    python3 workflows/bsky.py limits

Run `python3 workflows/bsky.py <command> --help` for the per-command surface.
Full operator documentation: docs/bluesky-client.md.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import random
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# Paths and constants
# --------------------------------------------------------------------------

REPO = Path(__file__).resolve().parent.parent
PROFILE = Path(os.environ.get("HERMES_HOME") or "/home/jake/.hermes/profiles/lightsword")
ENV_FILE = Path(os.environ.get("LIGHTSWORD_ENV_FILE") or (PROFILE / ".env"))
STATE_DIR = PROFILE / "state"
AUDIT_LOG = REPO / "logs" / "bsky-actions.ndjson"
MANIFEST = REPO / "published" / "manifest.ndjson"
OUTBOX = REPO / "queue" / "outbox"

XRPC_AUTH = "https://bsky.social/xrpc"
XRPC_PUBLIC = "https://public.api.bsky.app/xrpc"
BSKY_WEB = "https://bsky.app/profile"

# account key -> (env prefix, default handle)
ACCOUNTS = {
    "lt": ("LIGHTSWORD_BSKY_", "lightsword.bsky.social"),
    "fb": ("FLAMBEEE_BSKY_", "flambeee.bsky.social"),
}

# Operator caps (AGENTS.md rule 7 and rule 8). These are local guards in front
# of the platform limits, deliberately tighter than Bluesky's own allowance.
REPLY_CAP_24H = 5
REPLY_MIN_GAP_S = 10 * 60
REPLY_MAX_PER_THREAD = 2
POST_CAP_24H = 20
MAX_TEXT_GRAPHEMES = 300
MAX_IMAGE_BYTES = 1_000_000
ALLOWED_IMAGE_MIME = {"image/png", "image/jpeg", "image/webp"}
EXPIRED_AFTER = timedelta(hours=12)  # a slot older than this is reported, not fired

APP_PW_RE = re.compile(r"^[a-z0-9]{4}(?:-[a-z0-9]{4}){3}$")
URL_RE = re.compile(r"https?://[^\s<>\"\u2019]+")
MENTION_RE = re.compile(r"(?<![\w@/])@([a-zA-Z0-9](?:[a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,24})")
TAG_RE = re.compile(r"(?<![\w#/])#([\w]{1,64})")


class BskyError(Exception):
    """A failed XRPC call. `status` is None for network-level failures."""

    def __init__(self, status, payload, headers=None, method=""):
        self.status = status
        self.payload = payload
        self.headers = headers or {}
        self.method = method
        super().__init__(self._message())

    def _message(self):
        if isinstance(self.payload, dict):
            err = self.payload.get("error") or ""
            msg = self.payload.get("message") or ""
            return f"{self.method or 'xrpc'}: HTTP {self.status} {err} {msg}".strip()
        return f"{self.method or 'xrpc'}: HTTP {self.status} {self.payload}"


class Refused(Exception):
    """A local guard said no: missing credential, rate cap, bad input."""


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_iso(value: str, label: str = "timestamp") -> datetime:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise Refused(f"{label} is not ISO-8601: {value!r}") from exc
    if dt.tzinfo is None:
        raise Refused(f"{label} must carry a UTC offset (e.g. -06:00): {value!r}")
    return dt


def graphemes(text: str) -> int:
    """Approximate extended-grapheme count; combining marks and joiners free."""
    return sum(1 for ch in text if not unicodedata.combining(ch) and ch not in ("\u200d", "\ufe0f"))


def load_env(path: Path = ENV_FILE) -> dict:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def atomic_write(path: Path, text: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp{os.getpid()}")
    tmp.write_text(text, encoding="utf-8")
    if mode is not None:
        os.chmod(tmp, mode)
    os.replace(tmp, path)


def decode_json(raw: bytes) -> dict:
    """Always return a dict. Unparseable or non-object bodies are wrapped, never returned raw."""
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except Exception:
        return {"_raw": raw.decode("utf-8", "replace")[:2000]}
    return parsed if isinstance(parsed, dict) else {"_value": parsed}


def rkey_of(uri: str) -> str:
    return uri.rsplit("/", 1)[-1]


def web_url(handle: str, uri: str) -> str:
    return f"{BSKY_WEB}/{handle}/post/{rkey_of(uri)}"


# --------------------------------------------------------------------------
# HTTP / XRPC
# --------------------------------------------------------------------------

def _http(url, *, method="GET", data=None, headers=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), dict(exc.headers)


def _backoff(attempt: int) -> float:
    return min(30.0, 2.0 ** (attempt - 1)) + random.uniform(0.0, 0.4)


def _retry_wait(headers: dict, attempt: int) -> float:
    remaining = headers.get("ratelimit-remaining") or headers.get("RateLimit-Remaining")
    reset = headers.get("ratelimit-reset") or headers.get("RateLimit-Reset")
    if remaining is not None and str(remaining).strip() == "0" and reset:
        try:
            wait = int(reset) - int(time.time()) + 1
            if 0 < wait <= 120:
                return float(wait)
        except (TypeError, ValueError):
            pass
    retry_after = headers.get("retry-after") or headers.get("Retry-After")
    if retry_after:
        try:
            return min(120.0, float(retry_after))
        except (TypeError, ValueError):
            pass
    return _backoff(attempt)


def xrpc(method, payload=None, *, auth=None, base=XRPC_AUTH, retries=4, timeout=60, raw_body=None,
         content_type="application/json", method_verb="POST") -> tuple[dict, dict, int]:
    """Call an XRPC method. Returns (body, headers, attempts)."""
    url = f"{base}/{method}"
    if raw_body is not None:
        body = raw_body
    elif payload is not None:
        body = json.dumps(payload).encode()
    else:
        body = b""
    headers = {"Content-Type": content_type, "User-Agent": "lightsword-bsky/1.0"}
    if auth:
        headers["Authorization"] = f"Bearer {auth}"
    attempt = 0
    while True:
        attempt += 1
        try:
            status, raw, hdrs = _http(url, method=method_verb, data=body or b"", headers=headers, timeout=timeout)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt >= retries:
                raise BskyError(None, f"network error: {exc}", {}, method) from exc
            time.sleep(_backoff(attempt))
            continue
        if 200 <= status < 300:
            return decode_json(raw), hdrs, attempt
        parsed = decode_json(raw)
        if status == 429 or 500 <= status < 600:
            if attempt >= retries:
                raise BskyError(status, parsed, hdrs, method)
            time.sleep(_retry_wait(hdrs, attempt))
            continue
        raise BskyError(status, parsed, hdrs, method)


def public_call(method, params=None) -> dict:
    url = f"{XRPC_PUBLIC}/{method}"
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    status, raw, hdrs = _http(url, method="GET", headers={"User-Agent": "lightsword-bsky/1.0"})
    parsed = decode_json(raw)
    if not (200 <= status < 300):
        raise BskyError(status, parsed, hdrs, method)
    return parsed


# --------------------------------------------------------------------------
# Audit log
# --------------------------------------------------------------------------

def log_path(override: str | None = None) -> Path:
    return Path(override) if override else AUDIT_LOG


def audit(record: dict, path: Path | None = None) -> dict:
    path = path or AUDIT_LOG
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"v": 1, "ts": iso(now_utc()), **record}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def read_log(path: Path | None = None) -> list[dict]:
    path = path or AUDIT_LOG
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def find_success(id_key: str, path: Path | None = None) -> dict | None:
    if not id_key:
        return None
    for rec in read_log(path):
        if rec.get("idempotency_key") == id_key and rec.get("status") == "ok" and rec.get("action") in ("post", "reply"):
            return rec
    return None


def recent(account: str, actions: tuple[str, ...], hours: int = 24, path: Path | None = None) -> list[dict]:
    cutoff = now_utc() - timedelta(hours=hours)
    out = []
    for rec in read_log(path):
        if rec.get("account") != account or rec.get("action") not in actions or rec.get("status") != "ok":
            continue
        try:
            if parse_iso(rec["ts"]) >= cutoff:
                out.append(rec)
        except (KeyError, Refused):
            continue
    return out


# --------------------------------------------------------------------------
# Account + session
# --------------------------------------------------------------------------

class Account:
    def __init__(self, key: str):
        if key not in ACCOUNTS:
            raise Refused(f"unknown account {key!r}; choose one of {sorted(ACCOUNTS)}")
        self.key = key
        self.prefix, self.default_handle = ACCOUNTS[key]
        env = load_env()
        self.handle = env.get(self.prefix + "HANDLE", "").strip() or self.default_handle
        self.password = env.get(self.prefix + "APP_PASSWORD", "").strip()
        self._access: str | None = None
        self._did: str | None = None
        self.session_source: str | None = None

    # -- credential checks -------------------------------------------------
    def require_credentials(self) -> None:
        if self.password:
            return
        raise Refused(
            f"no app password for account {self.key!r}. Add to {ENV_FILE} (mode 600):\n"
            f"  {self.prefix}HANDLE={self.handle}\n"
            f"  {self.prefix}APP_PASSWORD=xxxx-xxxx-xxxx-xxxx\n"
            "Create the app password in Bluesky: Settings > Privacy and security > App passwords.\n"
            "Never put the account's main password here."
        )

    def credential_report(self) -> dict:
        mode = None
        try:
            mode = oct(ENV_FILE.stat().st_mode & 0o777)
        except OSError:
            pass
        return {
            "account": self.key,
            "handle": self.handle,
            "env_file": str(ENV_FILE),
            "env_file_mode": mode,
            "password_present": bool(self.password),
            "looks_like_app_password": bool(APP_PW_RE.match(self.password or "")),
        }

    # -- session cache -----------------------------------------------------
    @property
    def cache_file(self) -> Path:
        return STATE_DIR / f"bsky-session-{self.key}.json"

    def _load_cache(self) -> dict:
        try:
            data = json.loads(self.cache_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        if data.get("handle") != self.handle:
            return {}
        return data

    def _save_cache(self, data: dict) -> None:
        atomic_write(self.cache_file, json.dumps(data, indent=1) + "\n", mode=0o600)

    @staticmethod
    def _exp(token: str) -> int:
        try:
            payload = token.split(".")[1]
            payload += "=" * (-len(payload) % 4)
            return int(json.loads(base64.urlsafe_b64decode(payload))["exp"])
        except Exception:
            return 0

    def session(self, *, force=False, log: Path | None = None) -> str:
        """Return a usable access JWT, reusing the cache when possible."""
        if self._access and not force:
            return self._access
        self.require_credentials()
        cache = self._load_cache()
        now = int(time.time())

        if not force and cache.get("accessJwt") and self._exp(cache["accessJwt"]) > now + 180:
            self._access = cache["accessJwt"]
            self._did = cache.get("did")
            self.session_source = "cache"
            return self._access or ""

        # Try the refresh token first: createSession is capped at 10/day.
        if not force and cache.get("refreshJwt") and now - int(cache.get("refreshedAt") or 0) > 120:
            try:
                body, headers, attempts = xrpc(
                    "com.atproto.server.refreshSession", None, auth=cache["refreshJwt"], retries=2)
                self._access = body["accessJwt"]
                self._did = body.get("did")
                self.session_source = "refresh"
                self._save_cache({
                    "handle": self.handle, "did": body.get("did"),
                    "accessJwt": body["accessJwt"], "refreshJwt": body.get("refreshJwt", cache["refreshJwt"]),
                    "refreshedAt": now, "createdAt": cache.get("createdAt"),
                })
                audit({"account": self.key, "action": "session", "status": "ok", "source": "refresh",
                       "did": body.get("did"), "attempts": attempts}, log)
                return self._access or ""
            except BskyError as exc:
                audit({"account": self.key, "action": "session", "status": "error", "source": "refresh",
                       "http": exc.status, "error": str(exc)}, log)

        try:
            body, headers, attempts = xrpc("com.atproto.server.createSession",
                                           {"identifier": self.handle, "password": self.password})
        except BskyError as exc:
            audit({"account": self.key, "action": "session", "status": "error", "source": "create",
                   "http": exc.status, "error": str(exc)}, log)
            raise
        self._access = body["accessJwt"]
        self._did = body["did"]
        self.session_source = "create"
        self._save_cache({
            "handle": self.handle, "did": body["did"],
            "accessJwt": body["accessJwt"], "refreshJwt": body.get("refreshJwt"),
            "refreshedAt": now, "createdAt": now,
        })
        audit({"account": self.key, "action": "session", "status": "ok", "source": "create",
               "did": body["did"], "attempts": attempts,
               "ratelimit": _rl(headers)}, log)
        return self._access or ""

    # -- repo helpers ------------------------------------------------------
    def repo(self, *, log: Path | None = None) -> str:
        self.session(log=log)
        return self._did or ""

    def create_record(self, record: dict, *, log: Path | None = None):
        token = self.session(log=log)
        body, headers, attempts = xrpc(
            "com.atproto.repo.createRecord",
            {"repo": self._did or "", "collection": "app.bsky.feed.post", "record": record, "validate": True},
            auth=token)
        return body, headers, attempts


def authed_get(method, params, token, *, base=XRPC_AUTH) -> dict:
    """Authenticated GET (getRecord, listRecords, listNotifications are GETs)."""
    url = f"{base}/{method}?" + urllib.parse.urlencode(params, doseq=True)
    status, raw, hdrs = _http(url, method="GET",
                              headers={"Authorization": f"Bearer {token}",
                                       "User-Agent": "lightsword-bsky/1.0"})
    parsed = decode_json(raw)
    if not (200 <= status < 300):
        raise BskyError(status, parsed, hdrs, method)
    return parsed


def _rl(headers: dict) -> dict:
    return {
        "limit": headers.get("ratelimit-limit") or headers.get("RateLimit-Limit"),
        "remaining": headers.get("ratelimit-remaining") or headers.get("RateLimit-Remaining"),
        "reset": headers.get("ratelimit-reset") or headers.get("RateLimit-Reset"),
        "policy": headers.get("ratelimit-policy") or headers.get("RateLimit-Policy"),
    }


# --------------------------------------------------------------------------
# Record construction
# --------------------------------------------------------------------------

def trim_url(url: str) -> str:
    return url.rstrip(".,;:!?)]}'\"\u201d")


def resolve_handle(handle: str) -> str | None:
    try:
        return public_call("com.atproto.identity.resolveHandle", {"handle": handle})["did"]
    except BskyError:
        return None


def build_facets(text: str, *, resolve_mentions: bool = True) -> list[dict] | None:
    """Byte-offset facets for links, mentions and hashtags. Overlaps dropped."""
    encoded = text.encode("utf-8")
    spans: list[tuple[int, int, dict]] = []

    def byte_range(start_char: int, end_char: int) -> tuple[int, int]:
        return len(text[:start_char].encode("utf-8")), len(text[:end_char].encode("utf-8"))

    for match in URL_RE.finditer(text):
        url = trim_url(match.group(0))
        if len(url) <= len("https://"):
            continue
        start, end = byte_range(match.start(), match.start() + len(url))
        spans.append((start, end, {"$type": "app.bsky.richtext.facet#link", "uri": url}))

    if resolve_mentions:
        for match in MENTION_RE.finditer(text):
            did = resolve_handle(match.group(1))
            if not did:
                continue
            start, end = byte_range(match.start(), match.end())
            spans.append((start, end, {"$type": "app.bsky.richtext.facet#mention", "did": did}))

    for match in TAG_RE.finditer(text):
        start, end = byte_range(match.start(), match.end())
        spans.append((start, end, {"$type": "app.bsky.richtext.facet#tag", "tag": match.group(1)}))

    # Drop overlaps, keep the earliest/longest span.
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    kept: list[tuple[int, int, dict]] = []
    for span in spans:
        if kept and span[0] < kept[-1][1]:
            continue
        kept.append(span)
    if not kept:
        return None
    if kept[-1][1] > len(encoded):
        return None
    return [{"index": {"byteStart": s, "byteEnd": e}, "features": [f]} for s, e, f in kept]


def upload_image(acct: Account, path: Path, *, log: Path | None = None) -> dict:
    if not path.exists():
        raise Refused(f"image not found: {path}")
    data = path.read_bytes()
    if len(data) > MAX_IMAGE_BYTES:
        raise Refused(f"image {path.name} is {len(data)} bytes; Bluesky rejects over {MAX_IMAGE_BYTES}. "
                      "Downscale it first (PIL: im.save(..., optimize=True)).")
    mime = mimetypes.guess_type(path.name)[0] or ""
    if mime not in ALLOWED_IMAGE_MIME:
        raise Refused(f"image {path.name} has type {mime!r}; allowed: {sorted(ALLOWED_IMAGE_MIME)}")
    token = acct.session(log=log)
    body, headers, attempts = xrpc("com.atproto.repo.uploadBlob", None, auth=token,
                                   raw_body=data, content_type=mime, retries=3)
    blob = body.get("blob")
    if not blob:
        raise BskyError(200, f"uploadBlob returned no blob for {path.name}", headers, "com.atproto.repo.uploadBlob")
    audit({"account": acct.key, "action": "upload", "status": "ok", "path": str(path),
           "bytes": len(data), "mime": mime, "attempts": attempts, "ratelimit": _rl(headers)}, log)
    return blob


def validate_text(text: str, label: str = "text") -> str:
    text = (text or "").strip()
    if not text:
        raise Refused(f"{label} is empty")
    if any(ord(ch) < 32 and ch not in "\n\t" for ch in text):
        raise Refused(f"{label} contains control characters")
    count = graphemes(text)
    if count > MAX_TEXT_GRAPHEMES:
        raise Refused(f"{label} is {count} graphemes; the Bluesky limit is {MAX_TEXT_GRAPHEMES}")
    if count > 290:
        print(f"WARNING: {label} is {count} graphemes, close to the {MAX_TEXT_GRAPHEMES} limit", file=sys.stderr)
    return text


def thread_root_for(uri: str, acct: "Account | None" = None) -> tuple[dict | None, dict]:
    """Return (root_ref, parent_ref) for replying to `uri`.

    The public AppView lags a just-published post by seconds to a minute, so a
    thread chain (post 1, then reply 2 immediately) can miss its own parent
    there. Fall back to the authoritative repo read, which is immediate and
    works for any post in our own repo.
    """
    parent: dict = {}
    try:
        thread = public_call("app.bsky.feed.getPostThread",
                             {"uri": uri, "depth": 0, "parentHeight": 0})
        post = (thread or {}).get("thread") or {}
        parent = post.get("post") or {}
    except BskyError:
        parent = {}
    if not parent.get("uri") and acct is not None and "/app.bsky.feed.post/" in uri:
        rkey = rkey_of(uri)
        rec = authed_get("com.atproto.repo.getRecord",
                         {"repo": acct._did or "", "collection": "app.bsky.feed.post", "rkey": rkey},
                         acct.session())
        if rec.get("cid"):
            parent = {"uri": rec.get("uri"), "cid": rec.get("cid"), "record": rec.get("value") or {}}
    if not parent.get("uri"):
        raise Refused(f"cannot resolve parent post {uri} (deleted, blocked, not indexed, or wrong DID)")
    parent_ref = {"uri": parent["uri"], "cid": parent["cid"]}
    reply = (parent.get("record") or {}).get("reply") or {}
    root = reply.get("root")
    if root and root.get("uri") and root.get("cid"):
        return root, parent_ref
    # Fall back to the parent's own root, resolved if only the URI survived.
    if root and root.get("uri"):
        fetched = public_call("app.bsky.feed.getPosts", {"uris": [root["uri"]]})
        posts = (fetched or {}).get("posts") or []
        if posts:
            return {"uri": posts[0]["uri"], "cid": posts[0]["cid"]}, parent_ref
    return parent_ref, parent_ref


# --------------------------------------------------------------------------
# Rate guards
# --------------------------------------------------------------------------

def guard_post(acct: Account, count: int = 1, *, force=False, log: Path | None = None) -> dict:
    used = len(recent(acct.key, ("post", "thread"), path=log))
    if not force and used + count > POST_CAP_24H:
        raise Refused(f"local post cap: {used} posts in the last 24h, cap {POST_CAP_24H}, "
                      f"this action needs {count}. Nothing sent. (--force overrides and logs it.)")
    return {"posts_24h": used, "cap": POST_CAP_24H, "forced": bool(force)}


def guard_reply(acct: Account, thread_root: str | None, *, force=False, log: Path | None = None) -> dict:
    replies = recent(acct.key, ("reply",), path=log)
    if not force:
        if len(replies) >= REPLY_CAP_24H:
            raise Refused(f"reply cap reached: {len(replies)} replies in the last 24h "
                          f"(AGENTS.md rule 7, cap {REPLY_CAP_24H}). The block ends; roll to tomorrow.")
        if replies:
            last = max(parse_iso(r["ts"]) for r in replies)
            elapsed = (now_utc() - last).total_seconds()
            if elapsed < REPLY_MIN_GAP_S:
                wait = int(REPLY_MIN_GAP_S - elapsed)
                raise Refused(f"reply spacing: last reply {int(elapsed)}s ago, minimum {REPLY_MIN_GAP_S}s. "
                              f"Wait {wait}s.")
        if thread_root:
            same = [r for r in replies if r.get("thread_root") == thread_root]
            if len(same) >= REPLY_MAX_PER_THREAD:
                raise Refused(f"thread limit: already {len(same)} replies in {thread_root} "
                              f"(max {REPLY_MAX_PER_THREAD} per thread).")
    return {"replies_24h": len(replies), "cap": REPLY_CAP_24H, "forced": bool(force)}


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def _record_base(text: str, langs: list[str] | None) -> dict:
    rec = {"$type": "app.bsky.feed.post", "text": text, "createdAt": iso(now_utc())}
    if langs:
        rec["langs"] = langs
    facets = build_facets(text)
    if facets:
        rec["facets"] = facets
    return rec


def quote_target(uri: str) -> dict:
    """Resolve a quote target to the {uri, cid} strong ref the embed needs."""
    posts = public_call("app.bsky.feed.getPosts", {"uris": [uri]}).get("posts") or []
    if not posts:
        raise Refused(f"quote target not found or hidden: {uri}")
    return {"uri": posts[0]["uri"], "cid": posts[0]["cid"]}


def resolve_quote(item: dict) -> str | None:
    """Return the AT-URI a scheduled item should quote, or None.

    ``quote`` is an explicit URI. ``quote_asset`` names another outbox item and
    is resolved at tick time, so a quote can be armed before its target exists.
    """
    explicit = item.get("quote")
    ref = item.get("quote_asset")
    if explicit and ref:
        raise Refused(f"{item.get('id')}: set quote or quote_asset, not both")
    if explicit:
        return explicit
    if not ref:
        return None
    path = OUTBOX / f"{ref}.json"
    if not path.exists():
        raise Refused(f"{item.get('id')}: quote_asset {ref!r} has no outbox item")
    target = load_item(path)
    if not target.get("uri"):
        raise Refused(f"{item.get('id')}: quote_asset {ref!r} has not published yet")
    return target["uri"]


WINDOW_FILE = STATE_DIR / "flambeee-window.json"


def check_window(acct: "Account") -> None:
    """Hard authorization window for the client account.

    The last campaign's only operational failure was a reply shift that ran past
    its window; the check lived in prompt text and the prompt drifted. A window
    that can be typed around is not a control. This one is a file read that
    refuses the write and names the expired range.

    Renewal is deliberate: write state/flambeee-window.json with a new
    {"start", "end", "authority"} (mode 600, outside the repo).
    """
    if acct.key != "fb":
        return
    if not WINDOW_FILE.exists():
        raise Refused(
            f"no flambeee posting window at {WINDOW_FILE}; refusing to write on the client account")
    try:
        data = json.loads(WINDOW_FILE.read_text())
        start = datetime.fromisoformat(data["start"])
        end = datetime.fromisoformat(data["end"])
    except (ValueError, KeyError) as exc:
        raise Refused(f"flambeee window file is malformed ({exc}); refusing to write") from exc
    now = now_utc()
    if not (start <= now <= end):
        raise Refused(
            f"flambeee window closed: {start.isoformat()} -> {end.isoformat()} "
            f"(now {now.isoformat()}); authority: {data.get('authority', 'unnamed')}")


def do_post(acct: Account, text: str, *, images: list[Path] | None = None, alts: list[str] | None = None,
            langs: list[str] | None = None, reply_to: str | None = None, id_key: str | None = None,
            asset_id: str | None = None, dry_run: bool = False, force: bool = False,
            log: Path | None = None, note: str | None = None, quote: str | None = None) -> dict:
    images = images or []
    alts = alts or []
    if images and len(alts) != len(images):
        raise Refused("every --image needs exactly one --alt")
    text = validate_text(text)
    if reply_to is not None and not reply_to.strip().startswith("at://"):
        raise Refused(f"reply_to must be an AT-URI, got {reply_to!r}")
    if quote is not None:
        quote = (quote or "").strip()
        if not quote.startswith("at://"):
            raise Refused(f"quote must be an AT-URI, got {quote!r}")
        if images:
            raise Refused("a quote post cannot also carry images (needs app.bsky.embed.recordWithMedia)")
    if len(images) > 4:
        raise Refused("Bluesky allows at most 4 images per post")

    if not dry_run:
        check_window(acct)

    if id_key:
        prior = find_success(id_key, path=log)
        if prior:
            return {"status": "skipped", "reason": "idempotency_key already published",
                    "uri": prior.get("uri"), "idempotency_key": id_key}

    # Resolve the thread root before the guard, so the "2 replies per thread"
    # rule is enforced against the real root and not against nothing.
    root = parent = None
    if reply_to:
        root, parent = thread_root_for(reply_to, acct)
        guard = guard_reply(acct, (root or {}).get("uri"), force=force, log=log)
    else:
        guard = guard_post(acct, force=force, log=log)

    rec = _record_base(text, langs)
    if reply_to:
        rec["reply"] = {"root": root, "parent": parent}
    if images:
        blobs = [upload_image(acct, path, log=log) for path in images] if not dry_run else []
        if dry_run:
            rec["embed"] = {"$type": "app.bsky.embed.images",
                            "images": [{"alt": alt, "image": "<uploaded blob>", "path": str(p)}
                                       for alt, p in zip(alts, images)]}
        else:
            rec["embed"] = {"$type": "app.bsky.embed.images",
                            "images": [{"alt": alt, "image": blob} for alt, blob in zip(alts, blobs)]}
    elif quote:
        rec["embed"] = {"$type": "app.bsky.embed.record", "record": quote_target(quote)}

    base = {"account": acct.key, "action": "reply" if reply_to else "post",
            "text": text, "chars": graphemes(text), "idempotency_key": id_key,
            "asset_id": asset_id, "thread_root": (rec.get("reply") or {}).get("root", {}).get("uri"),
            "reply_to": reply_to, "quote": quote, "guard": guard, "note": note,
            "images": [{"path": str(p), "alt": a} for p, a in zip(images, alts)]}

    if dry_run:
        print(json.dumps({"record": rec, "audit": base}, indent=2, ensure_ascii=False))
        return {"status": "dry-run", "record": rec, "audit": base}

    started = time.time()
    try:
        body, headers, attempts = acct.create_record(rec, log=log)
    except BskyError as exc:
        audit({**base, "status": "error", "http": exc.status, "error": str(exc),
               "duration_ms": int((time.time() - started) * 1000)}, log)
        raise
    uri, cid = body.get("uri"), body.get("cid")
    if not uri or not cid:
        raise BskyError(200, f"createRecord returned no uri/cid: {body}", headers, "com.atproto.repo.createRecord")
    entry = audit({**base, "status": "ok", "uri": uri, "cid": cid, "rkey": rkey_of(uri),
                   "url": web_url(acct.handle, uri), "http": 200, "attempts": attempts,
                   "duration_ms": int((time.time() - started) * 1000),
                   "ratelimit": _rl(headers), "forced": bool(force)}, log)
    if asset_id:
        append_manifest(entry)
    return entry


def append_manifest(entry: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    line = {
        "approver": entry.get("approver") or "autonomous-2026-11-05-directive",
        "asset_id": entry["asset_id"],
        "account": entry["account"],
        "gate": entry.get("gate", "pass"),
        "idempotency_key": entry.get("idempotency_key"),
        "platform": "bsky",
        "timestamp": entry["ts"],
        "uri": entry.get("uri"),
        "url": entry.get("url"),
        "format": entry.get("format", "post"),
    }
    with MANIFEST.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(line) + "\n")


def cmd_probe(args) -> int:
    acct = Account(args.account)
    report = acct.credential_report()
    print(json.dumps(report, indent=2) if args.json else
          f"account={acct.key} handle={acct.handle} env={report['env_file']} mode={report['env_file_mode']} "
          f"password_present={report['password_present']} app_password={report['looks_like_app_password']}")
    if not report["looks_like_app_password"] and report["password_present"]:
        print("WARNING: the stored credential does not look like a Bluesky app password "
              "(expected xxxx-xxxx-xxxx-xxxx). Never store the main account password.", file=sys.stderr)
    acct.session()
    prof = public_call("app.bsky.actor.getProfile", {"actor": acct.handle})
    out = {
        "did": acct._did,
        "handle": prof.get("handle"),
        "displayName": prof.get("displayName"),
        "description": prof.get("description"),
        "followers": prof.get("followersCount"),
        "following": prof.get("followsCount"),
        "posts": prof.get("postsCount"),
        "pinned": (prof.get("pinnedPost") or {}).get("uri"),
        "session_source": acct.session_source,
    }
    print(json.dumps(out, indent=2) if args.json else
          f"session OK via {out['session_source']} did={out['did']}\n"
          f"profile: followers={out['followers']} following={out['following']} posts={out['posts']}\n"
          f"bio: {out['description']!r}")
    return 0


def cmd_post(args) -> int:
    acct = Account(args.account)
    text = Path(args.text_file).read_text(encoding="utf-8") if args.text_file else args.text
    entry = do_post(acct, text, images=[Path(p) for p in (args.image or [])], alts=args.alt or [],
                    langs=args.lang or ["en"], id_key=args.id_key, asset_id=args.asset_id,
                    dry_run=args.dry_run, force=args.force, note=args.note, quote=args.quote)
    return _report(entry, args)


def cmd_reply(args) -> int:
    if not (args.to or "").strip().startswith("at://"):
        raise Refused(f"--to must be an AT-URI (at://did:.../app.bsky.feed.post/...), got {args.to!r}")
    acct = Account(args.account)
    text = Path(args.text_file).read_text(encoding="utf-8") if args.text_file else args.text
    entry = do_post(acct, text, images=[Path(p) for p in (args.image or [])], alts=args.alt or [],
                    langs=args.lang or ["en"], reply_to=args.to, id_key=args.id_key,
                    dry_run=args.dry_run, force=args.force, note=args.note)
    return _report(entry, args)


def _report(entry: dict, args) -> int:
    if args.json:
        print(json.dumps(entry, indent=2, ensure_ascii=False))
    elif entry.get("status") == "dry-run":
        pass  # do_post already printed the plan
    elif entry.get("status") == "skipped":
        print(f"SKIPPED {entry['reason']}: {entry.get('uri')}")
    else:
        print(f"OK {entry['action']} {entry['ts']} {entry['uri']}\n   {entry['url']}")
    return 0


def cmd_thread(args) -> int:
    acct = Account(args.account)
    payload = json.loads(Path(args.source).read_text(encoding="utf-8"))
    posts = payload.get("posts") if isinstance(payload, dict) else payload
    if not isinstance(posts, list) or not posts:
        raise Refused("thread file must be a JSON list of posts or {\"posts\": [...]}")
    guard_post(acct, len(posts), force=args.force)
    parent_uri = args.to
    results = []
    for index, item in enumerate(posts):
        if isinstance(item, str):
            item = {"text": item}
        text = item.get("text") or ""
        images = [Path(p) for p in item.get("images", [])]
        alts = item.get("alts", [])
        if not images and item.get("image"):
            images, alts = [Path(item["image"])], [item.get("alt", "")]
        entry = do_post(acct, text, images=images, alts=alts, reply_to=parent_uri,
                        id_key=(args.id_key or f"thread-{args.source}") + f"-{index + 1}",
                        dry_run=args.dry_run, force=args.force, note=args.note)
        results.append(entry)
        if not args.dry_run:
            parent_uri = entry["uri"]
        print(f"  [{index + 1}/{len(posts)}] {entry.get('uri')}")
    print(json.dumps(results, indent=2, ensure_ascii=False) if args.json else
          f"thread: {len(results)} posts, head {results[0].get('url')}")
    return 0


def cmd_delete(args) -> int:
    acct = Account(args.account)
    token = acct.session()
    rkey = rkey_of(args.uri)
    try:
        body, headers, attempts = xrpc(
            "com.atproto.repo.deleteRecord",
            {"repo": acct._did, "collection": "app.bsky.feed.post", "rkey": rkey}, auth=token)
    except BskyError as exc:
        if exc.status == 400 and "Could not locate record" in json.dumps(exc.payload):
            audit({"account": acct.key, "action": "delete", "status": "ok", "uri": args.uri,
                   "why": args.why, "note": "already absent"}, args.log)
            print(f"ABSENT (already deleted): {args.uri}")
            return 0
        audit({"account": acct.key, "action": "delete", "status": "error", "uri": args.uri,
               "why": args.why, "http": exc.status, "error": str(exc)}, args.log)
        raise
    audit({"account": acct.key, "action": "delete", "status": "ok", "uri": args.uri,
           "why": args.why, "attempts": attempts}, args.log)
    print(json.dumps({"deleted": args.uri, "why": args.why}) if args.json else
          f"DELETED {args.uri}  ({args.why or 'no reason given'})")
    return 0


def cmd_get(args) -> int:
    posts = public_call("app.bsky.feed.getPosts", {"uris": [args.uri]}).get("posts") or []
    if not posts:
        print(f"NOT FOUND (hidden, deleted, or not indexed): {args.uri}")
        return 2 if not args.json else 0
    post = posts[0]
    out = {"uri": post["uri"], "cid": post["cid"], "author": (post.get("author") or {}).get("handle"),
           "indexedAt": post.get("indexedAt"), "likeCount": post.get("likeCount"),
           "replyCount": post.get("replyCount"), "repostCount": post.get("repostCount"),
           "record": post.get("record")}
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def cmd_replies(args) -> int:
    thread = public_call("app.bsky.feed.getPostThread", {"uri": args.uri, "depth": args.depth})
    root = (thread or {}).get("thread") or {}
    if not root.get("post"):
        print(f"NOT FOUND: {args.uri}")
        return 2
    rows = []

    def walk(node, level=0):
        post = node.get("post")
        if post:
            rows.append({
                "level": level,
                "uri": post["uri"],
                "author": (post.get("author") or {}).get("handle"),
                "indexedAt": post.get("indexedAt"),
                "text": (post.get("record") or {}).get("text", ""),
                "replyCount": post.get("replyCount"),
            })
        for child in node.get("replies") or []:
            walk(child, level + 1)

    walk(root)
    body = [(r.get("post") or {}).get("record", {}).get("text", "") for r in [root]]
    if args.json:
        print(json.dumps({"root": args.uri, "count": len(rows), "replies": rows}, indent=2, ensure_ascii=False))
    else:
        print(f"root {args.uri}\n  {body[0][:160]!r}")
        print(f"replies: {len(rows) - 1}")
        for row in rows[1:]:
            print(f"  {'  ' * (row['level'] - 1)}@{row['author']} {row['indexedAt']} {row['uri']}\n"
                  f"  {'  ' * (row['level'] - 1)}  {row['text'][:200]!r}")
    return 0


def cmd_mentions(args) -> int:
    acct = Account(args.account)
    token = acct.session()
    params = {"limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    parsed = authed_get("app.bsky.notification.listNotifications", params, token)
    wanted = {"mention", "reply", "quote"}
    rows = []
    for note in parsed.get("notifications", []):
        if note.get("reason") not in wanted:
            continue
        if args.unread_only and note.get("isRead"):
            continue
        rows.append({
            "reason": note.get("reason"),
            "author": (note.get("author") or {}).get("handle"),
            "author_did": (note.get("author") or {}).get("did"),
            "uri": note.get("uri"),
            "url": web_url((note.get("author") or {}).get("handle", ""), note["uri"]) if note.get("uri") else None,
            "indexedAt": note.get("indexedAt"),
            "isRead": note.get("isRead"),
            "text": (note.get("record") or {}).get("text", ""),
            "reply_parent": ((note.get("record") or {}).get("reply") or {}).get("parent", {}).get("uri"),
        })
    if args.mark_seen and rows:
        try:
            xrpc("app.bsky.notification.updateSeen", {"seenAt": iso(now_utc())}, auth=token)
        except BskyError as exc:
            print(f"WARNING: could not mark notifications seen: {exc}", file=sys.stderr)
    if args.json:
        print(json.dumps({"count": len(rows), "cursor": parsed.get("cursor"), "notifications": rows},
                         indent=2, ensure_ascii=False))
    else:
        print(f"{len(rows)} mention/reply/quote notifications (limit {args.limit})")
        for row in rows:
            flag = " " if row["isRead"] else "*"
            print(f"{flag}[{row['reason']}] @{row['author']} {row['indexedAt']}\n"
                  f"   {row['text'][:200]!r}\n   {row['uri']}")
    return 0


def cmd_limits(args) -> int:
    out = {}
    for key in (ACCOUNTS if args.all else [args.account]):
        acct = Account(key)
        posts = recent(key, ("post", "thread"))
        replies = recent(key, ("reply",))
        last = max((parse_iso(r["ts"]) for r in replies), default=None)
        next_allowed = None
        if last:
            next_allowed = iso(last + timedelta(seconds=REPLY_MIN_GAP_S))
        out[key] = {
            "posts_24h": len(posts), "post_cap": POST_CAP_24H,
            "replies_24h": len(replies), "reply_cap": REPLY_CAP_24H,
            "last_reply": iso(last) if last else None,
            "next_reply_allowed": next_allowed,
            "session_cached": acct.cache_file.exists(),
            "credentials_present": bool(acct.password),
        }
    print(json.dumps(out, indent=2))
    return 0


# -- profile helpers (used by the brand-rollout card) -----------------------

def cmd_search(args) -> int:
    """Authenticated post search. The public AppView returns 403 for searchPosts;
    the authenticated PDS does not. Read-only: no audit line, no write."""
    acct = Account(args.account)
    token = acct.session()
    params = {"q": args.query, "limit": str(args.limit)}
    if args.sort:
        params["sort"] = args.sort
    if args.since:
        params["since"] = args.since
    if args.until:
        params["until"] = args.until
    if args.author:
        params["author"] = args.author
    body = authed_get("app.bsky.feed.searchPosts", params, token)
    posts = body.get("posts") or []
    if args.json:
        print(json.dumps(body, indent=2, ensure_ascii=False))
        return 0
    for p in posts:
        a = p.get("author") or {}
        r = p.get("record") or {}
        is_reply = "reply" in r
        print(f"{a.get('handle')}  likes={p.get('likeCount', 0)} replies={p.get('replyCount', 0)} "
              f"reposts={p.get('repostCount', 0)}  {'[reply] ' if is_reply else ''}{p.get('uri')}")
        text = (r.get("text") or "").replace("\n", " ")
        print(f"   {text[:220]}")
        if p.get("indexedAt"):
            print(f"   indexed {p['indexedAt']}")
    print(f"-- {len(posts)} post(s)", file=sys.stderr)
    return 0


def cmd_profile_get(args) -> int:
    prof = public_call("app.bsky.actor.getProfile", {"actor": args.actor})
    keep = {k: prof.get(k) for k in ("did", "handle", "displayName", "description",
                                     "avatar", "banner", "followersCount", "followsCount", "postsCount")}
    print(json.dumps(keep, indent=2))
    return 0


def cmd_profile_set(args) -> int:
    acct = Account(args.account)
    token = acct.session()
    if acct._did != public_call("com.atproto.identity.resolveHandle", {"handle": acct.handle})["did"]:
        raise Refused("session DID does not match the configured handle")
    current = {}
    try:
        rec = authed_get("com.atproto.repo.getRecord",
                         {"repo": acct._did or "", "collection": "app.bsky.actor.profile",
                          "rkey": "self"}, token)
        current = rec.get("value") or {}
    except BskyError as exc:
        if exc.status != 400:
            raise
    updated = dict(current)
    updated["$type"] = "app.bsky.actor.profile"
    if args.description is not None:
        updated["description"] = args.description
    if args.display_name is not None:
        updated["displayName"] = args.display_name
    if args.unpin:
        updated.pop("pinnedPost", None)
    if args.pin:
        # Resolve a strongRef (uri + cid) the same way --quote does. A pinned
        # post is presentation: a profile visitor sees it first, which is the
        # cheapest conversion surface the account has.
        cid = None
        try:
            got = public_call("app.bsky.feed.getPosts", {"uris": [args.pin]})
            hits = got.get("posts") or []
            if hits:
                cid = hits[0].get("cid")
        except BskyError:
            cid = None
        if not cid:
            rec = authed_get("com.atproto.repo.getRecord",
                             {"repo": acct._did or "", "collection": "app.bsky.feed.post",
                              "rkey": rkey_of(args.pin)}, token)
            cid = rec.get("cid")
        if not cid:
            raise Refused(f"could not resolve a cid for {args.pin!r}; pin not changed")
        updated["pinnedPost"] = {"$type": "com.atproto.repo.strongRef",
                                 "uri": args.pin, "cid": cid}
    if args.dry_run:
        # No blob upload on a dry run: uploads are writes to the account.
        plan = dict(updated)
        if args.avatar:
            plan["avatar"] = f"<would upload {args.avatar}>"
        if args.banner:
            plan["banner"] = f"<would upload {args.banner}>"
        print(json.dumps(plan, indent=2, default=str))
        return 0
    if acct.key == "fb":
        check_window(acct)
    if args.avatar:
        updated["avatar"] = upload_image(acct, Path(args.avatar))
    if args.banner:
        updated["banner"] = upload_image(acct, Path(args.banner))
    body, headers, attempts = xrpc("com.atproto.repo.putRecord",
                                   {"repo": acct._did, "collection": "app.bsky.actor.profile",
                                    "rkey": "self", "record": updated}, auth=token)
    audit({"account": acct.key, "action": "profile", "status": "ok",
           "uri": body.get("uri"), "cid": body.get("cid"),
           "description": updated.get("description"),
           "avatar": bool(updated.get("avatar")), "banner": bool(updated.get("banner"))})
    print(f"PROFILE UPDATED {body.get('uri')}")
    return 0


# -- scheduler --------------------------------------------------------------

def load_item(path: Path) -> dict:
    item = json.loads(path.read_text(encoding="utf-8"))
    item["_path"] = str(path)
    return item


def save_item(item: dict) -> None:
    path = Path(item["_path"])
    clean = {k: v for k, v in item.items() if not k.startswith("_")}
    atomic_write(path, json.dumps(clean, indent=2, ensure_ascii=False) + "\n")


def cmd_schedule(args) -> int:
    if args.disarm:
        target = OUTBOX / f"{args.disarm}.json"
        if not target.exists():
            raise Refused(f"no outbox item named {args.disarm!r}")
        item = load_item(target)
        if item.get("status") == "published":
            raise Refused(f"{args.disarm} already published ({item.get('uri')}); delete the post instead")
        item["status"] = "cancelled"
        item["last_error"] = args.why or "disarmed by operator"
        save_item(item)
        print(f"DISARMED {args.disarm} (status=cancelled)")
        return 0
    if args.list:
        rows = []
        for path in sorted(OUTBOX.glob("*.json")):
            item = load_item(path)
            rows.append({k: item.get(k) for k in ("id", "account", "publish_at", "status", "uri", "attempts")})
        print(json.dumps(rows, indent=2))
        return 0
    if not args.file:
        raise Refused("schedule needs --file or --list")
    src = Path(args.file)
    item = json.loads(src.read_text(encoding="utf-8"))
    missing = [k for k in ("id", "publish_at", "text") if not item.get(k)]
    if missing:
        raise Refused(f"outbox item missing required keys: {missing}")
    item.setdefault("account", args.account)
    if item["account"] not in ACCOUNTS:
        raise Refused(f"item account {item['account']!r} is unknown")
    if item.get("quote") and item.get("quote_asset"):
        raise Refused("outbox item sets both quote and quote_asset; pick one")
    if item.get("quote") and not str(item["quote"]).startswith("at://"):
        raise Refused(f"quote must be an AT-URI, got {item['quote']!r}")
    if (item.get("quote") or item.get("quote_asset")) and (item.get("images") or item.get("image")):
        raise Refused("a quote post cannot also carry images")
    parse_iso(item["publish_at"], "publish_at")
    validate_text(item["text"])
    item.setdefault("idempotency_key", item["id"])
    item.setdefault("status", "queued")
    item.setdefault("attempts", 0)
    target = OUTBOX / f"{item['id']}.json"
    atomic_write(target, json.dumps(item, indent=2, ensure_ascii=False) + "\n")
    print(f"ARMED {target}  {item['account']} {item['publish_at']}  {item['id']}")
    return 0


def cmd_arm(args) -> int:
    """Turn a gate-passed staged asset in queue/social/ into a scheduled outbox item."""
    hits = []
    for path in sorted((REPO / "queue" / "social").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("asset_id") == args.asset_id:
            hits.append((path, data))
    if not hits:
        raise Refused(f"no staged asset with asset_id {args.asset_id!r} in queue/social/")
    path, asset = hits[-1]
    if asset.get("gate") != "pass":
        raise Refused(f"{args.asset_id} has gate={asset.get('gate')!r}; only a gate pass can be armed")
    if asset.get("status") in ("superseded", "do_not_publish"):
        raise Refused(f"{args.asset_id} is marked {asset.get('status')!r}; it cannot be armed")
    when = parse_iso(args.publish_at, "--publish-at")
    text = asset.get("text") or ""
    validate_text(text, f"{args.asset_id} text")
    # The brief's no-link CTA, used by the 18:45 link check (workflows/link-check.py)
    # when a blog URL in `text` is not live yet. Optional; absent means the check
    # holds the item instead of publishing a dead link.
    fallback = (asset.get("text_fallback") or "").strip()
    if fallback:
        validate_text(fallback, f"{args.asset_id} text_fallback")
    media = asset.get("media")
    images = media if isinstance(media, list) else ([media] if media else [])
    item = {
        "id": args.asset_id,
        "account": args.account if args.account_explicit else ("fb" if asset.get("client") == "fb" else "lt"),
        "publish_at": when.isoformat(),
        "text": text,
        "text_fallback": fallback or None,
        "images": images,
        "alts": [asset.get("alt_text", "")] * len(images),
        "idempotency_key": asset.get("idempotency_key") or args.asset_id,
        "asset_id": args.asset_id,
        "channel": asset.get("channel"),
        "client": asset.get("client"),
        "brief": asset.get("brief"),
        "draft": asset.get("draft"),
        "slot": asset.get("slot"),
        "status": "queued",
        "attempts": 0,
        "armed_from": str(path.relative_to(REPO)),
    }
    target = OUTBOX / f"{item['id']}.json"
    atomic_write(target, json.dumps(item, indent=2, ensure_ascii=False) + "\n")
    print(f"ARMED {item['id']} -> {item['publish_at']} on account {item['account']} "
          f"(from {path.name}, gate pass)")
    return 0


def acquire_lock() -> Path | None:
    lock = AUDIT_LOG.parent / ".bsky-tick.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        return lock
    except FileExistsError:
        try:
            age = time.time() - lock.stat().st_mtime
        except OSError:
            return lock
        if age < 600:
            return None
        lock.unlink(missing_ok=True)
        return acquire_lock()


def cmd_tick(args) -> int:
    OUTBOX.mkdir(parents=True, exist_ok=True)
    lock = acquire_lock()
    if lock is None:
        return 0  # another tick is running
    published, warnings = [], []

    def persist(it):
        """Dry runs must never mutate the outbox: the campaign dry-checks 12 slots."""
        if not args.dry_run:
            save_item(it)
    try:
        now = parse_iso(args.now) if args.now else now_utc()
        items = []
        for path in sorted(OUTBOX.glob("*.json")):
            try:
                items.append(load_item(path))
            except (OSError, json.JSONDecodeError) as exc:
                warnings.append(f"unreadable outbox item {path.name}: {exc}")
        due = [it for it in items if it.get("status") in ("queued", "retry")]
        due.sort(key=lambda it: it.get("publish_at") or "")
        for item in due:
            try:
                when = parse_iso(item["publish_at"], f"{item.get('id')}.publish_at")
            except Refused as exc:
                item["status"] = "failed"
                item["last_error"] = str(exc)
                persist(item)
                warnings.append(str(exc))
                continue
            if when > now:
                continue
            if now - when > EXPIRED_AFTER and not args.allow_expired:
                item["status"] = "expired"
                item["last_error"] = f"slot {item['publish_at']} was more than {EXPIRED_AFTER} old at tick"
                persist(item)
                warnings.append(f"EXPIRED {item['id']} ({item['publish_at']}); not published automatically")
                continue
            acct = Account(item.get("account", "lt"))
            if args.dry_run:
                # A dry run must work before the credential exists: the campaign
                # checks all 12 slots before the account is connected.
                try:
                    validate_text(item["text"], item["id"])
                    chars = f"{graphemes(item['text'])} graphemes"
                    images = item.get("images") or ([item["image"]] if item.get("image") else [])
                    detail = f"{chars}, {len(images)} image(s)"
                    if item.get("quote") or item.get("quote_asset"):
                        detail += f", quote {item.get('quote') or ('asset:' + item['quote_asset'])}"
                except Refused as exc:
                    detail = f"INVALID: {exc}"
                print(f"DRY-RUN {item['id']} ({acct.key}) {item['publish_at']} {detail} "
                      f"creds={'ok' if acct.password else 'MISSING'}")
                continue
            if not acct.password:
                # Leave it queued; warn at most once an hour so cron does not spam.
                last_warn = item.get("last_warn_at")
                if not last_warn or (now_utc() - parse_iso(last_warn)).total_seconds() > 3600:
                    item["last_warn_at"] = iso(now_utc())
                    persist(item)
                    warnings.append(f"BLOCKED {item['id']}: no app password for account {acct.key!r} "
                                    f"in {ENV_FILE}")
                continue
            try:
                entry = do_post(acct, item["text"],
                                images=[Path(p) for p in item.get("images") or ([item["image"]] if item.get("image") else [])],
                                alts=item.get("alts") or ([item["alt"]] if item.get("alt") else []),
                                langs=item.get("langs") or ["en"],
                                reply_to=item.get("reply_to"),
                                quote=resolve_quote(item),
                                id_key=item.get("idempotency_key") or item["id"],
                                asset_id=item.get("asset_id"),
                                dry_run=args.dry_run,
                                note=f"scheduled {item['publish_at']}")
            except Refused as exc:
                if "idempotency_key already published" in str(exc):
                    item["status"] = "published-duplicate"
                    persist(item)
                    continue
                if "has not published yet" in str(exc):
                    # The quote target is late: stay queued, do not burn attempts,
                    # warn at most once an hour so cron does not spam.
                    last_warn = item.get("last_warn_at")
                    if not last_warn or (now_utc() - parse_iso(last_warn)).total_seconds() > 3600:
                        item["last_warn_at"] = iso(now_utc())
                        persist(item)
                        warnings.append(f"WAITING {item['id']}: {exc}")
                    continue
                item["attempts"] = int(item.get("attempts") or 0) + 1
                item["last_error"] = str(exc)
                item["status"] = "failed" if item["attempts"] >= 3 else "retry"
                persist(item)
                warnings.append(f"REFUSED {item['id']}: {exc}")
                continue
            except BskyError as exc:
                item["attempts"] = int(item.get("attempts") or 0) + 1
                item["last_error"] = str(exc)
                item["status"] = "failed" if item["attempts"] >= 3 else "retry"
                persist(item)
                warnings.append(f"FAILED {item['id']} attempt {item['attempts']}: {exc}")
                continue
            if entry.get("status") == "skipped":
                item["status"] = "published-duplicate"
                item["uri"] = entry.get("uri")
                persist(item)
                continue
            item.update({"status": "published", "uri": entry["uri"], "url": entry["url"],
                         "published_at": entry["ts"], "attempts": int(item.get("attempts") or 0) + 1,
                         "last_error": None})
            persist(item)
            published.append(item)
            print(f"PUBLISHED {item['account']} {item['publish_at']} {item['id']} {entry['uri']}\n  {entry['url']}")
        for warning in warnings:
            print(f"WARNING {warning}", file=sys.stderr)
        summary = {"due": len(due), "published": len(published), "warnings": len(warnings)}
        if summary["due"] or summary["warnings"]:
            # A tick with nothing to do is a heartbeat, not an action: keeping
            # those out of the log stops 288 lines a day burying real events.
            audit({"account": args.account, "action": "tick", "status": "ok", **summary})
        return 0 if not warnings else 3
    finally:
        lock.unlink(missing_ok=True)


# -- self-test --------------------------------------------------------------

def cmd_selftest(args) -> int:
    """Post a clearly-marked internal test with an image, verify, delete, verify."""
    acct = Account(args.account)
    stamp = iso(now_utc())
    text = args.text or f"INTERNAL TEST — Lightsword posting client check at {stamp}. Deleted right after verification."
    stamp_slug = re.sub(r"[^0-9]", "", stamp)[:14]
    id_key = f"selftest-{acct.key}-{stamp_slug}"
    steps = []

    def step(name, ok, detail="", fatal=True):
        steps.append({"step": name, "ok": bool(ok), "fatal": fatal, "detail": detail})
        label = "PASS" if ok else ("WARN" if not fatal else "FAIL")
        print(f"{label}  {name}  {detail}")

    acct.session()
    step("session", True, f"{acct.key} handle={acct.handle} did={acct._did} via {acct.session_source}")

    entry = do_post(acct, text,
                    images=[Path(args.image)] if args.image else [],
                    alts=[args.alt] if args.image else [],
                    langs=["en"], id_key=id_key, asset_id=args.asset_id, note="selftest")
    uri = entry["uri"]
    step("post with image+alt", True, uri)

    # Primary proof the record exists: the authoritative repo read.
    record = {}
    try:
        got = authed_get("com.atproto.repo.getRecord",
                         {"repo": acct._did or "", "collection": "app.bsky.feed.post",
                          "rkey": rkey_of(uri)}, acct.session())
        record = got.get("value") or {}
    except BskyError as exc:
        step("repo read-back", False, str(exc))
    else:
        embed = record.get("embed") or {}
        images = embed.get("images") or []
        alt_ok = (not args.image) or bool(images and images[0].get("alt") == args.alt)
        step("repo read-back", bool(record.get("text")) and alt_ok,
             f"text_match={record.get('text') == text} images={len(images)} alt_match={alt_ok}")

    # Secondary proof: the public AppView sees it. Indexing lag is a warning, not a failure.
    public_seen = False
    for _ in range(20):
        try:
            posts = public_call("app.bsky.feed.getPosts", {"uris": [uri]}).get("posts") or []
        except BskyError:
            posts = []
        if posts:
            public_seen = True
            post = posts[0]
            embed = (post.get("record") or {}).get("embed") or {}
            images = embed.get("images") or []
            alt_ok = (not args.image) or bool(images and images[0].get("alt") == args.alt)
            step("public read-back", alt_ok,
                 f"author=@{post['author']['handle']} images={len(images)} alt_match={alt_ok}")
            break
        time.sleep(3)
    if not public_seen:
        step("public read-back", False,
             "AppView had not indexed the post within 60s (record is in the repo; lag, not loss)",
             fatal=False)

    thread = public_call("app.bsky.feed.getPostThread", {"uri": uri, "depth": 2})
    replies = (thread.get("thread") or {}).get("replies") or []
    step("reply fetch", True, f"getPostThread ok, {len(replies)} replies at test time")

    mentions_ok = True
    try:
        cmd_mentions(argparse.Namespace(account=acct.key, limit=10, unread_only=False,
                                        mark_seen=False, cursor=None, json=False))
    except Exception as exc:  # noqa: BLE001 - reported, not fatal
        mentions_ok = False
        step("mentions fetch", False, str(exc))
    if mentions_ok:
        step("mentions fetch", True, "listNotifications ok")

    if args.keep:
        step("delete", True, f"skipped (--keep); live at {entry['url']}")
    else:
        token = acct.session()
        xrpc("com.atproto.repo.deleteRecord",
             {"repo": acct._did, "collection": "app.bsky.feed.post", "rkey": rkey_of(uri)}, auth=token)
        audit({"account": acct.key, "action": "delete", "status": "ok", "uri": uri,
               "why": "selftest cleanup", "idempotency_key": id_key})
        try:
            authed_get("com.atproto.repo.getRecord",
                       {"repo": acct._did or "", "collection": "app.bsky.feed.post",
                        "rkey": rkey_of(uri)}, token)
            step("delete", False, "record still readable after delete")
        except BskyError as exc:
            gone = exc.status == 400
            step("delete", gone, "record gone from repo" if gone else str(exc))
        time.sleep(2)
        lingering = public_call("app.bsky.feed.getPosts", {"uris": [uri]}).get("posts") or []
        print(f"   note: AppView still lists the URI ({'yes' if lingering else 'no'}) - "
              "indexing lag, not a publish")

    ok = all(s["ok"] or not s["fatal"] for s in steps)
    warn = sum(1 for s in steps if not s["ok"] and not s["fatal"])
    print(f"\nselftest {'PASS' if ok else 'FAIL'} ({sum(s['ok'] for s in steps)}/{len(steps)} steps, "
          f"{warn} warning{'s' if warn != 1 else ''}) account={acct.key}")
    audit({"account": acct.key, "action": "selftest", "status": "ok" if ok else "error",
           "text": text, "uri": uri, "steps": steps})
    return 0 if ok else 1


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bsky.py", description="Lightsword Bluesky client (AT Protocol).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Docs: docs/bluesky-client.md   Log: logs/bsky-actions.ndjson")
    parser.add_argument("--account", default=os.environ.get("LIGHTSWORD_BSKY_ACCOUNT", "lt"),
                        choices=sorted(ACCOUNTS), help="which credential set to use (default: lt)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--log", default=None, help=f"audit log path (default: {AUDIT_LOG})")
    parser.add_argument("--env-file", default=None, help="override the .env path")
    sub = parser.add_subparsers(dest="command", required=True)

    # --json is accepted before or after the subcommand, because both spellings
    # get typed in practice and argparse only knows the position it was given.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS)

    def add(name, help_text, func, **kwargs):
        p = sub.add_parser(name, help=help_text, parents=[common], **kwargs)
        p.set_defaults(func=func)
        return p

    add("probe", "verify credentials and print the account profile", cmd_probe)

    p = add("post", "publish a post (text, optional images with alt text)", cmd_post)
    p.add_argument("--text", "-t")
    p.add_argument("--text-file")
    p.add_argument("--image", action="append", help="image path; repeat up to 4 times")
    p.add_argument("--alt", action="append", help="alt text, one per --image")
    p.add_argument("--quote", help="AT-URI of a post to quote (embed.record); no images")
    p.add_argument("--lang", action="append", help="language tag, default en")
    p.add_argument("--id-key", help="idempotency key")
    p.add_argument("--asset-id", help="calendar asset id; writes a manifest line")
    p.add_argument("--note")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")

    p = add("reply", "reply to a post, with correct root/parent refs", cmd_reply)
    p.add_argument("--to", required=True, help="AT-URI of the post being replied to")
    p.add_argument("--text", "-t")
    p.add_argument("--text-file")
    p.add_argument("--image", action="append")
    p.add_argument("--alt", action="append")
    p.add_argument("--lang", action="append")
    p.add_argument("--id-key")
    p.add_argument("--note")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")

    p = add("thread", "publish a chain of posts from a JSON file", cmd_thread)
    p.add_argument("--from", dest="source", required=True)
    p.add_argument("--to", help="reply the thread under this URI")
    p.add_argument("--id-key")
    p.add_argument("--note")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")

    p = add("delete", "delete a post by AT-URI", cmd_delete)
    p.add_argument("--uri", required=True)
    p.add_argument("--why")

    p = add("get", "fetch one post from the public AppView", cmd_get)
    p.add_argument("--uri", required=True)

    p = add("replies", "fetch the conversation under a post", cmd_replies)
    p.add_argument("--uri", required=True)
    p.add_argument("--depth", type=int, default=4)

    p = add("mentions", "list mentions, replies and quotes", cmd_mentions)
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--cursor")
    p.add_argument("--unread-only", action="store_true")
    p.add_argument("--mark-seen", action="store_true")

    add("limits", "local rate caps and remaining allowance", cmd_limits)
    sub.choices["limits"].add_argument("--all", action="store_true")

    p = add("arm", "schedule a gate-passed asset from queue/social/", cmd_arm)
    p.add_argument("--asset-id", required=True)
    p.add_argument("--publish-at", required=True, help="ISO timestamp with offset, e.g. 2026-11-13T12:05:00-06:00")

    p = add("schedule", "arm an outbox item, list the outbox, or disarm one", cmd_schedule)
    p.add_argument("--file")
    p.add_argument("--list", action="store_true")
    p.add_argument("--disarm", metavar="ID")
    p.add_argument("--why", help="reason recorded when disarming")

    p = add("tick", "publish due outbox items (cron entry point)", cmd_tick)
    p.add_argument("--now", help="pretend it is this ISO timestamp")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--allow-expired", action="store_true")

    p = add("selftest", "post a marked test with image+alt, verify, delete", cmd_selftest)
    p.add_argument("--text")
    p.add_argument("--image")
    p.add_argument("--alt")
    p.add_argument("--asset-id")
    p.add_argument("--keep", action="store_true", help="do not delete the test post")

    p = add("profile-get", "read a public profile", cmd_profile_get)
    p.add_argument("--actor", default=None)

    p = add("profile-set", "update bio/avatar/banner/pinned post (merges the existing record)", cmd_profile_set)
    p.add_argument("--description")
    p.add_argument("--display-name")
    p.add_argument("--avatar")
    p.add_argument("--banner")
    p.add_argument("--pin", help="AT-URI of a post to pin on the profile")
    p.add_argument("--unpin", action="store_true", help="remove the pinned post")
    p.add_argument("--dry-run", action="store_true")

    p = add("search", "search posts (authenticated; the public AppView 403s on searchPosts)", cmd_search)
    p.add_argument("--query", "-q", required=True)
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--sort", choices=["latest", "top"], default="latest")
    p.add_argument("--since", help="ISO timestamp lower bound")
    p.add_argument("--until", help="ISO timestamp upper bound")
    p.add_argument("--author", help="restrict to one handle")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.env_file:
        global ENV_FILE
        ENV_FILE = Path(args.env_file)
    args.log = Path(args.log) if args.log else AUDIT_LOG
    args.account_explicit = any(a == "--account" or a.startswith("--account=") for a in (argv or sys.argv[1:]))
    if getattr(args, "actor", None) is None and hasattr(args, "actor"):
        args.actor = ACCOUNTS.get(args.account, ("", "lightsword.bsky.social"))[1]
    try:
        return args.func(args)
    except Refused as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    except BskyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        if isinstance(exc.payload, dict):
            print(json.dumps(exc.payload, indent=2), file=sys.stderr)
        return 1
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    sys.exit(main())