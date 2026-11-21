#!/usr/bin/env python3
"""Render the Lightsword public brand set: avatar, banner, mark, favicons, OG.

    python3 render.py            # every asset
    python3 render.py --check    # verify existing exports, no render

The mark is a vertical sword drawn as a beam: a bright core with a periwinkle
edge, a narrow crossguard and a pommel. Vertical because a 40px circular avatar
crop wastes a diagonal; the silhouette has to survive at avatar size.

No hand-edited PNGs. Edit MARK or a template here and re-run.
"""
import subprocess
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXP = ROOT / "exports"
BUILD = ROOT / "build"
CHROME = (
    shutil.which("chromium")
    or shutil.which("chromium-browser")
    or shutil.which("google-chrome")
)

INK = "#0B0E14"
PAPER = "#F2F5FA"
DIM = "#9AA6BF"
BEAM = "#5B7FFF"
EDGE = "#8FA9FF"

# viewBox 0 0 256 256. Blade 36 wide at the base, 104 across the guard.
MARK = """
<g>
  <defs>
    <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.55" stop-color="#DCE6FF"/>
      <stop offset="1" stop-color="#8FA9FF"/>
    </linearGradient>
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="7" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g filter="url(#glow)">
    <!-- blade: tip, straight edges, flat base -->
    <path d="M128 22 L147 64 L147 158 L109 158 L109 64 Z" fill="url(#beam)"/>
    <!-- fuller: the light core -->
    <path d="M128 38 L135 68 L135 150 L121 150 L121 68 Z" fill="#FFFFFF"/>
    <!-- crossguard -->
    <rect x="74" y="158" width="108" height="17" rx="7" fill="#E7ECF5"/>
    <!-- grip -->
    <rect x="117" y="175" width="22" height="46" rx="6" fill="#39415A"/>
    <!-- pommel -->
    <circle cx="128" cy="231" r="14" fill="#5B7FFF"/>
  </g>
</g>
"""

TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:{w}px; height:{h}px; overflow:hidden; background:{bg}; }}
  body {{ font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          color:{paper}; -webkit-font-smoothing:antialiased; }}
  .field {{ position:absolute; inset:0; background:
      radial-gradient(120% 90% at 72% 20%, rgba(91,127,255,.20), rgba(91,127,255,0) 62%),
      radial-gradient(90% 70% at 8% 100%, rgba(91,127,255,.10), rgba(91,127,255,0) 60%),
      {bg}; }}
  .grain {{ position:absolute; inset:0; opacity:.5; background:
      repeating-linear-gradient(115deg, rgba(255,255,255,.022) 0 1px, transparent 1px 9px); }}
  .mark {{ position:absolute; {mark_box} }}
  .mark svg {{ width:100%; height:100%; display:block; }}
  .word {{{word_box}}}
  .word .name {{ font-size:{name_px}px; font-weight:700; letter-spacing:-0.035em; line-height:.95; }}
  .word .rule {{ height:6px; width:{rule_w}px; background:{beam}; border-radius:3px; margin:{rule_gap}px 0; margin-left:auto; }}
  .word .tag {{ font-size:{tag_px}px; font-weight:400; color:{dim}; letter-spacing:-0.01em; line-height:1.25; }}
  .corner {{ position:absolute; right:{pad}px; bottom:{pad}px; font-size:{tiny_px}px;
             color:{dim}; letter-spacing:.16em; text-transform:uppercase; }}
</style></head>
<body>
  <div class="field"></div><div class="grain"></div>
  <div class="mark"><svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">{mark}</svg></div>
  <div class="word">
    <div class="name">Lightsword</div>
    <div class="rule"></div>
    <div class="tag">{tag}</div>
  </div>
  {corner}
</body></html>
"""


def shoot(html, out, w, h):
    out.parent.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(exist_ok=True)
    page = BUILD / f"{out.stem}-{w}x{h}.html"
    page.write_text(html)
    cmd = [
        CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        "--force-color-profile=srgb", "--disable-lcd-text",
        f"--default-background-color={INK.lstrip('#')}ff",
        f"--window-size={w},{h}", "--virtual-time-budget=3000",
        f"--screenshot={out}", page.as_uri(),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if proc.returncode != 0 or not out.exists():
        raise SystemExit(f"render failed for {out.name}: {proc.stderr[-600:]}")
    print(f"  ok  {out.name:<38} {w}x{h}  {out.stat().st_size // 1024} KB")
    return out


def avatar():
    w = h = 1000
    html = TEMPLATE.format(
        w=w, h=h, bg=INK, paper=PAPER, dim=DIM, beam=BEAM, mark=MARK,
        mark_box="left:50%; top:50%; width:72%; height:72%; transform:translate(-50%,-52%);",
        word_box="display:none;", name_px=10, tag_px=10, rule_w=10, rule_gap=0,
        pad=40, tiny_px=10, tag="", corner="",
    )
    return shoot(html, EXP / "lightsword-avatar-1000x1000.png", w, h)


def banner():
    w, h = 3000, 1000
    # Content lives in the right 62%: Bluesky drops the avatar over the
    # bottom-left of the banner, so nothing important may sit there.
    html = TEMPLATE.format(
        w=w, h=h, bg=INK, paper=PAPER, dim=DIM, beam=BEAM, mark=MARK,
        mark_box="right:170px; top:50%; width:520px; height:520px; transform:translateY(-50%);",
        word_box="position:absolute; right:770px; top:50%; transform:translateY(-50%); text-align:right; width:1700px;",
        name_px=250, tag_px=70, rule_w=430, rule_gap=34,
        pad=64, tiny_px=26, tag="Clear marketing for small product teams", corner="",
    )
    png = shoot(html, EXP / "lightsword-banner-bluesky-3000x1000.png", w, h)
    # Bluesky rejects a blob over 1,000,000 bytes. The gradient field compresses
    # far better as JPEG; keep both so the PNG master stays lossless.
    from PIL import Image
    jpg = EXP / "lightsword-banner-bluesky-3000x1000.jpg"
    Image.open(png).convert("RGB").save(jpg, quality=88, optimize=True, progressive=True)
    print(f"  ok  {jpg.name:<38} {w}x{h}  {jpg.stat().st_size // 1024} KB")
    return jpg


def og():
    w, h = 1200, 630
    html = TEMPLATE.format(
        w=w, h=h, bg=INK, paper=PAPER, dim=DIM, beam=BEAM, mark=MARK,
        mark_box="right:46px; top:50%; width:250px; height:250px; transform:translateY(-50%);",
        word_box="position:absolute; left:64px; top:50%; transform:translateY(-50%); width:760px;",
        name_px=104, tag_px=31, rule_w=190, rule_gap=18,
        pad=34, tiny_px=13, tag="Every claim links a source", corner="lightsword.org",
    )
    return shoot(html, EXP / "lightsword-og-1200x630.png", w, h)


def mark_only():
    w = h = 512
    html = f"""<!DOCTYPE html><html><head><style>
      *{{margin:0;padding:0}} html,body{{width:{w}px;height:{h}px;overflow:hidden}}
      body{{background:{INK}}} svg{{width:100%;height:100%;display:block}}
    </style></head><body>
    <svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">{MARK}</svg>
    </body></html>"""
    return shoot(html, EXP / "lightsword-mark-512x512.png", w, h)


def favicons():
    from PIL import Image
    src = Image.open(EXP / "lightsword-mark-512x512.png").convert("RGBA")
    out = []
    for size in (32, 16):
        p = EXP / f"lightsword-favicon-{size}x{size}.png"
        src.resize((size, size), Image.LANCZOS).save(p)
        print(f"  ok  {p.name:<38} {size}x{size}")
        out.append(p)
    return out


def check():
    from PIL import Image
    ok = True
    for name, want in {
        "lightsword-avatar-1000x1000.png": (1000, 1000),
        "lightsword-banner-bluesky-3000x1000.png": (3000, 1000),
        "lightsword-og-1200x630.png": (1200, 630),
        "lightsword-mark-512x512.png": (512, 512),
        "lightsword-favicon-32x32.png": (32, 32),
        "lightsword-favicon-16x16.png": (16, 16),
    }.items():
        p = EXP / name
        if not p.exists():
            print(f"  MISSING {name}")
            ok = False
            continue
        img = Image.open(p)
        size_ok = img.size == want
        print(f"  {'OK  ' if size_ok else 'BAD '} {name:<38} {img.size[0]}x{img.size[1]}")
        ok = ok and size_ok
    return ok


def main(argv):
    if "--check" in argv:
        ok = check()
        print("PASS" if ok else "FAIL")
        return 0 if ok else 1
    if not CHROME:
        raise SystemExit("no chromium on PATH")
    avatar()
    banner()
    og()
    mark_only()
    favicons()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
