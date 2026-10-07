"""001 큰 책상 확정안 — 큰 화면용 한 장 (책상이 화면을 채우도록)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy
import studio

bpy.ops.wm.open_mainfile(filepath=os.path.join(studio.REPO, "exports", "001_desk_big_final.blend"))
cam = bpy.context.scene.camera
bpy.data.objects.remove(cam)
studio.camera(target=(0.6, 0, 4.2), distance=27, height=12, angle_deg=-26, lens=48)
print(studio.render("001_desk_big_hero", samples=96, resolution=(2400, 1500), view="Standard", exposure=-1.6))
