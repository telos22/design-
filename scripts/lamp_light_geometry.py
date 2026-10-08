"""조명 003 — 앉은 사람 기준, 빛이 어디서 어떤 모양으로 와야 하나 (몸체는 그리지 않음).
단위 cm. 책상 001: 높이 72, 깊이 60. 눈높이 120(WELL 앉은 눈높이 1.2m), 천장 260 가정.
오른손잡이 → 빛은 왼쪽, 조금 앞에서."""
import math

import matplotlib
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon, Rectangle

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False

DESK_H, DESK_D, CEIL = 72, 60, 260
EYE = (-30, 120)  # (앞뒤 y, 높이 z) — 책상 앞 모서리에서 30cm 뒤
TASK = (10, 35)  # 종이·키보드가 놓이는 깊이 범위
SRC = (-55, 10, 190)  # 빛이 나오는 곳 (x 왼쪽, y, z)
INK, RED, ORANGE, GREEN, GREY, LIGHT = "#222", "#d9534f", "#f0ad4e", "#3a9d5d", "#9a9a9a", "#f6d365"


def arrow(ax, a, b, color=LIGHT, lw=2.2, style="-|>"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=14, color=color, lw=lw))


def person_side(ax):
    ax.add_patch(Circle((-33, 130), 10, fc="white", ec=INK, lw=1.6))
    ax.plot([-36, -42], [119, 50], color=INK, lw=2.5)  # 몸통
    ax.plot([-42, 8, 8], [50, 52, 0], color=INK, lw=2.5)  # 허벅지, 정강이
    ax.plot([-37, -16, 14], [108, 80, 75], color=INK, lw=2.2)  # 팔
    ax.plot([-55, -20], [45, 45], color=GREY, lw=3)  # 의자 좌판
    ax.plot(*EYE, "o", color=INK, ms=5)


def desk_side(ax):
    ax.add_patch(Rectangle((0, DESK_H - 2.5), DESK_D, 2.5, fc="#c9c3b8", ec=INK))
    for y in (1.5, DESK_D - 1.5):
        ax.plot([y, y], [0, DESK_H - 2.5], color=INK, lw=2)


fig = plt.figure(figsize=(18, 11))
fig.suptitle("조명 003 — 앉은 사람에게 빛은 어디서, 어떤 모양으로 와야 하나 (몸체 없이 빛만)", fontsize=18, y=0.98)

# ---------------- 1. 옆에서 본 단면 ----------------
ax = fig.add_axes([0.04, 0.08, 0.44, 0.82])
ax.set_title("① 옆에서 (사람 → 책상 방향)", fontsize=14, loc="left")
ax.set_xlim(-80, 200); ax.set_ylim(0, 275); ax.set_aspect("equal")
ax.axhline(CEIL, color=GREY, lw=1.5); ax.text(195, CEIL + 4, "천장 260 (가정)", ha="right", fontsize=10, color=GREY)

# 눈부신 범위: 눈높이 수평선 ~ 위로 45°, 앞쪽
gz = EYE[1] + (CEIL - EYE[1])
y45 = EYE[0] + (CEIL - EYE[1])
ax.add_patch(Polygon([EYE, (200, EYE[1]), (200, CEIL), (y45, CEIL)], fc=ORANGE, alpha=0.18, ec=ORANGE, lw=1))
ax.text(150, 150, "눈부신 범위\n(눈높이 수평 ~ 위 45°)\n밝은 면이 여기 보이면 (피함)", fontsize=10.5, color="#b9770e", ha="center")

# 반사 구역: 작업면에서 정반사되어 눈으로 오는 빛의 출발 구역
ex, ez = EYE[0], EYE[1] - DESK_H
pts = []
for t in TASK:
    slope = ez / (t - ex)
    pts.append((t, DESK_H))
far = [(t + (CEIL - DESK_H) / (ez / (t - ex)), CEIL) for t in TASK]
ax.add_patch(Polygon([(TASK[0], DESK_H), (TASK[1], DESK_H), far[1], far[0]], fc=RED, alpha=0.20, ec=RED, hatch="//", lw=1))
ax.text(118, 215, "반사 구역 (정면 위)\n여기서 온 빛은 종이·화면에\n비쳐 눈으로 들어옴 (피함)", fontsize=10.5, color="#a94442", ha="center")
for t in TASK:
    ang = math.degrees(math.atan(ez / (t - ex)))
ax.text(40, 92, f"{math.degrees(math.atan(ez/(TASK[1]-ex))):.0f}°~{math.degrees(math.atan(ez/(TASK[0]-ex))):.0f}°", fontsize=10, color="#a94442")

desk_side(ax); person_side(ax)
ax.plot(TASK, [DESK_H + 0.8] * 2, color=GREEN, lw=6, solid_capstyle="butt")
ax.text(sum(TASK) / 2, DESK_H + 6, "쓰는 곳", ha="center", fontsize=10, color=GREEN)

# 이상적인 빛의 자리 (왼쪽으로 55cm 떨어진 곳을 옆에서 본 위치)
sy, sz = SRC[1], SRC[2]
ax.add_patch(Ellipse((sy, sz), 46, 16, fc=GREEN, alpha=0.30, ec=GREEN, lw=2))
ax.text(sy - 26, sz + 14, "빛나는 넓은 면\n(실제로는 왼쪽 55cm)", fontsize=10.5, color=GREEN)
arrow(ax, (sy + 4, sz - 8), (sum(TASK) / 2, DESK_H + 3))
for dx in (-30, 0, 30):
    arrow(ax, (sy + dx * 0.4, sz + 8), (sy + dx, CEIL - 3), lw=1.6)
ax.text(sy + 34, CEIL - 22, "위로: 천장이\n넓은 '하늘'이 됨", fontsize=10, color="#b98b00")
ax.text(EYE[0] - 5, EYE[1] + 22, "눈 120", fontsize=10, ha="right")
ax.text(DESK_D + 3, DESK_H - 8, "책상 72", fontsize=9)
ax.set_xlabel("앞뒤 (cm, 0 = 책상 앞 모서리)"); ax.set_ylabel("높이 (cm)")

# ---------------- 2. 뒤에서 본 모습 ----------------
ax = fig.add_axes([0.52, 0.50, 0.46, 0.42])
ax.set_title("② 사람 뒤에서 (왼쪽 = 사람의 왼쪽)", fontsize=14, loc="left")
ax.set_xlim(-100, 130); ax.set_ylim(0, 275); ax.set_aspect("equal")
ax.axhline(CEIL, color=GREY, lw=1.5)
ax.add_patch(Rectangle((-40, DESK_H - 2.5), 160, 2.5, fc="#c9c3b8", ec=INK))
for x in (-38.5, 118.5):
    ax.plot([x, x], [0, DESK_H - 2.5], color=INK, lw=2)
ax.plot([40, 40], [DESK_H, DESK_H + 3], color=GREY, lw=1); ax.text(0, 4, "왼쪽 칸 80", ha="center", fontsize=9, color=GREY); ax.text(80, 4, "오른쪽 칸 80", ha="center", fontsize=9, color=GREY)
ax.add_patch(Circle((0, 130), 10, fc="white", ec=INK, lw=1.6))
ax.plot([-20, 20], [108, 108], color=INK, lw=2.5); ax.plot([0, 0], [119, 50], color=INK, lw=2.5)
ax.plot([-20, -14], [108, 75], color=INK, lw=2); ax.plot([20, 12], [108, 75], color=INK, lw=2)
ax.text(14, 62, "오른손", fontsize=9)
# 눈에서 위 45° 선 (왼쪽)
ax.plot([0, -100], [EYE[1], EYE[1] + 100], color=ORANGE, lw=1.5, ls="--")
ax.text(-96, 158, "눈에서 위 45°", color="#b9770e", fontsize=10)
sx = SRC[0]
ax.add_patch(Ellipse((sx, sz), 34, 14, fc=GREEN, alpha=0.30, ec=GREEN, lw=2))
ax.text(-96, 226, "빛나는 면", fontsize=10.5, color=GREEN)
arrow(ax, (sx + 8, sz - 6), (-5, DESK_H + 3)); arrow(ax, (sx + 4, sz - 6), (-28, DESK_H + 3), lw=1.5)
ax.add_patch(Ellipse((24, DESK_H + 1), 18, 3, fc="#555", alpha=0.5))
ax.text(36, DESK_H + 10, "손 그림자는 오른쪽으로\n→ 쓰는 곳은 밝다", fontsize=10)
el = math.degrees(math.atan((sz - EYE[1]) / math.hypot(sx, sy - EYE[0])))
ax.text(22, 200, f"눈에서 올려다본 각 약 {el:.0f}°\n(45° 위 → 밝은 면이 시야 밖)", fontsize=10, color=GREEN)

# ---------------- 3. 위에서 본 평면 ----------------
ax = fig.add_axes([0.52, 0.05, 0.46, 0.36])
ax.set_title("③ 위에서", fontsize=14, loc="left")
ax.set_xlim(-100, 130); ax.set_ylim(-60, 75); ax.set_aspect("equal")
ax.add_patch(Rectangle((-40, 0), 160, DESK_D, fc="#e8e3d9", ec=INK))
ax.add_patch(Rectangle((-25, TASK[0]), 50, TASK[1] - TASK[0], fc=GREEN, alpha=0.35, ec=GREEN))
ax.text(0, 22, "쓰는 곳", ha="center", fontsize=10, color=GREEN)
ax.add_patch(Rectangle((-25, TASK[0]), 50, 75 - TASK[0], fc=RED, alpha=0.12, ec=RED, hatch="//", lw=0.8))
ax.text(0, 52, "반사 구역\n(눈-쓰는 곳 앞쪽)", ha="center", fontsize=9.5, color="#a94442")
ax.add_patch(Circle((0, EYE[0]), 11, fc="white", ec=INK, lw=1.6)); ax.text(0, -50, "사람", ha="center", fontsize=10)
ax.add_patch(Ellipse((sx, sy), 20, 44, fc=GREEN, alpha=0.30, ec=GREEN, lw=2))
ax.text(sx - 2, sy + 28, "빛나는 면\n(왼쪽, 조금 앞)", ha="center", fontsize=10, color=GREEN)
arrow(ax, (sx + 9, sy + 2), (-18, 22))
ax.text(122, -55, "책상 001: 160 × 60", ha="right", fontsize=9, color=GREY)

out = "concepts/img/lamp_light_geometry.png"
fig.savefig(out, dpi=90, facecolor="white")
print(out, f"elevation={el:.1f}")
