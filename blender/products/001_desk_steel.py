"""001 큰 책상 — 강철 프레임 + 자석 수납 + 구멍에 거는 고리.
다리: 알루미늄 그대로 30×30mm / 프레임: 강철 사각관 40×20mm, 분체도장(상판과 같은 따뜻한 회색)
프레임 안쪽 면(뒤·옆 레일)에 세로 구멍 5×20mm, 50mm 간격 → 무거운 것(가방)은 고리를 꽂아 건다
가벼운 것(전원 박스, 필기구 트레이)은 고무 씌운 자석으로 아무 데나 붙인다. 앞 레일은 비워 둔다(허벅지 공간)
단위 1 = 10cm"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy
import mathutils
import props
import studio

W, D, T, H = 16.0, 6.0, 0.25, 7.2
LEG, FR_H, FR_T = 0.3, 0.4, 0.2
IX, IY = W / 2 - LEG, D / 2 - LEG
FZ = H - T - FR_H / 2
PITCH = 0.5


def materials():
    return {
        "top": studio.material("Top", (0.47, 0.45, 0.41), roughness=0.65),
        "ply": studio.material("PlyEdge", (0.62, 0.48, 0.32), roughness=0.7),
        "alu": studio.material("Alu", (0.80, 0.80, 0.82), roughness=0.35, metallic=1.0),
        "steel": studio.material("SteelPowder", (0.47, 0.45, 0.41), roughness=0.5),
        "hole": studio.material("Hole", (0.01, 0.01, 0.01), roughness=0.9),
        "acc": studio.material("Accessory", (0.47, 0.45, 0.41), roughness=0.5),
        "white": studio.material("Plastic", (0.75, 0.75, 0.73), roughness=0.5),
        "pen": studio.material("Pen", (0.03, 0.03, 0.035), roughness=0.3),
        "pencil": studio.material("Pencil", (0.7, 0.5, 0.08), roughness=0.6),
        "bag": studio.material("Bag", (0.08, 0.09, 0.10), roughness=0.9),
    }


def desk(m, holes=True):
    zt = H - T / 2
    studio.box("Ply", (W, D, T - 0.02), (0, 0, zt), m["ply"])
    studio.box("SkinTop", (W, D, 0.01), (0, 0, zt + T / 2 - 0.005), m["top"])
    studio.box("SkinBottom", (W, D, 0.01), (0, 0, zt - T / 2 + 0.005), m["top"])
    for s in (-1, 1):
        studio.box("RailLong", (2 * IX, FR_T, FR_H), (0, s * (IY - FR_T / 2), FZ), m["steel"])
        studio.box("RailShort", (FR_T, 2 * IY, FR_H), (s * (IX - FR_T / 2), 0, FZ), m["steel"])
    # 구멍: 뒤 레일(+y)과 양옆 레일의 안쪽 면
    n = int((2 * IX - 0.6) / PITCH) if holes else -1
    for i in range(n + 1):
        x = -IX + 0.3 + i * PITCH
        studio.box("HoleBack", (0.05, 0.012, 0.2), (x, IY - FR_T - 0.004, FZ), m["hole"])
    n = int((2 * IY - 0.6) / PITCH) if holes else -1
    for s in (-1, 1):
        for i in range(n + 1):
            y = -IY + 0.3 + i * PITCH
            studio.box("HoleSide", (0.012, 0.05, 0.2), (s * (IX - FR_T - 0.004), y, FZ), m["hole"])
    for sx in (-1, 1):
        for sy in (-1, 1):
            studio.box("Leg", (LEG, LEG, H - T), (sx * (W / 2 - LEG / 2), sy * (D / 2 - LEG / 2), (H - T) / 2), m["alu"])


def open_box(name, size, center, mat, t=0.03):
    w, d, h = size
    x, y, z = center
    studio.box(name, (w, d, t), (x, y, z - h / 2), mat)
    for sy in (-1, 1):
        studio.box(name, (w, t, h), (x, y + sy * (d / 2 - t / 2), z), mat)
    for sx in (-1, 1):
        studio.box(name, (t, d, h), (x + sx * (w / 2 - t / 2), y, z), mat)


def power_box(x, m):
    """자석: 뒤 레일 안쪽 면에 상자 뒷벽이 붙는다"""
    w, d, h = 3.5, 1.2, 0.7
    y = IY - FR_T - d / 2
    z = FZ + FR_H / 2 - h / 2
    open_box("PowerBox", (w, d, h), (x, y, z), m["acc"])
    studio.box("PowerStrip", (2.6, 0.5, 0.4), (x - 0.2, y, z - h / 2 + 0.22), m["white"], bevel=0.05)
    studio.box("Charger", (0.6, 0.6, 0.3), (x + 1.2, y + 0.2, z - h / 2 + 0.17), m["white"], bevel=0.06)
    studio.cable("Cable", [(x + 1.2, y + 0.2, z), (x + 1.2, D / 2 + 0.05, H - 0.4), (x + 1.2, D / 2 + 0.05, H + 0.02),
           (x + 0.8, D / 2 - 0.6, H + 0.02), (x + 0.2, -0.2, H + 0.02)], m["white"])


def pen_tray(y, m, side=-1):
    """자석: 옆 레일 안쪽 면, 앞쪽"""
    w, d, h = 0.7, 2.0, 0.4
    x = side * (IX - FR_T - w / 2)
    z = FZ + FR_H / 2 - h / 2
    open_box("PenTray", (w, d, h), (x, y, z), m["acc"], t=0.025)
    for i, dx in enumerate((-0.18, 0.0, 0.18)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.045, depth=1.5, location=(x + dx, y, z - h / 2 + 0.08))
        bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
        studio.assign(bpy.context.object, m["pencil"] if i == 1 else m["pen"])


def hook_with_bag(y, m, side=1):
    """구멍에 꽂는 고리 + 가방"""
    x = side * (IX - FR_T)
    studio.box("HookTab", (0.06, 0.04, 0.18), (x + side * 0.02, y, FZ), m["acc"])       # 구멍 속으로
    studio.box("HookStem", (0.04, 0.12, 0.6), (x - side * 0.03, y, FZ - 0.25), m["acc"])
    studio.box("HookLip", (0.3, 0.12, 0.04), (x - side * 0.18, y, FZ - 0.55), m["acc"])
    studio.box("HookTip", (0.04, 0.12, 0.15), (x - side * 0.31, y, FZ - 0.48), m["acc"])
    studio.box("BagStrap", (0.2, 0.08, 0.5), (x - side * 0.18, y, FZ - 0.8), m["bag"])
    studio.box("Bag", (1.0, 3.4, 2.8), (x - side * 0.55, y, FZ - 2.4), m["bag"], bevel=0.12)


def build(name, cam_loc, cam_target, lens, res=(1600, 1050)):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    m = materials()
    desk(m)
    power_box(3.0, m)
    pen_tray(-1.6, m, side=-1)
    hook_with_bag(0.6, m, side=1)
    studio.box("Laptop", (3.1, 2.15, 0.16), (3.2, -0.6, H + 0.08), m["alu"], bevel=0.04)
    props.notebook(-3.5, -0.8, H, angle=0.05)
    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(cam_target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=64, resolution=res, view="Standard", exposure=-1.6)


if __name__ == "__main__":
    print(build("001_desk_steel_hero", (-13.0, -21.0, 12.5), (0.6, 0.0, 4.2), 40))      # 전체 모습
    print(build("001_desk_steel_under", (7.5, 14.5, 3.6), (0.5, 0.0, 6.0), 26))         # 뒤쪽 아래: 구멍·자석 수납
