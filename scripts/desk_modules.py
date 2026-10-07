"""사각형 모듈 + 삼각형 모듈 조합으로 만드는 책상 (위에서 본 모습, 단위 cm).
사각형 R: 한 사람이 앉아 쓰는 단위 (W x D)
삼각형 T: 두 변 = D, 꼭지각 α 인 이등변삼각형 → 두 사각형 사이를 α만큼 꺾어 준다"""
import os

import matplotlib
import numpy as np
from matplotlib.patches import Circle, Polygon

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "concepts", "img", "desk_modules.png")
W, D, ALPHA = 80, 58, 30


def rot(v, deg):
    a = np.radians(deg)
    return np.array([v[0] * np.cos(a) - v[1] * np.sin(a), v[0] * np.sin(a) + v[1] * np.cos(a)])


def build(seq):
    """seq 예: 'RTR'. 안쪽(사람 쪽) 모서리를 따라 왼쪽→오른쪽으로 이어 붙인다."""
    p, u = np.zeros(2), np.array([1.0, 0.0])
    pieces, seats, pivots = [], [], []
    for i, s in enumerate(seq):
        n = rot(u, 90)                       # 바깥쪽(사람 반대편)
        if s == "R":
            pieces.append(("R", np.array([p, p + W * u, p + W * u + D * n, p + D * n])))
            seats.append(p + W / 2 * u - 22 * n)
            p = p + W * u
        else:                                 # T: 시계 방향으로 α 꺾기 → 양 끝이 사람 쪽으로 감싼다
            if i == 0 or seq[i - 1] != "T":   # 삼각형 묶음의 꼭짓점 = 몸을 돌려 쓰는 자리
                k = len(seq[i:]) - len(seq[i:].lstrip("T"))
                pivots.append(p - 30 * rot(u, 90 - k * ALPHA / 2))
            u2 = rot(u, -ALPHA)
            pieces.append(("T", np.array([p, p + D * rot(u2, 90), p + D * n])))
            u = u2
    # 처음과 끝을 잇는 선이 수평이 되도록 돌리고 가운데로
    ang = np.degrees(np.arctan2(*(p[::-1])))
    mid = p / 2
    out = [(k, np.array([rot(v - mid, -ang) for v in poly])) for k, poly in pieces]
    seats = [rot(sp - mid, -ang) for sp in seats]
    pivots = [rot(sp - mid, -ang) for sp in pivots]
    return out, seats, pivots


combos = [
    ("모듈", None),
    ("RRR  직선", "RRR"),
    ("RTRTR  완만한 곡선 (60°)", "RTRTR"),
    ("RTTTR  ㄱ자 (90°)", "RTTTR"),
    ("RTTRTTR  감싸는 형태 (120°)", "RTTRTTR"),
    ("RTTR  1인용 코너 (60°)", "RTTR"),
]
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
for ax, (title, seq) in zip(axes.ravel(), combos):
    if seq is None:
        ax.add_patch(Polygon([[-120, 0], [-40, 0], [-40, D], [-120, D]], fc="#c8a37a", ec="#5a4632", lw=2))
        ax.text(-80, D / 2, f"R\n{W}×{D}", ha="center", va="center", fontsize=13)
        ax.text(-80, -14, "사각형: 한 사람의 작업 단위", ha="center", fontsize=11)
        t = np.array([[30, 0], [30 + D * np.sin(np.radians(ALPHA)), D * np.cos(np.radians(ALPHA))], [30, D]])
        ax.add_patch(Polygon(t, fc="#a8835a", ec="#5a4632", lw=2))
        ax.text(42, D * 0.6, f"T\n{ALPHA}°", ha="center", va="center", fontsize=13)
        ax.text(60, -14, f"삼각형: 두 변 {D}cm, 꼭지각 {ALPHA}°\n→ 이어 붙이면 {ALPHA}°씩 꺾인다", ha="center", fontsize=11, va="top")
        ax.set_xlim(-140, 140); ax.set_ylim(-60, 110)
    else:
        pieces, seats, pivots = build(seq)
        for k, poly in pieces:
            ax.add_patch(Polygon(poly, fc="#c8a37a" if k == "R" else "#a8835a", ec="#5a4632", lw=1.5))
        for sp in seats:
            ax.add_patch(Circle(sp, 11, fc="#999", alpha=0.6))
        for sp in pivots:
            ax.add_patch(Circle(sp, 11, fc="#1f6fb2", alpha=0.8))
        allv = np.vstack([p for _, p in pieces] + [np.array(seats)])
        c = (allv.max(0) + allv.min(0)) / 2
        span = max(np.ptp(allv[:, 0]), np.ptp(allv[:, 1]) * 1.6) / 2 + 25
        ax.set_xlim(c[0] - span, c[0] + span); ax.set_ylim(c[1] - span / 1.6, c[1] + span / 1.6)
    ax.set_title(title, fontsize=14); ax.set_aspect("equal"); ax.axis("off")
fig.suptitle(f"사각형(R) + 삼각형(T) 모듈 조합 — 회색 = 사각형 앞 자리 · 파랑 = 삼각형 꼭짓점에서 몸을 돌려 쓰는 자리", fontsize=16)
fig.tight_layout(); fig.savefig(OUT, dpi=90, facecolor="white")
print(OUT)
