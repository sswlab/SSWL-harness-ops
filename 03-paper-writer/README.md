# 03-Paper-Writer 사용 가이드

이 하네스를 실행하기 전에 아래 항목을 준비하세요.
오케스트레이터가 시작 시 확인하며, **누락된 항목은 되물어봅니다.**

---

## 개요

연구 코드, 데이터, Figure를 입력하면 에이전트 팀이
**논문 초안 작성 → 내부 검토 → 피어리뷰 시뮬레이션 → 리비전**까지 수행합니다.
실제 저널 투고 프로세스(제출 → 심사 → 리비전 → 판정)를 최대 3회 반복합니다.

> **범위**: 연구 결과로부터 **새 논문을 작성**하는 하네스입니다.
> 기존 논문의 문법 교정, 팩트체크, 모의 리뷰 등 편집 작업은 이 하네스의 범위 밖입니다.

---

## 필수 입력 항목

### 1. 연구 결과물

논문의 기반이 되는 연구 자료를 제공합니다.

```
예: 연구 코드 (.py, .ipynb)
예: 실험 데이터 (.csv, .fits)
예: Figure 이미지, Table
예: 기존 논문 초안 (전체 리라이트 시)
```

### 2. 대상 저널

투고 대상 저널을 알려주세요. 미정이면 researcher가 3개 후보를 제안합니다.

```
예: ApJ (The Astrophysical Journal)
예: A&A (Astronomy & Astrophysics)
예: Solar Physics
예: 아직 미정
```

사용 가능한 LaTeX 템플릿: ApJ/ApJL/ApJS, A&A, MNRAS, arXiv(폴백)

### 3. 작업 경로

결과물을 저장할 외부 디렉토리 경로입니다.
하네스 내부의 `_workspace/`는 빈 구조 템플릿이며, 실행 결과는 여기에 저장하지 않습니다.

```
예: /home/youn_j/papers/stix-goes-paper/_workspace
```

---

## 실행 예시

### 모든 항목을 한번에 제시하는 경우

```
STIX-GOES 변환 연구 결과로 ApJ 논문 써줘.
결과물은 /home/youn_j/research/stix-goes/ 에 있어.
작업 경로: /home/youn_j/papers/stix-goes/_workspace
```

### 간단하게 요청하는 경우

```
이 연구 결과로 논문 써줘.
```

→ 오케스트레이터가 순차적으로 되물음:
1. "연구 결과물이 있는 경로를 알려주세요."
2. "대상 저널을 알려주세요."
3. "작업 경로를 알려주세요."

---

## 에이전트 구성

| 에이전트 | 역할 |
|---|---|
| researcher | 논문 초안 + 커버레터 작성, 리비전 수행 |
| co-worker | 한 문장씩 검토: 논리 흐름, 용어 통일, 팩트체크, 내부 용어 차단 |
| editor | 논문 접수, 저널 확인, 리뷰어 배정, 판정 |
| reviewer-1 | 한줄씩 팩트체크, 전문분야 중심 리뷰 |
| reviewer-2 | 한줄씩 팩트체크, reviewer-1과 다른 전문분야 (병렬) |

## 실행 흐름

```
연구 결과 입력
    │
    ▼
[researcher] 논문 초안 + 커버레터
    ▼
[co-worker] 한 문장씩 검토 → 이슈 시 researcher에 반환
    ▼
[LaTeX 변환] .md → .tex + .pdf
    ▼
[editor] 접수 → 리뷰어 배정
    ├──────────────────┐
    ▼                  ▼
[reviewer-1]       [reviewer-2]   ← 병렬
    └──────┬───────────┘
           ▼
        [editor] 판정 → Accept 또는 리비전 요청 (최대 3회)
```

---

## 작업 공간 구조

```
{작업경로}/
├── 01_paper_draft.md              # 논문 초안
├── 02_cover_letter.md             # 커버레터
├── 03_editorial_decision.md       # 에디터 결정
├── 04_reviewer_assignment.md      # 리뷰어 배정
├── cowork/                        # co-worker 검토 리포트
├── reviews/                       # 리뷰어 리포트 (라운드별)
├── revision/                      # 리비전 원고 + 리뷰 응답
├── decision/                      # 라운드별 판정
├── latex/{journal}/round{N}/      # LaTeX 출력 (라운드별)
└── editorial-log.md               # 전 과정 진행 기록
```
