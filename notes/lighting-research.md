# 조명 조사 — 빛의 색과 밝기 (2026-10-08)

## 빛의 색(색온도, K)
- 3000K vs 6500K 모의 사무실(57명, Building and Environment 2019): 차가운 빛이 각성·수행에 이득 없음, 오히려 부정적 감정 증가. 밝기(1000 vs 100 lx)가 반응 속도에 더 큰 영향
- Cochrane 리뷰(5연구 282명): 차가운 흰빛이 낮 근무자 각성을 높일 수도 있으나 근거 얇음(2연구 163명). 눈 불편·두통은 줄 수도
- 8000K·12000K(500 lx, 22명): 졸림 감소 — 매우 차가운 빛에서만
- 밤: 잠들기 전 4시간 아이패드 읽기(12명) → 잠드는 데 약 10분 더, 멜라토닌 감소, 다음 날 덜 깸 (Chang 2015). 따뜻한 빛이 낫다는 건 주로 판매처 주장, 가장 강한 근거는 '저녁엔 어둡게'
- Kruithof 곡선(밝기마다 맞는 색이 있다): 검증 실패. Fotios 2016: 낮은 밝기만 피하라, 특정 색을 선호하지 않음

## 표준 (EN 12464-1, 2차 자료)
- 읽기·쓰기·화면 작업: 유지 조도 500 lx 이상, 눈부심 UGR 19 이하, 연색성 Ra 80 이상, 균일도 0.6 이상
- 색온도는 숫자 요구 없음 (가이드: 사무실 3000~4000K)

## 정리 (Claude)
- 색보다 밝기와 눈부심이 중요하다는 쪽에 근거가 더 있음
- '이상적인 색'도 하나가 아님 → 하지 않아야 할 것: 너무 어둡지 않다(500 lx), 눈부시지 않다(UGR 19), 색이 왜곡되지 않는다(Ra 80), 밤에 밝은 빛을 오래 보지 않는다

## 출처
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6494162 (3000K vs 6500K)
- https://www.cochrane.org/evidence/CD012243_workplace-lighting-improving-alertness-and-mood-daytime-workers
- https://jhsw.tums.ac.ir/article-1-6581-en.html (4000~12000K)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4386345 · https://hms.harvard.edu/news/e-readers-foil-good-nights-sleep (Chang 2015)
- https://en.wikipedia.org/wiki/Kruithof_curve · https://eprints.whiterose.ac.uk/98531/ (Fotios 2016)
- https://boxic24.com/english/ratgeber/workplace-lux-levels · https://www.performanceinlighting.com/au/en/en-12464-1 (EN 12464-1)

## 빛이 어디서 와야 하나 (2026-10-08)
- 그림자: 오른손잡이는 왼쪽, 왼손잡이는 오른쪽에서. 조금 앞쪽(어깨선보다 앞)에서 (Lighting Research Center, 판매처 가이드)
- 반사(베일 반사): 빛이 작업면에 부딪혀 같은 각도로 눈에 들어오면 글씨가 뿌옇게 보임. 사람 바로 앞 위쪽이 '문제 구역'인데 스탠드가 흔히 거기 놓임 → 옆에서(한쪽 또는 양쪽) 비추는 게 해법 (LRC). 조명이 너무 낮아도 반사 (특허)
- 눈부심: 원인은 밝기보다 광원이 눈높이에서 직접 보이는 것. 깊은 갓, 아래로 기울이기, 높이기, 확산판 (가이드). 갓의 표준 차단 각도는 찾지 못함
- 화면 반사: 광원·화면·눈이 한 줄이 되면 반사. 모니터 위 막대 조명(BenQ ScreenBar)은 비대칭 반사판으로 빛을 책상에만 보낸다고 주장 (제조사)
- 무광 책상면이 반사를 줄임 → 책상 001 상판 무광 (이미 맞음)
- 출처: https://www.lrc.rpi.edu/programs/NLPIP/lightingAnswers/pdf/print/LAtask.pdf · https://www.lrc.rpi.edu/programs/lightHealth/AARP/senior/helpingOlderAdults/smallDetails.asp · https://www.back2.co.uk/blogs/article/ergonomic-desk-lamps · https://patents.google.com/patent/US4254449 · https://www.ulanzi.com/blogs/knowledges/desk-lighting-screen-glare · https://www.benq.eu/en-eu/lighting/monitor-light/screenbar

## 광원 종류와 빛이 나오는 모양 (2026-10-08)
| 광원 | 2700~4000K·조절 | 밝기 조절 | 깜빡임 | 열 | 눈부심 | 구할 수 있나 |
|---|---|---|---|---|---|---|
| 백열·할로겐 | 2700~3000K만 | 어둡게 하면 자연히 따뜻해짐 | 적음 | 뜨거움 | 작은 점 | 한국 2014 생산·수입 중단, EU 할로겐 2018~2023 퇴출 |
| 형광등 | 조절 어려움 | 어려움 | 옛 제품 문제 | 보통 | 긴 관 | EU 2021~2023 퇴출, 수은 |
| LED | 가능 (따뜻한·차가운 LED 섞기) | 가능 | 어둡게 할 때 위험(PWM) → 깜빡임 없는 구동 필요 (IEEE 1789: 120Hz면 10% 이하) | 적음 | 작고 매우 밝은 점 → 확산 필요 | 쉬움 |
| OLED | 가능 | 가능 | 적음 | 적음 | 넓은 면이라 적음 | 비쌈(LED의 수~수십 배), 효율 낮음, 수명 짧은 편 |
- 눈부심 원리: 같은 빛을 넓은 면에서 내면 면적당 밝기(휘도)가 낮아져 덜 눈부심. 밝은 점 여러 개는 고른 면보다 더 낮은 평균 밝기에서도 눈부심 (2011 연구). 확산판은 빛을 조금 잃음
- 출처: https://www.energy.gov/eere/ssl/articles/flicker-understanding-new-ieee-recommended-practice · https://www.ledsmagazine.com/content/leds/en/articles/2015/06/ieee-par1789-makes-recommendations-on-safe-levels-of-flicker-in-led-based-lighting.html · https://research.tue.nl/en/publications/a-study-on-overhead-glare-in-office-lighting-conditions/ · https://www.eeworldonline.com/top-ten-myths-of-leds-7-leds-have-high-glare/ · https://www.etoday.co.kr/news/view/763223 · https://engineerfix.com/are-halogen-bulbs-being-phased-out/ · https://www.energy.gov/eere/ssl/downloads/oled-lighting-products-capabilities-challenges-potential · https://www.eenewseurope.com/en/oleds-hardly-have-a-chance-against-led-lighting/
