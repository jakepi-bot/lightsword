# lightsword.org — where it lives and how it goes live

**Moved 2026-11-23** (Jake directive). The site no longer has a cloud docroot.
It is served by a Docker container on `ai-services`; cloud Caddy is a reverse
proxy and owns only TLS and the public hostname.

## Topology

```
                public                        tailnet only
browser ──► cloud Caddy ──proxy──► ai-services:8081 ──► lightsword-web (nginx:1.27-alpine)
             :443, TLS              100.65.253.95           /srv/lightsword-site/site
             reverse proxy                                  (bind mount, read-only)
                                                                    ▲
                                                                    │ rsync
                                                    ai-pc:~/share/lightsword-site/
                                                        (source of truth, ai-pc)
```

| Piece | Value |
|---|---|
| Origin URL | `http://100.65.253.95:8081` (also `http://ai-services.tailda6202.ts.net:8081`) |
| Container | `lightsword-web`, image `nginx:1.27-alpine`, `restart: unless-stopped` |
| Project dir | `/srv/lightsword-site` on `ai-services` (`docker-compose.yml`, `nginx/default.conf`, `site/`) |
| Docroot | `/srv/lightsword-site/site` |
| Source of truth | `~/share/lightsword-site/` on `ai-pc` — the directory the nightly run writes blog pages into |
| Deploy | `bash workflows/site-deploy.sh` (in this repo) |
| Host access | `ssh ai-services` (root, `~/.ssh/ai-services`) |

The public port is published on the Tailscale address only, matching the other
containers on that host. Nothing about this site listens on the LAN or on the
public internet; the only public door is cloud Caddy.

## Deploying

```bash
cd ~/.hermes/lightsword/lightsword
bash workflows/site-deploy.sh            # sync, verify sha256, check every page
bash workflows/site-deploy.sh --dry-run  # show the diff, change nothing
```

The script fails (exit 1) rather than reporting success when the origin stops
answering or a page does not answer as expected. It is the only supported way
to publish a site change. Do not edit files in `/srv/lightsword-site/site`
directly: the next rsync deletes them.

`README.md`, `Caddyfile.example` and `ANALYTICS.stub.html` sit in the source
directory but are excluded from the docroot.

**The nightly run deploys.** Nightly phase 7 writes a `channel: LT blog` page
into `~/share/lightsword-site/blog/`, links it from `blog/index.html`, adds it to
`sitemap.xml`, then runs `site-deploy.sh`. Before 2026-11-23 that last step did
not exist and the site depended on a manual cloud sync; a blog page could be
written and never served, which is why the 2026-11-22 run armed a link post
against a URL that returned 404.

## Behind cloud Caddy

Caddy needs one block, on the cloud host:

```caddy
lightsword.org {
    redir https://www.lightsword.org{uri} permanent
}

www.lightsword.org {
    reverse_proxy http://100.65.253.95:8081
}
```

The origin owns the behaviour Caddy used to own:

| Rule | Where it lives now |
|---|---|
| `lightsword.org` → `www` | cloud Caddy (it is the only thing that sees the public hostname) |
| `/downloads` and `/downloads/*` → `301 /` | nginx, `location = /downloads` / `location ^~ /downloads/` |
| 404 page (`404.html`) | nginx `error_page 404` |
| gzip, `nosniff`, `Referrer-Policy` | nginx |
| Asset caching (7 days) | nginx |

The origin emits **relative** `Location:` headers (`absolute_redirect off`), so a
redirect resolved by a browser on `https://www.lightsword.org` stays on the
public host instead of pointing at the tailnet IP.

`GET /healthz` returns `200 ok` and is what the container healthcheck and the
front proxy should probe. Do not probe `/` — it is a real page and costs a file
read plus gzip.

## Why a container

It gives the site a sandbox that can grow into a real app without touching the
host: add a service to `docker-compose.yml` on the `web` network with `expose`
(never `ports`), then proxy a path to it from `nginx/default.conf`. The static
container stays a static file server. There are commented examples in both
files, and `/srv/lightsword-site/README.md` repeats them for someone working on
the host.

## Rolling back

Point cloud Caddy's `root` at a synced copy again and
`docker compose -f /srv/lightsword-site/docker-compose.yml down`. Nothing else
depends on the container.

## Open item

`lightsword.org` apex still has an `A` record at `107.152.39.20` from the old
hosting. It does nothing now that the site is behind Caddy on that host, but the
DNS is worth a look when the Caddy block is applied: keep `www` as the canonical
host and let Caddy's apex redirect do the work.
