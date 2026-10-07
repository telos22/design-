"""001 큰 책상 — 프레임 레일 + 끼우는 수납.
프레임(알루미늄 40×20mm)의 안쪽 면에 홈(폭 6mm)을 길게 내서, 아무 위치에나 끼워 고정한다.
- 전원 박스: 뒤쪽 레일. 멀티탭·충전기를 넣는다 (35×12×7cm)
- 가방 고리: 옆 레일
- 필기구 트레이: 옆 레일 앞쪽 (20×7×4cm)
앞쪽 레일에는 걸지 않는다 → 허벅지 공간 (프레임 아래 ≈ 65.5cm)
단위 1 = 10cm"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy
import props
import studio

W, D, T, H = 16.0, 6.0, 0.25, 7.2
LEG, FR_H, FR_T = 0.3, 0.4, 0.2
IX, IY = W / 2 - LEG, D / 2 - LEG       # 프레임 바깥면 위치 (다리 안쪽 면)
FZ = H - T - FR_H / 2                   # 프레임 중심 높이


def desk(mats):
    top, ply, alu, groove = mats["top"], mats["ply"], mats["alu"], mats["groove"]
    zt = H - T / 2
    studio.box("Ply", (W, D, T - 0.02), (0, 0, zt), ply)
    studio.box("SkinTop", (W, D, 0.01), (0, 0, zt + T / 2 - 0.005), top)
    studio.box("SkinBottom", (W, D, 0.01), (0, 0, zt - T / 2 + 0.005), top)
    for s in (-1, 1):
        # 긴 레일(앞·뒤)과 짧은 레일(양옆), 안쪽 면에 홈
        studio.box("RailLong", (2 * IX, FR_T, FR_H), (0, s * (IY - FR_T / 2), FZ), alu)
        studio.box("GrooveLong", (2 * IX - 0.4, 0.01, 0.06), (0, s * (IY - FR_T - 0.004), FZ), groove)
        studio.box("RailShort", (FR_T, 2 * IY, FR_H), (s * (IX - FR_T / 2), 0, FZ), alu)
        studio.box("GrooveShort", (0.01, 2 * IY - 0.4, 0.06), (s * (IX - FR_T - 0.004), 0, FZ), groove)
    for sx in (-1, 1):
        for sy in (-1, 1):
            studio.box("Leg", (LEG, LEG, H - T), (sx * (W / 2 - LEG / 2), sy * (D / 2 - LEG / 2), (H - T) / 2), alu)


def power_box(x, mats):
    """뒤쪽 레일 안쪽에 거는 위가 열린 상자 + 안에 멀티탭, 충전기, 노트북으로 올라가는 선"""
    y = IY - FR_T - 0.6
    z = FZ - FR_H / 2 - 0.35
    w, d, h, t = 3.5, 1.2, 0.7, 0.03
    studio.box("BoxBottom", (w, d, t), (x, y, z - h / 2), mats["alu"])
    for sy in (-1, 1):
        studio.box("BoxWall", (w, t, h), (x, y + sy * (d / 2 - t / 2), z), mats["alu"])
    for sx in (-1, 1):
        studio.box("BoxWall", (t, d, h), (x + sx * (w / 2 - t / 2), y, z), mats["alu"])
    studio.box("Hanger", (w * 0.8, 0.03, 0.55), (x, IY - FR_T - 0.015, FZ - 0.05), mats["alu"])
    studio.box("PowerStrip", (2.6, 0.5, 0.4), (x - 0.2, y, z - h / 2 + 0.22), mats["white"], bevel=0.05)
    studio.box("Charger", (0.6, 0.6, 0.3), (x + 1.2, y + 0.2, z - h / 2 + 0.17), mats["white"], bevel=0.06)
    # 충전선: 상자 → 뒤쪽 가장자리를 넘어 → 노트북
    pts = [(x + 1.2, y + 0.2, z), (x + 1.2, D / 2 + 0.05, H - 0.4), (x + 1.2, D / 2 + 0.05, H + 0.02),
           (x + 0.8, D / 2 - 0.6, H + 0.02), (x + 0.2, -0.2, H + 0.02)]
    cable(pts, mats["white"])


def cable(points, mat):
    curve = bpy.data.curves.new("Cable", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.02
    spline = curve.splines.new("NURBS")
    spline.points.add(len(points) - 1)
    for p, co in zip(spline.points, points):
        p.co = (*co, 1)
    spline.use_endpoint_u = True
    spline.order_u = 3
    obj = bpy.data.objects.new("Cable", curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)


def bag_hook(y, mats, side=1):
    """옆 레일에 거는 J자 고리"""
    x = side * (IX - FR_T - 0.05)
    studio.box("HookPlate", (0.04, 0.3, 0.5), (x, y, FZ - 0.05), mats["alu"])
    studio.box("HookStem", (0.04, 0.3, 0.9), (x - side * 0.02, y, FZ - 0.7), mats["alu"])
    studio.box("HookLip", (0.35, 0.3, 0.04), (x - side * 0.19, y, FZ - 1.13), mats["alu"])
    studio.box("HookTip", (0.04, 0.3, 0.25), (x - side * 0.36, y, FZ - 1.02), mats["alu"])


def pen_tray(y, mats, side=-1):
    """옆 레일 앞쪽에 거는 얕은 트레이 + 펜·연필"""
    x = side * (IX - FR_T - 0.4)
    z = FZ - FR_H / 2 - 0.2
    w, d, h, t = 0.7, 2.0, 0.4, 0.025
    studio.box("TrayBottom", (w, d, t), (x, y, z - h / 2), mats["alu"])
    for sx in (-1, 1):
        studio.box("TrayWall", (t, d, h), (x + sx * (w / 2 - t / 2), y, z), mats["alu"])
    for sy in (-1, 1):
        studio.box("TrayWall", (w, t, h), (x, y + sy * (d / 2 - t / 2), z), mats["alu"])
    studio.box("TrayHanger", (0.03, d * 0.7, 0.5), (side * (IX - FR_T - 0.015), y, FZ - 0.05), mats["alu"])
    for i, dx in enumerate((-0.18, 0.0, 0.18)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.045, depth=1.5, location=(x + dx, y, z - h / 2 + 0.08))
        bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
        studio.assign(bpy.context.object, mats["pen"] if i != 1 else mats["pencil"])


def scene(name, cam_loc, cam_target, lens):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    mats = {
        "top": studio.material("Top", (0.47, 0.45, 0.41), roughness=0.65),
        "ply": studio.material("PlyEdge", (0.62, 0.48, 0.32), roughness=0.7),
        "alu": studio.material("Alu", (0.80, 0.80, 0.82), roughness=0.35, metallic=1.0),
        "groove": studio.material("Groove", (0.02, 0.02, 0.02), roughness=0.8),
        "white": studio.material("Plastic", (0.75, 0.75, 0.73), roughness=0.5),
        "pen": studio.material("Pen", (0.03, 0.03, 0.035), roughness=0.3),
        "pencil": studio.material("Pencil", (0.7, 0.5, 0.08), roughness=0.6),
    }
    desk(mats)
    power_box(3.0, mats)
    bag_hook(1.2, mats, side=1)
    pen_tray(-1.0, mats, side=-1)
    # 위에는 노트북만 (닫힌 노트북 대신 얇은 판)
    studio.box("Laptop", (3.1, 2.15, 0.16), (3.2, -0.6, H + 0.08), mats["alu"], bevel=0.04)
    props.notebook(-3.5, -0.8, H, angle=0.05)
    import mathutils
    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(cam_target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=64, resolution=(1500, 1000), view="Standard", exposure=-1.6)


print(scene("001_desk_rail_front", (-9.0, -17.0, 5.0), (0.5, 1.0, 5.6), 30))   # 앞에서 낮게: 책상 아래가 보이게
print(scene("001_desk_rail_back", (8.5, 15.0, 4.6), (1.5, 0.5, 5.6), 30))       # 뒤에서: 전원 박스와 선
print(scene("001_desk_rail_below", (0.0, 0.01, 0.4), (0.0, 0.0, 6.0), 14))     # 바닥에서 올려다보기
