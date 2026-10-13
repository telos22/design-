"""006 스탠드 — 작은 원 하나 / 원 두 개 / 고리 두 개 비교.
바닥 판(버튼) + 기둥 + 앞으로 나온 팔. 빛 면은 상판 위 40cm(앉은 눈높이 아래), 아래를 향한다.
  1 원 하나 (지름 8cm)   2 원 두 개 (45cm 간격)   3 고리 두 개 (바깥 10cm, 안 7cm)
세 가지 모두 같은 빛의 양. 저녁, 방의 다른 불은 끔.
보기: seat = 앉은 눈높이, top = 위에서 내려다봄
사용: python3 006_lamp_two_heads.py <1|2|3> <seat|top>
단위 1 = 10cm"""
import math
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
import bpy
import props
import studio

VARIANT, VIEW = int(sys.argv[-2]), sys.argv[-1]
H = 7.2
W, D = 16.0, 6.0
DESK_Y = -3.5
CEIL = 27.0
LIGHT_Z = H + 4.0            # 빛 면: 상판 위 40cm
POWER = float(os.environ.get("POWER", "40"))   # 스탠드 전체 빛의 양 (렌더용 값, 세 가지 같음)
SPACING = 4.5                # 원 두 개 간격 45cm
POLE_Y = DESK_Y + 2.2        # 기둥: 상판 뒤쪽
HEAD_Y = DESK_Y + 0.2        # 빛 면 중심: 상판 가운데 조금 앞


def room():
    wall = studio.material("Wall", (0.80, 0.79, 0.77), roughness=0.95)
    ceil = studio.material("Ceiling", (0.85, 0.85, 0.84), roughness=0.95)
    floor = studio.material("FloorWood", (0.30, 0.25, 0.20), roughness=0.8)
    studio.box("Floor", (40, 40, 0.2), (0, -18, -0.1), floor)
    studio.box("Ceil", (40, 40, 0.2), (0, -18, CEIL + 0.1), ceil)
    studio.box("Back", (40, 0.2, CEIL), (0, 0.1, CEIL / 2), wall)
    studio.box("Front", (40, 0.2, CEIL), (0, -38.1, CEIL / 2), wall)
    studio.box("Left", (0.2, 40, CEIL), (-15.1, -18, CEIL / 2), wall)
    studio.box("Right", (0.2, 40, CEIL), (15.1, -18, CEIL / 2), wall)
    w = bpy.data.worlds.new("World")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
    bpy.context.scene.world = w


def desk():
    top = studio.material("DeskTop", (0.45, 0.43, 0.40), roughness=0.75)
    alu = studio.material("Alu", (0.8, 0.8, 0.82), roughness=0.35, metallic=1.0)
    studio.box("Top", (W, D, 0.25), (0, DESK_Y, H - 0.125), top, bevel=0.02)
    for sx in (-1, 1):
        for sy in (-1, 1):
            studio.box("Leg", (0.4, 0.4, H - 0.25), (sx * (W / 2 - 0.3), DESK_Y + sy * (D / 2 - 0.3), (H - 0.25) / 2), alu)
    props.notebook(-2.6, DESK_Y + 0.2, H, angle=0.05)
    props.paper(2.4, DESK_Y + 0.4, H, angle=-0.12)
    props.pen(2.5, DESK_Y - 0.1, H + 0.006, angle=0.6)
    props.paper(-6.2, DESK_Y + 0.5, H, angle=0.15)      # 왼쪽 끝 종이
    props.paper(6.2, DESK_Y + 0.3, H, angle=-0.1)       # 오른쪽 끝 종이
    # 컵: 그림자가 또렷한지 부드러운지 보기 (지름 8cm, 높이 9cm)
    mug = studio.material("Mug", (0.75, 0.74, 0.72), roughness=0.4)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.4, depth=0.9, location=(0.3, DESK_Y - 1.2, H + 0.45))
    studio.assign(bpy.context.object, mug)
    bpy.ops.object.shade_smooth()


def emission(name, strength):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.93, 0.82, 1)   # 약 3500K
    em.inputs["Strength"].default_value = strength
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(em.outputs[0], out.inputs[0])
    return m


def annulus(name, r_out, r_in, loc, mat, n=64):
    """아래를 향한 납작한 고리 (r_in=0 이면 꽉 찬 원판)"""
    verts, faces = [], []
    for i in range(n):
        a = 2 * math.pi * i / n
        verts += [(r_out * math.cos(a), r_out * math.sin(a), 0), (max(r_in, 1e-4) * math.cos(a), max(r_in, 1e-4) * math.sin(a), 0)]
    for i in range(n):
        j = (i + 1) % n
        faces.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))   # 법선이 아래(-Z)
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    obj = bpy.data.objects.new(name, mesh)
    obj.location = loc
    bpy.context.collection.objects.link(obj)
    studio.assign(obj, mat)
    return obj


def head(x, r_out, r_in, strength, body):
    """머리: 알루미늄 원통 껍데기 + 아래 빛 면"""
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r_out + 0.06, depth=0.18, location=(x, HEAD_Y, LIGHT_Z + 0.1))
    shell = bpy.context.object
    studio.assign(shell, body)
    bpy.ops.object.shade_smooth()
    if r_in:   # 고리: 가운데가 뚫림 — 껍데기에도 구멍
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r_in - 0.06, depth=0.4, location=(x, HEAD_Y, LIGHT_Z + 0.1))
        hole = bpy.context.object
        mod = shell.modifiers.new("Hole", "BOOLEAN")
        mod.operation, mod.object = "DIFFERENCE", hole
        hole.hide_render = True
        hole.hide_viewport = True
    annulus("Light", r_out, r_in, (x, HEAD_Y, LIGHT_Z - 0.005), emission("Emit", strength))


def lamp():
    body = studio.material("LampBody", (0.80, 0.80, 0.82), roughness=0.35, metallic=1.0)
    # 바닥 판 20 × 14 × 1.5cm + 앞쪽 버튼
    studio.box("Base", (2.0, 1.4, 0.15), (0, POLE_Y, H + 0.075), body, bevel=0.02)
    btn = studio.material("Button", (0.15, 0.15, 0.16), roughness=0.5)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.12, depth=0.03, location=(0.6, POLE_Y - 0.45, H + 0.165))
    studio.assign(bpy.context.object, btn)
    # 기둥 + 앞으로 나온 팔
    top_z = LIGHT_Z + 0.2
    studio.box("Pole", (0.16, 0.16, top_z - H), (0, POLE_Y, (H + top_z) / 2), body)
    studio.box("Arm", (0.16, POLE_Y - HEAD_Y + 0.08, 0.16), (0, (POLE_Y + HEAD_Y) / 2, top_z), body)
    if VARIANT == 1:
        r_out, r_in, xs = 0.4, 0.0, [0.0]
    else:
        studio.box("Cross", (SPACING, 0.16, 0.16), (0, HEAD_Y, top_z), body)
        r_out, r_in = (0.4, 0.0) if VARIANT == 2 else (0.5, 0.35)
        xs = [-SPACING / 2, SPACING / 2]
    area = math.pi * (r_out ** 2 - r_in ** 2) * len(xs)
    for x in xs:
        head(x, r_out, r_in, POWER / area, body)


studio.new_scene()
room()
desk()
lamp()

scene = bpy.context.scene
if VIEW == "seat":
    studio.camera(lens=18)
    cam = scene.camera
    cam.location = (0, DESK_Y - D / 2 - 4.5, 12.0)
    cam.rotation_euler = ((studio.Vector((0, DESK_Y + 1.5, H + 1.0)) - cam.location)
                          .to_track_quat("-Z", "Y").to_euler())
else:
    studio.camera(lens=50)
    cam = scene.camera
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 18.0
    cam.location = (0, DESK_Y, 26.0)
    cam.rotation_euler = (0, 0, 0)

scene.cycles.max_bounces = 8
studio.render(os.path.join(os.environ.get("OUTDIR", ""), f"006_lamp_{VARIANT}_{VIEW}"),
              samples=int(os.environ.get("SAMPLES", "128")), resolution=(960, 720), view="Standard", exposure=1.5)
