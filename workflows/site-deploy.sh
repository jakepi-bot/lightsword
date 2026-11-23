#!/usr/bin/env bash
# Push the Lightsword site from ai-pc to the ai-services origin container.
#
#   workflows/site-deploy.sh              # sync, verify, report
#   workflows/site-deploy.sh --dry-run    # show what would change, change nothing
#
# Source of truth: ~/share/lightsword-site/ (the directory the nightly run
# writes blog pages into). Destination: /srv/lightsword-site/site on
# ai-services, served by the `lightsword-web` container on
# http://100.65.253.95:8081 — cloud Caddy reverse-proxies the public domain
# there.
#
# Exit codes: 0 synced and verified, 1 sync or verification failed.
# This script never publishes anything and never touches the repo.

set -euo pipefail

SRC="${LIGHTSWORD_SITE_SRC:-$HOME/share/lightsword-site}"
DEST_HOST="${LIGHTSWORD_SITE_HOST:-ai-services}"
DEST_DIR="${LIGHTSWORD_SITE_DEST:-/srv/lightsword-site/site}"
ORIGIN="${LIGHTSWORD_SITE_ORIGIN:-http://100.65.253.95:8081}"
DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

log() { printf '%s %s\n' "$(date -u +%H:%M:%SZ)" "$*"; }
die() { printf 'ERROR %s\n' "$*" >&2; exit 1; }

[[ -d "$SRC" ]] || die "source directory missing: $SRC"
[[ -f "$SRC/index.html" ]] || die "no index.html in $SRC — refusing to deploy an empty site"

# Infra files live beside the content but must never reach the docroot.
EXCLUDES=(
  --exclude=README.md
  --exclude=Caddyfile.example
  --exclude=ANALYTICS.stub.html
  --exclude=.git
  --exclude='*.swp'
  --exclude='.DS_Store'
)

if (( DRY_RUN )); then
  log "dry run: $SRC -> $DEST_HOST:$DEST_DIR"
  rsync -ani --delete "${EXCLUDES[@]}" "$SRC/" "$DEST_HOST:$DEST_DIR/"
  exit 0
fi

log "syncing $SRC -> $DEST_HOST:$DEST_DIR"
rsync -a --delete --stats "${EXCLUDES[@]}" "$SRC/" "$DEST_HOST:$DEST_DIR/" \
  | awk -F': ' '/Number of regular files transferred|Number of deleted files|Total transferred file size/ {print "  " $0}'

# Size alone does not prove the bytes: compare the two files that must never
# disagree with the origin's 200 for the page that matters.
LOCAL_SHA=$(sha256sum "$SRC/index.html" | cut -d' ' -f1)
REMOTE_SHA=$(ssh "$DEST_HOST" "sha256sum $DEST_DIR/index.html" | cut -d' ' -f1)
[[ "$LOCAL_SHA" == "$REMOTE_SHA" ]] || die "index.html differs after sync (local $LOCAL_SHA, origin $REMOTE_SHA)"
log "index.html sha256 matches ($LOCAL_SHA)"

CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$ORIGIN/" || true)
[[ "$CODE" == "200" ]] || die "origin $ORIGIN/ returned $CODE after sync"
log "origin $ORIGIN/ -> 200"

# Every real page the source carries must be reachable at the origin, or the
# nightly run's social link points at a 404. Three paths are deliberately not
# 200 and are checked for the behaviour they are meant to have instead:
#   404.html             served only as an internal error page -> 404 is correct
#   ANALYTICS.stub.html  excluded from the docroot on purpose -> 404 is correct
#   downloads/index.html retired, must redirect home -> 301 is correct
BLOG_FAIL=0
while IFS= read -r page; do
  rel="${page#"$SRC"/}"
  case "$rel" in
    404.html|ANALYTICS.stub.html|Caddyfile.example|README.md) continue ;;
    downloads/index.html) want="301" ;;
    *)                    want="200" ;;
  esac
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$ORIGIN/$rel" || true)
  if [[ "$code" != "$want" ]]; then
    printf 'WARNING %s -> %s at origin (expected %s)\n' "$rel" "$code" "$want" >&2
    BLOG_FAIL=$((BLOG_FAIL + 1))
  fi
done < <(find "$SRC" -name '*.html' -type f)

if (( BLOG_FAIL > 0 )); then
  log "synced, but $BLOG_FAIL HTML page(s) do not answer as expected at the origin"
  exit 1
fi

log "done: every HTML page under $SRC answers as expected at $ORIGIN"
