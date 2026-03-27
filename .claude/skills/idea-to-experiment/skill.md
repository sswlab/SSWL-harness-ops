---
name: idea-to-experiment
description: >
  연구 아이디어를 실험 결과로 전환하는 시스템.
  아이디어 분석, 실험 설계, 실행, 결과 해석, 논문 초안까지 지원한다.
  키워드: 아이디어, 실험, 가설, ~하면 ~할까, 성능 비교,
  개선될까, 좋아질까, 시도해볼까, 테스트, 검증,
  연구 제안, 연구 질문, 파일럿 실험, 비교 실험,
  baseline, experiment, 논문 초안
---

# Idea-to-Experiment — 아이디어→실험 오케스트레이터

## 개요

연구자가 연구 아이디어를 제시하면, AI가 **실험을 설계**하고, 연구자와의 **피드백으로 계획을 정교화**한 뒤, **실험을 수행**하여 **결과를 보고**한다. 요청 시 **논문 초안 작성**까지 지원한다.

## 에이전트 구성표

| 에이전트 | 역할 | 호출 Phase |
|---|---|---|
| **research-assistant** | 아이디어 분석, 실험 설계, 결과 해석 | Phase 1, 5 |
| **query-planner** | 실험 실행 계획 수립 | Phase 3 |
| **data-fetcher** | 실험용 데이터 수집 | Phase 4 내부 |
| **model-runner** | 실험 모델 실행 | Phase 4 내부 |
| **task-executor** | 실험 파이프라인 실행 | Phase 4 |
| **result-reporter** | 실험 결과 보고 | Phase 5 |

## 워크플로우

```
[연구자: 아이디어 제시]
    │
    ▼
╔═════════════════════════╗
║   Phase 1: 아이디어 분석 ║
║   research-assistant    ║
║   (질문 파싱, 가설 수립)  ║
╚════════╤════════════════╝
         │ 실험 설계 초안
         ▼
╔═════════════════════════╗
║   Phase 2: 피드백 루프   ║
║   연구자 ↔ research-    ║
║   assistant             ║
║   (실험 계획 정교화)      ║
╚════════╤════════════════╝
         │ 확정된 실험 계획
         ▼
╔═════════════════════════╗
║   Phase 3: 실행 계획    ║
║   query-planner         ║
║   (구체적 실행 단계 수립)  ║
╚════════╤════════════════╝
         │ 승인
         ▼
╔═════════════════════════╗
║   Phase 4: 실험 실행    ║
║   task-executor         ║
║   ├ data-fetcher        ║
║   └ model-runner        ║
║   (Baseline + Experiment ║
║    + Reference 실행)     ║
╚════════╤════════════════╝
         │ 실험 결과
         ▼
╔═════════════════════════╗
║   Phase 5: 결과 해석    ║
║   research-assistant    ║
║   + result-reporter     ║
║   (비교 분석, 통계, 해석) ║
╚════════╤════════════════╝
         │ 결과 보고
         ▼
╔═════════════════════════╗
║   Phase 6: 후속         ║
║   - 추가 실험?          ║
║   - 논문 초안?          ║  ◀─── "논문 초안 써줘"
║   - 종료?              ║
╚═════════════════════════╝
```

## Phase별 상세

### Phase 1: 아이디어 분석

**에이전트**: research-assistant

1. 연구자의 아이디어를 파싱하여 핵심 질문, 변수, 가설을 추출한다.
2. 가용 데이터와 모델을 확인한다.
3. 실험 설계 초안을 제시한다.

### Phase 2: 피드백 루프

research-assistant가 연구자와 대화하며 실험 계획을 정교화한다:
- "비교할 때 영역별로 나눠서 봐줘" → 영역 분류 단계 추가
- "데이터 기간을 더 길게" → 수집 범위 확대
- "이 모델 대신 저 모델 써줘" → 모델 교체

최대 5회 피드백 반복. 이후 최종 확정을 요청한다.

### Phase 3: 실행 계획

**에이전트**: query-planner

research-assistant의 실험 설계를 구체적인 실행 계획으로 변환한다:
- 데이터 수집 단계 (소스, 기간, 형식)
- 전처리 단계
- Baseline 실행
- Experiment 실행
- Reference 실행 (있는 경우)
- 비교 분석 단계

### Phase 4: 실험 실행

**에이전트**: task-executor (data-fetcher, model-runner)

승인된 계획에 따라 실험을 수행한다. 복수 실험(Baseline, Experiment)은 가능하면 병렬 실행한다.

### Phase 5: 결과 해석

**에이전트**: research-assistant + result-reporter

1. 실험 결과를 수집한다.
2. Baseline vs Experiment 비교 분석을 수행한다.
3. 통계적 의미를 평가한다.
4. 결과를 과학적으로 해석한다.
5. 사용자에게 보고한다.

### Phase 6: 후속

- **추가 실험**: 파라미터 변경, 데이터 확대 → Phase 2로 복귀
- **논문 초안**: paper-draft 스킬 호출
- **종료**: 결과 아카이브

## 에러 핸들링

| Phase | 에러 | 대응 |
|---|---|---|
| 1 | 아이디어가 너무 추상적 | 구체적 질문으로 좁혀가기 |
| 3 | 필요 데이터 미가용 | 가용한 데이터로 수정된 실험 제안 |
| 4 | 모델 실행 실패 | 원인 분석, 파라미터 조정 또는 대체 방법 제안 |
| 5 | 결과가 모호 | 추가 분석 또는 실험 반복 제안 |

## _workspace/ 디렉토리 구조

```
_workspace/experiments/
└── exp_{timestamp}/
    ├── design.md              # 실험 설계
    ├── plan.json              # 실행 계획
    ├── baseline/              # Baseline 결과
    ├── experiment/            # Experiment 결과
    ├── reference/             # Reference 결과 (있는 경우)
    ├── analysis/              # 비교 분석
    │   ├── comparison.md
    │   └── figures/
    └── report.md              # 최종 보고서
```
