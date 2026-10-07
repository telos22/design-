"""003 책상 — 노트북과 휴대폰을 충전하는 모습.
충전기는 뒤 레일의 멀티탭 상자 안. 선은 상자 → 레일 아래 → 상판 뒤 모서리를 넘어 → 노트북·휴대폰.
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

spec = importlib.util.spec_from_file_location("dwb", os.path.join(HERE, "003_desk_with_boxes.py"))
dwb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dwb)
dk, bx, pb = dwb.dk, dwb.bx, dwb.pb
H, D = dk.H, dk.D


def laptop(x, y, m):
    """열린 노트북 (31 × 21.5cm), 화면 약 110°"""
    base = studio.box("LaptopBase", (3.1, 2.15, 0.15), (x, y, H + 0.075), m["alu"], bevel=0.03)
    studio.box("Keyboard", (2.7, 1.0, 0.005), (x, y + 0.25, H + 0.152), m["key"])
    studio.box("Trackpad", (1.1, 0.7, 0.004), (x, y - 0.6, H + 0.151), m["pad"])
    hinge_y, hinge_z = y + 1.075, H + 0.15
    screen = studio.box("Screen", (3.1, 2.1, 0.06), (0, 1.05, 0), m["alu"], bevel=0.02)
    glass = studio.box("Glass", (2.9, 1.9, 0.005), (0, 1.05, 0.032), m["glass"])
    pivot = bpy.data.objects.new("Hinge", None)
    bpy.context.collection.objects.link(pivot)
    screen.parent = glass.parent = pivot
    pivot.location = (x, hinge_y, hinge_z)
    pivot.rotation_euler.x = math.radians(70)   # 화면을 세워 뒤로 20° 젖힘 (키보드와 약 110°)
    return (x - 1.55, y + 0.6)   # 왼쪽 옆면 USB-C 위치


def phone(x, y, m):
    studio.box("Phone", (0.72, 1.5, 0.08), (x, y, H + 0.04), m["phone"], bevel=0.06)
    return (x, y + 0.75)        # 아래쪽 단자 (위쪽을 향해 둠)


def scene(name, cam_loc, target, lens):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    dk.desk(dk.materials(), holes=False)
    m = pb.mats()
    m.update({
        "alu": studio.material("Alu", (0.80, 0.80, 0.82), roughness=0.3, metallic=1.0),
        "key": studio.material("Keys", (0.05, 0.05, 0.06), roughness=0.6),
        "pad": studio.material("Pad", (0.70, 0.70, 0.72), roughness=0.4, metallic=0.6),
        "glass": studio.material("Glass", (0.02, 0.02, 0.025), roughness=0.08),
        "phone": studio.material("Phone", (0.04, 0.04, 0.045), roughness=0.2),
        "cable": studio.material("Cable", (0.85, 0.85, 0.83), roughness=0.5),
    })
    # 뒤 레일 멀티탭 상자 (충전기 2개)
    box_x = -0.5
    y0 = dwb.RAIL_IN_Y - bx.W / 2
    z0 = dwb.Z0

    def build():
        bx.box(0, 0, m)
        c = pb.strip(6, 0.15, 0, m)
        pb.plug(c[1], 0, m, "brick", (0, 0), rise=0.0)
        pb.plug(c[3], 0, m, "brick", (0, 0), rise=0.0)
    dwb.placed(build, (box_x, y0, z0), 0)
    c = [box_x + 0.15 - 2.5 * pb.PITCH + i * pb.PITCH for i in range(6)]

    lx, ly = laptop(1.8, -0.3, m)
    px, py = phone(4.6, -0.2, m)
    top_z = H + 0.012
    edge_y = D / 2 + 0.03
    under = dk.FZ - dk.FR_H / 2 - 0.05          # 레일 아래로 지나감
    charger_top = z0 + pb.T + 0.39 + 0.35
    for cx, (tx, ty), out_x in ((c[1], (lx, ly), lx - 0.6), (c[3], (px, py), px)):
        studio.cable("ChargeCable", [
            (cx, y0, charger_top), (cx, y0 + 0.2, charger_top + 0.05), (cx, y0 + 0.5, under),
            (cx, dk.IY + 0.1, under), (out_x, edge_y, under + 0.3), (out_x, edge_y, H - 0.1),
            (out_x, edge_y, top_z + 0.02), (out_x, D / 2 - 0.4, top_z), (tx - 0.3 if tx == lx else tx, ty + 0.5, top_z),
            (tx, ty, top_z + 0.02)], m["cable"], radius=0.022)

    props.notebook(-4.3, -0.9, H, angle=0.05)
    props.pen(-2.7, -1.2, H, angle=0.5)
    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=96, resolution=(1700, 1100), view="Standard", exposure=-1.6)


if __name__ == "__main__":
    print(scene("003_desk_charging_front", (-9.0, -17.0, 13.0), (1.0, 0.3, 6.0), 40))
    print(scene("003_desk_charging_back", (7.5, 13.5, 9.5), (1.5, 0.5, 6.4), 35))
