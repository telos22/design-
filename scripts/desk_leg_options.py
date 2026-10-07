"""다리 배치 후보 — 80×60 판 1개 / 2개 직선 / ㄱ자에서 다리가 어디 오는지 (위에서 본 모습, 단위 cm)."""
import os

import matplotlib
from matplotlib.patches import Rectangle

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "concepts", "img", "desk_legs.png")
W, D = 80, 60


def legs_four(x, y, w, h):      # 모서리 4개
    s = 6
    return [(x + 3, y + 3, s, s), (x + w - 9, y + 3, s, s), (x + 3, y + h - 9, s, s), (x + w - 9, y + h - 9, s, s)]


def legs_side(x, y, w, h):      # 양옆 T자 다리 2개 (발이 앞뒤로 길다)
    if w >= h:
        return [(x + 4, y + 5, 5, h - 10), (x + w - 9, y + 5, 5, h - 10)]
    return [(x + 5, y + 4, w - 10, 5), (x + 5, y + h - 9, w - 10, 5)]


def legs_column(x, y, w, h):    # 뒤쪽 가운데 기둥 1개 + 넓은 발
    if w >= h:   # 가로 놓기: 앉는 쪽 = 아래, 뒤 = 위
        return [(x + w / 2 - 6, y + h - 16, 12, 10), (x + w / 2 - 28, y + h - 8, 56, 5)]
    # 세로 놓기 (ㄱ자의 오른쪽): 앉는 쪽 = 왼쪽, 뒤 = 오른쪽
    return [(x + w - 16, y + h / 2 - 6, 10, 12), (x + w - 8, y + h / 2 - 28, 5, 56)]


options = [("A. 모서리 다리 4개", legs_four), ("B. 양옆 다리 2개 (T자 발)", legs_side), ("C. 뒤쪽 기둥 1개", legs_column)]
layouts = [("1개", [(0, 0, W, D)]), ("2개 직선", [(0, 0, W, D), (W, 0, W, D)]), ("ㄱ자", [(0, 0, W, D), (W, -20, D, W)])]

fig, axes = plt.subplots(3, 3, figsize=(15, 12))
for r, (oname, fn) in enumerate(options):
    for c, (lname, rects) in enumerate(layouts):
        ax = axes[r][c]
        for rx, ry, rw, rh in rects:
            ax.add_patch(Rectangle((rx, ry), rw, rh, fc="#e9e5dc", ec="#8a857a", lw=1.5))
            for lx, ly, lw, lh in fn(rx, ry, rw, rh):
                ax.add_patch(Rectangle((lx, ly), lw, lh, fc="#333", ec="none"))
        ax.set_xlim(-15, 160); ax.set_ylim(-35, 75); ax.set_aspect("equal"); ax.axis("off")
        if r == 0:
            ax.set_title(lname, fontsize=14)
        if c == 0:
            ax.text(-20, 20, oname, rotation=90, ha="right", va="center", fontsize=13)
fig.suptitle("다리 배치 후보 — 위에서 본 모습 (검정 = 다리·발, 아래쪽이 앉는 쪽)", fontsize=16)
fig.tight_layout(rect=(0.03, 0, 1, 0.95)); fig.savefig(OUT, dpi=85, facecolor="white")
print(OUT)
