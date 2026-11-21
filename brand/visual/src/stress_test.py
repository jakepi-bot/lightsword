"""Stress test: does the fixed frame survive copy that is far too long?

Renders T02 with a deliberately oversized headline and a long support line,
then asserts the canvas is exact, nothing bleeds into the margins, and the
display type is still present. Run: python3 src/stress_test.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import render as R

BACKGROUND = (11, 14, 22)  # --ink

data = R.load()
asset = next(a for a in data["assets"] if a["id"] == "T02")
fmt = dict(data["formats"]["T02"], slug="stress-test")
asset = {"id": "T02", "vars": dict(
    asset["vars"],
    headline="A deliberately oversized headline to prove the frame holds when "
             "the copy is far longer than the design intends",
    support="And a support paragraph that runs well past two lines, because real "
            "copy arrives long and nobody trims it before asking for a render at "
            "nine in the morning.",
)}

out = R.render(asset, fmt)
print("wrote", out)

from PIL import Image
img = Image.open(out).convert("RGB")
assert img.size == (1200, 1200), img.size

# Nothing may touch the outer margins (96 px on squares).
for side, box in (("left", (0, 0, 90, 1200)), ("right", (1110, 0, 1200, 1200))):
    colours = img.crop(box).getcolors(maxcolors=64) or []
    stray = sum(n for n, c in colours if c != BACKGROUND)
    print(f"{side:5} margin stray pixels: {stray}")
    assert stray == 0, f"content bled into the {side} margin"

# Display type must still be present (not shrunk to nothing / not blank).
bright = sum(n for i, n in enumerate(img.convert("L").histogram()) if i > 200)
print("bright pixels:", bright)
assert bright > 5000, "display type missing"

print("PASS — frame held under overlong copy")
