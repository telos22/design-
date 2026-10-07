"""003 책상 + 수납 상자(한 가지 크기 46cm) — 뒤 레일(가로)과 옆 레일(세로)에 붙인 모습.
프레임은 구멍 없는 매끈한 강철. 상자는 탭 끝 자석으로 레일 안쪽 면에 붙는다.
단위 1 = 10cm"""
import importlib.util
import math
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
import bpy
import mathutils
import props
import studio


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dk = load("001_desk_steel")
bx = load("002_power_box_v3")
pb = bx.pb

TOP_UNDER = dk.H - dk.T
RAIL_IN_X = dk.IX - dk.FR_T       # 옆 레일 안쪽 면 |x|
RAIL_IN_Y = dk.IY - dk.FR_T       # 뒤 레일 안쪽 면 y
Z0 = TOP_UNDER - (bx.H_TRAY + bx.TAB_H)   # 상자 바닥 높이


def placed(build, loc, rot_z):
    """build()로 원점에 만든 물체들을 빈 물체에 묶어 옮긴다."""
    before = set(bpy.data.objects)
    build()
    made = set(bpy.data.objects) - before
    pivot = bpy.data.objects.new("BoxPivot", None)
    bpy.context.collection.objects.link(pivot)
    for o in made:
        o.parent = pivot
    pivot.location = loc
    pivot.rotation_euler.z = rot_z


def with_strip(m):
    bx.box(0, 0, m)
    c = pb.strip(6, 0.15, 0, m)
    pb.plug(c[0], 0, m, "brick", (0.3, -0.6), rise=0.3)    # 상판 아래 공간 안에서 앞으로 휘어 나감
    pb.plug(c[2], 0, m, "plug", (0.0, -0.7), rise=0.35)
    pb.plug(c[4], 0, m, "brick", (-0.3, -0.6), rise=0.3)


def with_pens(m):
    bx.box(0, 0, m)
    bx.stationery(0, 0, m)


def scene(name, cam_loc, target, lens):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    dk.desk(dk.materials(), holes=False)
    m = pb.mats()
    # 뒤 레일 (가로): 멀티탭
    placed(lambda: with_strip(m), (2.4, RAIL_IN_Y - bx.W / 2, Z0), 0)
    # 왼쪽 레일 (세로): 필기구 — 앞쪽으로 당겨 손 닿게
    placed(lambda: with_pens(m), (-RAIL_IN_X + bx.W / 2, -0.2, Z0), math.pi / 2)
    # 오른쪽 레일 (세로): 멀티탭 하나 더
    placed(lambda: with_strip(m), (RAIL_IN_X - bx.W / 2, 0.0, Z0), -math.pi / 2)
    studio.box("Laptop", (3.1, 2.15, 0.16), (3.2, -0.6, dk.H + 0.08), studio.material("Alu", (0.8, 0.8, 0.82), 0.35, 1.0), bevel=0.04)
    props.notebook(-3.5, -0.8, dk.H, angle=0.05)
    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=64, resolution=(1600, 1050), view="Standard", exposure=-1.6)


if __name__ == "__main__":
    print(scene("003_desk_boxes_seat", (0.0, -10.5, 3.6), (0.0, 1.0, 6.2), 22))     # 앉은 자리 무릎 높이에서
    print(scene("003_desk_boxes_back", (9.0, 15.5, 4.2), (0.5, 0.0, 6.0), 26))      # 뒤쪽 아래에서
    print(scene("003_desk_boxes_hero", (-13.0, -21.0, 12.5), (0.6, 0.0, 4.2), 40))  # 전체 (위에서는 안 보임)
