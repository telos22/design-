"""기본 단위 R(80×60) + 연결 조각들. 모든 연결 조각의 맞닿는 변 = 60cm (= 단위 깊이).
위에서 본 모습, 단위 cm. 사람은 진행 방향의 오른쪽(아래)에 앉는다고 가정."""
import os

import matplotlib
import numpy as np
from matplotlib.patches import Circle, Polygon

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "concepts", "img", "desk_connectors.png")
W, D = 80, 60
COL = {"R": "#c8a37a", "T": "#a8835a", "Q": "#9c7a52", "L": "#b89468", "H": "#b89468"}


def rot(v, deg):
    a = np.radians(deg)
    return np.array([v[0] * np.cos(a) - v[1] * np.sin(a), v[0] * np.sin(a) + v[1] * np.cos(a)])


def place(a, b, tok):
    """포트(a=왼쪽 끝, b=오른쪽 끝, 길이 60)에 조각 하나를 붙인다 → (종류, 꼭짓점, 다음 포트들, 자리)"""
    f = rot(a - b, -90) / D                       # 진행 방향 (a가 왼쪽 끝)
    kind, sign, ang = tok[0], (tok[1:2] or "+"), int(tok[2:] or 90)
    if kind == "R":
        poly = [a, b, b + W * f, a + W * f]
        seat = (b + b + W * f) / 2 + 28 * rot(f, -90)
        return kind, poly, [(a + W * f, b + W * f)], [seat]
    if kind in "TQ":                               # 쐐기(T) / 부채꼴(Q): 한 끝을 축으로 회전
        piv, other, s = (a, b, 1) if sign == "+" else (b, a, -1)
        steps = np.linspace(0, ang, 2 if kind == "T" else 24)
        poly = [piv] + [piv + rot(other - piv, s * t) for t in steps]
        end = piv + rot(other - piv, s * ang)
        nxt = (a, end) if sign == "+" else (end, b)
        seat = [piv + 30 * rot(f, -90 - ang / 2)] if sign == "-" else []
        return kind, poly, [nxt], seat
    if kind in "LH":                               # 정사각 60×60: 꺾기(L) / 갈래(H)
        poly = [a, b, b + D * f, a + D * f]
        fwd, left, right = (a + D * f, b + D * f), (a, a + D * f), (b + D * f, b)
        if kind == "L":
            return kind, poly, [left if sign == "+" else right], []
        return kind, poly, [fwd, left, right], []


def build(spec, a=np.array([0.0, 30.0]), b=np.array([0.0, -30.0])):
    """spec: 토큰 리스트. 갈래는 ('H', [왼쪽 갈래], [오른쪽 갈래]) 뒤에 앞쪽이 이어진다."""
    pieces, seats = [], []
    for tok in spec:
        if isinstance(tok, tuple):
            kind, poly, ports, st = place(a, b, "H")
            pieces.append((kind, poly))
            for port, sub in zip(ports[1:], tok[1:]):
                p2, s2 = build(sub, *port)
                pieces += p2; seats += s2
            a, b = ports[0]
            continue
        kind, poly, ports, st = place(a, b, tok)
        pieces.append((kind, poly)); seats += st
        a, b = ports[0]
    return pieces, seats


catalog = [("R", "기본 단위\n80×60"), ("T-30", "쐐기 30°"), ("T-45", "쐐기 45°"),
           ("Q-90", "부채꼴 90°\n(둥근 꺾기)"), ("L-", "정사각 60×60\n(각진 꺾기·갈래)")]
layouts = [
    ("직선 (2인 또는 1인 2칸)", ["R", "R"]),
    ("ㄱ자 — 각진 꺾기", ["R", "L-", "R"]),
    ("ㄱ자 — 둥근 꺾기", ["R", "Q-90", "R"]),
    ("완만하게 감싸기 (30° × 2)", ["R", "T-30", "R", "T-30", "R"]),
    ("ㄷ자 — 둘러싸기", ["R", "L-", "R", "L-", "R"]),
    ("물결 (양쪽으로 꺾기)", ["R", "T-30", "R", "T+30", "R"]),
    ("ㅗ자 갈래", ["R", ("H", ["R"], []), "R"]),
    ("십자 — 네 사람", ["R", ("H", ["R"], ["R"]), "R"]),
]

fig = plt.figure(figsize=(20, 14))
gs = fig.add_gridspec(3, 4, height_ratios=[0.8, 1, 1])
ax0 = fig.add_subplot(gs[0, :])
x = 0
for tok, label in catalog:
    kind, poly, _, _ = place(np.array([x, 30.0]), np.array([x, -30.0]), tok)
    poly = np.array(poly)
    ax0.add_patch(Polygon(poly, fc=COL[kind], ec="#5a4632", lw=2))
    cx = poly[:, 0].mean()
    ax0.text(cx, -50, label, ha="center", va="top", fontsize=12)
    x = poly[:, 0].max() + 70
ax0.text(x - 20, 0, "규칙: 모든 연결 변 = 60cm\n(기본 단위의 깊이)", fontsize=13, va="center", color="#1f6fb2")
ax0.set_xlim(-30, x + 220); ax0.set_ylim(-95, 75); ax0.set_aspect("equal"); ax0.axis("off")
ax0.set_title("조각들", fontsize=15, loc="left")

for i, (title, spec) in enumerate(layouts):
    ax = fig.add_subplot(gs[1 + i // 4, i % 4])
    pieces, seats = build(spec)
    for kind, poly in pieces:
        ax.add_patch(Polygon(np.array(poly), fc=COL[kind], ec="#5a4632", lw=1.5))
    v = np.vstack([np.array(p) for _, p in pieces])
    c, span = (v.max(0) + v.min(0)) / 2, np.ptp(v, 0).max() / 2 + 25
    ax.set_xlim(c[0] - span, c[0] + span); ax.set_ylim(c[1] - span, c[1] + span)
    ax.set_title(title, fontsize=13); ax.set_aspect("equal"); ax.axis("off")

fig.suptitle("기본 단위 80×60 + 연결 조각 — 위에서 본 모습", fontsize=17)
fig.tight_layout(); fig.savefig(OUT, dpi=85, facecolor="white")
print(OUT)
