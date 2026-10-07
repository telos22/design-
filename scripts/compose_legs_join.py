"""다리 결합 렌더 3장 + 이음새 단면(위에서 본 모습)을 한 장으로."""
import os

import matplotlib
import matplotlib.image as mpimg
import numpy as np
from matplotlib.patches import Polygon, Rectangle

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
R = os.path.join(os.path.dirname(__file__), "..")
titles = {"A": "A. 안쪽 다리 — 이음새에 다리 2개", "B": "B. 모서리 사각 다리 — 둘이 붙어 하나", "C": "C. 모서리 1/4 원 다리 — 둘이면 반원"}
fig, axes = plt.subplots(2, 3, figsize=(18, 10), gridspec_kw={"height_ratios": [3, 1.3]})
for i, v in enumerate("ABC"):
    ax = axes[0][i]
    ax.imshow(mpimg.imread(f"{R}/renders/001_desk_legs_join_{v}.png")); ax.axis("off")
    ax.set_title(titles[v], fontsize=14)
    ax = axes[1][i]   # 이음새 부근 단면 (위에서), 판 4장이 만나는 경우까지
    for qx in (-1, 1):   # 단위 cm, 이음새 주변 ±20cm만 확대
        for qy in (-1, 1):
            ax.add_patch(Rectangle((min(0, qx * 80), min(0, qy * 60)), 80, 60, fc="#e9e5dc", ec="#8a857a", lw=1))
            if v == "A":
                ax.add_patch(Rectangle((qx * 5 - (4 if qx < 0 else 0), qy * 5 - (4 if qy < 0 else 0)), 4, 4, fc="#222"))
            elif v == "B":
                ax.add_patch(Rectangle((-3 if qx < 0 else 0, -3 if qy < 0 else 0), 3, 3, fc="#222"))
            else:
                t = np.linspace(0, np.pi / 2, 20)
                pts = np.c_[np.r_[0, 3.5 * np.cos(t)] * qx, np.r_[0, 3.5 * np.sin(t)] * qy]
                ax.add_patch(Polygon(pts, fc="#222"))
    ax.text(0, -19, "판 4장이 만나는 점 주변 ±15cm (위에서 본 단면)", ha="center", fontsize=11)
    ax.set_xlim(-15, 15); ax.set_ylim(-21, 15); ax.set_aspect("equal"); ax.axis("off")
fig.suptitle("모서리 다리 4개 — 판 두 개를 붙였을 때", fontsize=17)
fig.tight_layout(); fig.savefig(f"{R}/renders/001_desk_legs_join.png", dpi=80, facecolor="white")
print("ok")
