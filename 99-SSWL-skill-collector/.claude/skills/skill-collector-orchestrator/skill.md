---
name: skill-collector-orchestrator
description: >
  SSWL 연구실 코드를 수집·분석·분류·리팩터링하여 Claude Code 스킬로 변환하는
  파이프라인 총괄 오케스트레이터. 코드를 정리해줘, 스킬로 만들어줘, 코드 분석해줘,
  코드 모아줘, 코드 수집, 코드 변환, 스킬 수집, inbox에 코드 넣었어, 정리 안 된
  코드가 있어, 연구실 코드 정리, 기존 코드 활용, 코드 재사용, 코드 묶어줘,
  비슷한 코드 합쳐줘, 모듈화해줘, 원격 서버 코드 수집, 서버에서 코드 가져와,
  99서버 코드 정리, 다른 서버 코드 모아줘, SSH 코드 수집
  요청 시 반드시 이 스킬을 사용할 것.
---

# Skill-Collector-Orchestrator — 코드→스킬 변환 파이프라인 총괄

## 개요

사용자가 연구실 코드를 제시하면, 분석→분류→리팩터링→스킬 패키징→검증의 전 과정을 자동으로 조율한다.
에이전트 실행 순서, 데이터 전달 경로, 품질 게이트(PASS/REVISE), 사용자 승인 시점을 관리한다.

---

## 필수 입력 확인 및 검증

파이프라인 시작 전, 아래 항목을 확보한다. 누락 시 되물어서 확보한다.

| # | 항목 | 변수 | 누락 시 질문 |
|---|---|---|---|
| 1 | **코드 위치** | `{inbox경로}` | "변환할 코드가 있는 경로를 알려주세요." |
| 2 | **변환 목적** | `{목적}` | "이 코드를 스킬로 만드는 목적이 무엇인가요? (예: 연구실 공용 도구화, 하네스 보강 등)" |
| 3 | **변환 모드** | `{모드}` | 아래 모드 선택지를 제시 |
| 4 | **작업 경로** | `{작업경로}` | "중간 결과물을 저장할 작업 경로를 알려주세요." |
| 5 | **원격 서버 정보** (선택) | `{원격서버}` | "원격 서버에서 수집할 경우: user@hostname:/path (예: youn_j@163.180.171.99:/userhome/youn_j/)" |

### 변환 모드 선택지

```
변환 모드를 선택해주세요:

[1] 전체 변환 (Full Scan)
    - inbox의 모든 코드를 분석·분류·변환
    - 적합: 처음으로 연구실 코드를 정리할 때

[2] 추가 수집 (Incremental)
    - 기존 인벤토리/분류에 새 코드를 추가
    - 적합: 이미 1차 정리가 끝난 후 새 코드가 추가됐을 때

[3] 단일 변환 (Targeted)
    - 특정 파일/함수만 지정하여 스킬로 변환
    - 적합: 변환할 코드가 명확할 때

[4] 원격 수집 + 전체 변환 (Remote Collection + Full Scan)
    - 원격 서버에서 코드를 수집한 후, 전체 분석·분류·변환
    - 적합: 다른 서버에 흩어진 연구 코드를 처리할 때
    - 추가 필요: 원격 서버 SSH 접속 정보 (user@hostname:/path)
```

---

## 모드별 에이전트 프리셋

### 전체 변환 (Full Scan)

| Phase | 에이전트 | 프리셋 |
|---|---|---|
| 1 | code-archaeologist | **핵심.** 모든 파일 상세 분석. 의존성 그래프 + 중복 후보 완전 작성. |
| 2 | taxonomy-architect | **핵심.** 전체 분류 체계 설계. 기존 하네스와의 관계 분석 포함. |
| 3 | code-refactorer | 클러스터별 순차 리팩터링. 병합/분리 계획 전부 실행. |
| 4 | skill-builder | 모든 대상 클러스터를 스킬로 패키징. |
| 5 | integration-tester | 전체 스킬 검증. 트리거 + 실행 + 충돌 테스트. |

### 추가 수집 (Incremental)

| Phase | 에이전트 | 프리셋 |
|---|---|---|
| 1 | code-archaeologist | 신규 파일만 분석. 기존 인벤토리 참조하여 중복 판별 강화. |
| 2 | taxonomy-architect | 기존 분류 체계에 신규 코드 배치. 필요 시 클러스터 재조정. |
| 3 | code-refactorer | 신규/변경 클러스터만 리팩터링. |
| 4 | skill-builder | 신규/변경 스킬만 패키징. 기존 스킬 업데이트 포함. |
| 5 | integration-tester | 신규/변경 스킬만 검증. |

### 단일 변환 (Targeted)

| Phase | 에이전트 | 프리셋 |
|---|---|---|
| 1 | code-archaeologist | 지정 파일만 분석. |
| 2 | taxonomy-architect | **생략.** 사용자가 이미 스킬 범위를 지정. |
| 3 | code-refactorer | 지정 코드만 리팩터링. |
| 4 | skill-builder | 1개 스킬 패키징. |
| 5 | integration-tester | 1개 스킬 검증. |

### 원격 수집 + 전체 변환 (Remote Collection + Full Scan)

| Phase | 에이전트 | 프리셋 |
|---|---|---|
| 0 | remote-collector | **핵심.** 원격 서버 전체 스캔. 버전 계보 분석 + 최적 버전 선별 + 범주별 전송. 선별 목록 사용자 승인 후 전송 실행. |
| 1 | code-archaeologist | remote-collector의 `collection/` 매니페스트 활용. 버전 교차 검증 + 노트북 분석 포함. |
| 2 | taxonomy-architect | remote-collector의 범주를 기반으로 분류 체계 설계. 필요 시 재분류. |
| 3 | code-refactorer | 클러스터별 순차 리팩터링. 버전 간 통합 포함. |
| 4 | skill-builder | 모든 대상 클러스터를 스킬로 패키징. |
| 5 | integration-tester | 전체 스킬 검증. 트리거 + 실행 + 충돌 테스트. |

---

## 작업 경로 설정

하네스 디렉토리의 `_workspace/`는 빈 스캐폴드(디렉토리 구조 템플릿)이다.
실행 결과물은 사용자가 지정한 외부 경로에 저장한다.

1. 사용자가 쿼리에 출력 경로를 명시한 경우 → 해당 경로를 `{작업경로}`로 사용
2. 경로가 확정되면 하위 디렉토리(`inventory/`, `clusters/`, `modules/`, `skills/`, `reports/`, `logs/`)를 생성
3. 이후 모든 `_workspace/` 참조는 `{작업경로}`로 치환

---

## 실행 전 안내 메시지

모든 필수 항목이 확보된 후, 파이프라인 시작 전 사용자에게 안내한다:

```
코드 수집 파이프라인을 시작합니다.

코드 위치: {inbox경로}
변환 목적: {목적}
변환 모드: {모드}
작업 경로: {작업경로}

- 원본 코드는 수정하지 않습니다 (읽기 전용).
- 분류 체계가 나오면 확인을 요청드리겠습니다.
- 모든 과정은 {작업경로}/logs/collector-note.md에 기록됩니다.

파이프라인을 시작할까요?
```

**원격 수집 모드인 경우 추가 안내:**

```
[원격 수집 모드]
원격 서버: {원격서버}
- 원격 서버의 파일은 수정하지 않습니다 (읽기 전용 스캔).
- 수집 대상 파일 목록을 먼저 보여드리고 확인을 받겠습니다.
- 전송된 코드는 범주별로 inbox/에 정리됩니다.
```

---

## 파이프라인 흐름도

```
┌─────────────────────────────────────────────────────────────┐
│           사용자: 코드 위치 + 변환 요청                       │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │  Phase 0: 원격 수집     │  ← 원격 모드 전용
                │  remote-collector      │
                │  → collection/ + inbox/│
                │  ★ 선별 목록 승인 ★     │
                └───────────┬────────────┘
                            │ (로컬 모드는 여기서 시작)
                            ▼
                ┌────────────────────────┐
                │  Phase 1: 코드 분석     │
                │  code-archaeologist    │
                │  → inventory/          │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  Phase 2: 분류 설계     │
                │  taxonomy-architect    │
                │  → clusters/           │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  ★ 사용자 승인 ★        │
                │  분류 체계 검토 + 확인  │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  Phase 3: 리팩터링     │
                │  code-refactorer       │
                │  → modules/            │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  Phase 4: 스킬 패키징   │
                │  skill-builder         │
                │  → skills/             │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  Phase 5: 품질 검증     │
                │  integration-tester    │
                │  → reports/            │
                └───────────┬────────────┘
                            │
                   ┌────────┴────────┐
                   │                 │
                REVISE             PASS
                   │                 │
                   ▼                 ▼
              Phase 4로        ┌────────────────────────┐
              루프백            │  최종 결과 사용자에게    │
              (최대 2회)       │  전달 + 배포 안내       │
                               └────────────────────────┘
```

---

## 에이전트별 데이터 전달 프로토콜

| Phase | 에이전트 | 입력 | 출력 |
|---|---|---|---|
| 0 | remote-collector | `{원격서버}` + SSH (원격 모드 전용) | `collection/00_scan_manifest.md`, `01_version_lineages.md`, `02_selected_files.md`, `03_transfer_log.md`, `inbox/{category}/` |
| 1 | code-archaeologist | `{inbox경로}`, `collection/` (선택적) | `inventory/00_code_inventory.md`, `inventory/01_dependency_graph.md`, `inventory/02_duplicate_candidates.md`, `inventory/03_version_lineages.md`, `inventory/04_notebook_analysis.md` |
| 2 | taxonomy-architect | `inventory/*` | `clusters/00_taxonomy.md`, `clusters/01_merge_split_plan.md` |
| 3 | code-refactorer | `clusters/*`, `{inbox경로}` (읽기 전용) | `modules/{cluster}/`, `modules/refactoring_log.md` |
| 4 | skill-builder | `modules/*`, `inventory/*` | `skills/{skill-name}/`, `skills/skill_catalog.md` |
| 5 | integration-tester | `skills/*` | `reports/00_test_report.md` |

모든 파일은 사용자가 지정한 `{작업경로}` 하위에 위치한다.

---

## 사용자 승인 시점

| 시점 | 내용 | 형식 |
|---|---|---|
| Phase 0 완료 후 (원격 모드) | 수집 대상 파일 목록 + 버전 선택 근거 | `collection/02_selected_files.md` 요약 제시 |
| Phase 2 완료 후 | 분류 체계 + 병합/분리 계획 | `clusters/00_taxonomy.md` 요약 제시 |
| Phase 5 PASS 후 | 최종 스킬 목록 + 배포 대상 확인 | `skills/skill_catalog.md` 요약 제시 |

**승인 질문 형식:**

```
분류 결과가 나왔습니다:

클러스터 1: {이름} — {설명} (코드 N개 → 스킬 1개)
클러스터 2: {이름} — {설명} (코드 N개 → 스킬 1개)
아카이브: {이름} — {설명} (스킬 변환 대상 아님)

이대로 진행할까요? 수정이 필요한 부분이 있으면 알려주세요.
```

---

## 루프백 조건과 최대 횟수

| 루프백 유형 | 트리거 | 최대 횟수 | 초과 시 |
|---|---|---|---|
| **스킬 REVISE** | integration-tester가 REVISE 판정 | 2회 | 사용자에게 현 상태 보고, 수동 수정 안내 |
| **분류 재조정** | 사용자가 분류 수정 요청 | 1회 | 수정 반영 후 진행 |
| **코드 의도 확인** | code-archaeologist가 불확실 표시 | 필요 시 | 사용자 답변 후 진행 |

---

## 에러 핸들링 테이블

| Phase | 에러 유형 | 심각도 | 대응 |
|---|---|---|---|
| 0 | SSH 연결 실패 | 높음 | 서버 정보 재확인 요청, SSH 키 설정 안내 |
| 0 | 파일 수 과다 (>500개) | 중간 | 대규모 스캔 전략 적용, 예상 시간 안내 |
| 0 | 버전 선택 불분명 | 중간 | 후보 목록 제시, 사용자 판단 요청 |
| 0 | 전송 공간 부족 | 높음 | 총 용량 사전 안내, 사용자 확인 |
| 0 | 원격 디렉토리 접근 불가 | 중간 | 접근 가능 디렉���리만 스캔, 보고 |
| 1 | inbox 비어있음 | 높음 | 사용자에게 코드 경로 재확인 |
| 1 | 파일 수 과다 (>50개) | 중간 | 1차 스캔 후 우선순위 분류 |
| 1 | 비코드 파일 혼입 | 낮음 | 필터링 후 보고 |
| 2 | 모든 코드가 아카이브 판정 | 높음 | 사용자에게 보고, 기준 조정 요청 |
| 2 | 기존 스킬과 완전 중복 | 중간 | 기존 스킬 확장 vs 신규 생성 결정 요청 |
| 3 | 리팩터링 불가 (과도한 복잡도) | 중간 | 사용자에게 재작성 필요 보고 |
| 4 | skill.md 500줄 초과 | 낮음 | references/ 분리 |
| 5 | 스크립트 실행 실패 | 중간 | code-refactorer에 수정 요청 |
| 5 | REVISE 2회 초과 | 높음 | 사용자 에스컬레이션 |

---

## collector-note.md 기록 규칙

모든 에이전트는 `{작업경로}/logs/collector-note.md`에 판단 과정을 누적 기록한다.

```markdown
# Collector Note

## 변환 개요
- **코드 위치**: {inbox경로}
- **목적**: {목적}
- **모드**: {모드}
- **시작일**: {timestamp}

---

## [Phase 1: 코드 분석] {timestamp}
### code-archaeologist
- 분석 전략: ...
- 도메인 추론 근거: ...
- 불확실 판단 이유: ...

## [Phase 2: 분류 설계] {timestamp}
### taxonomy-architect
- 분류 기준 선택 이유: ...
- 입도 판단 근거: ...

...
```

**규칙:**
- 각 에이전트는 자기 Phase 섹션에만 추가한다
- 기존 내용을 수정하지 않고 누적만 한다
- 판단의 **이유**를 반드시 기록한다

---

## 최종 산출물 배포

검증 통과(PASS)한 스킬은 사용자에게 배포 옵션을 안내한다:

```
검증 완료된 스킬 N개가 준비되었습니다:

1. {skill-name} — {설명}
2. {skill-name} — {설명}

배포 옵션:
[A] 현재 하네스(.claude/skills/)에 바로 설치
[B] 다른 하네스 프로젝트에 복사
[C] 검토만 하고 나중에 배포

어떻게 하시겠습니까?
```

---

## 테스트 시나리오

### 시나리오 1: 전체 변환 — STIX/GOES 분석 코드

```
사용자: "연구실 코드 정리해줘. /home/youn_j/lab-codes/에 있어.
        목적: 연구실 공용 도구로 만들기
        모드: 전체 변환
        경로: /home/youn_j/skill-collector-workspace"

Phase 1: code-archaeologist
  → 15개 파일 분석
  → stix 관련 5개, goes 관련 4개, 유틸리티 3개, 불명확 3개
  → inventory/ 생성

Phase 2: taxonomy-architect
  → 클러스터 3개: stix-processing, goes-analysis, astro-utils
  → 아카이브 3개: 일회성 테스트 스크립트
  → [사용자 승인 대기]

→ 사용자 승인 후

Phase 3~5: 정상 진행
  → 스킬 3개 생성, 전부 PASS
  → 배포 옵션 제시
```

### 시나리오 2: 단일 변환 — 특정 코드만

```
사용자: "이 파일만 스킬로 만들어줘: /home/youn_j/lab-codes/dem_calculator.py"

→ 필수 항목 확인: 목적, 경로 질문
→ Phase 2 (분류) 생략
→ 직접 리팩터링 → 패키징 → 검증
```

### 시나리오 3: 루프백 — 트리거 충돌

```
Phase 5: integration-tester
  → data-fetcher 스킬의 description이 기존 변환 스킬 data-pipeline과 트리거 충돌
  → REVISE 판정, description 수정 요청

Phase 4 (2차): skill-builder
  → description 수정: "STIX 전용" 범위를 명시하여 충돌 해소

Phase 5 (2차): integration-tester
  → PASS
```

### 시나리오 4: 원격 수집 — 다중 서버 코드 수집

```
사용자: "99서버에 있는 연구 코드를 수집해서 스킬로 만들어줘.
        서버: youn_j@163.180.171.99:/userhome/youn_j/
        목적: 흩어진 코드를 정리하여 재사용 가능하게
        모드: 원격 수집 + 전체 변환
        경로: /home/youn_j/skill-collector-workspace"

Phase 0: remote-collector
  → SSH 접속, find로 628개 .py + 393개 .ipynb 발견
  → 45개 버전 계열 식별 (DEM_V1~V3, aurora_V3_1 등)
  → 각 계열에서 최적 버전 선별 → 162개 파일
  → 14개 범주로 분류 (전처리, DL Pix2Pix, DEM 등)
  → [사용자 승인: 선별 파일 목록 확인]
  → 승인 후 zip 전송 → inbox/에 범주별 배치

Phase 1: code-archaeologist
  → collection/ 매니페스트 활용하여 효율적 분석
  → 버전 계보 교차 검증
  → .ipynb 전용 분석 수행
  → inventory/ 생성

Phase 2~5: 정상 진행
  → 분류 → [승인] → 리팩터링 → 패키징 → 검증
  → 최종 스킬 배포
```
