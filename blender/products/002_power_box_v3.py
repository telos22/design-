"""002 수납 상자 v3 — 한 가지 형태로 멀티탭도, 필기구도.
- 쟁반: 46 × 8 × 6cm (6구 멀티탭까지 들어감), 앞 턱 2.5cm, 옆판 비스듬히
- 양쪽 옆판 모두 아래 홈 → 꼬리를 어느 쪽으로든 뺄 수 있다 (왼쪽·오른쪽 어디에 붙여도)
- 등판 대신 작은 탭 2개(폭 3cm, 높이 6cm) → 탭 끝에 지름 2.2cm 자석, 고무로 덮음 → 툭 대면 붙는다
- 알루미늄 판 1.5mm, 분체도장(책상 색)
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

T, W = pb.T, pb.W
L, H_TRAY, H_FRONT = 4.6, 0.6, 0.25
TAB_W, TAB_H = 0.3, 0.6


def box(x0, y0, m):
    studio.box("Bottom", (L, W, T), (x0, y0, T / 2), m["box"])
    studio.box("Back", (L, T, H_TRAY), (x0, y0 + W / 2 - T / 2, H_TRAY / 2), m["box"])
    studio.box("Front", (L, T, H_FRONT), (x0, y0 - W / 2 + T / 2, H_FRONT / 2), m["box"])
    notch = [(-W / 2, 0), (0.05, 0), (0.05, 0.12), (0.19, 0.12), (0.19, 0), (W / 2, 0), (W / 2, H_TRAY), (-W / 2, H_FRONT)]
    for xa, xb in ((x0 - L / 2, x0 - L / 2 + T), (x0 + L / 2 - T, x0 + L / 2)):
        studio.extrude_x("Side", [(y0 + y, z) for y, z in notch], xa, xb, m["box"])
    for sx in (-1, 1):
        tx = x0 + sx * (L / 2 - 0.6)
        studio.box("Tab", (TAB_W, T, TAB_H), (tx, y0 + W / 2 - T / 2, H_TRAY + TAB_H / 2), m["box"])
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.11, depth=0.05,
                                            location=(tx, y0 + W / 2 + 0.025, H_TRAY + TAB_H - 0.15))
        bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
        studio.assign(bpy.context.object, m["magnet"])
        studio.smooth_edges(bpy.context.object)


def stationery(x0, y0, m):
    yellow = studio.material("Pencil", (0.62, 0.45, 0.10), roughness=0.6)
    eraser = studio.material("Eraser", (0.78, 0.77, 0.74), roughness=0.8)
    ruler = studio.material("Ruler", (0.70, 0.71, 0.73), roughness=0.3, metallic=0.9)
    note = studio.material("Notes", (0.80, 0.78, 0.70), roughness=0.9)
    for i, (dx, dy, mat, ln) in enumerate(((-1.2, -0.18, m["dark"], 1.45), (-1.0, 0.0, yellow, 1.75), (-1.15, 0.18, m["dark"], 1.4))):
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.045, depth=ln, location=(x0 + dx, y0 + dy, T + 0.05))
        bpy.context.object.rotation_euler = (0, math.pi / 2, 0.04 * (i - 1))
        studio.assign(bpy.context.object, mat)
    studio.box("Ruler", (3.0, 0.3, 0.02), (x0 + 0.3, y0 + 0.2, T + 0.12), ruler)
    studio.box("Eraser", (0.45, 0.2, 0.12), (x0 + 1.5, y0 - 0.15, T + 0.06), eraser, bevel=0.02)
    studio.box("Notes", (0.75, 0.75, 0.15), (x0 + 0.6, y0 - 0.1, T + 0.075), note)


def scene(name, cam_loc, target):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=1.2)
    m = pb.mats()
    box(0.0, 0.75, m)                                  # 멀티탭
    c = pb.strip(6, 0.15, 0.75, m)
    pb.plug(c[0], 0.75, m, "brick", (0.2, -0.4))
    pb.plug(c[2], 0.75, m, "plug", (0.0, -0.5))
    pb.plug(c[4], 0.75, m, "brick", (-0.2, -0.4))
    box(0.0, -0.75, m)                                 # 필기구 (같은 상자)
    stationery(0.0, -0.75, m)
    cam = studio.camera(target=(0, 0, 0), lens=50)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=96, resolution=(1600, 1100), view="Standard", exposure=-1.2)


if __name__ == "__main__":
    print(scene("002_box_v3_front", (-3.0, -7.6, 5.0), (0.0, 0.0, 0.3)))
    print(scene("002_box_v3_back", (3.8, 7.4, 3.2), (0.0, 0.0, 0.45)))
