"""레일(프레임) 단면 — 홈에 끼워 돌려 잠그는 고정쇠와 수납 걸이 (단위 mm)."""
import os

import matplotlib
from matplotlib.patches import Polygon, Rectangle

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
OUT = os.path.join(os.path.dirname(__file__), "..", "concepts", "img", "desk_rail_profile.png")
fig, ax = plt.subplots(figsize=(9, 7))
alu, dark, top = "#c9ccd1", "#333", "#b3ada3"
ax.add_patch(Rectangle((-60, 40), 140, 25, fc=top, ec="#666"))                          # 상판
ax.text(10, 52, "상판 25mm", ha="center", va="center", fontsize=11)
# 레일 외곽 20×40, 안쪽(오른쪽) 면에 폭 6mm 홈, 속은 T자 공간
outer = [(0, 0), (20, 0), (20, 17), (17, 17), (17, 14), (8, 14), (8, 26), (17, 26), (17, 23), (20, 23), (20, 40), (0, 40)]
ax.add_patch(Polygon(outer, fc=alu, ec="#555", lw=1.5))
ax.add_patch(Rectangle((8, 14), 9, 12, fc="white", ec="none"))
ax.add_patch(Rectangle((17, 17), 3, 6, fc="white", ec="none"))
# 고정쇠(T너트) + 걸이판
ax.add_patch(Rectangle((10, 15.5), 5, 9, fc=dark))
ax.add_patch(Rectangle((15, 18.5), 8, 3, fc=dark))
ax.add_patch(Rectangle((23, -40), 3, 64, fc="#8f949b", ec="#555"))
ax.add_patch(Rectangle((23, -43), 45, 3, fc="#8f949b", ec="#555"))
ax.add_patch(Rectangle((65, -43), 3, 25, fc="#8f949b", ec="#555"))
ax.text(46, -32, "수납 상자", ha="center", fontsize=11)
ax.annotate("홈 폭 6mm\n(레일 전체 길이)", xy=(20, 20), xytext=(45, 30), fontsize=11, arrowprops=dict(arrowstyle="->"))
ax.annotate("고정쇠: 홈에 넣고 90° 돌려 잠금\n어느 위치든 고정", xy=(12, 18), xytext=(-60, -10), fontsize=11, arrowprops=dict(arrowstyle="->"))
ax.annotate("레일 20×40mm\n(알루미늄 압출)", xy=(4, 6), xytext=(-60, 15), fontsize=11, arrowprops=dict(arrowstyle="->"))
ax.text(-55, -58, "← 책상 바깥", fontsize=10, color="#666"); ax.text(55, -58, "책상 안쪽 →", fontsize=10, color="#666")
ax.set_xlim(-65, 95); ax.set_ylim(-62, 70); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("레일 단면 — 옆에서 자른 모습", fontsize=14)
fig.tight_layout(); fig.savefig(OUT, dpi=90, facecolor="white")
print(OUT)
