"""005 스탠드 — 직접 조명과 간접 조명이 사람 눈에 어떻게 보이는지 비교.
저녁, 방의 다른 불은 모두 끈 상태. 스탠드 하나만 켠다. 네 가지 모두 같은 빛의 양(루멘)이라고 가정.
  1 갓 스탠드 (좁은 직접)   2 긴 막대 + 확산판 (넓은 직접)
  3 위아래 겸용 (아래 60%, 위 40%)   4 간접 (천장으로만)
보기: seat = 앉은 눈높이, room = 방 뒤쪽에서
사용: python3 005_lamp_direct_indirect.py <1|2|3|4> <seat|room>
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
H = 7.2                 # 상판 높이 72cm
W, D = 16.0, 6.0        # 160 × 60
DESK_Y = -3.5           # 상판 중심: 뒤쪽 끝이 벽에서 5cm
CEIL = 27.0             # 천장 2.7m
LUMEN_W = 12.0          # 스탠드 하나의 빛의 양 (렌더용 값, 네 가지 모두 같음)
LAMP_Z = H + 4.5        # 빛이 나오는 높이: 상판 위 45cm


def room():
    wall = studio.material("Wall", (0.80, 0.79, 0.77), roughness=0.95)      # 무광 흰 벽
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
    top = studio.material("DeskTop", (0.45, 0.43, 0.40), roughness=0.75)   # 따뜻한 밝은 회색, 무광
    alu = studio.material("Alu", (0.8, 0.8, 0.82), roughness=0.35, metallic=1.0)
    studio.box("Top", (W, D, 0.25), (0, DESK_Y, H - 0.125), top, bevel=0.02)
    for sx in (-1, 1):
        for sy in (-1, 1):
            studio.box("Leg", (0.4, 0.4, H - 0.25), (sx * (W / 2 - 0.3), DESK_Y + sy * (D / 2 - 0.3), (H - 0.25) / 2), alu)
    props.desk_set(-1.0, DESK_Y + 0.2, H)
    props.paper(-5.8, DESK_Y + 0.4, H, angle=0.15)      # 왼쪽 끝 종이: 가장자리 밝기 보기
    props.paper(5.6, DESK_Y + 0.1, H, angle=-0.1)       # 오른쪽 끝 종이
    # 의자 대신 사람 자리 표시는 생략 (카메라가 앉은 눈)


def glow(name, size, loc, strength):
    """확산판: 눈에 보이는 밝은 면 (빛 계산은 따로 둔 조명이 맡음)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.93, 0.82, 1)
    em.inputs["Strength"].default_value = strength
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(em.outputs[0], out.inputs[0])
    return studio.box(name, size, loc, m)


def area(name, size_x, size_y, loc, power, up=False):
    bpy.ops.object.light_add(type="AREA", location=loc)
    l = bpy.context.object
    l.name = name
    l.data.shape = "RECTANGLE"
    l.data.size, l.data.size_y = size_x, size_y
    l.data.energy = power
    l.data.color = (1.0, 0.93, 0.82)       # 약 3500K 따뜻한 흰색
    if up:
        l.rotation_euler.x = math.pi
    return l


def shade_lamp():
    """1 갓 스탠드: 받침 + 기둥 + 팔 + 원뿔 갓, 빛은 아래로 좁게"""
    body = studio.material("LampBody", (0.08, 0.08, 0.085), roughness=0.4, metallic=0.6)
    bx, by = 4.5, DESK_Y + 1.8
    hx, hy = 2.0, DESK_Y + 0.3              # 갓 위치: 노트 위쪽
    bpy.ops.mesh.primitive_cylinder_add(radius=0.75, depth=0.25, location=(bx, by, H + 0.125))
    studio.assign(bpy.context.object, body)
    studio.box("Pole", (0.15, 0.15, LAMP_Z + 0.9 - H), (bx, by, (H + LAMP_Z + 0.9) / 2), body)
    arm_len = math.hypot(bx - hx, by - hy)
    arm = studio.box("Arm", (arm_len, 0.12, 0.12), ((bx + hx) / 2, (by + hy) / 2, LAMP_Z + 0.9), body)
    arm.rotation_euler.z = math.atan2(hy - by, hx - bx)
    shade = studio.lathe("Shade", [(0.25, 1.0), (0.45, 0.7), (0.9, 0.0)], thickness=0.04, smooth=False)
    shade.location = (hx, hy, LAMP_Z)
    studio.assign(shade, body)
    glow("Bulb", (0.5, 0.5, 0.05), (hx, hy, LAMP_Z + 0.2), 30)
    bpy.ops.object.light_add(type="SPOT", location=(hx, hy, LAMP_Z + 0.4))
    s = bpy.context.object
    s.data.spot_size = math.radians(60)
    s.data.spot_blend = 0.25
    s.data.shadow_soft_size = 0.25
    s.data.color = (1.0, 0.93, 0.82)
    # 같은 루멘: 스팟은 원뿔 밖 빛을 버리므로 그만큼 올려 준다
    frac = (1 - math.cos(s.data.spot_size / 2)) / 2
    s.data.energy = LUMEN_W / frac * 0.85


def bar_lamp(down, up):
    """2·3·4 긴 막대: 상판 뒤쪽 양 끝 두 기둥 + 길이 100cm 막대. down/up: 아래·위로 보내는 빛의 비율"""
    body = studio.material("BarBody", (0.80, 0.80, 0.82), roughness=0.35, metallic=1.0)   # 알루미늄
    y_post, y_bar = DESK_Y + 2.6, DESK_Y + 1.6
    for sx in (-1, 1):
        studio.box("Post", (0.2, 0.2, LAMP_Z + 0.3 - H), (sx * 5.2, y_post, (H + LAMP_Z + 0.3) / 2), body)
        studio.box("Foot", (0.6, 0.8, 0.08), (sx * 5.2, y_post - 0.1, H + 0.04), body)
        studio.box("Link", (0.2, y_post - y_bar + 0.3, 0.2), (sx * 5.2, (y_post + y_bar) / 2, LAMP_Z + 0.2), body)
    studio.box("Bar", (10.6, 0.6, 0.3), (0, y_bar, LAMP_Z + 0.15), body)
    if down:
        glow("DiffuserDown", (10.0, 0.45, 0.02), (0, y_bar, LAMP_Z - 0.01), 6)
        area("LightDown", 10.0, 0.45, (0, y_bar, LAMP_Z - 0.03), LUMEN_W * down)
    if up:
        glow("DiffuserUp", (10.0, 0.45, 0.02), (0, y_bar, LAMP_Z + 0.31), 6)
        area("LightUp", 10.0, 0.45, (0, y_bar, LAMP_Z + 0.33), LUMEN_W * up, up=True)


studio.new_scene()
room()
desk()
if VARIANT == 1:
    shade_lamp()
else:
    bar_lamp(*{2: (1.0, 0.0), 3: (0.6, 0.4), 4: (0.0, 1.0)}[VARIANT])

if VIEW == "seat":
    # 앉은 사람의 눈: 바닥에서 120cm, 상판 앞 끝에서 45cm 뒤
    studio.camera(target=(0, DESK_Y + 2.5, H + 1.0), distance=0, height=0, lens=18)
    cam = bpy.context.scene.camera
    cam.location = (0, DESK_Y - D / 2 - 4.5, 12.0)
    cam.rotation_euler = ((studio.Vector((0, DESK_Y + 2.0, H + 1.5)) - cam.location)
                          .to_track_quat("-Z", "Y").to_euler())
else:
    # 방 뒤쪽 모서리에서 선 눈높이로: 천장까지 보이게
    studio.camera(lens=18)
    cam = bpy.context.scene.camera
    cam.location = (8.0, -21.0, 14.5)
    cam.rotation_euler = ((studio.Vector((-0.5, DESK_Y, 12.5)) - cam.location)
                          .to_track_quat("-Z", "Y").to_euler())

bpy.context.scene.cycles.max_bounces = 8
studio.render(os.path.join(os.environ.get("OUTDIR", ""), f"005_lamp_{VARIANT}_{VIEW}"), samples=96, resolution=(960, 720), view="Standard", exposure=1.5)
