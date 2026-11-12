"""Dựng khối khách sạn (phỏng theo ảnh mặt tiền) và xuất assets/models/tower.glb.

Chạy: python3 blender/tower.py
Mỗi tầng khối tháp là một vật thể riêng (floor_05 … floor_16) để web bắt được chuột.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Builder, export_glb, mat, reset  # noqa: E402

random.seed(8)
reset()

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "models", "tower.glb")

PH = 4.0          # cao tầng khối đế
FH = 3.5          # cao tầng khối tháp
PODIUM_FLOORS = 4
TOP = 16
Z0 = PODIUM_FLOORS * PH

STONE = mat("stone", (0.78, 0.66, 0.50), 0.85)
STONE_L = mat("stone_light", (0.88, 0.78, 0.62), 0.8)
LEDGE = mat("ledge", (0.62, 0.50, 0.36), 0.8)
WIN_LIT = mat("win_lit", (0.9, 0.75, 0.4), 0.3, emit=(1.0, 0.78, 0.36), strength=2.6)
WIN_DIM = mat("win_dim", (0.10, 0.14, 0.24), 0.15, metal=0.4, emit=(0.25, 0.35, 0.6), strength=0.15)
LATTICE = mat("lattice", (0.42, 0.13, 0.09), 0.6, emit=(0.5, 0.12, 0.06), strength=0.25)
RED = mat("bracket_red", (0.55, 0.13, 0.09), 0.6, emit=(0.6, 0.12, 0.06), strength=0.35)
EAVE = mat("eave", (0.13, 0.10, 0.09), 0.7)
TILE = mat("tile", (0.20, 0.15, 0.13), 0.6)
TILE_WARM = mat("tile_warm", (0.62, 0.30, 0.14), 0.55, emit=(0.8, 0.35, 0.1), strength=0.3)
GOLD_LIT = mat("glow", (1.0, 0.8, 0.45), 0.4, emit=(1.0, 0.72, 0.3), strength=3.2)
GROUND = mat("ground", (0.05, 0.06, 0.09), 0.9)
PLAZA = mat("plaza", (0.30, 0.25, 0.20), 0.8)
CITY = mat("city", (0.10, 0.13, 0.22), 0.9)
CITY_WIN = mat("city_win", (0.9, 0.75, 0.45), 0.4, emit=(1.0, 0.8, 0.45), strength=1.2)
RIVER = mat("river", (0.05, 0.12, 0.26), 0.08, metal=0.6)
TRUNK = mat("trunk", (0.35, 0.27, 0.18), 0.9)
LEAF = mat("leaf", (0.10, 0.28, 0.14), 0.8)

# Ba khối tháp so le, mỗi khối một mái: (tâm x, tâm y, cạnh x, cạnh y, tầng trên cùng)
BAYS = [(-10.5, -1.5, 11.0, 12.0, 14), (-1.5, -4.5, 12.0, 13.0, 15), (7.0, -0.5, 11.0, 12.0, 16)]
CORE = (-2.0, 4.5, 27.0, 9.0, 15)


def window_row(b, cx, cy, sx, sy, zc, lit_ratio=0.82):
    """Cửa sổ đôi trên bốn mặt của một khối."""
    for axis, half, length in (("x", sy / 2, sx), ("y", sx / 2, sy)):
        n = max(2, int((length - 2.6) // 2.3))
        span = length - 3.0
        for i in range(n):
            t = (i + 0.5) / n - 0.5
            for side in (-1, 1):
                m = WIN_LIT if random.random() < lit_ratio else WIN_DIM
                for pane in (-0.45, 0.45):
                    if axis == "x":
                        b.box((cx + t * span + pane, cy + side * (half + 0.03), zc), (0.78, 0.12, 2.1), m)
                    else:
                        b.box((cx + side * (half + 0.03), cy + t * span + pane, zc), (0.12, 0.78, 2.1), m)


def bay_floor(b, bay, z):
    cx, cy, sx, sy, _ = bay
    b.box((cx, cy, z + FH / 2), (sx, sy, FH), STONE)
    b.box((cx, cy, z + 0.14), (sx + 0.5, sy + 0.5, 0.28), LEDGE)
    for dx in (-1, 1):
        for dy in (-1, 1):
            b.box((cx + dx * (sx / 2 - 0.5), cy + dy * (sy / 2 - 0.5), z + FH / 2), (1.5, 1.5, FH), STONE_L)
    window_row(b, cx, cy, sx, sy, z + FH / 2 + 0.2)


def hip_roof(b, cx, cy, sx, sy, z, tile=TILE, over=2.2, h=3.4):
    b.box((cx, cy, z + 0.45), (sx + 0.9, sy + 0.9, 0.9), RED)
    b.box((cx, cy, z + 1.05), (sx + 2 * over + 0.4, sy + 2 * over + 0.4, 0.3), EAVE)
    b.frustum((cx, cy, z + 1.2), (sx + 2 * over, sy + 2 * over), (sx * 0.34, sy * 0.34), h, tile)
    b.box((cx, cy, z + 1.2 + h + 0.2), (sx * 0.36, sy * 0.36, 0.4), EAVE)


# ---------- Khối tháp: mỗi tầng một vật thể ----------
for f in range(PODIUM_FLOORS + 1, TOP + 1):
    b = Builder(f"floor_{f:02d}")
    z = Z0 + (f - PODIUM_FLOORS - 1) * FH
    for bay in BAYS + [CORE]:
        if f <= bay[4]:
            bay_floor(b, bay, z)
    b.finish()

roofs = Builder("roofs")
for bay in BAYS:
    cx, cy, sx, sy, top = bay
    zt = Z0 + (top - PODIUM_FLOORS) * FH
    hip_roof(roofs, cx, cy, sx, sy, zt)
    # Diềm mái phụ, thấp hơn mái chính hai tầng
    zs = zt - 2 * FH
    roofs.box((cx, cy, zs - 0.25), (sx + 1.3, sy + 1.3, 0.5), RED)
    roofs.box((cx, cy, zs + 0.1), (sx + 2.6, sy + 2.6, 0.22), EAVE)
cx, cy, sx, sy, top = CORE
roofs.box((cx, cy, Z0 + (top - PODIUM_FLOORS) * FH + 0.3), (sx + 0.8, sy + 0.8, 0.6), LEDGE)
roofs.finish()

# ---------- Khối đế ----------
PX0, PX1, PY0, PY1 = -18.0, 24.0, -12.5, 11.0
pcx, pcy, psx, psy = (PX0 + PX1) / 2, (PY0 + PY1) / 2, PX1 - PX0, PY1 - PY0
p = Builder("podium")
p.box((pcx, pcy, Z0 / 2), (psx, psy, Z0), STONE)
p.box((pcx, pcy, Z0 + 0.3), (psx + 1.0, psy + 1.0, 0.6), LEDGE)
p.box((pcx, pcy, PH + 0.15), (psx + 0.6, psy + 0.6, 0.3), LEDGE)
n = 9
for i in range(n + 1):
    x = PX0 + i * psx / n
    for y in (PY0 - 0.2, PY1 + 0.2):
        p.box((x, y, Z0 / 2), (1.3, 0.9, Z0), STONE_L)
for i in range(n):
    x = PX0 + (i + 0.5) * psx / n
    w = psx / n - 1.6
    for y in (PY0 - 0.05, PY1 + 0.05):
        p.box((x, y, PH / 2 + 0.2), (w, 0.14, PH - 0.9), WIN_LIT)            # tầng trệt sáng đèn
        p.box((x, y, PH * 2.0), (w, 0.2, PH * 1.5), LATTICE)                 # mảng hoa văn đỏ
        p.box((x, y, PH * 3.5), (w, 0.14, PH * 0.55), WIN_LIT)
for j in range(5):
    y = PY0 + (j + 0.5) * psy / 5
    for x in (PX0 - 0.05, PX1 + 0.05):
        p.box((x, y, PH / 2 + 0.2), (0.14, psy / 5 - 1.6, PH - 0.9), WIN_LIT)
        p.box((x, y, PH * 2.0), (0.2, psy / 5 - 1.6, PH * 1.5), LATTICE)
        p.box((x, y, PH * 3.5), (0.14, psy / 5 - 1.6, PH * 0.55), WIN_LIT)
    for x in (PX0 - 0.2, PX1 + 0.2):
        p.box((x, PY0 + j * psy / 5, Z0 / 2), (0.9, 1.3, Z0), STONE_L)

# Lầu mái trên sân thượng khối đế
p.box((17.0, -1.0, Z0 + 2.2), (11.0, 13.0, 4.4), STONE)
for i in range(4):
    p.box((13.0 + i * 2.7, -7.55, Z0 + 2.3), (1.9, 0.14, 2.8), WIN_LIT)
hip_roof(p, 17.0, -1.0, 11.0, 13.0, Z0 + 4.4, tile=TILE, over=2.0, h=2.6)
hip_roof(p, 17.0, -1.0, 5.0, 6.0, Z0 + 7.6, tile=TILE, over=1.2, h=1.6)

# Sảnh đón xe phía trước, mái ngói hai tầng
ex, ey = 15.0, -19.5
for dx in (-4.5, 4.5):
    for dy in (-3.5, 3.5):
        p.box((ex + dx, ey + dy, 3.0), (0.7, 0.7, 6.0), RED)
p.box((ex, ey, 6.2), (10.5, 8.5, 0.4), GOLD_LIT)
hip_roof(p, ex, ey, 10.0, 8.0, 6.3, tile=TILE_WARM, over=1.8, h=1.8)
hip_roof(p, ex, ey, 5.0, 4.0, 8.9, tile=TILE_WARM, over=1.1, h=1.5)
p.box((ex, (ey + PY0) / 2 + 2.0, 5.6), (7.0, 4.0, 0.3), EAVE)
p.finish()

# ---------- Cảnh quan ----------
s = Builder("site")
s.box((0, 0, -0.5), (900, 900, 1.0), GROUND)
s.box((3, -6, 0.06), (62, 52, 0.12), PLAZA)
s.box((0, 215, 0.05), (900, 110, 0.1), RIVER)          # sông Hương ở phía bắc
for x in range(-16, 9, 4):                              # đèn hắt chân tường
    s.box((x, PY0 - 1.2, 0.2), (0.5, 0.5, 0.25), GOLD_LIT)
for x in list(range(-17, 8, 4)) + [24, 28]:             # hàng cau trước sảnh
    h = random.uniform(8.5, 10.5)
    y = -23.5 + random.uniform(-0.6, 0.6)
    s.cyl((x, y, 0), 0.22, h, TRUNK, r2=0.15, segs=8)
    s.ball((x, y, h + 0.2), 2.3, LEAF, squash=0.42)
    s.ball((x, y, h + 0.9), 1.3, LEAF, squash=0.5)
for _ in range(150):                                    # phố xá xung quanh
    x, y = random.uniform(-330, 330), random.uniform(-330, 150)
    if abs(x) < 52 and -62 < y < 46:
        continue
    if y < -62 and abs(x) < 150:          # để trống phía trước cho máy quay
        continue
    w, d, h = random.uniform(9, 24), random.uniform(9, 24), random.uniform(5, 19)
    if (x * x + y * y) ** 0.5 > 110:      # xa tòa nhà thì thấp, khỏi che máy quay
        h = min(h, 9.0)
    s.box((x, y, h / 2), (w, d, h), CITY)
    for _ in range(int(h // 4)):
        s.box((x + random.uniform(-w / 2 + 1, w / 2 - 1), y - d / 2 - 0.05, random.uniform(2, h - 1)),
              (1.2, 0.1, 0.9), CITY_WIN)
s.finish()

export_glb(OUT)
print("OK", OUT, os.path.getsize(OUT) // 1024, "KB")
