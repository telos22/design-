---
name: design-studio
description: 사용자의 디자인 철학(No more, No less)에서 출발해 제품을 정의하고 Blender(bpy)로 모델링·렌더하며, 철학·일지·제품 기록을 남기는 작업 흐름. 철학·개념 이야기, 제품 아이디어, 3D 모델링, 렌더, 블렌더, 디자인 피드백, 기록·일지 요청이 나오면 사용.
---

# Design Studio

전체 작업 방식은 저장소 루트의 `CLAUDE.md` 를 따른다. 요약:

1. **시작:** `notes/no-more-no-less.md`, `notes/design-process.md`, 최근 `products/*/README.md`, 최근 `journal/` 을 읽고 이어갈 지점을 묻는다.
2. **철학·기능 정의:** 사용자의 말을 정리해 되묻는다. 모델링은 사용자가 요청할 때만.
3. **표현·구현:** 선택지 2~3개 + 추천 하나, 근거(자료·치수·계산) 포함. 판단용은 평면도(matplotlib), 느낌은 렌더(Blender).
4. **확인:** 렌더는 직접 열어 보고 문제를 고친 뒤 `SendUserFile` 로 보낸다.
5. **기록:** 결정은 `concepts/제품.md` 에 바로, 작업 끝에는 `products/NNN-이름/README.md` 와 `journal/날짜.md` 를 갱신하고, 새 원칙은 철학 노트에 추가. 커밋·푸시.

새 제품은 `templates/product.md` 를 복사해 `products/NNN-이름/README.md` 로 시작한다.
