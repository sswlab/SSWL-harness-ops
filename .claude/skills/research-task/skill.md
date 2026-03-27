---
name: research-task
description: >
  연구 업무 실행 시스템. 데이터 처리, synoptic map 생성,
  PFSS 시뮬레이션, 태양 데이터 분석 등 사용자 요청을 분석하고
  실행 계획을 수립하여 자동 처리한다.
  키워드: 작업 요청, 데이터 처리, synoptic map, 시뮬레이션,
  분석해줘, 만들어줘, 돌려줘, 생성해줘, 처리해줘,
  데이터 다운로드, 보정, 전처리, 시각화, 비교,
  HMI, AIA, PHI, EUI, PFSS, 코로나홀, 자기장,
  Carrington rotation, 태양 관측, 연구 작업
---

# Research-Task — 연구 업무 오케스트레이터

## 개요

사용자의 자연어 작업 요청(데이터 처리, 분석, 시뮬레이션 등)을 분석하고, 실행 계획을 수립하여, 에이전트 팀이 자동으로 처리한다. 사용자 승인 후 실행하며, 결과 보고 후 후속 작업 피드백 루프를 지원한다.

## 에이전트 구성표

| 에이전트 | 역할 | 호출 Phase |
|---|---|---|
| **query-planner** | 요청 분석, 실행 계획 수립 | Phase 1 |
| **data-fetcher** | 데이터 수집 (task-executor가 호출) | Phase 3 내부 |
| **model-runner** | 모델/도구 실행 (task-executor가 호출) | Phase 3 내부 |
| **task-executor** | 계획에 따른 순차/병렬 실행 | Phase 3 |
| **result-reporter** | 결과 정리 및 보고 | Phase 4 |

## 워크플로우

```
[사용자 요청]
    │
    ▼
╔═══════════════════╗
║     Phase 1       ║
║  query-planner    ║
║ (요청 분석/계획)    ║
╚════════╤══════════╝
         │ 실행 계획 (Markdown + JSON)
         ▼
╔═══════════════════╗
║     Phase 2       ║
║  사용자 승인/수정   ║  ◀─── 사용자 피드백
╚════════╤══════════╝
         │ 승인됨
         ▼
╔═══════════════════╗
║     Phase 3       ║
║  task-executor    ║
║  ├ data-fetcher   ║
║  ├ 전처리          ║
║  └ model-runner   ║
╚════════╤══════════╝
         │ 실행 결과
         ▼
╔═══════════════════╗
║     Phase 4       ║
║ result-reporter   ║
╚════════╤══════════╝
         │ 결과 보고
         ▼
╔═══════════════════╗
║     Phase 5       ║
║   피드백 루프      ║  ◀─── "이걸로 PFSS 돌려줘"
║ (후속 작업 요청)    ║ ────▶ Phase 1로 복귀
╚═══════════════════╝
```

## Phase별 상세

### Phase 1: 요청 분석 및 계획 수립

**에이전트**: query-planner

1. 사용자의 자연어 요청을 query-planner에 전달한다.
2. 이전 작업의 컨텍스트(있는 경우)도 함께 전달한다.
3. query-planner가 실행 계획을 반환한다.

### Phase 2: 사용자 승인

1. 계획을 사용자에게 제시한다.
2. 사용자 응답을 대기한다:
   - **승인**: "좋아", "진행해" → Phase 3
   - **수정**: "PHI 대신 HMI만으로 해줘" → query-planner 재호출 (최대 3회)
   - **거부**: "취소" → 작업 종료

### Phase 3: 작업 실행

**에이전트**: task-executor (내부: data-fetcher, model-runner)

1. 승인된 계획을 task-executor에 전달한다.
2. 단계별 실행, 검증, 에러 대응.
3. 장시간 단계는 사용자에게 중간 상태를 알린다.

### Phase 4: 결과 보고

**에이전트**: result-reporter

1. 결과를 사용자용 보고서로 정리한다.
2. 성공/실패/부분성공 모두 보고한다.
3. 후속 작업 가능성을 제안한다.

### Phase 5: 피드백 루프

1. 사용자가 후속 작업을 요청하면 Phase 1로 복귀한다.
2. 이전 작업의 출력을 context에 포함시킨다.

## 에러 핸들링

| Phase | 에러 | 대응 |
|---|---|---|
| 1 | 요청 해석 불가 | 사용자에게 구체적 질문 |
| 1 | 실현 불가능 요청 | 불가 사유 + 대안 제시 |
| 3 | 단계별 실패 | task-executor의 복구 전략 따름 |
| 3 | 전체 실패 | 부분 결과 보존 + 실패 보고서 생성 |
| 4 | 보고서 생성 실패 | 원시 결과 JSON을 직접 전달 |

## _workspace/ 디렉토리 구조

```
_workspace/
├── plans/
│   └── plan_{timestamp}.json
├── tasks/
│   └── plan_{timestamp}/
│       ├── plan.json
│       ├── status.json
│       ├── step1/ ~ stepN/
│       └── output/
├── reports/
│   └── report_plan_{timestamp}.md
└── data/
```
