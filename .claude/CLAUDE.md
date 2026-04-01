# SSWL AI Harness v2.0

태양 및 우주환경연구실(SSWL)의 연구자 업무 지원 AI 시스템.

## 프로젝트 개요

연구실에서 개발된 모델들을 **아카이빙·관리**하고, 연구자의 요청에 따라 **데이터 수집·모델 실행·결과 보고**를 수행하며, **연구 아이디어를 빠른 실험 결과**로 전환하는 하네스.

## 에이전트 팀 구성표

| 에이전트 | 역할 | 핵심 기능 |
|---|---|---|
| **research-planner** | 연구설계 | 요청 파싱, 가설 수립, 실험 설계, 실행 계획 수립 |
| **data-engineer** | 데이터처리 | 데이터 수집/검증, 모델 등록/카드 생성/버전관리 |
| **research-executor** | 실험실행 | 계획 기반 순차/병렬 실행, 모델 실행, 실패 복구 |
| **paper-writer** | 논문작성 | 결과 보고, 논문/초록 초안, Figure/Table, 후속 제안 |
| **reviewer** | 품질검토(QA) | 실험 설계 검토, 결과 교차 검증, 논문 심사 |

## 실행 모드: 에이전트 팀

모든 작업은 에이전트 팀이 협력하여 수행한다. 오케스트레이터 스킬이 에이전트 실행 순서와 데이터 전달을 관리한다.

**기본 흐름:**
```
research-planner → [사용자 승인] → research-executor → paper-writer → reviewer
```

**데이터 흐름:**
```
research-planner  ──(계획)──▶  research-executor
data-engineer     ──(데이터)──▶  research-executor
research-executor ──(결과)──▶  paper-writer
paper-writer      ──(초안)──▶  reviewer
reviewer          ──(피드백)──▶  research-planner (루프백)
```

## 데이터 전달 규칙

1. **파일 기반 전달**: 에이전트 간 데이터는 `_workspace/` 하위 파일로 전달한다
2. **JSON 프로토콜**: 구조화된 데이터는 JSON 형식으로 저장/전달한다
3. **경로 규칙**: 각 에이전트는 자신의 출력을 지정된 디렉토리에 저장한다
4. **중간 결과 보존**: 모든 중간 산출물은 삭제하지 않고 보존한다

| 에이전트 | 출력 디렉토리 |
|---|---|
| research-planner | `_workspace/plans/` |
| data-engineer | `_workspace/data/`, `_workspace/model_registry/` |
| research-executor | `_workspace/tasks/`, `_workspace/models/`, `_workspace/experiments/` |
| paper-writer | `_workspace/reports/`, `_workspace/papers/` |
| reviewer | `_workspace/reviews/` |

## 스킬 구성

| 스킬 | 역할 |
|---|---|
| **research-orchestrator** | 전체 파이프라인 조율, 에이전트 실행 순서, 루프백, 알림 |
| **data-pipeline** | 데이터 수집 절차 (5개 소스), 모델 아카이빙 절차 |
| **research-workflow** | 아이디어→실험→논문 워크플로우 |

## 핵심 운용 모드

1. **연구 업무 수행**: 자연어 요청 → 계획 수립 → 승인 → 실행 → 결과 보고
2. **모델 아카이빙/활용**: 연구실 모델을 표준 형식으로 등록·관리, 누구나 활용
3. **아이디어 → 실험 결과**: 연구 아이디어 → 실험 설계 → 실행 → 결과 + 논문 초안

## 작업 공간

```
_workspace/
├── plans/                  # 실행 계획
├── tasks/                  # 작업별 실행 결과
├── data/                   # 수집 데이터
├── models/                 # 모델 실행 결과
├── model_registry/         # 등록된 모델 아카이브
├── experiments/            # 실험 결과
├── papers/                 # 논문 초안
├── reports/                # 결과 보고서
├── reviews/                # 품질 검토 결과
└── logs/                   # 시스템 로그
```

## 사용 언어

- 사용자 대면: 한국어
- 코드/설정: 영어
- 예보문/보고서: 한국어

## 핵심 원칙

1. **사용자 승인 필수**: 모든 작업은 계획 제시 후 사용자 승인을 받아야 실행
2. **모델 표준화**: 등록된 모델은 표준 모델 카드를 갖고, 누구나 동일하게 사용 가능
3. **결과 투명성**: 성공이든 실패든, 과정과 결과를 명확히 보고
4. **연속 작업 지원**: 이전 결과를 다음 작업의 입력으로 자동 연결
5. **품질 검증**: reviewer 에이전트가 실험 설계, 결과, 논문을 교차 검증
