"""001 책상 — 밝은 무채색 계열 비교 (람스 방향). 80×60 판 + 펼친 노트, A4, 펜.
기준: 상판 반사율 25~50%, 무광. 흰 종이(≈80%)와의 밝기 비율은 3:1 이내. 단위 1 = 10cm"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import props
import studio

CANDIDATES = [  # (이름, 선형 RGB ≈ 반사율, 표기)
    ("오프화이트", (0.72, 0.70, 0.65), "70% · 1.1:1"),
    ("람스 밝은 회색", (0.56, 0.55, 0.53), "55% · 1.5:1"),
    ("따뜻한 밝은 회색 ★", (0.47, 0.45, 0.41), "45% · 1.8:1"),
    ("실버 그레이", (0.39, 0.40, 0.42), "40% · 2.0:1"),
    ("베이지 회색", (0.38, 0.36, 0.31), "36% · 2.2:1"),
    ("웜 그레이", (0.29, 0.28, 0.26), "28% · 2.9:1"),
]
W, D, T = 8.0, 6.0, 0.25
GX, GY = 10.0, 9.0

studio.new_scene()
studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=4)
for i, (name, col, info) in enumerate(CANDIDATES):
    x, y = (i % 3 - 1) * GX, (0.5 - i // 3) * GY
    studio.box(f"Top_{i}", (W, D, T), (x, y, T / 2), studio.material(name, col, roughness=0.65), bevel=0.03)
    props.desk_set(x, y, T)
    studio.label(name, (x, y - D / 2 - 0.9, 0.01), size=0.7)
    studio.label(f"반사율 {info}", (x, y - D / 2 - 1.8, 0.01), size=0.5, color=(0.25, 0.25, 0.25))

studio.camera(target=(0, -0.8, 0), distance=26, height=34, angle_deg=0, lens=50)
print(studio.render("001_desk_colors_light", samples=64, resolution=(1500, 1150), view="Standard", exposure=-1.6))
