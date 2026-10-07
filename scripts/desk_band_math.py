"""폭(깊이)이 일정한 길게 휜 상판 — 옆으로 조금씩 이동하며 쓰는 책상.
단위 cm. 곡선 중심선 길이 L, 깊이 D, 곡률 반지름 ρ(중심선 기준, 클수록 직선에 가까움)."""
import os

import matplotlib
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon
from matplotlib.path import Path

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "concepts", "img", "desk_band.png")
REACH, GAP = 70, 12   # 팔 닿는 거리, 몸 중심 ~ 상판 안쪽 가장자리

# 표: 넓이 = 깊이 × 중심선 길이 (휘어도 똑같다)
print("L(중심선) D(깊이) | ρ → 감싸는 각도, 양 끝 가로 폭, 가운데가 들어간 깊이")
for L, D in ((120, 60), (140, 70), (160, 60)):
    cells = []
    for rho in (120, 200, 300):
        th = L / rho
        cells.append(f"ρ{rho}: {np.degrees(th):.0f}° 폭{2*rho*np.sin(th/2):.0f} 휨{rho*(1-np.cos(th/2)):.0f}")
    print(f"{L}x{D} ({L*D/1e4:.2f}㎡) | " + " | ".join(cells))


def band(L, D, rho):
    """사람 쪽으로 오목한 띠. 원의 중심은 사람 뒤쪽 (0, -c)."""
    if rho is None:   # 직선
        return np.array([[-L/2, GAP], [L/2, GAP], [L/2, GAP + D], [-L/2, GAP + D]]), None
    r_in = rho - D / 2
    c = r_in - GAP                 # 원 중심 = 사람 뒤 c cm
    a = np.linspace(-L / rho / 2, L / rho / 2, 200)
    inner = np.c_[r_in * np.sin(a), -c + r_in * np.cos(a)]
    outer = np.c_[(rho + D/2) * np.sin(a), -c + (rho + D/2) * np.cos(a)]
    return np.r_[inner[::-1], outer], (c, a)


def seats(L, rho, k):
    """앉는 위치 k곳 (몸 중심), 상판 안쪽에서 GAP만큼 떨어져 곡선을 따라 이동."""
    if rho is None:
        return np.c_[np.linspace(-L/2 + 12, L/2 - 12, k), np.zeros(k)], np.zeros(k)
    r_in = rho - 60 / 2
    c = r_in - GAP
    half = (L / 2 - 12) / rho
    a = np.linspace(-half, half, k)
    return np.c_[(c) * np.sin(a), -c + c * np.cos(a)], a


L, D = 160, 60
cases = [("직선 160×60", None), ("곡률 반지름 300cm", 300), ("곡률 반지름 200cm", 200), ("곡률 반지름 120cm", 120)]
gx, gy = np.meshgrid(np.linspace(-120, 120, 720), np.linspace(-60, 100, 480))
pts = np.c_[gx.ravel(), gy.ravel()]

fig, axes = plt.subplots(1, 4, figsize=(22, 6.2))
for ax, (title, rho) in zip(axes, cases):
    poly, _ = band(L, D, rho)
    inside = Path(poly).contains_points(pts)
    still = np.hypot(*pts.T) <= REACH
    pos, ang = seats(L, rho, 9)
    moving = np.zeros(len(pts), bool)
    for p in pos:
        moving |= np.hypot(*(pts - p).T) <= REACH
    lost_still = 100 * (inside & ~still).sum() / inside.sum()
    lost_move = 100 * (inside & ~moving).sum() / inside.sum()

    ax.add_patch(Polygon(poly, fc="#c8a37a", ec="#5a4632", lw=2))
    ax.add_patch(Circle((0, 0), REACH, fill=False, ec="#e08a00", ls="--", lw=1.3))
    for p, aa in zip(pos[::4], ang[::4]):
        ghost = abs(p[0]) > 1
        e = Ellipse(p, 42, 22, angle=-np.degrees(aa), fc="#555", alpha=0.25 if ghost else 1)
        ax.add_patch(e)
        ax.add_patch(Circle(p, 9, fc="#888", alpha=0.25 if ghost else 1))
    ax.plot(*pos.T, color="#1f6fb2", lw=2, ls=":")
    ax.set_title(f"{title}\n깊이 {D}cm 일정 · 중심선 길이 {L}cm", fontsize=12)
    ax.text(0, -45, f"제자리: 손 안 닿음 {lost_still:.0f}%   →   옆으로 이동하며: {lost_move:.0f}%",
            ha="center", fontsize=11, weight="bold", color="#2e7d32" if lost_move < 1 else "#d9534f")
    ax.set_xlim(-115, 115); ax.set_ylim(-55, 95); ax.set_aspect("equal"); ax.axis("off")
fig.suptitle("길게 휜 상판 — 파란 점선을 따라 옆으로 이동 (주황 점선 = 가운데 자리에서 닿는 70cm)", fontsize=15)
fig.tight_layout(); fig.savefig(OUT, dpi=100, facecolor="white")
print(OUT)
