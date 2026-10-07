"""002 멀티탭 상자 — A안: 위가 열린 얕은 쟁반.
책상 프레임(강철) 안쪽에 자석으로 붙인다. 떼서 꽂고 다시 붙인다.
- 뒷벽 6cm (자석 2개, 프레임에 붙는 면) / 앞 턱 2.5cm / 옆판은 뒤에서 앞으로 비스듬히 낮아짐
- 한쪽 옆판 아래 홈: 멀티탭 꼬리(전원선)가 나감
- 위가 열려 있어 플러그 선이 위로 빠지고 열도 빠진다
- 긴 것: 6구 멀티탭(42cm) → 상자 46 × 8 × 6cm / 짧은 것: 3구(25cm) → 29 × 8 × 6cm
- 재질: 알루미늄 판 1.5mm 접기, 분체도장(책상과 같은 따뜻한 회색)
단위 1 = 10cm"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy
import mathutils
import studio

T = 0.015                  # 판 두께 1.5mm
W, H_BACK, H_FRONT = 0.8, 0.6, 0.25
PITCH = 0.63


def mats():
    return {
        "box": studio.material("BoxPowder", (0.47, 0.45, 0.41), roughness=0.5),
        "strip": studio.material("Strip", (0.78, 0.78, 0.76), roughness=0.45),
        "socket": studio.material("Socket", (0.55, 0.55, 0.53), roughness=0.5),
        "hole": studio.material("Hole", (0.02, 0.02, 0.02), roughness=0.9),
        "plug": studio.material("Plug", (0.80, 0.80, 0.78), roughness=0.4),
        "dark": studio.material("Dark", (0.04, 0.04, 0.045), roughness=0.5),
        "magnet": studio.material("Rubber", (0.02, 0.02, 0.02), roughness=0.8),
    }


def box(length, x0, y0, m):
    """x0, y0: 상자 중심. 앞(사람 쪽) = -y, 뒤(프레임 쪽) = +y"""
    L = length
    studio.box("Bottom", (L, W, T), (x0, y0, T / 2), m["box"])
    studio.box("Back", (L, T, H_BACK), (x0, y0 + W / 2 - T / 2, H_BACK / 2), m["box"])
    studio.box("Front", (L, T, H_FRONT), (x0, y0 - W / 2 + T / 2, H_FRONT / 2), m["box"])
    side = [(-W / 2, 0), (W / 2, 0), (W / 2, H_BACK), (-W / 2, H_FRONT)]
    notch = [(-W / 2, 0), (0.05, 0), (0.05, 0.12), (0.19, 0.12), (0.19, 0), (W / 2, 0), (W / 2, H_BACK), (-W / 2, H_FRONT)]
    studio.extrude_x("SideTail", [(y0 + y, z) for y, z in notch], x0 - L / 2, x0 - L / 2 + T, m["box"])
    studio.extrude_x("Side", [(y0 + y, z) for y, z in side], x0 + L / 2 - T, x0 + L / 2, m["box"])
    for sx in (-1, 1):   # 뒷면 자석 (지름 3cm)
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.15, depth=0.07,
                                            location=(x0 + sx * (L / 2 - 0.7), y0 + W / 2 + 0.035, 0.38))
        bpy.context.object.rotation_euler = (math.pi / 2, 0, 0)
        studio.assign(bpy.context.object, m["magnet"])


def strip(n, x0, y0, m):
    """n구 멀티탭, 콘센트가 위를 향함. 꼬리는 -x 끝."""
    L = n * PITCH + 0.32
    studio.box("Strip", (L, 0.55, 0.38), (x0, y0, T + 0.19), m["strip"], bevel=0.06)
    centers = [x0 - (n - 1) * PITCH / 2 + i * PITCH for i in range(n)]
    for cx in centers:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.2, depth=0.02, location=(cx, y0, T + 0.385))
        studio.assign(bpy.context.object, m["socket"])
        for dx in (-0.095, 0.095):
            bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.025, depth=0.01, location=(cx + dx, y0, T + 0.396))
            studio.assign(bpy.context.object, m["hole"])
    # 꼬리: 멀티탭 끝 → 옆판 홈 → 밖으로
    xe = x0 - L / 2
    studio.cable("Tail", [(xe, y0, T + 0.12), (xe - 0.15, y0 + 0.05, T + 0.06), (xe - 0.3, y0 + 0.05, T + 0.06),
                          (xe - 0.9, y0 + 0.3, 0.03), (xe - 1.6, y0 + 0.6, 0.03)], m["strip"], radius=0.035)
    return centers


def plug(cx, y0, m, kind, cord_to):
    """꽂힌 플러그와 위로 빠지는 선. kind: 'plug' 둥근 플러그 / 'brick' 충전기 일체형"""
    z = T + 0.39
    if kind == "brick":
        studio.box("Charger", (0.55, 0.5, 0.35), (cx, y0, z + 0.175), m["plug"], bevel=0.05)
        top = z + 0.35
    else:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.19, depth=0.28, location=(cx, y0, z + 0.14))
        studio.assign(bpy.context.object, m["dark"])
        studio.smooth_edges(bpy.context.object)
        top = z + 0.28
    studio.cable("Cord", [(cx, y0, top), (cx, y0, top + 0.25), (cx + cord_to[0] * 0.3, y0 + cord_to[1] * 0.3, top + 0.5),
                          (cx + cord_to[0], y0 + cord_to[1], top + 0.7)], m["dark"] if kind == "plug" else m["plug"], radius=0.025)


def scene(name, cam_loc, cam_target, lens, contents=True):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=1.2)
    m = mats()
    # 긴 것 (뒤), 짧은 것 (앞)
    box(4.6, 0.0, 0.7, m)
    box(2.9, -0.4, -0.7, m)
    if contents:
        c = strip(6, 0.15, 0.7, m)
        plug(c[0], 0.7, m, "brick", (0.2, 0.6))
        plug(c[2], 0.7, m, "plug", (0.0, 0.8))
        plug(c[4], 0.7, m, "brick", (-0.2, 0.7))
        c = strip(3, -0.25, -0.7, m)
        plug(c[1], -0.7, m, "brick", (0.1, 0.6))
    cam = studio.camera(target=(0, 0, 0), lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(cam_target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=96, resolution=(1600, 1100), view="Standard", exposure=-1.2)


if __name__ == "__main__":
    print(scene("002_power_box_front", (-3.2, -7.5, 5.2), (0.0, 0.0, 0.25), 50))
    print(scene("002_power_box_back", (4.2, 7.0, 3.0), (0.0, 0.0, 0.3), 50, contents=True))
    print(scene("002_power_box_empty", (-3.2, -7.5, 5.2), (0.0, 0.0, 0.25), 50, contents=False))
