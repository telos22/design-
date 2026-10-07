"""조각 한 종류(80×60)만으로 만드는 배치 — 위에서 본 모습, 단위 cm.
가로 놓기 = 80×60, 세로 놓기 = 60×80."""
import os

import matplotlib
from matplotlib.patches import Rectangle

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "concepts", "img", "desk_single_unit.png")
A, B = 80, 60


def h(x, y): return (x, y, A, B)   # 가로 놓기
def v(x, y): return (x, y, B, A)   # 세로 놓기


layouts = [
    ("1개 — 1인 기본", [h(0, 0)]),
    ("직선 — 2칸", [h(0, 0), h(80, 0)]),
    ("ㄱ자", [h(0, 0), v(80, -20)]),
    ("ㄷ자 — 둘러싸기", [v(0, -20), h(60, 0), v(140, -20)]),
    ("ㅜ자", [h(0, 0), h(80, 0), v(50, -80)]),
    ("바람개비 — 가운데 20×20 구멍 (케이블 통로?)", [(0, 0, A, B), (A, 0, B, A), (B, A, A, B), (0, B, B, A)]),
    ("4:3 비율 — 가로 3개 = 세로 4개 = 240cm", [h(0, 0), h(80, 0), h(160, 0)] + [v(60 * i, -80) for i in range(4)]),
]

fig, axes = plt.subplots(2, 4, figsize=(20, 10))
for ax, (title, rects) in zip(axes.ravel(), layouts):
    for x, y, w, hh in rects:
        ax.add_patch(Rectangle((x, y), w, hh, fc="#c8a37a", ec="#5a4632", lw=2))
    xs = [r[0] for r in rects] + [r[0] + r[2] for r in rects]
    ys = [r[1] for r in rects] + [r[1] + r[3] for r in rects]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    span = max(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 30
    ax.set_xlim(cx - span, cx + span); ax.set_ylim(cy - span, cy + span)
    ax.set_title(title, fontsize=13); ax.set_aspect("equal"); ax.axis("off")
ax = axes.ravel()[-1]
ax.axis("off")
ax.text(0.5, 0.5, "조각은 단 한 종류\n80 × 60\n\n짧은 변(60)끼리 → 직선\n짧은 변을 긴 변(80)에 → 꺾기·갈래",
        ha="center", va="center", fontsize=15, color="#1f6fb2", transform=ax.transAxes)
fig.suptitle("한 종류(80×60)만으로 만드는 형태 — 위에서 본 모습", fontsize=17)
fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(OUT, dpi=85, facecolor="white")
print(OUT)
