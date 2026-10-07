"""A2 초승달 상판의 수학: 표준 책상 크기와의 비교 + 원이 아닌 곡선(슈퍼타원, 큰 원의 일부) 비교.
단위 cm. 앉은 사람의 몸 중심이 원점, 정면이 +y."""
import os

import matplotlib
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon
from matplotlib.path import Path

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "concepts", "img", "desk_curves.png")
R_IN, MAX = 25, 70

# 1) 표준 책상 넓이와 같은 초승달을 만들려면 바깥 반지름 R은?
#    초승달 넓이 A = (θ/2)(R² - r²)  →  R = sqrt(2A/θ + r²)
print("표준 책상 → 같은 넓이의 초승달 (안쪽 r=25cm)")
for w, d in ((120, 60), (140, 70), (160, 80)):
    A = w * d
    row = [f"{w}x{d} ({A/1e4:.2f}㎡)"]
    for deg in (180, 150, 120):
        R = np.sqrt(2 * A / np.radians(deg) + R_IN**2)
        row.append(f"{deg}°→R={R:.0f}")
    print("  ", " | ".join(row))
print(f"   R=70, 180° 초승달 넓이 = {np.pi/2*(MAX**2-R_IN**2)/1e4:.2f}㎡")


def superellipse(a, b, n, t):
    """|x/a|^n + |y/b|^n = 1 위의 점. t는 -90°~90° (정면 0)."""
    s, c = np.sin(t), np.cos(t)
    return np.c_[a * np.sign(s) * np.abs(s) ** (2 / n), b * np.abs(c) ** (2 / n)]


t = np.radians(np.linspace(-90, 90, 361))
gx, gy = np.meshgrid(np.linspace(-110, 110, 660), np.linspace(-10, 110, 360))
pts = np.c_[gx.ravel(), gy.ravel()]
cell = (220 / 659) * (120 / 359)

cases = []
for n, name in ((2, "원 (A2)"), (3, "슈퍼타원 n=3"), (6, "슈퍼타원 n=6")):
    poly = np.r_[superellipse(R_IN, R_IN, n, t)[::-1], superellipse(MAX, MAX, n, t)]
    cases.append((f"{name}\n원 → 둥근 사각형", poly))
for rc in (120, 250):  # 큰 원의 일부: 원의 중심을 사람 뒤 rc-25 cm 에 둔다
    cy = -(rc - R_IN)
    half = np.arcsin(60 / (rc + 45))  # 바깥 폭 ±60cm 정도로 맞춤
    a = np.linspace(-half, half, 200)
    inner = np.c_[rc * np.sin(a), cy + rc * np.cos(a)]
    outer = np.c_[(rc + 45) * np.sin(a), cy + (rc + 45) * np.cos(a)]
    cases.append((f"큰 원의 일부 (곡률 반지름 {rc}cm)\n살짝 휜 판, 깊이 45cm", np.r_[inner[::-1], outer]))

fig, axes = plt.subplots(1, 5, figsize=(22, 6))
for ax, (title, poly) in zip(axes, cases):
    inside = Path(poly).contains_points(pts)
    lost = inside & (np.hypot(*pts.T) > MAX)
    area, pct = inside.sum() * cell / 1e4, 100 * lost.sum() / inside.sum()
    desk = Polygon(poly, fc="#d9534f", ec="#5a4632", lw=2)
    ax.add_patch(desk)
    ok = Circle((0, 0), MAX, fc="#c8a37a", ec="none"); ax.add_patch(ok); ok.set_clip_path(desk)
    ax.add_patch(Polygon(poly, fill=False, ec="#5a4632", lw=2))
    ax.add_patch(Circle((0, 0), MAX, fill=False, ec="#e08a00", ls="--", lw=1.3))
    ax.add_patch(Ellipse((0, 0), 42, 22, fc="#555")); ax.add_patch(Circle((0, 0), 9, fc="#888"))
    ax.set_title(title, fontsize=12)
    ax.text(0, -28, f"넓이 {area:.2f}㎡ · 손 안 닿음 {pct:.0f}%", ha="center", fontsize=11,
            color="#d9534f" if pct >= 1 else "#2e7d32", weight="bold")
    ax.set_xlim(-105, 105); ax.set_ylim(-35, 105); ax.set_aspect("equal"); ax.axis("off")
fig.suptitle("곡선의 종류 비교 — 위에서 본 모습 (주황 점선 = 최대로 닿는 70cm)", fontsize=15)
fig.tight_layout(); fig.savefig(OUT, dpi=100, facecolor="white")
print(OUT)
