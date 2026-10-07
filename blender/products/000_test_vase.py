"""설치 확인용 테스트: 단면 윤곽선을 회전시켜 만든 꽃병."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import studio

studio.new_scene()
studio.studio()

# (반지름, 높이) — 바닥 중심에서 시작해 몸통이 부풀고 목이 좁아졌다 입구가 살짝 벌어짐
profile = [(0.0, 0.0), (0.32, 0.0), (0.45, 0.25), (0.48, 0.55), (0.30, 1.0),
           (0.16, 1.25), (0.15, 1.40), (0.20, 1.52)]
vase = studio.lathe("Vase", profile, thickness=0.025)
studio.assign(vase, studio.material("Ceramic", (0.55, 0.42, 0.33), roughness=0.35))

studio.camera(target=(0, 0, 0.75), distance=5.5, height=1.8)
print(studio.render("000_test_vase", samples=48))
studio.save("000_test_vase")
