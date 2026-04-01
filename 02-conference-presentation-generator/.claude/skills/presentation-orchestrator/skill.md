---
name: presentation-orchestrator
description: >
  학회 발표 PPT 생성 파이프라인 총괄 오케스트레이터.
  연구 결과를 입력받아 콘텐츠 추출→스토리 설계→슬라이드 구성→PPTX 생성→검토까지 조율한다.
  PPT 만들어줘, 발표 자료, 슬라이드, 학회 발표, 컨퍼런스,
  프레젠테이션, 포스터, 세미나, 논문 발표, 연구 발표
---

# Presentation-Orchestrator — PPT 생성 파이프라인 총괄

## 개요

연구 결과(논문 초안, Figure, Table)를 입력받아, 학회 발표용 PPTX 파일을 자동 생성한다.
5명의 에이전트가 순차적으로 협력하여 콘텐츠 추출부터 발표 코칭까지 수행한다.

---

## 실행 전 안내 메시지

```
📋 학회 발표 PPT 생성 파이프라인을 시작합니다.

다음 정보를 확인합니다:
• 발표 제목: {제목 또는 미정}
• 학회/세미나: {학회명}
• 발표 시간: {분}분 (기본: 15분)
• 언어: {영어/한국어} (기본: 영어)
• 입력 자료: {논문 경로 / Figure 경로}

파이프라인을 시작할까요?
```

---

## 파이프라인 흐름도

```
┌─────────────────────────────────────────────────────┐
│              사용자: 연구 결과 + 발표 정보             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │  Phase 1: 콘텐츠 추출   │
          │  content-extractor     │
          │  → 01_content_brief.md │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │  Phase 2: 스토리 설계   │
          │  story-architect       │
          │  → 02_story_           │
          │    structure.md        │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │  Phase 3: 슬라이드 구성 │
          │  slide-composer        │◀─── REVISE 루프백 (최대 2회)
          │  → 03_slide_deck.md    │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │  Phase 4: PPTX 생성    │
          │  pptx-engineer         │
          │  → 04_make_ppt.py      │
          │  → output/*.pptx       │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │  Phase 5: 검토/코칭    │
          │  deck-reviewer         │
          │  → 05_review_report.md │
          │  → 06_speaker_guide.md │
          └───────────┬────────────┘
                      │
             ┌────────┴────────┐
          REVISE             PASS
             │                 │
             ▼                 ▼
        Phase 3로        최종 결과 전달
        루프백            (PPTX + 발표 가이드)
```

---

## 에이전트별 데이터 전달 프로토콜

| Phase | 에이전트 | 입력 | 출력 |
|---|---|---|---|
| 1 | content-extractor | 연구 결과 (논문, figures, tables) | `01_content_brief.md` |
| 2 | story-architect | `01_content_brief.md` | `02_story_structure.md` |
| 3 | slide-composer | `02_story_structure.md`, `01_content_brief.md`, (REVISE 시) `05_review_report.md` | `03_slide_deck.md` |
| 4 | pptx-engineer | `03_slide_deck.md`, `figures/` | `04_make_ppt.py`, `output/*.pptx` |
| 5 | deck-reviewer | `01~04` 전부, `output/*.pptx` | `05_review_report.md`, `06_speaker_guide.md` |

---

## 루프백 조건과 최대 횟수

| 루프백 유형 | 트리거 | 최대 횟수 | 초과 시 |
|---|---|---|---|
| **슬라이드 REVISE** | deck-reviewer가 필수 수정 판정 | 2회 | 사용자에게 현 상태로 전달 |
| **Figure 추가 요청** | slide-composer가 Figure 부족 보고 | 1회 | placeholder 유지 |
| **코드 재실행** | pptx-engineer 실행 에러 | 2회 | 에러 로그와 함께 사용자 보고 |

---

## 에러 핸들링 테이블

| Phase | 에러 | 심각도 | 대응 |
|---|---|---|---|
| 1 | 입력 자료 없음 | 높음 | 사용자에게 자료 요청 |
| 1 | Figure 파일 없음 | 중간 | 텍스트 기반 설명으로 대체 |
| 2 | 콘텐츠 부족 (< 8 블록) | 중간 | content-extractor에 추가 추출 요청 |
| 3 | REVISE 2회 초과 | 중간 | 현 상태로 pptx-engineer에 전달 |
| 4 | python-pptx 미설치 | 높음 | 설치 안내 (`pip install python-pptx`) |
| 4 | 코드 실행 에러 | 중간 | 에러 분석 후 수정, 재실행 |
| 5 | 과학적 오류 발견 | 높음 | REVISE 판정, 원본 대조 수정 |

---

## 실행 모드

| 모드 | 에이전트 | 용도 |
|---|---|---|
| **Full Pipeline** | 5명 전원 | 처음부터 PPTX 생성 |
| **Slide Only** | slide-composer + pptx-engineer | 스토리가 이미 있을 때 |
| **Review Only** | deck-reviewer | 기존 PPT 검토 + 발표 코칭 |
| **Regenerate** | pptx-engineer | 슬라이드 덱은 유지, PPTX만 재생성 |

---

## 테스트 시나리오

### 시나리오 1: 정상 흐름 — 15분 학회 발표

```
사용자: "01-research-production의 태양 플레어 예측 연구 결과로
        15분 학회 발표 PPT를 만들어줘. AGU 발표, 영어."

Phase 1: content-extractor
  → 논문 초안 + Figure 4개 + Table 1개에서 콘텐츠 추출
  → 핵심 메시지: "XRS 전구체 패턴으로 M급 플레어 24h 전 예측 가능"
  → 14개 콘텐츠 블록 도출

Phase 2: story-architect
  → ACT 1 (도입, 3분, 3장): 태양 플레어 배경 → 예측의 중요성 → 기존 한계
  → ACT 2 (전개, 4분, 4장): GOES XRS 데이터 → 전처리 → ML 모델
  → ACT 3 (결과, 6분, 5장): 정확도 비교 → 핵심 Figure → 사례 분석
  → ACT 4 (결론, 2분, 2장): 요약 → 향후 연구 → Q&A

Phase 3: slide-composer
  → 14장 슬라이드 덱 작성 (레이아웃, 텍스트, Figure 배치)

Phase 4: pptx-engineer
  → python-pptx 코드 생성/실행
  → output/flare_prediction_AGU.pptx 생성 (14 slides)

Phase 5: deck-reviewer
  → 검토: PASS (사소한 제안 2건)
  → 발표 가이드: 슬라이드별 스크립트 + Q&A 5개 + 타이밍 체크포인트
```

### 시나리오 2: REVISE 흐름

```
사용자: "DEM 분석 결과로 세미나 발표 PPT 만들어줘. 30분, 한국어."

Phase 1~4: 정상 진행 (20장 슬라이드)

Phase 5: deck-reviewer
  → 문제 발견: Slide 8 Figure 캡션이 원본 데이터와 불일치
  → 문제 발견: Slide 12~14 내용 중복
  → 판정: REVISE

Phase 3 (재수행): slide-composer
  → Slide 8 캡션 수정
  → Slide 12~14 통합하여 12~13으로 축소

Phase 4 (재수행): pptx-engineer
  → 수정된 19장 PPTX 재생성

Phase 5 (재검토): deck-reviewer
  → 판정: PASS
  → 발표 가이드 생성
```
