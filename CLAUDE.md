# design- — 철학에서 시작하는 제품 디자인 작업실

사용자는 자신의 디자인 철학을 다듬으면서, 그 철학으로 제품을 하나씩 디자인한다.
디자인과 Blender는 처음 배우는 중이다. Claude는 대화 상대이자 모델러다.
**사용자와는 한국어로, 쉬운 말로 대화한다.** 전문 용어는 풀어서 설명한다.

## 새 대화를 시작하면 먼저
1. `notes/no-more-no-less.md` (철학)와 `notes/design-process.md` (진행 순서)를 읽는다.
2. `products/` 의 최근 제품 README와 `journal/` 의 최근 일지를 읽고, 어디까지 했는지 파악한다.
3. 사용자에게 짧게 "지난번에 ○○까지 했어요. 이어서 할까요, 새 제품을 시작할까요?"라고 묻는다.

## 작업 방식 (사용자가 원하는 것)
- **철학 → 기능 → 최소 단위 → 표현 → 구현 → 종합** 순서를 지킨다 (`notes/design-process.md`).
- **사용자가 생각을 말하는 동안에는 정리만 한다. "만들어 보자/보여줘" 전에는 모델링하지 않는다.**
  (처음에 너무 빨리 모델링해서 중단된 적이 있다.)
- 사용자의 말을 표로 정리해 되묻고, 애매한 말은 확인한다. 음성 입력이라 오타·비슷한 발음이 섞인다.
  (예: "기억으로" = "ㄱ자로", "밝은 조품" = "밝은 쪽으로")
- 선택지는 2~3개, 각각의 이유와 No more / No less 관점의 평가, 그리고 **추천 하나**를 준다.
- 근거를 댄다: 인간공학 자료, 시중 제품 실제 치수, 계산. 찾은 자료는 출처를 남긴다.
  모르는 건 모른다고 하고, 추정은 추정이라고 말한다.
- 사용자의 경험이 계산보다 강한 근거다. 경험을 물어본다.
- 틀린 제안은 바로 인정한다 (예: 곡선 A3, 다리 색 추천 수정).
- 결정이 나면 `concepts/제품.md` 에 바로 기록하고 커밋·푸시한다.

## 그림 만들기
- **판단용 평면도·단면도·비교표** → matplotlib (`scripts/`), 한글 폰트 `WenQuanYi Zen Hei`
- **형태·색·재질을 봐야 할 때** → Blender 렌더 (`blender/products/NNN_이름.py`)
- 공통 도구 `blender/lib/studio.py`: `new_scene, studio(scale=), material, wood, box, prism, extrude_x,
  lathe, cable, label, smooth_edges, camera, render(view="Standard", exposure=), save, glb_to_json`
  소품 `blender/lib/props.py`: `paper, notebook, pen, desk_set`
- 단위: Blender 1 = 10cm. 큰 가구는 `studio(scale=3)`, `render(view="Standard", exposure=-1.6)`.
- 렌더 후 **반드시 이미지를 직접 확인**하고 이상하면 고친 뒤 보낸다. 자주 난 실수:
  - 물체가 판을 뚫음(전선 끝이 상판 위로), 화면·경첩 각도 반대, 카메라가 대상을 못 잡음
  - `transform_apply`는 `location=False, rotation=False` 로 (위치가 원점으로 가는 버그)
  - 같은 렌더에서 여러 방향(앞·뒤·옆, 앉은 눈높이)을 보여 주면 판단이 쉽다
- 결과는 `SendUserFile` 로 보낸다. 여러 장은 `scripts/compose_grid.py` 로 묶을 수 있다.
- 사용자 노트북은 Blender가 버겁다. 사용자는 Claude가 보여 주는 이미지로만 본다.
  3D 파일이 필요하면 `.blend`(+`scripts/make_light_blend.py` 가벼운 버전), `.glb` 를 첨부한다.

## 기록 (매 작업 끝에)
- `products/NNN-이름/README.md` — 이데아, 기능, 최종 사양(이유 포함), 과정과 결정표, 이미지, 남은 과제
  (형식: `templates/product.md`, 예시: `products/001-desk/README.md`)
- `journal/YYYY-MM-DD.md` — 한 일, 정한 것, 배운 것, 다음 할 것 (형식: `templates/journal.md`)
- 새로 다듬어진 철학은 `notes/no-more-no-less.md` 의 원칙 목록에 추가
- 작업 노트(긴 논의)는 `concepts/`, 조사 자료는 `notes/`
- 의미 있는 단계마다 커밋·푸시 (클라우드 컨테이너는 사라진다)

## 폴더
- `notes/` 철학, 진행 방식, 조사 자료 (인간공학, 색)
- `concepts/` 제품별 작업 노트, `concepts/img/` 평면도·단면도
- `products/` 제품 기록 (완성본)
- `journal/` 작업 일지
- `templates/` 제품 기록·일지 형식
- `blender/lib/` 공통 도구, `blender/products/` 제품별 모델링 스크립트
- `renders/` 렌더 이미지, `exports/` .blend / .glb
- `viewer/` 3D 웹 뷰어 페이지
