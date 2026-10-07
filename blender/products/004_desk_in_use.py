"""004 책상 — 실제로 쓰는 모습.
오른쪽 칸: 노트북 거치대 + 노트북(충전 중), 휴대폰(충전 중). 멀티탭 상자는 뒤 레일 바깥 면 오른쪽.
왼쪽 칸: 책, 노트, 펜. 왼쪽 짧은 변(옆 레일 바깥 면)에 같은 상자 — 펜들.
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
    spec = importlib.util.spec_from_file_location("m_" + name.replace("0", "z"), os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v6 = load("002_box_v6")
v5, dk, pb, cm = v6.v5, v6.dk, v6.pb, v6.cm
H, D = dk.H, dk.D
TOP_Z = H + 0.003


def group(build, loc, rot_z=0.0, rot_x=0.0):
    before = set(bpy.data.objects)
    build()
    made = set(bpy.data.objects) - before
    pivot = bpy.data.objects.new("Group", None)
    bpy.context.collection.objects.link(pivot)
    for o in made:
        if o.parent is None:
            o.parent = pivot
    pivot.location = loc
    pivot.rotation_euler = (rot_x, 0, rot_z)
    return pivot


def mats():
    m = pb.mats()
    m.update({
        "alu": studio.material("Alu", (0.80, 0.80, 0.82), roughness=0.3, metallic=1.0),
        "key": studio.material("Keys", (0.05, 0.05, 0.06), roughness=0.6),
        "glass": studio.material("Glass", (0.02, 0.02, 0.025), roughness=0.08),
        "phone": studio.material("Phone", (0.04, 0.04, 0.045), roughness=0.2),
        "cable": studio.material("Cable", (0.85, 0.85, 0.83), roughness=0.5),
        "book1": studio.material("Book1", (0.16, 0.20, 0.24), roughness=0.7),
        "book2": studio.material("Book2", (0.55, 0.50, 0.42), roughness=0.7),
        "pages": studio.material("BookPages", (0.80, 0.78, 0.72), roughness=0.9),
        "pencil": studio.material("Pencil", (0.62, 0.45, 0.10), roughness=0.6),
    })
    return m


STAND_TILT = math.radians(15)
STAND_FRONT, STAND_DEPTH, STAND_W = cm(3), cm(24), cm(26)


def laptop_stand(x, y, m):
    """앞 3cm, 15° 기울어진 판 + 양옆 삼각 다리. 반환: 판 윗면 중심과 각도"""
    rear = STAND_FRONT + STAND_DEPTH * math.sin(STAND_TILT)
    prof = [(y - STAND_DEPTH / 2, 0), (y + STAND_DEPTH / 2, 0), (y + STAND_DEPTH / 2, rear), (y - STAND_DEPTH / 2, STAND_FRONT)]
    for sx in (-1, 1):
        xa = x + sx * (STAND_W / 2 - cm(0.4))
        studio.extrude_x("StandSide", [(py, TOP_Z + pz) for py, pz in prof], min(xa, xa + sx * cm(0.4)), max(xa, xa + sx * cm(0.4)), m["alu"])
    mid_z = TOP_Z + (STAND_FRONT + rear) / 2
    plate = studio.box("StandPlate", (STAND_W, STAND_DEPTH / math.cos(STAND_TILT), cm(0.4)), (x, y, mid_z), m["alu"])
    plate.rotation_euler.x = STAND_TILT
    studio.box("StandLip", (STAND_W * 0.6, cm(0.4), cm(1.2)), (x, y - STAND_DEPTH / 2 + cm(0.2), TOP_Z + STAND_FRONT + cm(0.6)), m["alu"])
    return (x, y, mid_z + cm(0.2))


def laptop_local(m):
    """원점 = 바닥 중심. 화면은 키보드와 105°"""
    studio.box("LaptopBase", (3.1, 2.15, 0.15), (0, 0, 0.075), m["alu"], bevel=0.03)
    studio.box("Keyboard", (2.7, 1.0, 0.005), (0, 0.25, 0.152), m["key"])
    studio.box("Trackpad", (1.1, 0.7, 0.004), (0, -0.6, 0.151), m["glass"])
    scr = studio.box("Screen", (3.1, 2.1, 0.06), (0, 1.05, 0), m["alu"], bevel=0.02)
    gl = studio.box("Glass", (2.9, 1.9, 0.005), (0, 1.05, 0.032), m["glass"])
    hinge = bpy.data.objects.new("Hinge", None)
    bpy.context.collection.objects.link(hinge)
    scr.parent = gl.parent = hinge
    hinge.location = (0, 1.075, 0.15)
    hinge.rotation_euler.x = math.radians(75)


def book(x, y, z, size, mat, m, rot=0.0):
    w, d, t = size
    studio.box("Cover", (w, d, t), (x, y, z + t / 2), mat, bevel=0.01).rotation_euler.z = rot
    studio.box("Pages", (w - 0.06, d - 0.1, t - 0.04), (x + 0.03 * math.cos(rot), y + 0.03 * math.sin(rot), z + t / 2), m["pages"]).rotation_euler.z = rot


def pens_in_box(m):
    v6.box(m)
    for i, (dy, mat, ln) in enumerate(((-0.2, m["dark"], 1.45), (-0.07, m["pencil"], 1.75), (0.06, m["dark"], 1.4), (0.19, m["pencil"], 1.6))):
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.045, depth=ln, location=(-0.6 + 0.1 * i, dy, v5.T + 0.05))
        bpy.context.object.rotation_euler = (0, math.pi / 2, 0.03 * (i - 1.5))
        studio.assign(bpy.context.object, mat)
    studio.box("Eraser", (0.45, 0.2, 0.12), (1.2, 0.0, v5.T + 0.06), m["plug"], bevel=0.02)


def power_box(m):
    v6.box(m)
    c, top = v5.strip(m)
    for i, kind in ((0, "laptop"), (2, "phone"), (4, "plug")):
        if kind == "plug":
            bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=cm(1.85), depth=cm(4.5), location=(c[i], 0, top + cm(2.25)))
            studio.assign(bpy.context.object, m["dark"])
        elif kind == "laptop":
            studio.box("LaptopCharger", (cm(5.0), cm(3.0), cm(5.0)), (c[i], 0, top + cm(2.5)), m["plug"], bevel=cm(0.5))
        else:
            studio.box("PhoneCharger", (cm(3.0), cm(3.0), cm(4.0)), (c[i], 0, top + cm(2.0)), m["plug"], bevel=cm(0.5))
    return c, top


def scene(name, cam_loc, target, lens, res=(1700, 1100)):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    dk.desk(dk.materials(), holes=False)
    m = mats()
    box_z = H - dk.T - v6.DROP

    # 멀티탭 상자: 뒤 레일 바깥 면, 오른쪽
    bx_x, bx_y = 4.6, dk.IY + v5.W / 2 + cm(0.5)
    group(lambda: power_box(m), (bx_x, bx_y, box_z))
    c = [bx_x - (v5.N - 1) * v5.PITCH / 2 + i * v5.PITCH for i in range(v5.N)]
    plug_top = box_z + v5.T + v5.STRIP_H

    # 펜 상자: 왼쪽 옆 레일 바깥 면 (열린 쪽이 왼쪽 바깥)
    group(lambda: pens_in_box(m), (-(dk.IX + v5.W / 2 + cm(0.5)), -0.3, box_z), rot_z=math.pi / 2)

    # 오른쪽 칸: 거치대 + 노트북, 휴대폰
    sx, sy, sz = laptop_stand(4.0, 0.6, m)
    group(lambda: laptop_local(m), (sx, sy - cm(1.5), sz), rot_x=STAND_TILT)
    studio.box("Phone", (0.72, 1.5, 0.08), (6.3, -1.2, TOP_Z + 0.04), m["phone"], bevel=0.06)
    edge_y = D / 2 + 0.03
    # 노트북 충전선: 상자 → 위로 → 뒤 모서리 → 거치대 뒤 → 노트북 오른쪽 옆면
    lap_port = (sx + 1.56, sy + cm(4), sz + cm(5.5))
    studio.cable("LaptopCable", [(c[0], bx_y, plug_top + cm(5)), (c[0], bx_y, plug_top + cm(8)),
                                 (c[0] - 0.1, edge_y + 0.05, H - 0.15), (c[0] - 0.1, edge_y + 0.03, TOP_Z + 0.02),
                                 (c[0] + 0.6, D / 2 - 0.5, TOP_Z + 0.02), (lap_port[0] + 0.25, lap_port[1] + 0.3, TOP_Z + 0.03),
                                 (lap_port[0] + 0.2, lap_port[1], lap_port[2] - 0.2), lap_port], m["cable"], radius=cm(0.25))
    ph_port = (6.3, -1.2 + 0.75, TOP_Z + 0.04)
    studio.cable("PhoneCable", [(c[2], bx_y, plug_top + cm(4)), (c[2], bx_y, plug_top + cm(7)),
                                (c[2] + 0.05, edge_y + 0.05, H - 0.15), (c[2] + 0.05, edge_y + 0.03, TOP_Z + 0.02),
                                (c[2] + 0.4, D / 2 - 0.8, TOP_Z + 0.02), (6.4, 0.2, TOP_Z + 0.02),
                                (ph_port[0], ph_port[1] + 0.25, TOP_Z + 0.02), ph_port], m["cable"], radius=cm(0.2))

    # 왼쪽 칸: 책, 노트, 펜
    book(-6.0, 1.2, TOP_Z, (1.7, 2.4, 0.3), m["book1"], m, rot=0.06)
    book(-6.0, 1.2, TOP_Z + 0.3, (1.5, 2.2, 0.22), m["book2"], m, rot=-0.04)
    book(-4.2, 1.5, TOP_Z, (1.48, 2.1, 0.08), m["dark"], m, rot=0.1)
    props.notebook(-3.3, -0.9, H, angle=0.04)
    props.pen(-2.1, -1.1, H, angle=0.5)

    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=96, resolution=res, view="Standard", exposure=-1.6)


if __name__ == "__main__":
    print(scene("004_in_use_front", (-4.0, -19.0, 14.5), (0.3, 0.3, 6.2), 38))
    print(scene("004_in_use_back", (11.0, 14.0, 10.0), (3.0, 1.5, 6.4), 35))
    print(scene("004_in_use_left", (-15.5, -4.5, 8.0), (-7.5, 0.0, 6.2), 35))
