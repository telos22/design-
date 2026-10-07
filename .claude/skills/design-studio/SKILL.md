---
name: design-studio
description: 사용자가 공부한 철학/개념을 노트로 정리하고, 그 개념을 디자인 언어로 번역해 Blender(bpy)로 제품을 모델링·렌더링하는 작업 흐름. 철학·개념 이야기, 제품 아이디어, 3D 모델링, 렌더, 블렌더, 디자인 피드백이 나오면 사용.
---

# Design Studio 작업 흐름

사용자는 디자인과 Blender를 처음 배우는 사람이다. 한국어로, 용어는 쉽게 풀어서 설명하고,
매 단계에서 "왜 이런 형태/재질을 골랐는지"를 개념과 연결해 짧게 알려준다.

## 1. 개념 기록 → `notes/`
- 사용자가 말한 철학·개념을 `notes/<주제>.md` 로 정리한다 (말투·표현은 최대한 사용자 것 유지).
- 구조: `## 핵심 개념` / `## 내 해석` / `## 출처·인용` / `## 디자인으로 옮길 단서`
- 이미 있는 노트면 덧붙이고 날짜를 남긴다.

## 2. 디자인 언어로 번역 → `concepts/`
`concepts/<제품명>.md` 에 개념 → 디자인 요소 대응표를 만든다:
형태(실루엣, 비례), 재질, 색, 표면 질감, 사용 방식/행위, 치수(cm).
선택지가 갈리면 2~3안으로 제시하고 사용자에게 고르게 한다.

## 3. 모델링 → `blender/products/NNN_<이름>.py`
- 반드시 `blender/lib/studio.py` 를 import 해서 쓴다:
  `new_scene()`, `studio()`, `material()`, `assign()`, `lathe(profile)`, `camera()`, `render(name)`, `save(name)`.
- 회전체(컵, 꽃병, 조명 갓)는 `lathe`, 그 외는 bpy primitive + modifier(Bevel, Solidify, Subsurf, Boolean, Array).
- 단위는 1 = 10cm 정도로 통일하고, 스크립트 상단 docstring에 개념과 치수를 적는다.
- 반복 쓰이는 도구는 `studio.py` 에 추가한다.

## 4. 렌더 → 보여주기 → 반복
- 실행: `python3 blender/products/NNN_<이름>.py` (Cycles CPU, 30~60초)
- 결과 `renders/*.png` 를 Read로 직접 확인한 뒤 SendUserFile로 사용자에게 보낸다.
- 시안 비교가 필요하면 각도/버전을 바꿔 여러 장 렌더한다 (`NNN_<이름>_v2`).
- Draco/MeshOptimizer ERROR 로그는 무해하다.

## 5. 저장
- `exports/*.blend`(사용자 PC Blender에서 열기), `*.glb`(웹/폰 3D 뷰어).
- 의미 있는 단계마다 커밋·푸시 (컨테이너는 사라진다).
