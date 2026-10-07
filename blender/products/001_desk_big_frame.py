"""001 큰 책상 160×60, 높이 72cm — 사각 다리 + 프레임.
A. 다리·프레임 = 상판과 같은 색 (모서리 끝)
B. 다리·프레임 = 알루미늄 (모서리 끝)
C. 알루미늄, 다리를 상판이 가장 덜 처지는 위치로 (양 끝에서 길이의 22.3% ≈ 36cm 안쪽)
흔들림(옆으로 밀릴 때)은 다리 위치가 아니라 다리-프레임 연결의 단단함이 막는다.
단위 1 = 10cm"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import props
import studio

W, D, T, H = 16.0, 6.0, 0.25, 7.2
LEG = 0.3            # 다리 3×3cm
FR_H, FR_T = 0.4, 0.2  # 프레임 높이 4cm, 두께 2cm
TOP_COLOR = (0.47, 0.45, 0.41)


def build(variant):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
    studio.box("Top", (W, D, T), (0, 0, H - T / 2), studio.material("Top", TOP_COLOR, roughness=0.65), bevel=0.015)
    if variant == "A":
        mat = studio.material("Frame", TOP_COLOR, roughness=0.5)
    else:
        mat = studio.material("Alu", (0.80, 0.80, 0.82), roughness=0.35, metallic=1.0)

    lx = W / 2 if variant != "C" else W / 2 - 0.223 * W   # 다리 바깥면의 x
    ly = D / 2 if variant != "C" else D / 2 - 0.5          # C는 앞뒤로도 5cm 들임
    leg_h = H - T
    for sx in (-1, 1):
        for sy in (-1, 1):
            studio.box("Leg", (LEG, LEG, leg_h), (sx * (lx - LEG / 2), sy * (ly - LEG / 2), leg_h / 2), mat)
    # 프레임: 다리 안쪽 면에 맞춰 네 변을 잇는다 (상판 바로 아래)
    fz = H - T - FR_H / 2
    inner_x, inner_y = lx - LEG, ly - LEG
    for sy in (-1, 1):   # 긴 쪽 (앞·뒤)
        studio.box("FrameLong", (2 * inner_x, FR_T, FR_H), (0, sy * (ly - LEG + FR_T / 2 + 0.05), fz), mat)
    for sx in (-1, 1):   # 짧은 쪽 (양옆)
        studio.box("FrameShort", (FR_T, 2 * inner_y, FR_H), (sx * (lx - LEG + FR_T / 2 + 0.05), 0, fz), mat)

    props.notebook(-3.5, -0.8, H, angle=0.05)
    props.paper(3.5, 0.3, H, angle=-0.1)
    props.pen(3.7, -0.4, H + 0.006, angle=0.6)
    studio.camera(target=(0, 0, 3.6), distance=24, height=6.5, angle_deg=-28, lens=40)
    return studio.render(f"001_desk_big_frame_{variant}", samples=64, resolution=(1000, 720), view="Standard", exposure=-1.6)


for v in "ABC":
    print(build(v))
