"""002 수납 상자 v5 — 실제 멀티탭 치수 기준, 멀티탭은 눕히고, 선은 바깥(책상 뒤)으로.
기준 멀티탭: 일자형 6구 337.8 × 73.5 × 약 40mm (일신전기 6구 2호 기준, 높이는 대략)
플러그: 지름 37mm, 길이 45mm / 노트북 충전기 50 × 30 × 50mm (세워 꽂힘) / 휴대폰 충전기 30 × 30 × 40mm
상자(바깥): 38 × 8.6cm — 멀티탭 + 양 끝 꼬리 여유 2cm씩
- 사람 쪽 벽 6cm: 멀티탭과 플러그 몸통을 가린다
- 바깥(책상 뒤) 쪽 턱 2cm: 플러그 선이 이쪽으로 넘어 나간다
- 바깥 턱에서 탭 2개가 위로 올라가 뒤 레일 안쪽 면에 자석으로 붙는다
- 상자 바닥은 상판 아래 12cm → 플러그 위로 선이 휘어 나갈 공간
- 양쪽 옆판 아래 꼬리 홈
치수는 cm로 적고 cm()로 단위 변환 (1 = 10cm)"""
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


def cm(v):
    return v / 10.0


T = cm(0.15)
STRIP_L, STRIP_W, STRIP_H = cm(33.8), cm(7.35), cm(4.0)
L, W = cm(38.0), cm(8.6)
H_USER, H_OUT = cm(6.0), cm(2.0)
DROP = cm(12.0)                      # 상판 아랫면 ~ 상자 바닥
TAB_W = cm(3.0)
N, PITCH = 6, cm(5.2)


def box(m):
    """원점 = 상자 바닥 중심. 사람 쪽 = -y, 바깥(책상 뒤, 레일 쪽) = +y"""
    studio.box("Bottom", (L, W, T), (0, 0, T / 2), m["box"])
    studio.box("UserWall", (L, T, H_USER), (0, -W / 2 + T / 2, H_USER / 2), m["box"])
    studio.box("OuterLip", (L, T, H_OUT), (0, W / 2 - T / 2, H_OUT / 2), m["box"])
    n0, n1 = cm(0.5), cm(2.0)
    prof = [(-W / 2, 0), (n0, 0), (n0, cm(1.2)), (n1, cm(1.2)), (n1, 0), (W / 2, 0), (W / 2, H_OUT), (-W / 2, H_USER)]
    for xa, xb in ((-L / 2, -L / 2 + T), (L / 2 - T, L / 2)):
        studio.extrude_x("Side", prof, xa, xb, m["box"])
    for sx in (-1, 1):   # 바깥 턱에서 위로 올라가는 탭 + 자석
        tx = sx * (L / 2 - cm(5))
        tab_h = DROP - H_OUT
        studio.box("Tab", (TAB_W, T, tab_h), (tx, W / 2 - T / 2, H_OUT + tab_h / 2), m["box"])
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=cm(1.1), depth=cm(0.5),
                                            location=(tx, W / 2 + cm(0.25), DROP - cm(2.0)))
        bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
        studio.assign(bpy.context.object, m["magnet"])


def strip(m):
    z = T + STRIP_H / 2
    studio.box("Strip", (STRIP_L, STRIP_W, STRIP_H), (0, 0, z), m["strip"], bevel=cm(0.6))
    top = T + STRIP_H
    centers = [-(N - 1) * PITCH / 2 + i * PITCH for i in range(N)]
    for cx in centers:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=cm(2.0), depth=cm(0.2), location=(cx, 0, top))
        studio.assign(bpy.context.object, m["socket"])
        for dx in (-cm(0.95), cm(0.95)):
            bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=cm(0.25), depth=cm(0.1), location=(cx + dx, 0, top + cm(0.1)))
            studio.assign(bpy.context.object, m["hole"])
    xe = -STRIP_L / 2
    studio.cable("Tail", [(xe, 0, T + cm(1.5)), (xe - cm(1.0), cm(0.6), T + cm(0.6)), (-L / 2 + cm(0.3), cm(1.2), T + cm(0.6)),
                          (-L / 2 - cm(4), cm(1.5), T + cm(0.6)), (-L / 2 - cm(12), cm(3), cm(0.3))], m["strip"], radius=cm(0.35))
    return centers, top


def plug(cx, top, m, kind):
    """kind: 'plug' 둥근 플러그 / 'laptop' 노트북 충전기 / 'phone' 휴대폰 충전기. 선은 바깥(+y)으로 넘어간다."""
    if kind == "plug":
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=cm(1.85), depth=cm(4.5), location=(cx, 0, top + cm(2.25)))
        studio.assign(bpy.context.object, m["dark"])
        studio.smooth_edges(bpy.context.object)
        h, mat = cm(4.5), m["dark"]
    elif kind == "laptop":
        studio.box("LaptopCharger", (cm(5.0), cm(3.0), cm(5.0)), (cx, 0, top + cm(2.5)), m["plug"], bevel=cm(0.5))
        h, mat = cm(5.0), m["plug"]
    else:
        studio.box("PhoneCharger", (cm(3.0), cm(3.0), cm(4.0)), (cx, 0, top + cm(2.0)), m["plug"], bevel=cm(0.5))
        h, mat = cm(4.0), m["plug"]
    z = top + h
    studio.cable("Cord", [(cx, 0, z), (cx, 0, z + cm(1.2)), (cx, cm(2.5), z + cm(2.2)), (cx, W / 2 + cm(1), z + cm(1.0)),
                          (cx, W / 2 + cm(3), z - cm(3)), (cx, W / 2 + cm(4), z - cm(8))], mat, radius=cm(0.25))


def contents(m):
    box(m)
    c, top = strip(m)
    plug(c[0], top, m, "laptop")
    plug(c[2], top, m, "phone")
    plug(c[4], top, m, "plug")


def look(cam_loc, target, lens):
    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()


def standalone(name, cam_loc, target):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=1.0)
    contents(pb.mats())
    look(cam_loc, target, 50)
    return studio.render(name, samples=96, resolution=(1600, 1100), view="Standard", exposure=-1.2)


def on_desk(name, cam_loc, target, lens):
    spec2 = importlib.util.spec_from_file_location("dk", os.path.join(HERE, "001_desk_steel.py"))
    dk = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(dk)
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    dk.desk(dk.materials(), holes=False)
    before = set(bpy.data.objects)
    contents(pb.mats())
    made = set(bpy.data.objects) - before
    pivot = bpy.data.objects.new("Pivot", None)
    bpy.context.collection.objects.link(pivot)
    for o in made:
        o.parent = pivot
    pivot.location = (0.5, dk.IY - dk.FR_T - W / 2 - cm(0.5), dk.H - dk.T - DROP)
    look(cam_loc, target, lens)
    return studio.render(name, samples=64, resolution=(1600, 1100), view="Standard", exposure=-1.6)


if __name__ == "__main__":
    print(standalone("002_box_v5_front", (-2.4, -5.2, 3.4), (0.0, 0.0, 0.35)))
    print(standalone("002_box_v5_side", (4.6, 0.6, 1.2), (0.0, 0.1, 0.45)))
    print(on_desk("002_box_v5_on_desk", (-1.0, -6.5, 4.0), (0.4, 2.2, 5.9), 28))
