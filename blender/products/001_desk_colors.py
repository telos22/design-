"""001 책상 — 상판 색 비교. 80×60 판 위에 A4 종이와 펜.
기준: 상판 반사율 25~50%, 무광 (notes/color-surface.md). 색 값은 선형 RGB로 반사율을 맞췄다.
단위: 1 = 10cm"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import studio

CANDIDATES = [  # (이름, 선형 RGB, 나무결 여부, 대략 반사율)
    ("흰색", (0.85, 0.85, 0.84), False, "85%"),
    ("밝은 오크", (0.58, 0.37, 0.19), True, "40%"),
    ("베이지 회색", (0.36, 0.33, 0.27), False, "33%"),
    ("중간 회색", (0.22, 0.22, 0.22), False, "22%"),
    ("월넛", (0.20, 0.095, 0.045), True, "11%"),
    ("검정", (0.045, 0.045, 0.045), False, "5%"),
]
W, D, T = 8.0, 6.0, 0.25
GX, GY = 10.0, 9.0

studio.new_scene()
studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=4)
paper = studio.material("Paper", (0.8, 0.8, 0.78), roughness=0.9)
ink = studio.material("Pen", (0.03, 0.03, 0.035), roughness=0.3, metallic=0.3)

for i, (name, col, grain, refl) in enumerate(CANDIDATES):
    x = (i % 3 - 1) * GX
    y = (0.5 - i // 3) * GY
    mat = studio.wood(name, col, scale=1.0) if grain else studio.material(name, col, roughness=0.6)
    studio.box(f"Top_{i}", (W, D, T), (x, y, T / 2), mat, bevel=0.03)
    # A4 (21 x 29.7cm) 를 살짝 비스듬히, 펜 하나
    sheet = studio.box(f"A4_{i}", (2.1, 2.97, 0.005), (x - 1.2, y, T + 0.003), paper)
    sheet.rotation_euler.z = 0.12
    pen = studio.box(f"Pen_{i}", (1.4, 0.09, 0.09), (x + 1.8, y - 0.6, T + 0.045), ink, bevel=0.03)
    pen.rotation_euler.z = 0.5
    studio.label(f"{name}  {refl}", (x, y - D / 2 - 1.1, 0.01), size=0.75)

studio.camera(target=(0, -0.5, 0), distance=26, height=34, angle_deg=0, lens=50)
print(studio.render("001_desk_colors", samples=64, resolution=(1500, 1100), view="Standard", exposure=-1.6))
