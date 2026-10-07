"""001 큰 책상 160×60, 높이 72cm(고정) — 다리 모양 × 색 비교.
다리: 모서리에 딱 붙임 (책상끼리 붙이면 맞닿은 다리가 하나로 보이도록)
모양: 사각 3×3cm / 1/4 원 반지름 3.5cm
색: 상판과 같은 색 / 알루미늄 그대로 / 차콜
단위 1 = 10cm"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import props
import studio

W, D, T, H = 16.0, 6.0, 0.25, 7.2
TOP_COLOR = (0.47, 0.45, 0.41)


def leg_shape(kind, sx, sy):
    if kind == "square":
        s = 0.3
        pts = [(0, 0), (s, 0), (s, s), (0, s)]
    else:
        r = 0.35
        pts = [(0, 0)] + [(r * math.cos(i * math.pi / 24), r * math.sin(i * math.pi / 24)) for i in range(13)]
    pts = [(sx * x, sy * y) for x, y in pts]
    return pts[::-1] if sx * sy < 0 else pts


def leg_material(color):
    if color == "top":
        return studio.material("LegTop", TOP_COLOR, roughness=0.65)
    if color == "alu":
        return studio.material("LegAlu", (0.80, 0.80, 0.82), roughness=0.35, metallic=1.0)
    return studio.material("LegCharcoal", (0.05, 0.05, 0.055), roughness=0.5, metallic=0.3)


def build(kind, color):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    studio.box("Top", (W, D, T), (0, 0, H - T / 2), studio.material("Top", TOP_COLOR, roughness=0.65), bevel=0.015)
    mat = leg_material(color)
    for px, sx in ((-W / 2, 1), (W / 2, -1)):
        for py, sy in ((-D / 2, 1), (D / 2, -1)):
            studio.smooth_edges(studio.prism("Leg", leg_shape(kind, sx, sy), H - T, (px, py, 0), mat))
    props.notebook(-3.5, -0.8, H, angle=0.05)
    props.paper(3.5, 0.3, H, angle=-0.1)
    props.pen(3.7, -0.4, H + 0.006, angle=0.6)
    studio.camera(target=(0, 0, 3.8), distance=25, height=10, angle_deg=-28, lens=40)
    return studio.render(f"001_desk_big_{kind}_{color}", samples=48, resolution=(900, 680),
                         view="Standard", exposure=-1.6)


if not os.environ.get("CLOSEUP"):
    for kind in ("square", "quarter"):
        for color in ("top", "alu", "charcoal"):
            print(build(kind, color))


def closeup(kind):
    """앞 왼쪽 모서리 다리를 위에서 비스듬히 가까이"""
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    studio.box("Top", (W, D, T), (0, 0, H - T / 2), studio.material("Top", TOP_COLOR, roughness=0.65), bevel=0.015)
    mat = leg_material("charcoal")
    for px, sx in ((-W / 2, 1), (W / 2, -1)):
        for py, sy in ((-D / 2, 1), (D / 2, -1)):
            leg = studio.prism("Leg", leg_shape(kind, sx, sy), H - T, (px, py, 0), mat)
            studio.smooth_edges(leg)
    import mathutils   # 책상 안쪽(앉는 쪽 아래)에서 앞 왼쪽 모서리 다리를 본다
    cam = studio.camera(target=(0, 0, 0))
    cam.data.lens = 28
    cam.location = (-W / 2 + 4.0, -D / 2 + 3.4, 2.6)
    d = mathutils.Vector((-W / 2 + 0.2, -D / 2 + 0.2, 4.6)) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return studio.render(f"001_desk_big_{kind}_close", samples=48, resolution=(900, 680), view="Standard", exposure=-1.6)


if __name__ == "__main__" and os.environ.get("CLOSEUP"):
    for kind in ("square", "quarter"):
        print(closeup(kind))
