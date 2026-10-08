"""006 조명 003 — 빛을 내는 부분(머리)과 조절 다이얼. 몸체(받침)는 아직 정하지 않아 머리를 빛의 자리에 띄워 둔다.
머리: 앞뒤로 긴 판 60 × 22 × 2.5cm, 알루미늄 테두리, 아래·위 두 면이 빛남 (LED는 테두리 안에 숨김)
     긴 축(앞뒤)을 중심으로 기울어짐 — 아래 빛이 쓰는 곳(오른쪽 아래)을 향하게 약 20°
자리: 오른손잡이 기준, 사람 왼쪽 55cm, 책상 앞 모서리에서 10cm 안쪽, 높이 190cm
다이얼: 책상 앞 레일 왼쪽 바깥 면 (손을 내리면 닿는 곳). 돌리기 = 밝기·색·위 빛 함께, 누르기 = 켜고 끄기
단위 1 = 10cm, 사람 쪽 = -y"""
import importlib.util
import math
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
import bpy
import mathutils
import props
import studio


def load(name):
    spec = importlib.util.spec_from_file_location("m_" + name.replace("0", "z"), os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dk = load("001_desk_steel")
FRONT = -dk.D / 2  # 책상 앞 모서리 y
PERSON_X = -4.0  # 왼쪽 칸 가운데
HEAD = (PERSON_X - 5.5, FRONT + 1.0, 19.0)
TILT = math.radians(12)
L, Wd, Th = 6.0, 2.2, 0.25


def emission(name, strength, color=(1.0, 0.87, 0.74)):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*color, 1)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return mat


def head(m, lit=True):
    """원점 = 판 가운데. 반환: 머리 묶음(빈 객체)"""
    before = set(bpy.data.objects)
    studio.box("HeadRim", (Wd, L, Th), (0, 0, 0), m["alu"], bevel=0.08)
    studio.box("FaceDown", (Wd - 0.16, L - 0.16, 0.01), (0, 0, -Th / 2 - 0.004), m["down"] if lit else m["opal"])
    studio.box("FaceUp", (Wd - 0.16, L - 0.16, 0.01), (0, 0, Th / 2 + 0.004), m["up"] if lit else m["opal"])
    # 아래 면 칸살: 긴 축과 나란한 얇은 날개 13장, 간격 약 1.5cm·깊이 2cm
    # → 아래(쓰는 곳, 내려다본 각 약 64°)로는 빛이 나가고, 눈(약 46°) 쪽 비스듬한 방향은 가린다
    n = 13
    for i in range(n):
        x = -(Wd - 0.2) / 2 + i * (Wd - 0.2) / (n - 1)
        studio.box("Louver", (0.012, L - 0.2, 0.2), (x, 0, -Th / 2 - 0.1), m["louver"])
    for s in (-1, 1):  # 기울기 축 (앞뒤 끝의 짧은 축 — 몸체가 여기에 붙는다)
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.12, depth=0.2, location=(0, s * (L / 2 + 0.1), 0))
        pin = bpy.context.object
        pin.rotation_euler.x = math.pi / 2
        bpy.ops.object.shade_smooth()
        studio.assign(pin, m["alu"])
    if lit:
        for name, z, energy, rot in (("DownLight", -Th / 2 - 0.02, 9000, 0.0), ("UpLight", Th / 2 + 0.02, 5000, math.pi)):
            bpy.ops.object.light_add(type="AREA", location=(0, 0, z))
            lt = bpy.context.object
            lt.name = name
            lt.data.shape = "RECTANGLE"
            lt.data.size, lt.data.size_y = Wd - 0.2, L - 0.2
            lt.data.energy = energy
            lt.data.color = (1.0, 0.88, 0.76)
            lt.rotation_euler.x = rot
    made = set(bpy.data.objects) - before
    pivot = bpy.data.objects.new("Head", None)
    bpy.context.collection.objects.link(pivot)
    for o in made:
        o.parent = pivot
    pivot.location = HEAD
    pivot.rotation_euler.y = -TILT  # 아래 면이 오른쪽(+x) 아래를 향함
    return pivot


def dial(m):
    """앞 레일 바깥 면 왼쪽, 사람 쪽을 보는 둥근 다이얼"""
    y = FRONT + dk.LEG - 0.0  # 레일 바깥 면 근처
    x, z = -7.0, dk.FZ
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.24, depth=0.22, location=(x, -(dk.IY) - 0.11, z))
    d = bpy.context.object
    d.name = "Dial"
    d.rotation_euler.x = math.pi / 2
    bpy.ops.object.shade_smooth()
    b = d.modifiers.new("Bevel", "BEVEL")
    b.width, b.segments = 0.03, 3
    studio.assign(d, m["alu"])
    studio.box("DialMark", (0.03, 0.01, 0.12), (x, -(dk.IY) - 0.225, z + 0.14), m["dark"])
    return d


def person(m):
    g = m["ghost"]
    px, ey = PERSON_X, FRONT - 3.0
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.95, location=(px, ey - 0.3, 12.4))
    bpy.ops.object.shade_smooth()
    studio.assign(bpy.context.object, g)
    studio.box("Torso", (3.4, 1.9, 4.8), (px, ey - 0.6, 8.9), g, bevel=0.6)
    for s in (-1, 1):
        sx = px + s * 1.6
        studio.cable("Arm", [(sx, ey - 0.4, 10.8), (sx + s * 0.4, ey + 1.2, 8.6), (px + s * 0.9, FRONT + 1.4, dk.H + 0.25)], g, radius=0.38)
        studio.cable("Leg", [(px + s * 0.9, ey - 0.4, 4.9), (px + s * 0.9, FRONT + 0.6, 5.0), (px + s * 0.9, FRONT + 0.8, 0.3)], g, radius=0.55)
    studio.box("Stool", (4.0, 4.0, 0.4), (px, ey - 0.6, 4.3), m["dark"], bevel=0.1)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=4.1, location=(px, ey - 0.6, 2.05))
    studio.assign(bpy.context.object, m["dark"])


def scene(name, cam_loc, target, lens=35, lit=True, res=(1500, 1000), samples=96):
    studio.new_scene()
    studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.18 if lit else 0.5, scale=3)
    if lit:  # 스튜디오 조명은 아주 약하게 — 조명 003의 빛이 주인공
        for o in list(bpy.data.objects):
            if o.type == "LIGHT":
                o.data.energy *= 0.08
    m = dk.materials()
    m.update({
        "down": emission("DownFace", 9.0),
        "up": emission("UpFace", 7.0),
        "opal": studio.material("Opal", (0.85, 0.84, 0.82), roughness=0.4),
        "louver": studio.material("Louver", (0.9, 0.9, 0.89), roughness=0.3),
        "ghost": studio.material("Ghost", (0.55, 0.55, 0.56), roughness=0.8),
        "dark": studio.material("Dark", (0.08, 0.08, 0.085), roughness=0.6),
        "ceiling": studio.material("Ceiling", (0.80, 0.80, 0.79), roughness=0.9),
    })
    dk.desk(m, holes=False)
    props.notebook(PERSON_X + 0.4, FRONT + 2.2, dk.H, angle=0.05)
    props.pen(PERSON_X + 1.6, FRONT + 2.0, dk.H, angle=0.4)
    person(m)
    head(m, lit)
    dial(m)
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 26.0))
    ceil = bpy.context.object
    ceil.rotation_euler.x = math.pi  # 아래를 보는 면
    studio.assign(ceil, m["ceiling"])
    cam = studio.camera(lens=lens)
    cam.location = cam_loc
    cam.rotation_euler = (mathutils.Vector(target) - mathutils.Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
    return studio.render(name, samples=samples, resolution=res, view="Standard", exposure=-0.6 if lit else -1.6)


if __name__ == "__main__":
    only = sys.argv[1:]
    shots = {
        "006_lamp_head_overview": dict(cam_loc=(-27.0, -24.0, 15.0), target=(-6.0, -1.5, 11.5), lens=30),
        "006_lamp_head_behind": dict(cam_loc=(-4.0, -26.0, 14.0), target=(-6.0, 0.0, 11.5), lens=32),
        "006_lamp_head_close": dict(cam_loc=(-16.5, -10.0, 14.5), target=(-9.5, -2.0, 18.6), lens=40, lit=False),
        "006_lamp_eye_view": dict(cam_loc=(-4.0, -5.2, 12.2), target=(-4.6, 0.5, 8.4), lens=16),
        "006_lamp_dial": dict(cam_loc=(-5.5, -9.0, 5.0), target=(-7.0, -2.8, 6.7), lens=50, lit=False),
    }
    for k, v in shots.items():
        if not only or k in only:
            print(scene(k, **v))
