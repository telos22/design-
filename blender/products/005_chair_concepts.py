"""005 의자 002 — 두 갈래 개념 모델.
A (옵스비크 쪽): 의자는 가만히, 사람이 움직인다 — 말안장 좌판 + 작은 등받이, 팔걸이 없음
B (암바스 쪽): 의자가 몸을 따라온다 — 좌판과 등받이가 한 장으로 이어진 휘는 껍데기 + 기울기 기구
공통: 5발 받침 + 바퀴, 높이 조절 기둥, 책상 001과 같은 색 (상판 회색, 칠 없는 알루미늄)
앞쪽 = -y. 단위 1 = 10cm"""
import math
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
import bpy
import mathutils
import studio

SEAT_Z = 4.5  # 좌판 높이 약 45cm (책상 72cm 기준)


def mats():
    return {
        "alu": studio.material("Alu", (0.80, 0.80, 0.82), roughness=0.3, metallic=1.0),
        "shell": studio.material("Shell", (0.47, 0.45, 0.41), roughness=0.65),
        "fabric": studio.material("Fabric", (0.42, 0.40, 0.37), roughness=0.95),
        "dark": studio.material("Dark", (0.06, 0.06, 0.065), roughness=0.6),
    }


def surface(name, grid, mat, thickness, offset=-1.0, levels=2):
    """grid: 행마다 점 목록 [(x, y, z), ...] → 사각면 → 두께 → 부드럽게"""
    rows, cols = len(grid), len(grid[0])
    verts = [p for row in grid for p in row]
    faces = [(r * cols + c, r * cols + c + 1, (r + 1) * cols + c + 1, (r + 1) * cols + c)
             for r in range(rows - 1) for c in range(cols - 1)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    sol = obj.modifiers.new("Thick", "SOLIDIFY")
    sol.thickness, sol.offset = thickness, offset
    obj.modifiers.new("Smooth", "SUBSURF").levels = levels
    for p in mesh.polygons:
        p.use_smooth = True
    studio.assign(obj, mat)
    return obj


def cylinder(name, r, z0, z1, mat, x=0.0, y=0.0, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=z1 - z0, location=(x, y, (z0 + z1) / 2))
    obj = bpy.context.object
    obj.name = name
    bpy.ops.object.shade_smooth()
    studio.assign(obj, mat)
    return obj


def base(m, top_z):
    """5발 받침 + 바퀴 + 높이 조절 기둥 (top_z까지)"""
    cylinder("Hub", 0.38, 0.62, 1.05, m["alu"])
    for i in range(5):
        a = math.radians(90 + i * 72)
        leg = studio.box("Leg", (3.0, 0.42, 0.26), (1.65 * math.cos(a), 1.65 * math.sin(a), 0.72), m["alu"], bevel=0.08)
        leg.rotation_euler = (0, math.radians(5), a)
        cx, cy = 3.05 * math.cos(a), 3.05 * math.sin(a)
        studio.box("Fork", (0.28, 0.32, 0.28), (cx, cy, 0.5), m["dark"], bevel=0.05).rotation_euler.z = a
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.24, depth=0.22, location=(cx, cy, 0.24))
        wheel = bpy.context.object
        wheel.rotation_euler = (math.pi / 2, 0, a)
        bpy.ops.object.shade_smooth()
        studio.assign(wheel, m["dark"])
    cylinder("ColumnCover", 0.3, 1.0, 2.3, m["alu"])
    cylinder("Column", 0.2, 2.3, top_z, m["alu"])


# ---------- A: 말안장 좌판 + 작은 등받이 ----------
def chair_a(m):
    grid = []
    for i in range(25):
        t = i / 24  # 0 = 앞(안장 머리), 1 = 뒤
        y = -2.2 + 4.4 * t
        w = 1.7 + 2.7 * t ** 0.55
        row = []
        for j in range(21):
            u = -1 + 2 * j / 20
            z = SEAT_Z - 0.05 + 0.30 * (1 - t) ** 3 + 0.18 * t ** 4 - 0.55 * u * u * (1 - 0.45 * t)
            row.append((u * w / 2, y, z))
        grid.append(row)
    surface("SaddleSeat", grid, m["fabric"], 0.6)
    studio.box("SeatPlate", (1.8, 2.0, 0.22), (0, 0.3, 3.8), m["dark"], bevel=0.05)
    base(m, 3.69)
    # 등받이 기둥 (알루미늄 띠) + 작은 등받이
    studio.cable("BackPost", [(0, 1.0, 3.8), (0, 2.2, 3.83), (0, 2.75, 4.3), (0, 2.85, 5.6), (0, 2.8, 6.6)], m["alu"], radius=0.12)
    grid = []
    for i in range(9):
        v = i / 8
        row = []
        for j in range(17):
            u = -1 + 2 * j / 16
            w = 1.7 * (1 - 0.12 * (2 * v - 1) ** 2)
            row.append((u * w, 2.55 - 0.35 * u * u + 0.18 * v, 6.2 + 1.9 * v))
        grid.append(row)
    surface("BackPad", grid, m["fabric"], 0.45, offset=1.0)


# ---------- B: 한 장으로 이어진 휘는 껍데기 ----------
PROFILE = [(-2.4, 4.25), (-2.3, 4.5), (-2.0, 4.62), (-1.0, 4.62), (0.0, 4.52), (1.0, 4.42), (1.6, 4.45),
           (2.0, 4.85), (2.25, 5.6), (2.4, 6.6), (2.5, 7.6), (2.58, 8.6), (2.65, 9.5)]
PIVOT = (1.4, 4.42)
WIDTH = [(0.0, 4.5), (0.12, 4.8), (0.36, 4.8), (0.47, 4.2), (0.55, 3.5), (0.63, 3.7), (0.8, 4.4), (1.0, 3.9)]


def catmull(points, n=8):
    out = []
    pts = [points[0]] + points + [points[-1]]
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = (mathutils.Vector(p) for p in pts[i - 1:i + 3])
        for k in range(n):
            s = k / n
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s + (-p0 + 3 * p1 - 3 * p2 + p3) * s ** 3))
    out.append(mathutils.Vector(points[-1]))
    return out


def lerp_table(table, f):
    for (f0, v0), (f1, v1) in zip(table, table[1:]):
        if f <= f1:
            return v0 + (v1 - v0) * (f - f0) / (f1 - f0)
    return table[-1][1]


def shell_profile(recline_deg):
    """기대면: 좌판은 뒤로 4°, 등받이는 피벗을 중심으로 recline_deg만큼 (허리 부분에서 서서히 휨)"""
    pts = catmull(PROFILE)
    seat_rot = math.radians(4 * recline_deg / 18)
    out = []
    for p in pts:
        y, z = p
        # 좌판 전체 살짝 뒤로 (중심 (0, SEAT_Z))
        dy, dz = y, z - SEAT_Z
        y, z = dy * math.cos(seat_rot) + dz * math.sin(seat_rot), -dy * math.sin(seat_rot) + dz * math.cos(seat_rot) + SEAT_Z
        if p[0] > PIVOT[0]:
            d = math.hypot(p[0] - PIVOT[0], p[1] - PIVOT[1])
            k = min(1.0, d / 1.6)
            a = math.radians(recline_deg) * (k * k * (3 - 2 * k))
            dy, dz = y - PIVOT[0], z - PIVOT[1]
            y, z = PIVOT[0] + dy * math.cos(a) + dz * math.sin(a), PIVOT[1] - dy * math.sin(a) + dz * math.cos(a)
        out.append(mathutils.Vector((y, z)))
    return out


def chair_b(m, recline_deg=0.0):
    prof = shell_profile(recline_deg)
    lengths = [0.0]
    for a, b in zip(prof, prof[1:]):
        lengths.append(lengths[-1] + (b - a).length)
    total = lengths[-1]
    grid = []
    for i, p in enumerate(prof):
        f = lengths[i] / total
        t = (prof[min(i + 1, len(prof) - 1)] - prof[max(i - 1, 0)]).normalized()
        n = mathutils.Vector((-t.y, t.x))  # 사람 쪽(위·앞)
        w = lerp_table(WIDTH, f)
        row = []
        for j in range(21):
            u = -1 + 2 * j / 20
            dish = 0.16 * min(1.0, f / 0.12, (1 - f) / 0.12)  # 양 끝에서는 오목함을 줄여 꼬임 방지
            q = p - dish * (1 - u * u) * n
            row.append((u * w / 2, q.x, q.y))
        grid.append(row)
    surface("Shell", grid, m["shell"], 0.22)
    studio.box("Mechanism", (2.2, 2.0, 0.46), (0, 0.2, 3.92), m["dark"], bevel=0.08)
    base(m, 3.7)
    # 등뼈: 기구 뒤에서 등받이 가운데 뒤로
    back = [p for p in prof if p.y > 6.6][0]
    studio.cable("Spine", [(0, 1.1, 3.92), (0, 2.2, 4.0), (0, back.x + 0.75, back.y - 1.3), (0, back.x + 0.45, back.y)], m["alu"], radius=0.14)


def shoot(name, build, cam_loc, target, lens=50, res=(1100, 1000)):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=2)
    build(mats())
    cam = studio.camera(lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=64, resolution=res, view="Standard", exposure=-1.1)


if __name__ == "__main__":
    only = sys.argv[1:]
    q, side = (-9.5, -13.0, 8.5), (16.0, 0.3, 5.2)
    tq, ts = (0, 0.3, 4.6), (0, 0.4, 4.9)
    (not only or "005_chair_A_quarter" in only) and print(shoot("005_chair_A_quarter", chair_a, q, tq))
    (not only or "005_chair_A_side" in only) and print(shoot("005_chair_A_side", chair_a, side, ts))
    (not only or "005_chair_A_back" in only) and print(shoot("005_chair_A_back", chair_a, (9.5, 13.0, 8.5), tq))
    (not only or "005_chair_B_quarter" in only) and print(shoot("005_chair_B_quarter", lambda m: chair_b(m), q, tq))
    (not only or "005_chair_B_side" in only) and print(shoot("005_chair_B_side", lambda m: chair_b(m), side, ts))
    (not only or "005_chair_B_side_recline" in only) and print(shoot("005_chair_B_side_recline", lambda m: chair_b(m, 18), side, ts))
