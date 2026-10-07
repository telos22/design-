#!/bin/bash
# 클라우드 세션 시작 시 Blender(bpy) 설치. 이미 있으면 건너뜀.
python3 -c "import bpy" 2>/dev/null && exit 0
pip install --quiet bpy numpy >/dev/null 2>&1 || echo "bpy 설치 실패: pip install bpy 를 수동으로 실행하세요" >&2
exit 0
