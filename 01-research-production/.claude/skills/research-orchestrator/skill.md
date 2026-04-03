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

## 작업 경로 설정

**하네스 디렉토리의 `_workspace/`는 빈 스캐폴드(디렉토리 구조 템플릿)이다. 실행 결과물은 사용자가 지정한 외부 경로에 저장한다.**

1. 사용자가 쿼리에 출력 경로를 명시한 경우 → 해당 경로를 `{작업경로}`로 사용
2. 사용자가 출력 경로를 명시하지 않은 경우 → **반드시 경로를 질문한다**:
   ```
   📂 결과물을 저장할 작업 경로를 알려주세요.
   예: /home/youn_j/projects/flare-prediction/_workspace
   ```
3. 경로가 확정되면 해당 경로에 필요한 하위 디렉토리(`code/`, `figures/`, `tables/` 등)를 생성한다
4. 이후 모든 `_workspace/` 참조는 사용자가 지정한 `{작업경로}`로 치환된다

---

## 실행 전 안내 메시지

파이프라인 시작 시 사용자에게 다음을 안내한다:

```
📋 연구 생산 파이프라인을 시작합니다.

• 무제한의 시간을 들여 꼼꼼하게 진행합니다.
• 1M 토큰을 최대한 활용하여 깊이 있는 연구를 수행합니다.
• 모든 생각의 흐름은 {작업경로}/research-note.md에 누적 기록됩니다.
• 각 단계 완료 시 진행 상황을 보고합니다.

연구 주제: "{사용자 제시 주제}"
작업 경로: "{작업경로}"

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

### 시나리오 1: 정상 흐름 — 태양 플레어 예측 연구

```
사용자: "GOES XRS 데이터를 이용한 태양 플레어 발생 예측 연구를 해줘"

Phase 1: literature-reviewer
  → arXiv/ADS에서 "solar flare prediction GOES XRS" 검색
  → 핵심 선행연구 15편 선별, 연구 갭 식별
  → 01_literature_review.md, references.bib 생성

Phase 2: research-designer
  → 가설: "GOES XRS의 전구체 패턴으로 M급 이상 플레어를 24시간 전 예측 가능"
  → 실험 설계: Baseline(임계값 기반) vs Experiment(ML 기반)
  → 02_research_design.md 생성

Phase 3: research-executor
  → GOES XRS 데이터 다운로드 (2020-2025)
  → 전처리, 특징 추출
  → Baseline/Experiment 실행
  → Figure 4개, Table 1개 생성
  → 03_execution_log.md 생성

Phase 4: reviewer (검토)
  → 설계-결과 대조: 모든 항목 PASS
  → 판정: PASS
  → 05_review_report.md 생성

Phase 5: paper-writer
  → 논문 초안 작성 (Figure 4 + Table 1 = 5개)
  → 04_paper_draft.md 생성

Phase 6: reviewer (심사)
  → 문장별 팩트체크, 관대하게 판정
  → 판정: Minor Revision
  → 06_referee_report.md 생성

→ 최종 결과를 사용자에게 전달
```

### 시나리오 2: 루프백 흐름 — 코로나 온도 분석

```
사용자: "SDO/AIA 다중 파장으로 코로나 온도 분포를 분석해줘"

Phase 1: literature-reviewer
  → DEM(Differential Emission Measure) 관련 문헌 조사
  → 01_literature_review.md 생성

Phase 2: research-designer (1차)
  → DEM 방법 중 regularized inversion 선택
  → AIA 6채널 사용, 1일 데이터 분석 설계
  → 02_research_design.md 생성

Phase 3: research-executor
  → 코드 작성 및 실행
  → DEM 결과 생성, Figure 3개

Phase 4: reviewer (검토)
  → 문제 발견: 평가 지표(chi-squared)가 미계산
  → 판정: REVISE
  → 05_review_report.md: "chi-squared 적합도 평가 추가 필요"

Phase 2: research-designer (2차, 루프백)
  → 05_review_report.md 피드백 반영
  → chi-squared 평가 단계 추가
  → 02_research_design.md 업데이트

Phase 3: research-executor (재실행)
  → chi-squared 계산 추가, Table 1개 추가 생성

Phase 4: reviewer (재검토)
  → 판정: PASS

Phase 5~6: 정상 진행
```
