# Lightsword brand set

The company's own public mark, so `@lightsword.bsky.social` and `lightsword.org`
read as a brand rather than a placeholder.

## Why this exists

The previous mark was a diagonal blade that read as a **nail** at avatar size,
and the banner put the sword in the bottom-left, exactly where Bluesky draws the
profile avatar. The company whose product is public image had a weak one.

## The mark

A vertical sword drawn as a beam: white core, periwinkle edge, narrow guard,
blue pommel. Vertical on purpose. A 40px avatar is a circle crop, and a diagonal
loses most of its length to the corners; a vertical silhouette keeps a full
blade, a clear crossbar and a distinct pommel. Verified legible at 40x40.

Palette: field `#0B0E14`, beam `#5B7FFF`, edge `#8FA9FF`, paper `#F2F5FA`,
dim `#9AA6BF`. Type is the system sans stack, same as the site.

## Files

| File | Size | Destination |
|---|---|---|
| `exports/lightsword-avatar-1000x1000.png` | 1000x1000 | Bluesky avatar |
| `exports/lightsword-banner-bluesky-3000x1000.png` | 3000x1000 | Bluesky banner master (lossless) |
| `exports/lightsword-banner-bluesky-3000x1000.jpg` | 3000x1000, 145 KB | Bluesky upload (blob cap is 1,000,000 bytes) |
| `exports/lightsword-og-1200x630.png` | 1200x630 | `lightsword.org/assets/og-link-card-1200x630.png` |
| `exports/lightsword-mark-512x512.png` | 512x512 | master for favicons and app icon |
| `exports/lightsword-favicon-32x32.png` | 32x32 | `lightsword.org/favicon` fallback |
| `exports/lightsword-favicon-16x16.png` | 16x16 | legacy favicon |
| `favicon.svg` | vector | `lightsword.org/favicon.svg` (committed copy of the site file) |

## Banner safe zone

Bluesky overlays the avatar on the bottom-left of the banner. All banner content
sits in the right 62%. Nothing important is inside the left third, so the layout
survives both desktop and mobile crops.

## Rebuild

```bash
python3 render.py           # every asset
python3 render.py --check   # size check only
```

`render.py` drives headless Chromium, same as `brand/flambeee-assets/render.py`.
Never hand-edit an export; edit the template and re-run.

## Rules kept

- Client artwork is not used here. flambeee's flame mark belongs to flambeee.
- No hype words, no taglines that make a claim we cannot source. "Clear
  marketing for small product teams" is the site's existing line.
- The site's header, 404 page and favicon use the same geometry as the avatar,
  so the mark is identical everywhere it appears.
