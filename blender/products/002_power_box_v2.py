"""002 멀티탭 상자 v2 — 알루미늄 쟁반 + 뒷면 자석(고무 시트로 덮음), 프레임 아래로 매달림.
- 뒷벽 12cm: 위 4cm = 프레임에 붙는 띠(안에 작은 자석, 겉은 고무 시트) / 아래 8cm = 쟁반
- 쟁반: 뒤 6cm, 앞 턱 2.5cm, 옆판 비스듬히, 한쪽 옆판 아래 꼬리 홈
- 알루미늄이라 가볍다 → 자석이 버틸 무게가 줄어든다
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


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pb = _load("002_power_box")      # 멀티탭·플러그 모델 재사용
T, W = pb.T, pb.W
H_TRAY, H_FRONT, BAND = 0.6, 0.25, 0.4
H_BACK = H_TRAY + 0.2 + BAND      # 6 + 2(틈) + 4 = 12cm


def box(L, x0, y0, z0, m):
    """z0 = 쟁반 바닥 높이. 뒤 = +y"""
    studio.box("Bottom", (L, W, T), (x0, y0, z0 + T / 2), m["box"])
    studio.box("Back", (L, T, H_BACK), (x0, y0 + W / 2 - T / 2, z0 + H_BACK / 2), m["box"])
    studio.box("Front", (L, T, H_FRONT), (x0, y0 - W / 2 + T / 2, z0 + H_FRONT / 2), m["box"])
    side = [(-W / 2, 0), (W / 2, 0), (W / 2, H_TRAY), (-W / 2, H_FRONT)]
    notch = [(-W / 2, 0), (0.05, 0), (0.05, 0.12), (0.19, 0.12), (0.19, 0), (W / 2, 0), (W / 2, H_TRAY), (-W / 2, H_FRONT)]
    studio.extrude_x("SideTail", [(y0 + y, z0 + z) for y, z in notch], x0 - L / 2, x0 - L / 2 + T, m["box"])
    studio.extrude_x("Side", [(y0 + y, z0 + z) for y, z in side], x0 + L / 2 - T, x0 + L / 2, m["box"])
    # 고무 시트 띠 (속에 자석) — 뒷면 위쪽 4cm
    studio.box("RubberBand", (L - 0.1, 0.02, BAND), (x0, y0 + W / 2 + 0.01, z0 + H_BACK - BAND / 2), m["magnet"])


def fill(n, x0, y0, z0, m, plugs):
    # 002_power_box 의 strip/plug 는 바닥 z=0 기준 → 만든 뒤 z0만큼 올린다
    before = set(bpy.data.objects)
    c = pb.strip(n, x0, y0, m)
    for i, kind, to in plugs:
        pb.plug(c[i], y0, m, kind, to)
    for o in set(bpy.data.objects) - before:
        o.location.z += z0


def look(cam_loc, target, lens):
    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()


def standalone(name, cam_loc, target):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=1.2)
    m = pb.mats()
    box(4.6, 0.0, 0.7, 0, m)
    fill(6, 0.15, 0.7, 0, m, [(0, "brick", (0.2, -0.4)), (2, "plug", (0.0, -0.5)), (4, "brick", (-0.2, -0.4))])
    box(2.9, -0.4, -0.7, 0, m)
    fill(3, -0.25, -0.7, 0, m, [(1, "brick", (0.1, -0.4))])
    look(cam_loc, target, 50)
    return studio.render(name, samples=96, resolution=(1600, 1100), view="Standard", exposure=-1.2)


def attached(name):
    """책상 뒤 레일에 붙인 모습 (책상 안쪽 아래에서)"""
    desk_mod = _load("001_desk_steel")
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    dm = desk_mod.materials()
    desk_mod.desk(dm)
    m = pb.mats()
    rail_inner = desk_mod.IY - desk_mod.FR_T          # 뒤 레일 안쪽 면 y
    top_under = desk_mod.H - desk_mod.T               # 상판 아랫면 높이
    y0 = rail_inner - W / 2 - 0.02
    z0 = top_under - H_BACK
    box(4.6, 2.5, y0, z0, m)
    fill(6, 2.65, y0, z0, m, [(0, "brick", (0.2, -0.4)), (2, "plug", (0.0, -0.5)), (4, "brick", (-0.2, -0.4))])
    look((0.5, -2.5, 4.2), (2.5, y0, z0 + 0.4), 30)
    return studio.render(name, samples=64, resolution=(1600, 1100), view="Standard", exposure=-1.6)


if __name__ == "__main__":
    print(standalone("002_power_box_v2_front", (-3.2, -7.5, 5.2), (0.0, 0.0, 0.4)))
    print(standalone("002_power_box_v2_back", (4.2, 7.0, 3.4), (0.0, 0.0, 0.5)))
    print(attached("002_power_box_v2_attached"))
