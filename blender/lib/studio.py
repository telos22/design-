"""제품 렌더링용 공통 도구: 빈 씬 만들기, 스튜디오 조명, 카메라, 재질, 렌더/내보내기."""
import math
import os

import bpy
from mathutils import Vector

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def new_scene():
    """기본 큐브/조명/카메라를 지운 빈 씬."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def material(name, color=(0.8, 0.8, 0.8), roughness=0.5, metallic=0.0, transmission=0.0):
    """간단한 PBR 재질. color는 0~1 RGB."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Transmission Weight"].default_value = transmission
    return mat


def box(name, size, location, mat=None, bevel=0.0):
    """size=(가로, 깊이, 높이) 직육면체, location은 중심, bevel은 모서리 둥글기."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        b = obj.modifiers.new("Bevel", "BEVEL")
        b.width, b.segments = bevel, 3
    if mat:
        assign(obj, mat)
    return obj


def wood(name, color, grain=0.15, roughness=0.6, scale=1.0):
    """나무결 재질. color는 평균색(선형 RGB), grain은 결의 진하기."""
    mat = material(name, color, roughness)
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (0.15 * scale, 1.2 * scale, 1.0)
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type, wave.bands_direction = "BANDS", "Y"
    wave.inputs["Scale"].default_value = 3.0
    wave.inputs["Distortion"].default_value = 6.0
    wave.inputs["Detail"].default_value = 3.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    lo = tuple(c * (1 - grain) for c in color)
    hi = tuple(min(1.0, c * (1 + grain)) for c in color)
    ramp.color_ramp.elements[0].color = (*lo, 1)
    ramp.color_ramp.elements[1].color = (*hi, 1)
    nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
    nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def label(text, location, size=0.6, color=(0.1, 0.1, 0.1)):
    """바닥에 눕힌 한글 글자."""
    bpy.ops.object.text_add(location=location)
    obj = bpy.context.object
    obj.data.body = text
    obj.data.size = size
    obj.data.align_x = "CENTER"
    font = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
    if os.path.exists(font):
        obj.data.font = bpy.data.fonts.load(font, check_existing=True)
    assign(obj, material("Label", color, roughness=0.8))
    return obj


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def studio(floor_color=(0.92, 0.91, 0.89), world_strength=0.35, scale=1.0):
    """무한 배경(사이클로라마) 바닥 + 키/필/림 3점 조명.
    scale: 큰 제품(가구 등)일 때 배경·조명을 함께 키운다."""
    scene = bpy.context.scene
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (*floor_color, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = world_strength
    scene.world = world

    bpy.ops.mesh.primitive_plane_add(size=40 * scale, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Floor"
    # 뒤쪽 벽으로 부드럽게 휘어 올라가는 배경
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.mode_set(mode="OBJECT")
    for v in floor.data.vertices:
        v.select = v.co.y > 0
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 15 * scale)})
    bpy.ops.object.mode_set(mode="OBJECT")
    bev = floor.modifiers.new("Bevel", "BEVEL")
    bev.width, bev.segments = 4 * scale, 16
    floor.location.y = 6 * scale
    assign(floor, material("Floor", floor_color, roughness=0.9))

    def area(name, loc, energy, size):
        bpy.ops.object.light_add(type="AREA", location=Vector(loc) * scale)
        light = bpy.context.object
        light.name = name
        light.data.energy, light.data.size = energy * scale**2, size * scale
        direction = Vector((0, 0, 0.5 * scale)) - light.location
        light.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        return light

    area("Key", (4, -4, 5), 800, 3)
    area("Fill", (-5, -3, 3), 250, 4)
    area("Rim", (0, 5, 4), 400, 2)


def camera(target=(0, 0, 0.5), distance=6, height=2.5, angle_deg=-35, lens=60):
    """target을 바라보는 카메라. angle_deg는 정면 기준 좌우 회전."""
    a = math.radians(angle_deg)
    loc = Vector((distance * math.sin(a), -distance * math.cos(a), height))
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.data.lens = lens
    cam.rotation_euler = (Vector(target) - loc).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    return cam


def render(name, samples=64, resolution=(1200, 900), view="AgX", exposure=0.0):
    """Cycles CPU로 renders/<name>.png 저장."""
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.view_settings.view_transform = view
    scene.view_settings.exposure = exposure
    path = os.path.join(REPO, "renders", f"{name}.png")
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def save(name):
    """exports/<name>.blend 와 .glb 저장 (내 컴퓨터 블렌더/웹 뷰어에서 열기용)."""
    base = os.path.join(REPO, "exports", name)
    bpy.ops.wm.save_as_mainfile(filepath=base + ".blend")
    bpy.ops.export_scene.gltf(filepath=base + ".glb", use_selection=False)
    return base


def lathe(name, profile, segments=96, thickness=0.0, smooth=True):
    """단면 윤곽선을 Z축으로 회전시켜 회전체를 만든다 (꽃병, 컵, 조명 갓 등).
    profile: [(반지름, 높이), ...] 아래에서 위 순서."""
    mesh = bpy.data.meshes.new(name)
    verts = [(r, 0, z) for r, z in profile]
    edges = [(i, i + 1) for i in range(len(verts) - 1)]
    mesh.from_pydata(verts, edges, [])
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    screw = obj.modifiers.new("Lathe", "SCREW")
    screw.steps = screw.render_steps = segments
    screw.use_merge_vertices = True
    screw.use_normal_calculate = True
    if thickness:
        obj.modifiers.new("Thick", "SOLIDIFY").thickness = thickness
    if smooth:
        obj.modifiers.new("Smooth", "SUBSURF").levels = 2
        for poly in mesh.polygons:
            poly.use_smooth = True
    return obj


def prism(name, points, height, location=(0, 0, 0), mat=None):
    """바닥 모양(points: [(x, y), ...], 반시계 방향)을 height만큼 위로 세운 기둥. location은 바닥 기준점."""
    n = len(points)
    verts = [(x, y, 0) for x, y in points] + [(x, y, height) for x, y in points]
    faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    bpy.context.collection.objects.link(obj)
    if mat:
        assign(obj, mat)
    return obj


def smooth_edges(obj, angle_deg=40):
    """곡면은 부드럽게, 각진 모서리는 날카롭게 (자동 스무스)."""
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_auto_smooth(angle=math.radians(angle_deg))
    return obj


def glb_to_json(glb_path, out_path):
    """GLB를 버퍼를 base64로 품은 glTF JSON 한 파일로 바꾼다 (.glb를 못 올리는 웹 게시용)."""
    import base64
    import json
    import struct
    data = open(glb_path, "rb").read()
    offset, doc, binary = 12, None, b""
    while offset < len(data):
        length, kind = struct.unpack_from("<II", data, offset)
        chunk = data[offset + 8: offset + 8 + length]
        if kind == 0x4E4F534A:
            doc = json.loads(chunk)
        elif kind == 0x004E4942:
            binary = chunk
        offset += 8 + length
    doc["buffers"][0]["uri"] = "data:application/octet-stream;base64," + base64.b64encode(binary).decode()
    with open(out_path, "w") as f:
        json.dump(doc, f, separators=(",", ":"))


def cable(name, points, mat, radius=0.02):
    """점들을 부드럽게 잇는 전선 (NURBS 곡선)."""
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = radius
    spline = curve.splines.new("NURBS")
    spline.points.add(len(points) - 1)
    for p, co in zip(spline.points, points):
        p.co = (*co, 1)
    spline.use_endpoint_u = True
    spline.order_u = 3
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def extrude_x(name, profile_yz, x0, x1, mat=None):
    """(y, z) 단면을 x0에서 x1까지 밀어낸 덩어리 (옆판, 단면이 있는 레일 등)."""
    n = len(profile_yz)
    verts = [(x0, y, z) for y, z in profile_yz] + [(x1, y, z) for y, z in profile_yz]
    faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if mat:
        assign(obj, mat)
    return obj
