"""002 수납 상자 v4 — 콘센트가 앉은 사람 쪽을 향하도록 세운 형태.
멀티탭을 등판에 기대 세워 두고, 플러그를 앞에서 수평으로 꽂는다.
- 단면: 등판 7cm(프레임 쪽) + 바닥 선반 5.5cm + 앞 턱 1.5cm, 옆판 비스듬히, 양쪽 옆판 아래 꼬리 홈
- 등판 위로 탭 2개(자석) → 뒤 레일 안쪽 면에 툭 붙임
- 같은 상자에 필기구도 (바닥 선반에 눕혀서)
단위 1 = 10cm"""
import importlib.util
import math
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
import bpy
import mathutils
import studio

spec = importlib.util.spec_from_file_location("pb", os.path.join(HERE, "002_power_box.py"))
pb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pb)

T = 0.015
L, DEPTH, H_BACK, H_LIP = 4.6, 0.55, 0.7, 0.15
TAB_W, TAB_H = 0.3, 0.5
PITCH = 0.63


def box(m):
    """원점 기준. 등판 = +y 쪽, 앞(사람 쪽) = -y"""
    yb = DEPTH / 2
    studio.box("Bottom", (L, DEPTH, T), (0, 0, T / 2), m["box"])
    studio.box("Back", (L, T, H_BACK), (0, yb - T / 2, H_BACK / 2), m["box"])
    studio.box("Lip", (L, T, H_LIP), (0, -yb + T / 2, H_LIP / 2), m["box"])
    prof = [(-yb, 0), (-0.12, 0), (-0.12, 0.12), (0.02, 0.12), (0.02, 0), (yb, 0), (yb, H_BACK), (-yb, H_LIP)]
    for xa, xb in ((-L / 2, -L / 2 + T), (L / 2 - T, L / 2)):
        studio.extrude_x("Side", prof, xa, xb, m["box"])
    for sx in (-1, 1):
        tx = sx * (L / 2 - 0.6)
        studio.box("Tab", (TAB_W, T, TAB_H), (tx, yb - T / 2, H_BACK + TAB_H / 2), m["box"])
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.11, depth=0.05, location=(tx, yb + 0.025, H_BACK + TAB_H - 0.15))
        bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
        studio.assign(bpy.context.object, m["magnet"])


def strip_standing(n, m):
    """멀티탭을 등판에 기대 세움: 콘센트가 -y(사람 쪽)를 향함"""
    Ls = n * PITCH + 0.32
    yb = DEPTH / 2
    sy = yb - T - 0.19                       # 멀티탭 중심 y (두께 0.38)
    sz = T + 0.275 + 0.02                    # 높이 0.55 중 중심
    studio.box("Strip", (Ls, 0.38, 0.55), (0.15, sy, sz), m["strip"], bevel=0.06)
    centers = [0.15 - (n - 1) * PITCH / 2 + i * PITCH for i in range(n)]
    face_y = sy - 0.19
    for cx in centers:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.2, depth=0.02, location=(cx, face_y - 0.005, sz))
        bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
        studio.assign(bpy.context.object, m["socket"])
        for dx in (-0.095, 0.095):
            bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.025, depth=0.01, location=(cx + dx, face_y - 0.016, sz))
            bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
            studio.assign(bpy.context.object, m["hole"])
    xe = 0.15 - Ls / 2
    studio.cable("Tail", [(xe, sy, T + 0.1), (xe - 0.2, sy - 0.1, T + 0.06), (xe - 0.4, -0.05, T + 0.06),
                          (-L / 2 - 0.5, -0.1, 0.03), (-L / 2 - 1.3, -0.3, 0.03)], m["strip"], radius=0.035)
    return centers, face_y, sz


def plug_front(cx, face_y, sz, m, kind):
    """앞에서 수평으로 꽂힌 플러그, 선은 아래·앞으로"""
    if kind == "brick":
        studio.box("Charger", (0.55, 0.35, 0.5), (cx, face_y - 0.175, sz), m["plug"], bevel=0.05)
        front = face_y - 0.35
        mat = m["plug"]
    else:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.19, depth=0.28, location=(cx, face_y - 0.14, sz))
        bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
        studio.assign(bpy.context.object, m["dark"])
        front = face_y - 0.28
        mat = m["dark"]
    studio.cable("Cord", [(cx, front, sz), (cx, front - 0.2, sz - 0.05), (cx + 0.05, front - 0.35, sz - 0.3),
                          (cx + 0.1, front - 0.4, sz - 0.7)], mat, radius=0.025)


def pens(m):
    for i, (dx, dy) in enumerate(((-1.2, -0.12), (-1.0, 0.0), (-1.15, 0.12))):
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.045, depth=1.5, location=(dx, dy, T + 0.05))
        bpy.context.object.rotation_euler = (0, math.pi / 2, 0.04 * (i - 1))
        studio.assign(bpy.context.object, m["dark"])
    studio.box("Eraser", (0.45, 0.2, 0.12), (1.4, 0.0, T + 0.06), m["plug"], bevel=0.02)


def with_strip(m):
    box(m)
    c, fy, sz = strip_standing(6, m)
    plug_front(c[1], fy, sz, m, "brick")
    plug_front(c[3], fy, sz, m, "plug")
    plug_front(c[4], fy, sz, m, "brick")


def look(cam_loc, target, lens):
    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()


def standalone(name):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=1.2)
    m = pb.mats()
    with_strip(m)
    look((-3.0, -7.0, 3.6), (0.0, 0.0, 0.35), 50)
    return studio.render(name, samples=96, resolution=(1600, 1100), view="Standard", exposure=-1.2)


def on_desk(name):
    spec2 = importlib.util.spec_from_file_location("dk", os.path.join(HERE, "001_desk_steel.py"))
    dk = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(dk)
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    dk.desk(dk.materials(), holes=False)
    m = pb.mats()
    before = set(bpy.data.objects)
    with_strip(m)
    made = set(bpy.data.objects) - before
    pivot = bpy.data.objects.new("Pivot", None)
    bpy.context.collection.objects.link(pivot)
    for o in made:
        o.parent = pivot
    pivot.location = (0.5, dk.IY - dk.FR_T - DEPTH / 2, dk.H - dk.T - (H_BACK + TAB_H))
    look((-1.0, -6.5, 3.8), (0.3, 2.2, 5.9), 28)    # 의자에 앉아 몸을 숙여 책상 아래를 보는 시선
    return studio.render(name, samples=64, resolution=(1600, 1100), view="Standard", exposure=-1.6)


if __name__ == "__main__":
    print(standalone("002_box_v4_front"))
    print(on_desk("002_box_v4_on_desk"))
