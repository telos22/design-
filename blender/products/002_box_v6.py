"""002 수납 상자 v6 — 뒤 레일 '바깥 면'에 붙여 책상 뒤쪽을 보게.
높은 벽(6cm) 위로 탭 2개 → 탭 끝 자석이 뒤 레일의 바깥 면에 붙는다.
상자는 프레임 밖, 상판 뒤쪽 아래에 매달리고, 낮은 턱(2cm)과 열린 쪽이 책상 바깥(뒤)을 향한다.
→ 앉은 자리에서는 안 보이고, 플러그 선은 바로 위로 올라가 상판 뒤 모서리로 넘어간다.
치수는 v5(실제 멀티탭 337.8 × 73.5mm 기준)와 같다. 1 = 10cm"""
import importlib.util
import math
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
import bpy
import mathutils
import studio


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("0", "m"), os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v5 = load("002_box_v5")
dk = load("001_desk_steel")
pb, cm = v5.pb, v5.cm
T, L, W, H_TALL, H_LOW, DROP = v5.T, v5.L, v5.W, v5.H_USER, v5.H_OUT, v5.DROP


def box(m):
    """원점 = 바닥 중심. 높은 벽(탭·자석) = -y (레일 쪽), 낮은 턱 = +y (책상 바깥)"""
    studio.box("Bottom", (L, W, T), (0, 0, T / 2), m["box"])
    studio.box("TallWall", (L, T, H_TALL), (0, -W / 2 + T / 2, H_TALL / 2), m["box"])
    studio.box("LowLip", (L, T, H_LOW), (0, W / 2 - T / 2, H_LOW / 2), m["box"])
    n0, n1 = -cm(2.0), -cm(0.5)
    prof = [(-W / 2, 0), (n0, 0), (n0, cm(1.2)), (n1, cm(1.2)), (n1, 0), (W / 2, 0), (W / 2, H_LOW), (-W / 2, H_TALL)]
    for xa, xb in ((-L / 2, -L / 2 + T), (L / 2 - T, L / 2)):
        studio.extrude_x("Side", prof, xa, xb, m["box"])
    for sx in (-1, 1):
        tx = sx * (L / 2 - cm(5))
        tab_h = DROP - H_TALL
        studio.box("Tab", (v5.TAB_W, T, tab_h), (tx, -W / 2 + T / 2, H_TALL + tab_h / 2), m["box"])
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=cm(1.1), depth=cm(0.5),
                                            location=(tx, -W / 2 - cm(0.25), DROP - cm(2.0)))
        bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
        studio.assign(bpy.context.object, m["magnet"])


def plug_up(cx, top, m, kind, reach_y):
    """플러그 선이 위로 올라가 상판 뒤 모서리를 넘는다 (reach_y = 상자 원점 기준 모서리 y)"""
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
    edge_z = DROP + dk.T
    studio.cable("Cord", [(cx, 0, z), (cx, cm(0.5), z + cm(2)), (cx, reach_y + cm(0.4), edge_z - cm(2)),
                          (cx, reach_y + cm(0.3), edge_z + cm(0.3)), (cx, reach_y - cm(3), edge_z + cm(0.3))], mat, radius=cm(0.25))


def build(m, reach_y):
    box(m)
    c, top = v5.strip(m)
    plug_up(c[0], top, m, "laptop", reach_y)
    plug_up(c[2], top, m, "phone", reach_y)
    plug_up(c[4], top, m, "plug", reach_y)


def scene(name, cam_loc, target, lens):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    dk.desk(dk.materials(), holes=False)
    m = pb.mats()
    y_center = dk.IY + W / 2 + cm(0.5)            # 레일 바깥 면에 붙음
    reach_y = dk.D / 2 - y_center                 # 상자 기준 상판 뒤 모서리
    before = set(bpy.data.objects)
    build(m, reach_y)
    made = set(bpy.data.objects) - before
    pivot = bpy.data.objects.new("Pivot", None)
    bpy.context.collection.objects.link(pivot)
    for o in made:
        o.parent = pivot
    pivot.location = (0.5, y_center, dk.H - dk.T - DROP)
    studio.box("Laptop", (3.1, 2.15, 0.15), (0.8, -0.4, dk.H + 0.075), studio.material("Alu", (0.8, 0.8, 0.82), 0.3, 1.0), bevel=0.03)
    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=64, resolution=(1600, 1100), view="Standard", exposure=-1.6)


if __name__ == "__main__":
    print(scene("002_box_v6_back", (5.0, 12.5, 9.0), (0.5, 2.8, 6.2), 32))     # 책상 뒤에서
    print(scene("002_box_v6_side", (9.6, 3.6, 6.1), (0.5, 3.2, 6.3), 40))     # 옆에서 (상자 높이)
    print(scene("002_box_v6_seat", (-9.0, -17.0, 13.0), (1.0, 0.3, 6.0), 40)) # 앉는 쪽에서 (안 보임)
