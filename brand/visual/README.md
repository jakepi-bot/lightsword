# Lightsword — visual direction v1.0

**Status:** working system, 2026-11-08. Supersedes nothing; it finishes what
`brand/brand-identity.md` v1.0 started (same mark, same palette, same voice) and
adds the pieces social actually needs: a type pairing that renders the same on
every machine, a fixed layout grid, six formats, and a one-command build.

**Built for:** the Lightsword profile posting without a designer in the loop.

---

## 1. The idea

The mark is a straight line through the noise. Every asset is that sentence
drawn once: a dark field, a single beam, one message, and the smallest possible
amount of metadata. Nothing is decorated. Nothing is stock. The confidence comes
from the crop and the type size, not from effects.

Two consequences you can see in every file:

- **One accent per asset.** Blade blue appears twice at most (the beam rule and
  one end-cap). Never three times, never as a gradient, never as a glow.
- **The message owns the frame.** Type is set large and left-aligned on a fixed
  baseline; if copy is long the type shrinks, the layout never moves.

## 2. Palette

Continuity with the live site — these are the tokens already in `brand.css`.
Nothing here is a new colour.

| Token | Hex | Use | Contrast on ink |
|---|---|---|---|
| `--ink` | `#0B0E16` | Every field, every page background | — |
| `--surface` | `#141926` | Cards, mark badge | — |
| `--line` | `#262C3A` | Hairlines, borders, grid texture | 1.38 — decoration only, never text |
| `--text` | `#D7DDE8` | Body, secondary lines | 14.1:1 |
| `--text-hi` | `#E9EEF7` | Display type only | 16.6:1 |
| `--muted` | `#8A93A3` | Captions, labels, footer. Never carries a claim | 6.2:1 |
| `--blade` | `#5B7FFF` | The beam, the one accent | 5.4:1 |
| `--signal` | `#3ECF8E` | "Verified" dots, only next to a date and a source | 9.7:1 |
| `--client` | `#E94560` | Client accent. Client-work cards only, twice max | 5.0:1 |

Every text colour passes WCAG AA at 4.5:1 on both `--ink` and `--surface`.
`--line` is the one value that must never be used for text.

**Client separation.** flambeee's palette is navy and flame; ours is ink and
blade. A client-work card puts the client's two colours inside our chrome and
signs the bottom with our mark — that is the only place a second palette is
allowed, and it is what stops the account reading as one undifferentiated brand.

## 3. Type

| Role | Face | Why |
|---|---|---|
| Display + body | **Inter** (variable, 100–900, bundled) | Plain, high x-height, reads at 30 % scale in a feed. Tracks tight at display sizes without looking styled. |
| Labels, dates, ids, numbers | **JetBrains Mono** 500–700 (bundled) | Makes metadata look like data, not marketing. Tells a reader instantly "this part is a receipt". |

Sizes are fixed in `tokens.css`; do not hand-set a size in a template.

| Token | Size | Used for |
|---|---|---|
| `--t-kicker` | 25 px | Eyebrows, uppercase, `0.18em` tracking |
| `--t-meta` | 22 px | Footer, attribution, proof lines |
| `--t-lede` | 34 px | Supporting paragraph, max two lines |
| `--t-d1` | 80 px | Quote / insight |
| `--t-d2` | 92 px | Announcement headline |
| `--t-d3` | 64 px | Thread cover, client headline, OG title |
| `--t-num` | 232 px | Metric numeral |

**Why fonts are bundled here but not on the site.** The site keeps the
zero-fetch system stack: 3.6 KB total, no webfont, nothing to block render.
These exports bundle two OFL files (~180 KB, local only) so the same copy
produces a byte-identical PNG on any machine that runs `render.py`. Different
medium, different trade-off, same skeleton.

## 4. Layout

A 1200 px canvas, **96 px margins, 6 columns of 148 px with 24 px gutters**
(6 × 148 + 5 × 24 = 1008 = 1200 − 192). The grid texture, when present, is on a
96 px pitch, so its rules land exactly on the content edges at x = 96 and
x = 1104. That is why the texture looks measured rather than decorative.

Vertical rules:

- Header band is 56 px at y = 96. Footer rule sits at y = 1046 on squares,
  y = 558 on 630-tall formats.
- The message block is **vertically centred** between header and footer by auto
  margins, and its height is **fixed per format**. A three-line quote and a
  four-line quote therefore start on the same optical line — a profile grid of
  mixed posts stays aligned without anyone adjusting anything.
- `fit.js` shrinks display type 1 px at a time until it fits the frame. Copy
  length changes the type size, never the composition. Floors: 44–54 px.

## 5. Imagery

There is no photography in this system, and there should not be. Stock people
at laptops would contradict every sentence in `brand-voice.md`.

The image policy is **evidence imagery**:

1. **Real screenshots of shipped things**, cropped tight, 1 px `--line` frame,
   24 px inset, no device mockup, no shadow, no perspective, no blur.
2. **Drawn diagrams** in CSS/SVG using only the palette above.
3. Nothing that shows an unshipped state, a fake metric, or a redacted bar
   chart. If it cannot be verified, it is not an image.

Screenshots are free to make and impossible to fake, which is precisely the
brand.

## 6. Formats

All six render from `templates/` at exact pixel size. `render.py --check`
verifies dimensions and non-blankness on every run.

| ID | File | Size | When to use |
|---|---|---|---|
| T01 | `quote-insight-1200x1200.png` | 1200² | One idea, attributed. The workhorse. |
| T02 | `announcement-1200x1200.png` | 1200² | Something shipped, changed, or was corrected. Kicker = verb. |
| T03 | `thread-cover-1200x630.png` | 1200×630 | First post of a thread. Header ticks show position. |
| T04 | `client-work-flambeee-1200x1200.png` | 1200² | Proof of work for the client. Client palette, our signature. |
| T05 | `og-link-card-1200x630.png` | 1200×630 | Site Open Graph / Bluesky link card. |
| T06 | `metric-1200x1200.png` | 1200² | One number, its source, its date. The most on-brand format we have. |

**Format rules.** T03 and T05 carry the grid texture; the squares stay flat and
quiet. Every asset gets a `T0n` id in the footer so a post can be traced back to
its template, and a date so a reader can check it.

## 7. Making a post (2 minutes)

```bash
cd ~/.hermes/lightsword/lightsword/brand/visual
# 1. edit copy in content.json (one object per asset)
python3 render.py T01              # render one
python3 render.py                  # render all + refresh alt-text.md + manifest.json
python3 render.py --check          # verify sizes/non-blank only
python3 src/stress_test.py         # prove the frame survives overlong copy
```

Paste the matching line from `exports/alt-text.md` into the Bluesky image
description field. Alt text is not optional — `brand-voice.md` requires it and
`render.py` generates it from the same copy, so they cannot drift.

To add a format: copy a template, set a fixed `.fitbox` height, add an entry to
`formats` and `assets` in `content.json`. Keep the 96 px margins and the
56 px header band or it will not sit in the profile grid.

## 8. Hard rules

1. One accent per asset; blade blue at most twice; `--signal` only beside a date and a source.
2. Never put a client's logo on a Lightsword asset. Client name in type is fine (permission granted 2026-11-07); the flame mark is not.
3. **T04 is gated:** flambeee palette + name in a portfolio context needs Jake's co-branding sign-off (due 2026-11-14). Build it, do not publish it.
4. No gradient, shadow, outline, or rotation on the wordmark or the mark.
5. No number without a source and a date. If the number is unverified, the asset is not finished.
6. Never edit an exported PNG. Edit `content.json` or the template, re-render.
7. Sentence case everywhere except mono labels, which are uppercase by design.

## 9. Files

```
brand/visual/
  tokens.css        palette, type scale, grid — the single source of truth
  base.css          shared frame: field, header, footer, components
  fit.js            shrinks display type to fit its fixed frame
  templates/        six editable HTML templates (copy is {{tokens}})
  content.json      all copy + alt text, one object per asset
  src/mark.html     the mark, single source
  fonts/            Inter + JetBrains Mono, OFL, local only
  render.py         chromium → exact-size PNG + manifest + alt-text.md
  exports/          shipped PNGs and alt-text.md
  build/            rendered HTML (throwaway)
```
