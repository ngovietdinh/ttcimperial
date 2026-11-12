"""Dựng mặt bằng cắt nóc của bốn hạng phòng và xuất assets/models/room-*.glb + rooms.json.

Chạy: python3 blender/rooms.py
Diện tích lấy theo số liệu khách sạn: Deluxe 36 m², Junior Suite 46 m²,
Imperial Suite 80 m², Grand Presidential Suite 160 m². Bố trí bên trong là phỏng dựng.
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
from kit import Builder, Place, export_glb, reset  # noqa: E402

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "models")
WALL_H = 1.45
T = 0.16


def materials():
    kit.clear_mats()
    m = kit.mat
    return dict(
        wall=m("wall", (0.93, 0.87, 0.74), 0.9),
        wood_a=m("floor_a", (0.30, 0.10, 0.06), 0.35),
        wood_b=m("floor_b", (0.36, 0.13, 0.07), 0.35),
        wood_c=m("floor_c", (0.25, 0.08, 0.05), 0.35),
        base=m("base", (0.10, 0.09, 0.10), 0.8),
        dark=m("dark_wood", (0.11, 0.06, 0.05), 0.4),
        linen=m("linen", (0.96, 0.95, 0.92), 0.9),
        pad=m("headboard", (0.74, 0.70, 0.25), 0.9),
        gold=m("gold", (0.80, 0.62, 0.28), 0.35, metal=0.6),
        curtain=m("curtain", (0.72, 0.52, 0.24), 0.9),
        glass=m("glass", (0.55, 0.75, 0.95), 0.05, alpha=0.28),
        screen=m("screen", (0.02, 0.02, 0.03), 0.2),
        shade=m("lamp_shade", (1.0, 0.92, 0.75), 0.6, emit=(1.0, 0.82, 0.5), strength=3.0),
        sofa=m("sofa", (0.45, 0.27, 0.17), 0.95),
        arm=m("armchair", (0.78, 0.40, 0.14), 0.95),
        rug=m("rug", (0.55, 0.12, 0.09), 1.0),
        rug2=m("rug_border", (0.80, 0.60, 0.25), 1.0),
        tile=m("bath_tile", (0.86, 0.84, 0.80), 0.3),
        white=m("ceramic", (0.97, 0.97, 0.97), 0.15),
        tglass=m("table_glass", (0.85, 0.92, 0.9), 0.05, alpha=0.45),
        leaf=m("leaf", (0.16, 0.36, 0.16), 0.8),
        pot=m("pot", (0.45, 0.30, 0.22), 0.7),
        cream=m("cream_wood", (0.90, 0.83, 0.62), 0.5),
    )


class Room:
    def __init__(self, key, w, d):
        self.key, self.w, self.d = key, w, d
        self.M = materials()
        self.b = Builder(f"room_{key}")
        self.hot = []
        M, b = self.M, self.b
        b.box((w / 2, d / 2, -0.25), (w + 0.5, d + 0.5, 0.3), M["base"])
        rnd = random.Random(3)
        n = int(w / 0.16)
        for i in range(n):                       # ván sàn gỗ
            tone = rnd.choice(["wood_a", "wood_a", "wood_b", "wood_c"])
            b.box(((i + 0.5) * w / n, d / 2, -0.05), (w / n, d, 0.1), M[tone])

    # ----- tường -----
    def wall(self, x0, y0, x1, y1, h=WALL_H, outer=False):
        """Mỗi bức tường có bề dày và chiều cao lệch nhau vài mm, đầu tường chìm vào tường kia,
        để không có hai mặt nào trùng khít (kết xuất sẽ ra vệt đen)."""
        self._nw = getattr(self, "_nw", 0) + 1
        n = self._nw
        horiz = abs(x1 - x0) >= abs(y1 - y0)
        length = abs(x1 - x0) if horiz else abs(y1 - y0)
        if outer:
            t = T + 0.1 + (0.0 if horiz else 0.008)
            length += (T + 0.1) if horiz else T
        else:
            t = T - 0.004 * (n % 9)
            length += T - 0.02
        size = (length, t) if horiz else (t, length)
        hh = h + 0.003 * n
        self.b.box(((x0 + x1) / 2, (y0 + y1) / 2, hh / 2), (*size, hh), self.M["wall"])

    def window(self, x0, y0, x1, y1):
        """Bệ tường thấp + kính + rèm hai bên."""
        M = self.M
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        horiz = abs(x1 - x0) > abs(y1 - y0)
        length = abs(x1 - x0) if horiz else abs(y1 - y0)
        s = (length, T, 0.35) if horiz else (T, length, 0.35)
        self.b.box((cx, cy, 0.175), s, M["wall"])
        g = (length, 0.04, WALL_H - 0.35) if horiz else (0.04, length, WALL_H - 0.35)
        self.b.box((cx, cy, 0.35 + (WALL_H - 0.35) / 2), g, M["glass"])
        inward = 0.2
        for e in (-1, 1):
            if horiz:
                iy = cy - inward if cy > self.d / 2 else cy + inward
                self.b.box((cx + e * (length / 2 - 0.3), iy, WALL_H / 2), (0.55, 0.14, WALL_H), M["curtain"])
            else:
                ix = cx - inward if cx > self.w / 2 else cx + inward
                self.b.box((ix, cy + e * (length / 2 - 0.3), WALL_H / 2), (0.14, 0.55, WALL_H), M["curtain"])

    def shell(self, door, win_n=True, win_e=None, win_w=None):
        """Tường bao: cửa vào ở tường nam (door=(x0,x1)), kính ở tường bắc."""
        w, d = self.w, self.d
        self.wall(0, 0, door[0], 0, outer=True)
        self.wall(door[1], 0, w, 0, outer=True)
        if win_n:
            self.wall(0, d, 0.5, d, outer=True)
            self.wall(w - 0.5, d, w, d, outer=True)
            self.window(0.5, d, w - 0.5, d)
        else:
            self.wall(0, d, w, d, outer=True)
        for x, win in ((0, win_w), (w, win_e)):
            if win:
                self.wall(x, 0, x, win[0], outer=True)
                self.window(x, win[0], x, win[1])
                self.wall(x, win[1], x, d, outer=True)
            else:
                self.wall(x, 0, x, d, outer=True)

    def lattice(self, x, y0, y1):
        """Vách hoa văn thếp vàng hai bên lối mở."""
        M = self.M
        self.b.box((x, (y0 + y1) / 2, WALL_H / 2), (0.08, y1 - y0, WALL_H), M["cream"])
        n = int((y1 - y0) / 0.22)
        for i in range(n):
            self.b.box((x, y0 + (i + 0.5) * (y1 - y0) / n, WALL_H / 2), (0.12, 0.05, WALL_H - 0.1), M["gold"])
        for z in (0.35, 0.75, 1.15):
            self.b.box((x, (y0 + y1) / 2, z), (0.12, y1 - y0, 0.05), M["gold"])

    def spot(self, sid, x, y, z=0.6):
        self.hot.append({"id": sid, "pos": [round(x - self.w / 2, 3), z, round(-(y - self.d / 2), 3)]})

    # ----- đồ nội thất (mặt trước hướng +y cục bộ) -----
    def bed(self, x, y, k, w=1.9, l=2.1):
        M, P = self.M, Place(self.b, x, y, k)
        P.box((0, 0, 0.19), (w + 0.25, l + 0.15, 0.3), M["dark"])
        P.box((0, 0.03, 0.47), (w, l - 0.1, 0.26), M["linen"])
        for px in (-w / 4, w / 4):
            P.box((px, -l / 2 + 0.42, 0.66), (w / 2 - 0.15, 0.45, 0.14), M["linen"])
        P.box((0, -l / 2 - 0.05, 0.62), (w + 0.35, 0.1, 1.24), M["dark"])
        P.box((0, -l / 2 + 0.02, 0.86), (w - 0.1, 0.06, 0.62), M["pad"])
        P.box((0, l / 2 - 0.35, 0.61), (w + 0.02, 0.5, 0.03), M["curtain"])
        for sx in (-1, 1):                          # tủ đầu giường + đèn
            nx = sx * (w / 2 + 0.5)
            P.box((nx, -l / 2 + 0.28, 0.27), (0.52, 0.46, 0.54), M["dark"])
            P.cyl((nx, -l / 2 + 0.28, 0.54), 0.05, 0.2, M["dark"])
            P.cyl((nx, -l / 2 + 0.28, 0.74), 0.2, 0.26, M["shade"], r2=0.11)

    def tv(self, x, y, k, w=1.8):
        M, P = self.M, Place(self.b, x, y, k)
        P.box((0, 0, 0.36), (w, 0.5, 0.72), M["dark"])
        P.box((0, 0, 0.735), (w + 0.04, 0.54, 0.03), M["tglass"])
        P.box((0, 0, 1.12), (1.15, 0.06, 0.66), M["screen"])
        P.box((0, 0, 0.78), (0.4, 0.2, 0.05), M["screen"])

    def tea_set(self, x, y):
        M, b = self.M, self.b
        b.cyl((x, y, 0), 0.07, 0.6, M["dark"])
        b.cyl((x, y, 0.6), 0.42, 0.05, M["dark"])
        b.cyl((x, y, 0.65), 0.07, 0.16, M["white"], r2=0.05)
        b.ball((x, y, 0.9), 0.13, M["leaf"])
        for sx, k in ((-1, 3), (1, 1)):
            P = Place(b, x + sx * 0.95, y, k)
            P.box((0, 0, 0.22), (0.6, 0.58, 0.44), M["dark"])
            P.box((0, 0.02, 0.47), (0.5, 0.48, 0.06), M["curtain"])
            P.box((0, -0.27, 0.72), (0.6, 0.06, 0.56), M["dark"])
            for ax in (-0.29, 0.29):
                P.box((ax, 0, 0.6), (0.05, 0.5, 0.05), M["dark"])

    def desk(self, x, y, k):
        M, P = self.M, Place(self.b, x, y, k)
        P.box((0, 0, 0.72), (1.2, 0.55, 0.06), M["dark"])
        for lx in (-0.52, 0.52):
            P.box((lx, 0, 0.35), (0.08, 0.5, 0.7), M["dark"])
        P.cyl((0.38, -0.05, 0.75), 0.05, 0.22, M["gold"])
        P.cyl((0.38, -0.05, 0.97), 0.15, 0.2, M["shade"], r2=0.09)
        P.box((0, 0.6, 0.23), (0.48, 0.46, 0.46), M["dark"])
        P.box((0, 0.6, 0.48), (0.42, 0.4, 0.05), M["curtain"])
        P.box((0, 0.82, 0.7), (0.48, 0.05, 0.5), M["dark"])

    def wardrobe(self, x, y, k, w=1.6):
        M, P = self.M, Place(self.b, x, y, k)
        P.box((0, 0, WALL_H / 2), (w, 0.6, WALL_H), M["dark"])
        for hx in (-0.06, 0.06):
            P.box((hx, 0.31, 0.8), (0.03, 0.03, 0.3), M["gold"])

    def armchair(self, x, y, k, col="arm"):
        M, P = self.M, Place(self.b, x, y, k)
        P.box((0, 0, 0.22), (0.9, 0.85, 0.36), M[col])
        P.box((0, 0.03, 0.44), (0.66, 0.7, 0.1), M[col])
        P.box((0, -0.34, 0.6), (0.9, 0.2, 0.6), M[col])
        for ax in (-0.37, 0.37):
            P.box((ax, 0.02, 0.5), (0.17, 0.78, 0.3), M[col])
        P.box((0, 0, 0.04), (0.92, 0.87, 0.06), M["gold"])

    def sofa(self, x, y, k, w=2.1):
        M, P = self.M, Place(self.b, x, y, k)
        P.box((0, 0, 0.22), (w, 0.9, 0.36), M["sofa"])
        P.box((0, 0.04, 0.44), (w - 0.4, 0.74, 0.1), M["rug"])
        P.box((0, -0.36, 0.62), (w, 0.2, 0.62), M["sofa"])
        for ax in (-w / 2 + 0.1, w / 2 - 0.1):
            P.box((ax, 0.02, 0.5), (0.2, 0.84, 0.32), M["sofa"])
        P.box((0, 0, 0.04), (w + 0.02, 0.92, 0.06), M["gold"])

    def coffee(self, x, y, k, w=1.3, d=0.7):
        M, P = self.M, Place(self.b, x, y, k)
        for lx in (-w / 2 + 0.08, w / 2 - 0.08):
            for ly in (-d / 2 + 0.08, d / 2 - 0.08):
                P.box((lx, ly, 0.2), (0.08, 0.08, 0.4), M["gold"])
        P.box((0, 0, 0.4), (w, d, 0.05), M["gold"])
        P.box((0, 0, 0.44), (w - 0.1, d - 0.1, 0.03), M["tglass"])
        P.cyl((0.2, 0, 0.46), 0.14, 0.06, M["white"], r2=0.17)
        P.ball((0.2, 0, 0.56), 0.07, M["arm"])

    def rug(self, x, y, sx, sy):
        self.b.box((x, y, 0.012), (sx, sy, 0.02), self.M["rug2"])
        self.b.box((x, y, 0.02), (sx - 0.4, sy - 0.4, 0.02), self.M["rug"])

    def floor_lamp(self, x, y):
        M = self.M
        self.b.cyl((x, y, 0), 0.14, 0.04, M["gold"])
        self.b.cyl((x, y, 0), 0.025, 1.15, M["gold"])
        self.b.cyl((x, y, 1.1), 0.22, 0.3, M["shade"], r2=0.2)

    def plant(self, x, y):
        M = self.M
        self.b.cyl((x, y, 0), 0.2, 0.4, M["pot"], r2=0.26)
        self.b.ball((x, y, 0.85), 0.42, M["leaf"], squash=1.2)

    def dining(self, x, y, k, seats=4):
        M, P = self.M, Place(self.b, x, y, k)
        l = 1.5 if seats == 4 else 2.2
        P.box((0, 0, 0.72), (l, 0.95, 0.06), M["dark"])
        P.box((0, 0, 0.35), (l - 0.5, 0.3, 0.7), M["dark"])
        n = seats // 2
        for i in range(n):
            cx = (i + 0.5) * l / n - l / 2
            for sy in (-1, 1):
                P.box((cx, sy * 0.72, 0.23), (0.46, 0.44, 0.46), M["sofa"])
                P.box((cx, sy * 0.93, 0.68), (0.46, 0.06, 0.5), M["sofa"])
                P.box((cx, sy * 0.93, 0.95), (0.3, 0.07, 0.08), M["gold"])

    def bath(self, x0, y0, x1, y1, tub=False):
        """Phòng tắm trong ô (x0,y0)-(x1,y1): lát gạch, lavabo, bồn cầu, vòi sen hoặc bồn tắm."""
        M, b = self.M, self.b
        b.box(((x0 + x1) / 2, (y0 + y1) / 2, 0.012), (x1 - x0 - T, y1 - y0 - T, 0.02), M["tile"])
        w = x1 - x0
        vx = x0 + 0.2 + min(1.4, w * 0.45) / 2                      # lavabo sát tường nam
        b.box((vx, y0 + 0.38, 0.4), (min(1.4, w * 0.45), 0.55, 0.8), M["dark"])
        b.box((vx, y0 + 0.38, 0.82), (min(1.4, w * 0.45) + 0.04, 0.6, 0.04), M["white"])
        b.cyl((vx, y0 + 0.38, 0.84), 0.2, 0.08, M["white"], r2=0.24)
        b.box((vx + min(1.4, w * 0.45) / 2 + 0.45, y0 + 0.42, 0.2), (0.4, 0.62, 0.4), M["white"])   # bồn cầu
        b.box((vx + min(1.4, w * 0.45) / 2 + 0.45, y0 + 0.2, 0.55), (0.42, 0.18, 0.4), M["white"])
        if tub:
            tx = x1 - 0.55
            b.box((tx, (y0 + y1) / 2 + 0.3, 0.3), (0.85, 1.75, 0.6), M["white"])
            b.box((tx, (y0 + y1) / 2 + 0.3, 0.58), (0.65, 1.5, 0.06), M["glass"])
        else:
            sx, sy = x1 - 0.65, y1 - 0.65
            b.box((sx, sy, 0.03), (1.0, 1.0, 0.06), M["white"])
            b.box((sx - 0.5, sy, WALL_H / 2), (0.03, 1.0, WALL_H), M["glass"])
            b.box((sx, sy - 0.5, WALL_H / 2), (1.0, 0.03, WALL_H), M["glass"])

    def export(self):
        ob = self.b.finish()
        ob.location = (-self.w / 2, -self.d / 2, 0)
        export_glb(os.path.join(OUT_DIR, f"room-{self.key}.glb"))
        return {"w": self.w, "d": self.d, "hotspots": self.hot}


def deluxe():
    reset()
    r = Room("deluxe", 4.5, 8.0)
    r.shell(door=(2.9, 3.8), win_e=(6.2, 7.7))
    r.wall(2.3, 0, 2.3, 1.2); r.wall(2.3, 2.1, 2.3, 2.9); r.wall(0, 2.9, 2.3, 2.9)
    r.bath(0, 0, 2.3, 2.9)
    r.wardrobe(4.1, 1.6, 1, w=1.5)
    r.bed(1.2, 5.1, 3)
    r.tv(4.15, 5.2, 1)
    r.desk(4.1, 3.55, 1)
    r.tea_set(2.25, 7.25)
    r.spot("bedroom", 1.6, 5.1); r.spot("window", 2.25, 7.25); r.spot("bath", 1.15, 1.5)
    return r.export()


def junior():
    reset()
    r = Room("junior", 5.75, 8.0)
    r.shell(door=(3.3, 4.2), win_e=(5.6, 7.7))
    r.wall(2.7, 0, 2.7, 1.2); r.wall(2.7, 2.1, 2.7, 3.2); r.wall(0, 3.2, 2.7, 3.2)
    r.bath(0, 0, 2.7, 3.2, tub=True)
    r.wardrobe(5.35, 1.5, 1, w=1.6)
    r.bed(1.2, 5.4, 3)
    r.tv(5.4, 3.9, 1, w=1.5)
    r.rug(4.3, 6.4, 2.6, 2.4)
    r.sofa(5.1, 6.4, 1, w=1.7)
    r.coffee(4.0, 6.4, 1, w=1.0, d=0.6)
    r.armchair(3.6, 7.35, 2)
    r.floor_lamp(5.3, 7.55)
    r.spot("bedroom", 1.6, 5.4); r.spot("lounge", 4.3, 6.4); r.spot("bath", 1.3, 1.6)
    return r.export()


def imperial():
    reset()
    r = Room("imperial", 10.0, 8.0)
    r.shell(door=(0.7, 1.7), win_w=(4.4, 7.6))
    r.wall(5.4, 0, 5.4, 2.6); r.wall(5.4, 6.6, 5.4, 8.0)       # vách ngăn phòng khách / phòng ngủ
    r.lattice(5.4, 2.6, 3.5); r.lattice(5.4, 5.7, 6.6)
    r.wall(7.0, 0, 7.0, 1.0); r.wall(7.0, 1.9, 7.0, 3.0); r.wall(7.0, 3.0, 10.0, 3.0)
    r.bath(7.0, 0, 10.0, 3.0, tub=True)
    r.wardrobe(6.2, 0.45, 0, w=1.3)
    r.rug(2.6, 5.7, 3.9, 3.0)
    r.sofa(1.0, 5.7, 3, w=2.1)
    r.coffee(2.5, 5.7, 1)
    r.armchair(4.0, 5.0, 1); r.armchair(4.0, 6.4, 1)
    r.tv(5.05, 7.25, 1, w=1.3)
    r.floor_lamp(0.55, 7.45); r.plant(4.9, 0.6)
    r.dining(2.6, 1.7, 0)
    r.bed(8.75, 5.5, 1)
    r.tea_set(6.6, 7.3)
    r.spot("living", 2.6, 5.4); r.spot("window", 3.0, 7.4); r.spot("dining", 2.6, 1.7); r.spot("bedroom", 8.3, 5.5); r.spot("bath", 8.5, 1.5)
    return r.export()


def presidential():
    reset()
    r = Room("presidential", 16.0, 10.0)
    r.shell(door=(7.7, 8.8), win_w=(2.0, 9.0), win_e=(4.2, 9.2))
    r.wall(9.6, 3.3, 9.6, 5.2); r.wall(9.6, 9.0, 9.6, 10.0)
    r.lattice(9.6, 5.2, 6.1); r.lattice(9.6, 8.1, 9.0)
    r.wall(9.6, 3.3, 11.0, 3.3); r.wall(12.0, 3.3, 16.0, 3.3)
    r.wall(9.6, 0, 9.6, 3.3)
    r.bath(9.6, 0, 16.0, 3.3, tub=True)
    r.lattice(6.9, 0.2, 2.6)                                   # bình phong tiền sảnh
    # Phòng khách lớn
    r.rug(3.4, 6.7, 5.2, 4.2)
    r.sofa(3.4, 8.6, 2, w=2.6)
    r.sofa(1.1, 6.6, 3, w=2.1)
    r.coffee(3.4, 6.6, 0, w=1.6, d=0.9)
    r.armchair(5.6, 6.0, 1); r.armchair(5.6, 7.3, 1)
    r.armchair(2.6, 4.8, 0); r.armchair(4.2, 4.8, 0)
    r.floor_lamp(0.6, 9.4); r.floor_lamp(6.2, 9.4)
    r.tv(9.25, 7.1, 1, w=1.6)
    r.plant(8.9, 9.3); r.plant(0.6, 0.6)
    # Bàn ăn sáu ghế
    r.dining(3.3, 1.9, 0, seats=6)
    r.desk(8.3, 4.2, 2)
    # Phòng ngủ chính
    r.bed(14.75, 6.7, 1, w=2.1)
    r.tea_set(11.6, 9.2)
    r.wardrobe(13.4, 3.78, 0, w=2.4)
    r.rug(12.6, 6.7, 2.0, 3.0)
    r.spot("living", 3.4, 6.7); r.spot("dining", 3.3, 1.9)
    r.spot("bedroom", 14.0, 6.7); r.spot("bath", 13.0, 1.6)
    return r.export()


if __name__ == "__main__":
    meta = {"deluxe": deluxe(), "junior": junior(), "imperial": imperial(), "presidential": presidential()}
    with open(os.path.join(OUT_DIR, "rooms.json"), "w") as f:
        json.dump(meta, f, indent=1)
    print("OK", {k: v["w"] * v["d"] for k, v in meta.items()})
