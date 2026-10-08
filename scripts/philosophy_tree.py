"""철학 로직 트리: 목표 → 슬로건 → No more / No less → 원칙"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"

DONE, TALK, TODO = "확정", "논의 중", "아직"
STATUS_COLOR = {DONE: "#2f6f4f", TALK: "#b7791f", TODO: "#8a8a8a"}

goal = ("목표", "제품은 문제를 해결하기\n위한 도구로서만\n존재한다",
        "모든 원칙 위에 '목적 달성'\n디자인의 양은 목적이 정한다")
slogan = ("슬로건", "No more, No less",
          "덜도 더도 말고, 딱 필요한 만큼\n기준은 '적게'가 아니라 '정확하게'")

branches = [
    ("No more", "목적을 넘어서 더하지 않는다",
     "질문: 이게 없으면 무슨 문제가 생기나?", [
         ("쓰는 방법은 단순하게", "사용하기에 복잡하지 않게 (겉모양 X)", DONE),
         ("조각은 합치고, 종류·개수 최소로", "예) 책상 한 장, 상자 한 종류", DONE),
         ("목적이 요구하지 않는 장식은 하지 않는다", "더할 때는 이유가 기능 (상판 색, 녹 방지 칠)", TALK),
         ("있는 요소에 두 번째 역할", "예) 프레임 = 자석 상자 붙는 자리", TODO),
     ]),
    ("No less", "목적을 이루는 데 빠뜨리지 않는다",
     "질문: 빠진 게 있나?", [
         ("문제를 해결하는 기능", "철학의 중심", TODO),
         ("사용하기 편하다", "", TODO),
         ("직관적으로 쓸 수 있다", "'쓰는 방법은 단순하게'와 합칠지 확인 중", TALK),
         ("오래간다", "튼튼함? 질리지 않음? 둘 다?", TODO),
         ("치수는 몸과 실제 사용에서", "예) 안 쓰는 뒤 20cm → 깊이 60", TODO),
         ("목적이 아름다움이면 아름답게", "아니면 기능을 해치지 않는 선까지", TODO),
     ]),
]
shared = ("양쪽에 걸침", "사람마다 다른 것은 자유로 둔다",
          "정해 두지 않음(No more) + 각자의 필요를 채움(No less)", TODO)

fig, ax = plt.subplots(figsize=(17, 11))
ax.set_xlim(0, 17)
ax.set_ylim(0, 11)
ax.axis("off")


def box(x, y, w, h, title, sub="", fc="#ffffff", ec="#333333", tc="#111111",
        tsize=13, ssize=9.5, bold=True):
    ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=ec, lw=1.4))
    if sub:
        ax.text(x + 0.18, y + 0.12, title, fontsize=tsize, color=tc, va="bottom",
                weight="bold" if bold else "normal")
        ax.text(x + 0.18, y + 0.05, sub, fontsize=ssize, color="#555555", va="top", linespacing=1.3)
    else:
        ax.text(x + 0.18, y, title, fontsize=tsize, color=tc, va="center",
                weight="bold" if bold else "normal")


def link(x0, y0, x1, y1):
    xm = (x0 + x1) / 2
    ax.plot([x0, xm, xm, x1], [y0, y0, y1, y1], color="#999999", lw=1.2)


# 열 위치
XG, WG = 0.2, 3.0
XS, WS = 3.6, 3.0
XB, WB = 7.0, 3.2
XP, WP = 10.6, 6.2

# 원칙 행 위치
rows = []
y = 10.3
for _, _, _, ps in branches:
    ys = []
    for _ in ps:
        ys.append(y)
        y -= 0.85
    rows.append(ys)
    y -= 0.35
y_shared = y - 0.1

yb = [sum(r) / len(r) for r in rows]
ys_ = (yb[0] + yb[1]) / 2

ax.add_patch(FancyBboxPatch((XG, ys_ - 1.0), WG, 2.0, boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc="#1f2933", ec="#1f2933"))
ax.text(XG + 0.18, ys_ + 0.8, goal[0], fontsize=9, color="#aab4be", va="center")
ax.text(XG + 0.18, ys_ + 0.15, goal[1], fontsize=12.5, color="#ffffff", weight="bold", va="center", linespacing=1.4)
ax.text(XG + 0.18, ys_ - 0.65, goal[2], fontsize=9.5, color="#d9dee3", va="center", linespacing=1.4)
box(XS, ys_, WS, 1.4, slogan[1], slogan[2], fc="#e9ecef", tsize=14)
ax.text(XS + 0.18, ys_ + 0.85, slogan[0], fontsize=9, color="#666666")
link(XG + WG, ys_, XS, ys_)

for (name, desc, q, ps), yy, ycen in zip(branches, rows, yb):
    box(XB, ycen, WB, 1.5, name, desc + "\n\n" + q, fc="#f6f7f8", tsize=15)
    link(XS + WS, ys_, XB, ycen)
    for (title, sub, st), py in zip(ps, yy):
        c = STATUS_COLOR[st]
        box(XP, py, WP, 0.72, title, sub, ec=c, tsize=11.5, ssize=9)
        ax.text(XP + WP - 0.15, py + 0.2, st, fontsize=9, color="#ffffff", ha="right", va="center",
                bbox=dict(boxstyle="round,pad=0.25", fc=c, ec=c))
        link(XB + WB, ycen, XP, py)

# 양쪽에 걸친 것
c = STATUS_COLOR[shared[3]]
box(XP, y_shared, WP, 0.72, shared[1], shared[2], ec=c, tsize=11.5, ssize=9)
ax.text(XP + WP - 0.15, y_shared + 0.2, shared[3], fontsize=9, color="#ffffff", ha="right", va="center",
        bbox=dict(boxstyle="round,pad=0.25", fc=c, ec=c))
ax.text(XB + 0.18, y_shared, shared[0] + " →", fontsize=11, color="#555555", va="center")
link(XS + WS, ys_, XB, y_shared)

ax.text(0.2, 10.75, "나의 디자인 철학 — 로직 트리  (2026-10-08)", fontsize=16, weight="bold")
ax.text(0.2, 0.25, "확정 = 사용자 확정 · 논의 중 = 문장 확인 대기 · 아직 = 책상·대화에서 나왔지만 하나씩 다루지 않음",
        fontsize=9.5, color="#666666")

plt.savefig("concepts/img/philosophy_tree.png", dpi=150, bbox_inches="tight", facecolor="white")
print("saved")
