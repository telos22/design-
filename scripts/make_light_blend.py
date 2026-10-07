"""노트북용 가벼운 .blend: 화면을 Solid(재질 색 표시)로 열고, 렌더 엔진은 EEVEE, 바닥 베벨 단순화.
사용: python3 scripts/make_light_blend.py 원본.blend 출력.blend"""
import sys

import bpy

src, out = sys.argv[1], sys.argv[2]
bpy.ops.wm.open_mainfile(filepath=src)
scene = bpy.context.scene
for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    try:
        scene.render.engine = engine
        break
    except TypeError:
        continue
floor = bpy.data.objects.get("Floor")
if floor and "Bevel" in floor.modifiers:
    floor.modifiers["Bevel"].segments = 4
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type == "VIEW_3D":
                space.shading.type = "SOLID"
                space.shading.color_type = "MATERIAL"
                space.shading.light = "STUDIO"
                space.overlay.show_floor = False
bpy.ops.wm.save_as_mainfile(filepath=out)
print("engine:", scene.render.engine)
