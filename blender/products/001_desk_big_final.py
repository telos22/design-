"""001 큰 책상 — 현재 확정안 (3D 보기용 모델 + 렌더).
상판 160×60×2.5cm 자작합판 + 무광 따뜻한 밝은 회색(반사율 ≈45%)
다리 알루미늄 30×30mm, 모서리 끝 / 프레임 알루미늄 40×20mm, 다리 안쪽 면 / 높이 72cm
단위 1 = 10cm (내보낼 때 미터로 변환)"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy
import props
import studio

W, D, T, H = 16.0, 6.0, 0.25, 7.2
LEG, FR_H, FR_T = 0.3, 0.4, 0.2


def desk():
    top = studio.material("Top", (0.47, 0.45, 0.41), roughness=0.65)
    ply = studio.material("PlyEdge", (0.62, 0.48, 0.32), roughness=0.7)
    alu = studio.material("Alu", (0.80, 0.80, 0.82), roughness=0.35, metallic=1.0)
    zt = H - T / 2
    studio.box("Ply", (W, D, T - 0.02), (0, 0, zt), ply)
    studio.box("SkinTop", (W, D, 0.01), (0, 0, zt + T / 2 - 0.005), top)
    studio.box("SkinBottom", (W, D, 0.01), (0, 0, zt - T / 2 + 0.005), top)
    fz = H - T - FR_H / 2
    ix, iy = W / 2 - LEG, D / 2 - LEG
    for s in (-1, 1):
        studio.box("FrameLong", (2 * ix, FR_T, FR_H), (0, s * (iy - FR_T / 2), fz), alu)
        studio.box("FrameShort", (FR_T, 2 * iy, FR_H), (s * (ix - FR_T / 2), 0, fz), alu)
    leg_h = H - T
    for sx in (-1, 1):
        for sy in (-1, 1):
            studio.box("Leg", (LEG, LEG, leg_h), (sx * (W / 2 - LEG / 2), sy * (D / 2 - LEG / 2), leg_h / 2), alu)
    props.notebook(-3.5, -0.8, H, angle=0.05)
    props.paper(3.5, 0.3, H, angle=-0.1)
    props.pen(3.7, -0.4, H + 0.006, angle=0.6)


# 1) 렌더
studio.new_scene()
studio.studio(floor_color=(0.62, 0.62, 0.61), world_strength=0.5, scale=3)
desk()
studio.camera(target=(0, 0, 4.4), distance=24, height=13, angle_deg=-30, lens=40)
print(studio.render("001_desk_big_final", samples=96, resolution=(1600, 1100), view="Standard", exposure=-1.6))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(studio.REPO, "exports", "001_desk_big_final.blend"))  # 조명·카메라 포함

# 2) 3D 모델 (책상만, 미터 단위)
studio.new_scene()
desk()
for o in bpy.data.objects:   # 10cm 단위 → 미터 (모디파이어는 export_apply로 적용)
    o.location = o.location * 0.1
    o.scale = o.scale * 0.1
base = os.path.join(studio.REPO, "exports", "001_desk_big_final")
bpy.ops.export_scene.gltf(filepath=base + ".glb", export_apply=True)
studio.glb_to_json(base + ".glb", base + ".gltf.json")   # 웹 뷰어용 (JSON 한 파일)
print(base, os.path.getsize(base + ".gltf.json"))
