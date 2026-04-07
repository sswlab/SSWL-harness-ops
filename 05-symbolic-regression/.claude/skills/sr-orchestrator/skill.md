---
name: sr-orchestrator
description: >
  Symbolic Regression 하네스의 전체 워크플로우 가이드. sr-planner → sr-executor →
  expression-analyst → sr-reporter로 이어지는 단계별 흐름과 사용자 상호작용 정책.
  키워드: SR 워크플로우, 전체 흐름, orchestration, SR 실행 순서
---

# sr-orchestrator — SR 하네스 전체 워크플로우

이 skill은 사용자가 SR 연구를 요청했을 때 전체 흐름을 어떻게 진행할지 정의합니다.

## 단계별 흐름

```
[Step 0] 입력 확보
    ↓
[Step 1] sr-planner: 진단 + 라우팅 + 사용자 승인
    ↓
[Step 2] sr-executor: 선택 도구 병렬 실행
    ↓
[Step 3] expression-analyst: 단순화·동등성·Pareto·차원 분석
    ↓
[Step 4] sr-reporter: Figure·표·LaTeX·한국어 보고서
    ↓
[Step 5] 사용자 보고 + 후속 질문 대응
```

## Step 0 — 입력 확보

다음 5가지가 모두 확보될 때까지 사용자에게 묻는다:

1. **데이터** — 파일 경로 또는 인메모리 배열 설명
2. **연구 질문** — 발견하고자 하는 관계 (정적 함수 vs 시간 진화 등)
3. **변수 의미·단위** — 각 입력 변수의 물리적 의미와 단위
4. **제약·사전지식** — 사용 연산자, 알려진 점근 거동 (선택)
5. **작업 경로** — 결과물 저장 위치 `{작업경로}`

표준 질문 예시:

> "SR 연구를 시작하기 전에 몇 가지 확인할게요.
> 1. 데이터 파일 경로 또는 형태가 어떻게 되나요? (예: data/measurement.csv)
> 2. 발견하고 싶은 관계가 무엇인가요? (예: y와 x들 사이의 관계, 또는 x(t)의 진화식)
> 3. 각 변수의 물리적 의미와 단위를 알려주시면 dimensional analysis도 활용할 수 있어요.
>    예: x1=속도[m/s], x2=시간[s], y=거리[m]
> 4. 사용에 제한할 연산자나 알려진 사전지식이 있나요?
> 5. 결과물을 저장할 작업 경로는 어디로 할까요?"

## Step 1 — sr-planner

- 데이터 파일을 읽어 shape, 결측, 분포, 노이즈 진단
- 연구 질문을 정적 (X,y) / 시계열 / ODE 식별
- 라우팅 정책에 따라 도구 선택 (PySR 항상 + 추가 도구들)
- 시간 예산, 시드, 연산자 집합, 데이터 분할 결정
- `01_diagnosis.md`, `02_routing_plan.md` 생성
- **사용자 승인 요청** — "이 계획대로 진행해도 될까요?"

승인 후에만 Step 2로 진행.

## Step 2 — sr-executor

- 도구별 러너 코드 생성 (`code/run_<tool>.py`)
- 가능한 도구는 병렬 실행 (subprocess 또는 multiprocessing)
- 각 도구의 결과를 표준 스키마로 저장 (`results/<tool>/candidates.json`)
- 모든 결과를 `results/all_candidates.json`으로 통합
- `03_execution_log.md`에 환경/시간/에러 기록

## Step 3 — expression-analyst

- 모든 후보를 SymPy로 파싱·단순화
- 무효 후보 (NaN/Inf, 도메인 위반) 제거
- 동등성 클러스터링
- Validation 데이터로 R² 재평가 (도구 자체 보고치 외 별도 검증)
- (단위 정보 있는 경우) dimensional consistency 검사
- Pareto front 추출
- `04_expression_analysis.md`, `pareto.csv`, `equivalence_clusters.json` 생성

## Step 4 — sr-reporter

- Pareto plot, fit plot, residual, 도구 비교 bar 등 Figure 생성 (DPI=300)
- 비교표 생성 (CSV + Markdown)
- 추천 후보를 LaTeX로 변환
- 한국어 해석 보고서 작성
- `05_report.md`, `figures/`, `tables/` 생성

## Step 5 — 사용자 보고

- `05_report.md`의 핵심을 사용자에게 요약 전달
- 발견된 추천 수식 1~3개를 LaTeX로 표시
- 한계와 다음 단계 제안
- 후속 질문(다른 시간 예산, 다른 연산자, 추가 데이터 등)에 대응

## 사용자 상호작용 원칙

- **모호성은 즉시 질문**: 변수 의미·단위·연구 목적이 분명치 않으면 추측하지 않는다
- **계획은 승인 후 실행**: sr-planner의 라우팅 계획은 항상 사용자 승인 후 실행
- **중간 실패도 보고**: 일부 도구가 실패해도 다른 도구 결과는 정상 진행하고 사용자에게 알린다
- **결론에 정직**: 모든 후보의 R²가 낮으면 부풀리지 말고 한계를 명시한다

## 빠른 호출 패턴

사용자가 간단히 요청하는 경우:

```
> "data/measurement.csv 로 y와 x1, x2 사이의 관계를 찾아줘"
```

→ sr-planner가 데이터 진단 후, 변수 단위 등 부족한 정보를 묻고, 라우팅 계획을 제시.

```
> "이 시계열 데이터에서 ODE를 찾아줘"
```

→ sr-planner가 시계열로 인식하고 PySINDy를 우선 라우팅.

```
> "이 물리 데이터(단위 포함)로 수식 발견해줘"
```

→ sr-planner가 단위 정보를 확인 후 AI Feynman을 라우팅에 포함.
