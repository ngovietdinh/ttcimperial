"""Bộ hàm dựng hình dùng chung cho tower.py và rooms.py (Blender / bpy)."""
import math
import bpy
import bmesh
from mathutils import Matrix, Vector


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


_mats = {}


def mat(name, color, rough=0.7, metal=0.0, emit=None, strength=0.0, alpha=1.0):
    """Tạo (hoặc lấy lại) vật liệu Principled theo tên."""
    if name in _mats:
        return _mats[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1.0)
        b.inputs["Emission Strength"].default_value = strength
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.blend_method = "BLEND"
    _mats[name] = m
    return m


def clear_mats():
    _mats.clear()


class Builder:
    """Gom nhiều khối vào một lưới, mỗi khối một vật liệu."""

    def __init__(self, name):
        self.name = name
        self.bm = bmesh.new()
        self.slots = []

    def _slot(self, m):
        if m not in self.slots:
            self.slots.append(m)
        return self.slots.index(m)

    def box(self, c, s, m):
        """Khối hộp tâm c=(x,y,z), kích thước s=(sx,sy,sz)."""
        idx = self._slot(m)
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        vs = r["verts"]
        for v in vs:
            v.co = Vector((v.co.x * s[0] + c[0], v.co.y * s[1] + c[1], v.co.z * s[2] + c[2]))
        for f in {f for v in vs for f in v.link_faces}:
            f.material_index = idx

    def cyl(self, c, r1, h, m, r2=None, segs=20):
        """Trụ / nón cụt đứng, tâm đáy c."""
        idx = self._slot(m)
        r2 = r1 if r2 is None else r2
        r = bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=segs,
                                  radius1=r1, radius2=r2, depth=h)
        vs = r["verts"]
        for v in vs:
            v.co = Vector((v.co.x + c[0], v.co.y + c[1], v.co.z + c[2] + h / 2))
        for f in {f for v in vs for f in v.link_faces}:
            f.material_index = idx

    def ball(self, c, r, m, squash=1.0):
        idx = self._slot(m)
        res = bmesh.ops.create_icosphere(self.bm, subdivisions=2, radius=r)
        vs = res["verts"]
        for v in vs:
            v.co = Vector((v.co.x + c[0], v.co.y + c[1], v.co.z * squash + c[2]))
        for f in {f for v in vs for f in v.link_faces}:
            f.material_index = idx

    def frustum(self, c, base, top, h, m):
        """Mái hông: đáy chữ nhật base=(bx,by) thu về top=(tx,ty), cao h, tâm đáy c."""
        idx = self._slot(m)
        bx, by = base[0] / 2, base[1] / 2
        tx, ty = top[0] / 2, top[1] / 2
        co = [(-bx, -by, 0), (bx, -by, 0), (bx, by, 0), (-bx, by, 0),
              (-tx, -ty, h), (tx, -ty, h), (tx, ty, h), (-tx, ty, h)]
        vs = [self.bm.verts.new((c[0] + x, c[1] + y, c[2] + z)) for x, y, z in co]
        for q in [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7), (3, 2, 1, 0)]:
            f = self.bm.faces.new([vs[i] for i in q])
            f.material_index = idx

    def finish(self):
        me = bpy.data.meshes.new(self.name)
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        self.bm.to_mesh(me)
        self.bm.free()
        for m in self.slots:
            me.materials.append(m)
        ob = bpy.data.objects.new(self.name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob


class Place:
    """Đặt đồ nội thất: gốc (ox, oy), xoay k*90 độ quanh trục đứng."""

    def __init__(self, b, ox, oy, k=0):
        self.b, self.ox, self.oy, self.k = b, ox, oy, k % 4

    def _xy(self, x, y):
        for _ in range(self.k):
            x, y = -y, x
        return self.ox + x, self.oy + y

    def box(self, c, s, m):
        x, y = self._xy(c[0], c[1])
        sx, sy = (s[0], s[1]) if self.k % 2 == 0 else (s[1], s[0])
        self.b.box((x, y, c[2]), (sx, sy, s[2]), m)

    def cyl(self, c, r1, h, m, r2=None):
        x, y = self._xy(c[0], c[1])
        self.b.cyl((x, y, c[2]), r1, h, m, r2)

    def ball(self, c, r, m, squash=1.0):
        x, y = self._xy(c[0], c[1])
        self.b.ball((x, y, c[2]), r, m, squash)


def export_glb(path):
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", export_apply=True,
                              export_yup=True, export_cameras=False, export_lights=False)
