# Lightsword.org — refresh spec v1.0

**Date:** 2026-11-08 · **Author:** designer · **Inputs:** `reports/audit/2026-11-08-baseline.md` (13 ranked defects, W1–W13), `brand/brand-voice.md`, `brand/brand-identity.md`, `brand/visual/README.md`
**Deploy:** edit `~/share/lightsword-site/` on ai-pc. A cloud-host cron sync publishes it; there is no git push to live (`plans/scope-flambeee.md` §6).
**Scope:** copy, section order, and the fix order. This is the spec, not the patch. Every string below is final and can be pasted without editing.

---

## 1. What is actually wrong

The audit says the value proposition is clear and the performance is excellent (3.6 KB, 149 ms, no JS). Three things are not.

1. **The H1 is the company name.** The most valuable line on the page says "Lightsword" — a word the visitor already sees in the tab, the nav, and the mark. The promise is sitting underneath it in 16 px grey.
2. **There is no primary action.** The only path is an inline "Reply on Bluesky" link inside the third card. A stranger has to read the whole page, leave, open an app, and find the account.
3. **One sentence on the page is no longer true.** "Nothing auto-publishes" / "every asset passes one human gate" contradicts `AGENTS.md` hard rule 1 (Phase 2 is autonomous after a gate pass plus Strategist adjudication). A shop that sells honesty cannot host a factual contradiction on its sales page.

Fix those three and the site is credible. The other ten issues are craft.

## 2. Above the fold — final copy

| Slot | Final text | Notes |
|---|---|---|
| Nav | `Services` `How it works` `Contact` | Anchors on one page. `Downloads` goes; `Blog` returns with A00. |
| H1 | **Clear marketing for small product teams.** | Keep the earned positioning. It is the one line a stranger can repeat back. |
| Subhead | **We write the posts, pages, and proposals that explain what you built. Every claim links a source, or it does not ship.** | Names the deliverable and the standard. 118 chars. |
| Primary CTA | **Send one paragraph** | Button. Concrete, low-commitment, no "Let's talk". |
| CTA sub-line | **Tell us what you shipped. We answer on Bluesky.** | Says exactly what happens after the click. |
| Proof line | **First client: flambeee. Eight games and six apps, free in the browser.** | Real, verifiable, and names the client (permission granted 2026-11-07). |

CTA target today: `https://bsky.app/profile/lightsword.bsky.social`.
When `lightsword.org` has an MX record, swap the `href` to `mailto:hello@lightsword.org` and the sub-line to "Tell us what you shipped. We reply within one business day." Nothing else changes. **One CTA per page — do not add a second button.**

```html
<header class="site-head">
  <a class="lockup" href="/" aria-label="Lightsword home">
    <svg class="mark" width="40" height="40" viewBox="0 0 256 256" aria-hidden="true">…</svg>
    <span class="wordmark">Lightsword</span>
  </a>
  <nav aria-label="Primary">
    <a href="#services">Services</a>
    <a href="#how">How it works</a>
    <a href="#contact">Contact</a>
  </nav>
</header>

<section class="hero">
  <h1>Clear marketing for small product teams.</h1>
  <p class="lede">We write the posts, pages, and proposals that explain what you built.
     Every claim links a source, or it does not ship.</p>
  <p class="cta-row">
    <a class="btn" href="https://bsky.app/profile/lightsword.bsky.social">Send one paragraph</a>
  </p>
  <p class="cta-note">Tell us what you shipped. We answer on Bluesky.</p>
  <p class="proof">First client: flambeee. Eight games and six apps, free in the browser.</p>
</section>
```

## 3. Section order

| # | Section | Job | Ship when |
|---|---|---|---|
| 1 | Hero | State the promise, give one action | P0 |
| 2 | `#services` What we make | Replace three vague cards with three concrete deliverables | P0 |
| 3 | `#how` How it works | Four steps. Answers "what happens if I click" without a call | P0 |
| 4 | `#record` The record | Proof of habit: dated log of what shipped | With A00 (2026-11-09) |
| 5 | `#contact` Start with one paragraph | Repeat the CTA, state how the shop runs | P0 |
| 6 | Footer | Close the loop: who runs this, what is not claimed, when it changed | P0 |

Ordering rationale: promise → what you get → what happens next → proof → ask. The record sits fourth on purpose: it is evidence, and evidence belongs after the reader knows what it is evidence *of*. Nothing sits above the hero — no logo bar, no carousel, no newsletter popup.

## 4. Copy deck (final)

### 4.1 `#services` — What we make

> **What we make**
>
> **Posts.** A fixed weekly cadence on the same days. Each post makes one point and links its source.
>
> **Pages.** Homepages, release notes, pricing lines. Short enough that someone finishes reading.
>
> **Proposals.** One page: what we will do, what it costs, how you check the work.

Why these three: they are the three things the shop actually produces, they match `copy-blocks.md` services 1:1, and each one ends in something the reader can hold. "Fixed weekly cadence" replaces a specific number because the 3/week amendment is still open (due 2026-11-12) — do not put a cadence number on the page until it is settled.

### 4.2 `#how` — How it works

> **How it works**
>
> **1. You send one paragraph about what you shipped.** No brief, no call, no deck.
>
> **2. We write a draft and link every claim.** If we cannot source a line, it does not go in.
>
> **3. It goes out on schedule.** Drafts and checks are logged in the public repo.
>
> **4. We log what happened every Friday.** What worked stays. What did not gets cut.

### 4.3 `#record` — The record *(ships with A00)*

> **The record**
>
> Every asset we publish is logged with its date and what changed. No highlight reel. If a post did nothing, it says so.
>
> [Read the notes →](/blog/)

### 4.4 `#contact` — Start with one paragraph

> **Start with one paragraph**
>
> Tell us what you made and who it is for. If we are not the right shop for it, we will say so in the first reply.
>
> **[Send one paragraph]** → Bluesky
>
> Lightsword is AI-staffed. A bot drafts every asset and checks it against a written gate before publishing. When a check fails, the Strategist decides and logs it. The rules are public: `github.com/jakepi-bot/lightsword`.

This paragraph is the W2 fix. It is accurate against `AGENTS.md` hard rule 1 and 3 (the repo is public, verified 200 today), and it turns the company's strangest property — it is run by a bot — into the reason to trust it rather than something to hide.

### 4.5 Footer

> Lightsword · lightsword.org
> AI-staffed. First client: flambeee. No client results are published here yet.
> [Bluesky](https://bsky.app/profile/lightsword.bsky.social) · [GitHub](https://github.com/jakepi-bot/lightsword) · Last updated 2026-11-08

Drop "First client: a small web-games studio." Naming permission exists; the anonymous version now costs more than it protects.

### 4.6 Head metadata

```html
<title>Lightsword — clear marketing for small product teams</title>
<meta name="description" content="Short posts, pages, and proposals for small product teams. Every claim links a source. First client: flambeee.">
<link rel="canonical" href="https://www.lightsword.org/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lightsword">
<meta property="og:title" content="Clear marketing for small product teams.">
<meta property="og:description" content="Short posts, pages, and proposals. Every claim links a source.">
<meta property="og:url" content="https://www.lightsword.org/">
<meta property="og:image" content="https://www.lightsword.org/assets/og-link-card-1200x630.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Lightsword link card. Title: Clear marketing for small product teams.">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

The OG image already exists: `brand/visual/exports/og-link-card-1200x630.png`. Copy it to `~/share/lightsword-site/assets/` — do not re-cut it.

### 4.7 404 page

> **That page is not here.**
> The link may be old, or we may have retired it.
> [Start at the homepage](/)

0-byte 404s are the cheapest credibility leak on the site: every mistyped URL currently renders a blank page.

## 5. Prioritized fix list

Ordered by trust risk × cost. P0 is one commit and should land together, because the copy in §4 depends on the 404, favicon, and OG existing.

### P0 — ship now (one commit)

| # | Audit id | Fix | Why this order | Effort |
|---|---|---|---|---|
| 1 | W2 | Replace the Services and Contact copy with §4.1 and §4.4 | The only *false* statement on the site. It is also the one a client is most likely to check, because the page brags about honesty. Trust debt compounds; a correction posted later costs more than the sentence ever earned. | 20 min |
| 2 | W3 | Add the hero CTA and the `#contact` repeat (§2, §4.4) | Zero primary action is the largest commercial defect. Everything else on this list is polish around a page that currently asks for nothing. | 45 min |
| 3 | W1, W6, W13 | **Retire `/downloads/`**: remove it from nav and sitemap, add a 301 to `/` | 7 dead links, a page with no logo and no nav, and a top-level nav item that has nothing to do with the offer. Retiring is a 10-minute change; restoring means copying 7 binaries and maintaining a second product line on a marketing site. If Jake wants the builds public, they belong on the games' own surface, not here. | 15 min |
| 4 | W7 | Add the head block from §4.6 + copy the OG image | Every share of the site currently renders as bare text while a finished 1200×630 card sits unused in `brand/visual/exports/`. Cheapest visible upgrade on the list. | 20 min |
| 5 | W10 | Branded 404 (§4.7) | Finishes the trust story: the site stops dying silently on a typo. Also catches `/contact/`, `/services/`, `/work/` 404s, which the new nav no longer points at. | 25 min |
| 6 | W9 | Favicon: reuse the mark as `favicon.svg` + 180 px PNG | A 404 on every single visit, including the client's. One SVG, already drawn. | 10 min |

### P1 — this week

| # | Audit id | Fix | Why | Effort |
|---|---|---|---|---|
| 7 | W4 | Unlink `/blog/` from nav until A00 publishes, then add `#record` (§4.3) | Six "Pending" cards is worse than no page: it shows the machine stalling. A00 is dated 2026-11-09, so this is a two-day gap, not a rewrite. Ship `#record` in the same commit as A00 so the section is never empty. | 15 min + A00 |
| 8 | W5 | Install the Umami tag on all three pages | Without it, no traffic claim can ever be made and the weekly report has no referrer column. This is the difference between "we shipped posts" and "we know what the posts did". The page already has the comment marking the slot. | 20 min + access |
| 9 | W11 | Nav tap targets to 44 px, logo above nav in DOM | 19 px targets are a real miss on the one device most visitors arrive on. Also fixes the odd mobile read order. | 20 min |

### P2 — next two weeks

| # | Audit id | Fix | Why | Effort |
|---|---|---|---|---|
| 10 | W8 | Apex → `www` 301; canonical on every page | Two self-canonicalizing copies of the same page split whatever authority the site earns. | 20 min (Caddy) |
| 11 | W12 | Enable `encode gzip`/`br`, add `Cache-Control`, HSTS, `X-Content-Type-Options`, `Referrer-Policy` | `Caddyfile.example` already specifies these; live Caddy has drifted from it. 3.6 KB does not need compression, but the headers are free correctness. | 20 min |
| 12 | W13 | Sitemap: drop retired pages, add `lastmod` | Partly resolved by fix 3. `lastmod` matters once `/blog/` carries dated entries. | 10 min |

**Not on the list, deliberately.** No redesign, no new pages, no pricing page, no animations, no cookie banner, no newsletter. The site is 3.6 KB and reads in 149 ms; the fix is hierarchy and honesty, not more surface area.

## 6. Design notes for whoever applies this

Reuse `brand.css` tokens; do not introduce new colours except one interactive tint.

```css
/* additions to brand.css — same tokens, one new state colour */
:root { --blade-hi: #7A96FF; }          /* hover/active only, never text on ink */

.site-head { display: flex; align-items: center; justify-content: space-between;
             gap: 24px; padding: 8px 0 40px; }
.lockup { display: inline-flex; align-items: center; gap: 12px;
          color: var(--text-hi); text-decoration: none; }
.wordmark { font-weight: 600; font-size: 1.05rem; letter-spacing: -.02em; }
nav a { display: inline-flex; align-items: center; min-height: 44px;
        padding: 12px 4px; margin-left: 20px; color: var(--text); }

.hero h1 { font-size: clamp(2rem, 5vw, 2.75rem); line-height: 1.1;
           letter-spacing: -.03em; max-width: 20ch; margin: 0 0 16px; }
.lede { font-size: 1.125rem; line-height: 1.55; color: var(--text);
        max-width: 54ch; margin: 0 0 32px; }
.btn { display: inline-flex; align-items: center; min-height: 52px;
       padding: 0 28px; border-radius: 10px; background: var(--blade);
       color: var(--ink); font-weight: 600; text-decoration: none; }
.btn:hover { background: var(--blade-hi); }
.btn:focus-visible { outline: 2px solid var(--text-hi); outline-offset: 3px; }
.cta-note { color: var(--muted); font-size: .95rem; margin: 12px 0 32px; }
.proof { color: var(--muted); font-size: .9rem; border-top: 1px solid var(--line);
         padding-top: 16px; max-width: 54ch; }
```

Accessibility, already verified against the palette: body 14.1:1, muted 6.2:1, blade 5.4:1, ink-on-blade 5.4:1 — all pass AA. Keep `--line` (#262C3A, 1.38:1) for hairlines only. Every icon-only control needs an `aria-label`. One `h1` per page; do not promote a section heading to `h1`.

**Above-the-fold check:** at 390 px wide and 844 px tall, the H1, subhead, and button must all fit without scrolling. If the button falls below the fold on a phone, cut the proof line — not the CTA.

## 7. Done when

- [ ] `/` contains the H1, subhead, and "Send one paragraph" button from §2, above the fold at 390 × 844.
- [ ] No page contains "nothing auto-publishes" or "every asset passes one human gate".
- [ ] `/downloads/` returns 301 to `/` and appears in no nav and no sitemap.
- [ ] Sharing the URL in a feed renders the card, not bare text.
- [ ] An unknown path returns a branded page with a link home.
- [ ] Tab shows the Lightsword mark, not a default globe.
- [ ] HTML + CSS still under 8 KB gzipped; no JS added.
- [ ] One CTA per page. Count them.

## 8. Open decisions (Jake)

1. **Email.** The CTA ends at Bluesky because `lightsword.org` has no MX record. A mail host + one mailbox turns the CTA into a normal link and the spec's fallback line is already written (§2).
2. **Downloads.** Spec retires `/downloads/`. If the RETRO 4K and TETRINET builds should stay public, they need a home that is not the marketing site's nav.
3. **Analytics access.** Fix 8 needs the Umami tag; the site has the slot and the comment ready.
