"""Kết xuất sẵn (Cycles) vòng xoay mặt bằng từng hạng phòng → assets/turn/<phòng>/NN.jpg + turn.json.

Chạy: python3 blender/render_rooms.py [số_khung] [mẫu] [phòng…]
"""
import json
import math
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rooms  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("-")]
FRAMES = int(args[0]) if args else 24
SAMPLES = int(args[1]) if len(args) > 1 else 48
ONLY = args[2:]
OUT = os.path.join(HERE, "..", "assets", "turn")
RES = (1200, 900)
BG = (0.012, 0.022, 0.085)


def render_room(self):
    ob = self.b.finish()
    ob.location = (-self.w / 2, -self.d / 2, 0)
    sc = bpy.context.scene
    for p in ob.data.polygons:
        p.use_smooth = False
    bev = ob.modifiers.new("bevel", "BEVEL")           # bo mềm mọi cạnh
    bev.width, bev.segments, bev.limit_method = 0.018, 3, "ANGLE"
    for m in ob.data.materials:
        b = m.node_tree.nodes["Principled BSDF"]
        if m.name == "lamp_shade":
            b.inputs["Emission Strength"].default_value = 14.0
        if m.name == "glass":
            b.inputs["Alpha"].default_value = 0.1

    radius = math.hypot(self.w, self.d) / 2
    # Nền và ánh sáng
    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.42))
    ground = bpy.context.object
    gm = bpy.data.materials.new("ground"); gm.use_nodes = True
    g = gm.node_tree.nodes["Principled BSDF"]
    g.inputs["Base Color"].default_value = (*BG, 1); g.inputs["Roughness"].default_value = 0.35
    ground.data.materials.append(gm)
    world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
    bgn = world.node_tree.nodes["Background"]
    bgn.inputs["Color"].default_value = (0.10, 0.16, 0.45, 1); bgn.inputs["Strength"].default_value = 0.35

    def light(kind, loc, energy, color, size=1.0, rot=(0, 0, 0)):
        d = bpy.data.lights.new(kind, kind); d.energy = energy; d.color = color
        if kind == "AREA":
            d.size = size
        if kind == "SUN":
            d.angle = math.radians(6)
        o = bpy.data.objects.new(kind, d); o.location = loc; o.rotation_euler = rot
        sc.collection.objects.link(o)
    light("SUN", (0, 0, 10), 2.4, (1.0, 0.86, 0.68), rot=(math.radians(48), 0, math.radians(35)))
    light("AREA", (0, 0, 7.5), 160 * radius, (1.0, 0.9, 0.78), size=radius * 1.6)

    cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 70
    cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
    tgt = bpy.data.objects.new("tgt", None); tgt.location = (0, 0, 0.2); sc.collection.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO"); con.target = tgt

    sc.render.engine = "CYCLES"
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 5
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 86
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.render.threads_mode = "AUTO"

    out_dir = os.path.join(OUT, self.key); os.makedirs(out_dir, exist_ok=True)
    dist, elev = radius * 5.0, math.radians(40)
    frames = []
    for i in range(FRAMES):
        a = math.radians(-125) + i * 2 * math.pi / FRAMES
        cam.location = (math.cos(a) * math.cos(elev) * dist, math.sin(a) * math.cos(elev) * dist, math.sin(elev) * dist)
        bpy.context.view_layer.update()
        sc.render.filepath = os.path.join(out_dir, f"{i:02d}.jpg")
        bpy.ops.render.render(write_still=True)
        pts = {}
        for h in self.hot:                       # h["pos"] đang ở hệ trục web (x, y lên, z)
            x, y, z = h["pos"]
            v = world_to_camera_view(sc, cam, Vector((x, -z, y)))
            pts[h["id"]] = [round(v.x, 4), round(1 - v.y, 4)]
        frames.append(pts)
    return {"w": self.w, "d": self.d, "frames": frames}


rooms.Room.export = render_room
meta_path = os.path.join(OUT, "turn.json")
meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
for key in ("deluxe", "junior", "imperial", "presidential"):
    if ONLY and key not in ONLY:
        continue
    meta[key] = getattr(rooms, key)()
    os.makedirs(OUT, exist_ok=True)
    json.dump(meta, open(meta_path, "w"))
    print("DONE", key, flush=True)
