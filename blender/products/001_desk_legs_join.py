"""001 책상 — 모서리 다리 4개: 판 두 개를 붙였을 때 '하나'로 보이는가.
A. 안쪽으로 들어간 다리: 이음새에 다리 두 개가 떨어져 보인다
B. 모서리에 딱 붙은 사각 다리: 두 다리가 맞붙어 하나의 넓은 다리가 된다
C. 모서리에 딱 붙은 1/4 원 다리: 둘이면 반원, 넷이면 원 하나가 된다
판 80×60, 높이 72cm, 단위 1 = 10cm"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import studio

W, D, T, H = 8.0, 6.0, 0.25, 7.2
LEG = H - T


def leg_points(variant, sx, sy):
    """판 모서리(원점)에서 판 안쪽 방향(sx, sy = ±1)으로 그린 다리 단면"""
    if variant == "A":   # 4cm 각, 모서리에서 5cm 안쪽
        o, s = 0.5, 0.4
        pts = [(o, o), (o + s, o), (o + s, o + s), (o, o + s)]
    elif variant == "B":  # 3cm 각, 모서리에 딱 붙음
        s = 0.3
        pts = [(0, 0), (s, 0), (s, s), (0, s)]
    else:                 # 반지름 3.5cm 1/4 원, 직각 꼭짓점이 판 모서리
        r = 0.35
        pts = [(0, 0)] + [(r * math.cos(t), r * math.sin(t)) for t in [i * math.pi / 2 / 12 for i in range(13)]]
    pts = [(sx * x, sy * y) for x, y in pts]
    if sx * sy < 0:       # 뒤집히면 면 방향이 바뀌므로 순서 반전
        pts = pts[::-1]
    return pts


def build(variant):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    top = studio.material("WarmLightGrey", (0.47, 0.45, 0.41), roughness=0.65)
    metal = studio.material("Leg", (0.06, 0.06, 0.065), roughness=0.45, metallic=0.6)
    for cx in (-W / 2, W / 2):
        studio.box("Top", (W - 0.004, D, T), (cx, 0, H - T / 2), top, bevel=0.015)
        x0, x1, y0, y1 = cx - W / 2, cx + W / 2, -D / 2, D / 2
        for (px, sx) in ((x0, 1), (x1, -1)):
            for (py, sy) in ((y0, 1), (y1, -1)):
                studio.prism("Leg", leg_points(variant, sx, sy), LEG, (px, py, 0), metal)
    studio.camera(target=(0, 0, 3.4), distance=24, height=8.5, angle_deg=-25, lens=40)
    return studio.render(f"001_desk_legs_join_{variant}", samples=64, resolution=(1000, 760),
                         view="Standard", exposure=-1.6)


for v in "ABC":
    print(build(v))
