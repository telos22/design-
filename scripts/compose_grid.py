"""렌더 여러 장을 행×열 격자로 합치기.
사용: python3 compose_grid.py 출력.png "제목" "행1,행2" "열1,열2,열3" 파일1 파일2 ... (행 우선 순서)"""
import sys

import matplotlib
import matplotlib.image as mpimg

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
out, title, rows, cols, files = sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4].split(","), sys.argv[5:]
fig, axes = plt.subplots(len(rows), len(cols), figsize=(6 * len(cols), 4.7 * len(rows)), squeeze=False)
for i, f in enumerate(files):
    ax = axes[i // len(cols)][i % len(cols)]
    ax.imshow(mpimg.imread(f)); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    if i < len(cols):
        ax.set_title(cols[i], fontsize=15)
    if i % len(cols) == 0:
        ax.set_ylabel(rows[i // len(cols)], fontsize=15)
fig.suptitle(title, fontsize=18)
fig.tight_layout(); fig.savefig(out, dpi=80, facecolor="white")
