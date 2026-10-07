"""책상 상판 곡선안 A1/A2/A3 비교 — 위에서 본 평면도 (단위 cm, 앉은 사람 기준)."""
import os

import matplotlib
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon
from matplotlib.path import Path

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
OUT = os.path.join(os.path.dirname(__file__), "..", "concepts", "img", "desk_shapes_A.png")

R_IN = 25      # 몸 중심 ~ 상판 안쪽 가장자리
EASY = 50      # 편하게 닿는 거리
MAX = 70       # 팔을 뻗어 최대로 닿는 거리
th = np.radians(np.linspace(-90, 90, 181))   # 0 = 정면, ±90 = 양옆


def arc(r):
    r = np.broadcast_to(r, th.shape)
    return np.c_[r * np.sin(th), r * np.cos(th)]


inner = arc(R_IN)[::-1]
shapes = {
    "A1  앞만 오목 · 뒤는 직선": np.r_[inner, [[MAX, 0], [MAX, MAX], [-MAX, MAX], [-MAX, 0]]],
    "A2  초승달 · 앞뒤 모두 곡선": np.r_[inner, arc(MAX)],
    "A3  가운데 얕고 양 끝 깊은 곡선": np.r_[inner, arc(55 + 30 * (np.abs(th) / (np.pi / 2)) ** 2)],
}

fig, axes = plt.subplots(1, 3, figsize=(16, 6.4))
gx, gy = np.meshgrid(np.linspace(-100, 100, 600), np.linspace(-10, 100, 330))
pts = np.c_[gx.ravel(), gy.ravel()]
for ax, (title, poly) in zip(axes, shapes.items()):
    inside = Path(poly).contains_points(pts)
    lost = inside & (np.hypot(pts[:, 0], pts[:, 1]) > MAX)
    pct = 100 * lost.sum() / inside.sum()

    desk = Polygon(poly, closed=True, fc="#d9534f", ec="#5a4632", lw=2)
    ax.add_patch(desk)
    reach = Circle((0, 0), MAX, fc="#c8a37a", ec="none")
    ax.add_patch(reach)
    reach.set_clip_path(desk)
    ax.add_patch(Polygon(poly, closed=True, fill=False, ec="#5a4632", lw=2))
    for r, c, lbl in ((EASY, "#2e7d32", "편하게 닿음 50cm"), (MAX, "#e08a00", "최대로 닿음 70cm")):
        ax.add_patch(Circle((0, 0), r, fill=False, ec=c, ls="--", lw=1.4))
        ax.text(0, r + 1.5, lbl, color=c, ha="center", fontsize=9)
    ax.add_patch(Ellipse((0, 0), 42, 22, fc="#555", ec="none"))
    ax.add_patch(Circle((0, 0), 9, fc="#888", ec="none"))
    ax.text(0, -18, "앉은 사람", ha="center", fontsize=9)

    ax.set_title(title, fontsize=13, pad=10)
    ax.text(0, -30, f"손이 안 닿는 면적 (빨강): {pct:.0f}%", ha="center", fontsize=11,
            color="#d9534f" if pct else "#2e7d32", weight="bold")
    ax.set_xlim(-100, 100); ax.set_ylim(-38, 100)
    ax.set_aspect("equal"); ax.axis("off")

fig.suptitle("책상 상판 — 위에서 본 모습 (단위 cm)", fontsize=15)
fig.tight_layout()
fig.savefig(OUT, dpi=110, facecolor="white")
print(OUT)
