---
name: research-orchestrator
description: >
  SSWL 연구 생산 파이프라인 총괄 오케스트레이터.
  연구 주제가 주어지면 문헌조사→설계→실행→검토→논문의 전 과정을 조율한다.
  모든 연구 작업 시작 시 반드시 이 스킬이 파이프라인을 관리한다.
  키워드: 연구 시작, 논문 써줘, 실험해줘, 분석해줘,
  ~에 대해 연구해줘, ~를 조사해줘, 아이디어, 가설,
  새로운 연구, 프로젝트 시작, 파이프라인, 전체 실행
---

# Research-Orchestrator — 연구 생산 파이프라인 총괄

## 개요

사용자가 연구 주제를 제시하면, 문헌조사부터 논문 초안까지 전 과정을 자동으로 조율한다.
에이전트 실행 순서, 데이터 전달 경로, 품질 게이트(PASS/REVISE), 루프백을 관리한다.

---

## 필수 입력 확인 및 검증

파이프라인 시작 전, 아래 4가지 항목을 **모두** 확보해야 한다.
사용자의 쿼리에서 확인되지 않는 항목은 **반드시 되물어서** 확보한다.
한 번에 모든 누락 항목을 질문한다 (항목별로 따로 묻지 않는다).

### 필수 항목

| # | 항목 | 변수 | 누락 시 질문 |
|---|---|---|---|
| 1 | **연구 주제** | `{주제}` | "어떤 주제를 연구할까요?" |
| 2 | **연구 목적** | `{목적}` | "이 연구의 최종 목적(왜, 무엇을 달성)을 1~2문장으로 알려주세요." |
| 3 | **연구 모드** | `{모드}` | 아래 모드 선택지를 제시 |
| 4 | **작업 경로** | `{작업경로}` | "결과물을 저장할 작업 경로를 알려주세요." |

**연구 목적**은 파이프라인 전체에 걸쳐 모든 에이전트의 판단 기준이 된다:
- literature-reviewer: 목적 달성에 필요한 문헌을 우선 선별
- research-designer: 목적을 검증할 수 있는 실험 설계
- research-executor: 목적에 부합하는 결과 생성에 집중
- reviewer: 결과가 연구 목적을 달성했는지 판정
- paper-writer: 논문의 contribution을 목적에 맞게 서술

`{목적}`은 `{작업경로}/research-note.md` 최상단에 기록하여, 모든 에이전트가 Phase 시작 시 참조한다.

### 연구 모드 선택지

사용자에게 다음을 제시하여 선택받는다:

```
연구 모드를 선택해주세요:

[1] 탐색형 (Survey)
    - 넓은 범위 문헌조사 중심 (30~50편)
    - 실험은 최소/생략, 리뷰 페이퍼 스타일 산출물
    - 적합: 분야 동향 파악, 리뷰 논문, 새 프로젝트 착수 전 조사

[2] 심층형 (Deep Dive)
    - 특정 주제에 집중 (문헌 10~15편)
    - 가설 → 실험 → 검증 전체 수행, 오리지널 리서치 산출물
    - 적합: 가설 검증, 모델 개발, 저널 투고용 연구

[3] 전체 (Full Pipeline)
    - 넓은 문헌조사 + 깊은 실험 모두 수행
    - 적합: 새 분야 진입 + 첫 논문, 종합적 연구
```

---

## 모드별 에이전트 프리셋

모드가 확정되면, 각 에이전트에 해당 프리셋을 전달한다.

### 탐색형 (Survey)

| Phase | 에이전트 | 프리셋 |
|---|---|---|
| 1 | literature-reviewer | **핵심 Phase.** 논문 30~50편 검토. 넓은 키워드(동의어, 인접 분야 포함). 연구 동향 타임라인 + 방법론 분류표 작성. 미해결 과제(open questions) 5개 이상 식별. |
| 2 | research-designer | 경량 수행. 분석 프레임워크 수준의 설계. 실험 변수/가설 대신 "분류 기준"과 "비교 축"을 정의. |
| 3 | research-executor | **최소/생략.** 기존 논문에서 추출한 데이터로 비교표/요약 Figure만 생성. 새 실험 코드 작성하지 않음. |
| 4 | reviewer | 문헌 커버리지 중심 검토. "주요 논문이 누락되지 않았는가", "분류 체계가 일관적인가" 판정. |
| 5 | paper-writer | 리뷰 페이퍼 스타일. Introduction에 분야 배경을 상세히, Results 대신 "Current State of Research" 서술. |

### 심층형 (Deep Dive)

| Phase | 에이전트 | 프리셋 |
|---|---|---|
| 1 | literature-reviewer | 보조 Phase. 논문 10~15편, 좁은 키워드. 직접 관련 선행연구에 집중. 연구 갭 1~2개만 식별. |
| 2 | research-designer | **핵심 Phase.** 검증 가능한 가설, 구체적 실험 변수, Baseline vs Experiment 설계, 정량적 평가 지표(metric) 정의. |
| 3 | research-executor | **핵심 Phase.** 코드 작성, 데이터 수집/처리, 모델 학습/평가. Figure 3~5개, Table 1~2개. 재현 가능한 파이프라인 구축. |
| 4 | reviewer | 실험 재현성 중심 검토. "설계대로 실행되었는가", "수치가 코드와 일치하는가", "평가 지표가 계산되었는가" 판정. |
| 5 | paper-writer | 오리지널 리서치 스타일. 가설-방법-결과-해석 흐름. Contribution을 연구 목적에 직접 연결. |

### 전체 (Full Pipeline)

| Phase | 에이전트 | 프리셋 |
|---|---|---|
| 1 | literature-reviewer | 논문 20~30편. 넓은 커버리지 + 핵심 논문 깊이 분석. 연구 동향 + 연구 갭 모두 식별. |
| 2 | research-designer | 심층형과 동일. |
| 3 | research-executor | 심층형과 동일. |
| 4 | reviewer | 문헌 커버리지 + 실험 재현성 모두 검토. |
| 5 | paper-writer | 오리지널 리서치 스타일. Introduction에 충실한 배경 + 강한 실험 결과. |

---

## 작업 경로 설정

**하네스 디렉토리의 `_workspace/`는 빈 스캐폴드(디렉토리 구조 템플릿)이다. 실행 결과물은 사용자가 지정한 외부 경로에 저장한다.**

1. 사용자가 쿼리에 출력 경로를 명시한 경우 → 해당 경로를 `{작업경로}`로 사용
2. 사용자가 출력 경로를 명시하지 않은 경우 → 필수 입력 확인 단계에서 질문
3. 경로가 확정되면 해당 경로에 필요한 하위 디렉토리(`code/`, `figures/`, `tables/` 등)를 생성한다
4. 이후 모든 `_workspace/` 참조는 `{작업경로}`로 치환된다

---

## 실행 전 안내 메시지

**모든 필수 항목이 확보된 후**, 파이프라인 시작 전 사용자에게 다음을 안내한다:

```
📋 연구 생산 파이프라인을 시작합니다.

연구 주제: "{주제}"
연구 목적: "{목적}"
연구 모드: {모드} ({모드 설명})
작업 경로: {작업경로}

• 모든 생각의 흐름은 {작업경로}/research-note.md에 누적 기록됩니다.
• 각 단계 완료 시 진행 상황을 보고합니다.

파이프라인을 시작할까요?
```

---

## 파이프라인 흐름도

```
┌─────────────────────────────────────────────────────────────┐
│                      사용자: 연구 주제 제시                     │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │  Phase 1: 문헌조사      │
                │  literature-reviewer   │
                │  → 01_literature_      │
                │    review.md           │
                │  → references.bib      │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  Phase 2: 연구 설계     │
                │  research-designer     │◀─── REVISE 루프백 (최대 2회)
                │  → 02_research_        │
                │    design.md           │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  Phase 3: 실험 실행     │
                │  research-executor     │
                │  → code/, figures/,    │
                │    tables/,            │
                │    03_execution_log.md │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  Phase 4: 품질 검토     │
                │  reviewer              │
                │  → 05_review_report.md │
                └───────────┬────────────┘
                            │
                   ┌────────┴────────┐
                   │                 │
                REVISE             PASS
                   │                 │
                   ▼                 ▼
              Phase 2로        ┌────────────────────────┐
              루프백            │  Phase 5: 논문 작성     │
              (최대 2회)       │  paper-writer          │
                               │  → 04_paper_draft.md   │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │  Phase 6: 레퍼리 심사   │
                               │  reviewer              │
                               │  → 06_referee_         │
                               │    report.md           │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │  최종 결과 사용자에게    │
                               │  전달                   │
                               └────────────────────────┘
```

---

## 에이전트별 데이터 전달 프로토콜

| Phase | 에이전트 | 입력 파일 | 출력 파일 |
|---|---|---|---|
| 1 | literature-reviewer | 사용자 요청 | `01_literature_review.md`, `references.bib` |
| 2 | research-designer | `01_literature_review.md`, `references.bib`, (REVISE 시) `05_review_report.md` | `02_research_design.md` |
| 3 | research-executor | `02_research_design.md` | `code/`, `figures/`, `tables/`, `03_execution_log.md` |
| 4 | reviewer (검토) | `02_research_design.md`, `03_execution_log.md`, `figures/`, `tables/` | `05_review_report.md` |
| 5 | paper-writer | `01~03` 전부, `figures/`, `tables/`, `references.bib` | `04_paper_draft.md` |
| 6 | reviewer (심사) | `04_paper_draft.md`, `03_execution_log.md`, `figures/`, `tables/` | `06_referee_report.md` |

**모든 파일은 사용자가 지정한 `{작업경로}` 하위에 위치한다.**

---

## 루프백 조건과 최대 횟수

| 루프백 유형 | 트리거 | 최대 횟수 | 초과 시 |
|---|---|---|---|
| **설계 REVISE** | reviewer가 REVISE 판정 | 2회 | 사용자에게 현 상태 보고, 방향 재설정 요청 |
| **추가 문헌 조사** | research-designer가 문헌 부족 보고 | 1회 | 가용 문헌 범위에서 설계 진행 |
| **추가 Figure/Table** | paper-writer가 research-executor에 요청 | 2회 | 가용 자료만으로 작성 |

---

## 에러 핸들링 테이블

| Phase | 에러 유형 | 심각도 | 대응 |
|---|---|---|---|
| 1 | 검색 결과 부족 | 중간 | 키워드 확장, 인접 분야 검색 |
| 1 | 완전 중복 연구 발견 | 높음 | 사용자에게 즉시 보고, 차별화 방향 제안 |
| 2 | 설계 정보 부족 | 중간 | 사용자에게 질문 |
| 2 | REVISE 2회 초과 | 높음 | 사용자 에스컬레이션 |
| 3 | 데이터 다운로드 실패 | 중간 | 대체 소스 시도, 실패 시 보고 |
| 3 | 모델 실행 에러 | 중간 | 파라미터 조정 후 1회 재시도 |
| 3 | 전체 실행 실패 | 높음 | 부분 결과 보존 + 사용자 보고 |
| 4 | 검토 불가 (자료 부재) | 높음 | research-executor에 재실행 요청 |
| 5 | Figure 5개 초과 | 낮음 | 우선순위에 따라 자동 선별 |
| 6 | 팩트체크 불일치 발견 | 중간 | paper-writer에 수정 요청 |

---

## research-note.md 기록 규칙

모든 에이전트는 `{작업경로}/research-note.md`에 자신의 판단 과정을 누적 기록한다.

```markdown
# Research Note

## 연구 개요
- **주제**: {주제}
- **목적**: {목적}
- **모드**: {모드}
- **시작일**: {timestamp}

---

## [Phase 1: 문헌조사] {timestamp}
### literature-reviewer
- 검색 전략 선택 이유: ...
- 논문 선별 기준: ...
- 아이디어 구체화 판단: ...

## [Phase 2: 연구 설계] {timestamp}
### research-designer
- 가설 설정 근거: ...
- 방법론 선택 이유: ...
- 고려한 대안: ...

## [Phase 3: 실험 실행] {timestamp}
### research-executor
- 구현 결정 사항: ...
- 예상과 다른 결과: ...

## [Phase 4: 품질 검토] {timestamp}
### reviewer
- 판정 근거: ...
- 관대하게 넘어간 항목: ...

...
```

**규칙:**
- 각 에이전트는 자기 Phase 섹션에만 추가한다
- 기존 내용을 수정하지 않고 누적만 한다
- timestamp를 반드시 포함한다
- 판단의 **이유**를 반드시 기록한다

---

## 테스트 시나리오

### 시나리오 1: 심층형 — 태양 플레어 예측 연구

```
사용자: "GOES XRS 데이터를 이용한 태양 플레어 발생 예측 연구를 해줘.
        목적: 기존 임계값 기반 예측 대비 ML의 우위를 정량적으로 입증.
        모드: 심층형
        경로: /home/youn_j/projects/flare-prediction/_workspace"

→ 필수 항목 확인: 4개 모두 확보 ✓

Phase 1: literature-reviewer [심층형 프리셋: 10~15편, 좁은 키워드]
  → "solar flare prediction GOES XRS machine learning" 검색
  → 직접 관련 선행연구 12편 선별, 연구 갭 1개 식별
  → 01_literature_review.md, references.bib 생성

Phase 2: research-designer [심층형 프리셋: 가설+Baseline vs Experiment]
  → 가설: "GOES XRS의 전구체 패턴으로 M급 이상 플레어를 24시간 전 예측 가능"
  → 실험 설계: Baseline(임계값 기반) vs Experiment(ML 기반)
  → 평가 지표: TSS, HSS, AUC-ROC
  → 02_research_design.md 생성

Phase 3: research-executor [심층형 프리셋: 전체 실행]
  → GOES XRS 데이터 다운로드 (2020-2025)
  → 전처리, 특징 추출, 모델 학습
  → Figure 4개, Table 1개 생성
  → 03_execution_log.md 생성

Phase 4: reviewer [심층형 프리셋: 재현성 중심]
  → 목적 대비 검증: "ML이 임계값 기반보다 우위인가?" → TSS 비교 확인
  → 판정: PASS

Phase 5~6: 정상 진행

→ 최종 결과를 사용자에게 전달
```

### 시나리오 2: 탐색형 — 코로나 가열 메커니즘 서베이

```
사용자: "코로나 가열 메커니즘 연구 동향을 조사해줘."

→ 필수 항목 확인:
  ✓ 주제: 코로나 가열 메커니즘 연구 동향
  ✗ 목적: 누락 → 질문
  ✗ 모드: 누락 → 질문
  ✗ 경로: 누락 → 질문

→ 오케스트레이터 질문:
  "다음 정보를 알려주세요:
   1. 연구 목적: 이 연구로 최종 달성하고자 하는 것은?
   2. 연구 모드: [1] 탐색형 [2] 심층형 [3] 전체
   3. 작업 경로: 결과물 저장 경로"

→ 사용자 응답:
  "1. 최근 10년간 나노플레어 vs 파동 가열 논쟁의 현황을 정리하여 신규 연구 방향을 도출한다.
   2. 탐색형
   3. /home/youn_j/projects/coronal-heating-survey/_workspace"

Phase 1: literature-reviewer [탐색형 프리셋: 30~50편, 넓은 키워드]
  → "coronal heating nanoflare wave" + 동의어/인접 분야 검색
  → 38편 선별, 연구 동향 타임라인 작성
  → 미해결 과제 6개 식별

Phase 2: research-designer [탐색형 프리셋: 분석 프레임워크]
  → 비교 축 정의: 관측 증거 / 시뮬레이션 결과 / 에너지 예산
  → 분류 기준: nanoflare 계열 vs wave 계열 vs 하이브리드

Phase 3: research-executor [탐색형 프리셋: 최소]
  → 기존 논문 데이터로 비교표 Figure 2개 생성
  → 새 실험 코드 없음

Phase 4: reviewer [탐색형 프리셋: 커버리지 중심]
  → 목적 대비 검증: "나노플레어 vs 파동 논쟁이 균형 있게 다뤄졌는가?"
  → 판정: PASS

Phase 5: paper-writer [탐색형 프리셋: 리뷰 페이퍼]
  → "Current State of Research" 스타일 서술
  → 미해결 과제 기반 향후 연구 제안

Phase 6: 정상 진행

→ 최종 결과를 사용자에게 전달
```

### 시나리오 3: 루프백 흐름 — 심층형 + REVISE

```
사용자: "SDO/AIA 다중 파장으로 코로나 온도 분포를 분석해줘.
        목적: 기존 DEM 대비 계산 속도 10배 향상 + 정확도 유지하는 경량 모델 개발.
        모드: 심층형
        경로: /home/youn_j/projects/dem-fast/_workspace"

Phase 1~3: 정상 진행 (심층형 프리셋)

Phase 4: reviewer
  → 목적 대비 검증: "속도 10배 향상이 달성되었는가?" → 속도 비교 미계산
  → "chi-squared 적합도 + 속도 벤치마크 추가 필요"
  → 판정: REVISE

Phase 2: research-designer (2차, 루프백)
  → 속도 벤치마크 + chi-squared 평가 단계 추가

Phase 3~4: 재실행 → PASS

Phase 5~6: 정상 진행
```
