"""001 책상 — 추천 색: 따뜻한 밝은 회색 (반사율 ≈45%, 무광).
No less: 권장 범위(25~50%) 안, 종이와 1.8:1 → 종이가 또렷하되 눈이 편하다.
No more: 무늬·광택·채도 없음 → 판이 물러나고 위의 것이 앞에 나온다 (람스 원칙 5).
단위 1 = 10cm"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import props
import studio

W, D, T = 8.0, 6.0, 0.25
studio.new_scene()
studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=4)
studio.box("Top", (W, D, T), (0, 0, T / 2), studio.material("WarmLightGrey", (0.47, 0.45, 0.41), roughness=0.65), bevel=0.03)
props.desk_set(0, 0, T)
studio.camera(target=(0, 0.2, 0), distance=10.5, height=7.5, angle_deg=-18, lens=50)
print(studio.render("001_desk_color_pick", samples=96, resolution=(1500, 1000), view="Standard", exposure=-1.6))
studio.save("001_desk_color_pick")
