"""Builds supporters.png for the Club Neko supporter wall.

Every entry in supporters.json with a "photo" gets the next cell of an 8 x 8 grid (256 px cells, 2048 x 2048), in
file order, left to right then top to bottom. That order is exactly how the world counts them, so don't reorder by
hand without rebuilding. Photos are centre-cropped to squares; the 8 px border round each picture repeats its edge so
the cells don't bleed into each other when the world shrinks them.

    pip install pillow
    python tools/build_supporter_photos.py
"""
import json
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRID, CELL, PAD = 8, 256, 8

data = json.loads((ROOT / "supporters.json").read_text(encoding="utf-8"))
atlas = Image.new("RGB", (GRID * CELL, GRID * CELL), (51, 31, 61))
k = 0
missing = []
for s in data.get("supporters", []):
    photo = (s.get("photo") or "").strip()
    if not photo:
        continue
    if k >= GRID * GRID:
        print("more than", GRID * GRID, "photos: the rest are left out", file=sys.stderr)
        break
    path = ROOT / "photos" / photo
    if path.exists():
        img = Image.open(path).convert("RGB")
        side = min(img.size)
        left, top = (img.width - side) // 2, (img.height - side) // 2
        img = img.crop((left, top, left + side, top + side)).resize((CELL - 2 * PAD, CELL - 2 * PAD), Image.LANCZOS)
        cell = Image.new("RGB", (CELL, CELL))
        # stretch the picture's edge pixels over the border
        cell.paste(img.resize((CELL, CELL), Image.NEAREST), (0, 0))
        cell.paste(img, (PAD, PAD))
        atlas.paste(cell, ((k % GRID) * CELL, (k // GRID) * CELL))
    else:
        missing.append(photo)
    k += 1

atlas.save(ROOT / "supporters.png", optimize=True)
print("supporters.png:", k, "photo cells")
if missing:
    print("missing in photos/:", ", ".join(missing), file=sys.stderr)
    sys.exit(1)
