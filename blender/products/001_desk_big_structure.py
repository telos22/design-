"""001 큰 책상 — 구조 분해도.
상판: 자작합판 25mm + 양면 무광 마감재(따뜻한 밝은 회색)
프레임: 알루미늄 사각관 40×20×2mm, 다리 안쪽 면에 맞춰 네 변, 모서리 블록으로 다리와 볼트 결합
다리: 알루미늄 사각관 30×30×3mm, 투명 아노다이징(알루미늄 색 그대로)
발: 높이 조절 수평발 (다리 속에 숨김, ±1cm)
단위 1 = 10cm"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy
import studio

W, D, T, H = 16.0, 6.0, 0.25, 7.2
LEG, FR_H, FR_T = 0.3, 0.4, 0.2
LIFT_TOP, LIFT_FRAME = 2.6, 1.0      # 분해: 상판과 프레임을 띄운다

studio.new_scene()
studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
top = studio.material("Top", (0.47, 0.45, 0.41), roughness=0.65)
ply = studio.material("PlyEdge", (0.62, 0.48, 0.32), roughness=0.7)
alu = studio.material("Alu", (0.80, 0.80, 0.82), roughness=0.35, metallic=1.0)
dark = studio.material("Glide", (0.03, 0.03, 0.03), roughness=0.6)

# 상판: 합판 심 + 위아래 얇은 마감재
zt = H - T / 2 + LIFT_TOP
studio.box("Ply", (W, D, T - 0.02), (0, 0, zt), ply)
studio.box("SkinTop", (W, D, 0.01), (0, 0, zt + T / 2 - 0.005), top)
studio.box("SkinBottom", (W, D, 0.01), (0, 0, zt - T / 2 + 0.005), top)

# 프레임 + 모서리 블록
fz = H - T - FR_H / 2 + LIFT_FRAME
ix, iy = W / 2 - LEG, D / 2 - LEG
for sy in (-1, 1):
    studio.box("FrameLong", (2 * ix, FR_T, FR_H), (0, sy * (iy - FR_T / 2), fz), alu)
for sx in (-1, 1):
    studio.box("FrameShort", (FR_T, 2 * iy, FR_H), (sx * (ix - FR_T / 2), 0, fz), alu)
    for sy in (-1, 1):
        studio.box("CornerBlock", (0.5, 0.5, FR_H), (sx * (ix - 0.25), sy * (iy - 0.25), fz), alu)

# 다리 + 수평발
leg_h = H - T - 0.1
for sx in (-1, 1):
    for sy in (-1, 1):
        x, y = sx * (W / 2 - LEG / 2), sy * (D / 2 - LEG / 2)
        studio.box("Leg", (LEG, LEG, leg_h), (x, y, 0.1 + leg_h / 2), alu)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.1, depth=0.1, location=(x, y, 0.05))
        studio.assign(bpy.context.object, dark)

studio.camera(target=(0, 0, 4.8), distance=24, height=15, angle_deg=-30, lens=40)
print(studio.render("001_desk_big_structure", samples=64, resolution=(1300, 950), view="Standard", exposure=-1.6))
