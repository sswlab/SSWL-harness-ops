# 02-Conference-Presentation-Generator 사용 가이드

이 하네스를 실행하기 전에 아래 항목을 준비하세요.
오케스트레이터가 시작 시 확인하며, **누락된 항목은 되물어봅니다.**

---

## 개요

연구 결과(논문 초안, Figure, Table 등)를 입력하면, 에이전트 팀이
**스토리 설계 → 슬라이드 구성 → PPTX 생성 → 발표 코칭**까지 수행합니다.

---

## 필수 입력 항목

### 1. 연구 결과물

발표 자료의 원본이 되는 연구 결과를 제공합니다.

```
예: 논문 초안 (.md, .tex, .pdf)
예: Figure 이미지 파일들
예: Table, 실험 로그, 데이터
```

### 2. 발표 정보

학회/세미나 정보와 발표 조건을 알려주세요.

```
예: "AGU 2026, 15분 구두 발표, 영어"
예: "연구실 세미나, 30분, 한국어"
예: "EGU 포스터, 영어"
```

### 3. 작업 경로

결과물을 저장할 외부 디렉토리 경로입니다.
하네스 내부의 `_workspace/`는 빈 구조 템플릿이며, 실행 결과는 여기에 저장하지 않습니다.

```
예: /home/youn_j/presentations/agu-2026
```

---

## 실행 예시

### 모든 항목을 한번에 제시하는 경우

```
태양 플레어 예측 연구 결과로 15분 학회 발표 PPT를 만들어줘.
AGU 발표, 영어.
결과물은 /home/youn_j/research/flare-prediction/ 에 있어.
작업 경로: /home/youn_j/presentations/agu-2026
```

### 간단하게 요청하는 경우

```
이 논문으로 학회 PPT 만들어줘: /home/youn_j/papers/my_paper.pdf
```

→ 오케스트레이터가 순차적으로 되물음:
1. "발표 시간과 학회를 알려주세요."
2. "발표 언어를 알려주세요. (영어/한국어)"
3. "작업 경로를 알려주세요."

---

## 에이전트 구성

| 에이전트 | 역할 |
|---|---|
| content-extractor | 논문/결과에서 핵심 메시지, Figure, 데이터 추출 |
| story-architect | 발표 내러티브 구성, 시간 배분, 청중 맞춤 |
| slide-composer | 슬라이드별 콘텐츠 작성, 레이아웃, Figure 배치 |
| pptx-engineer | python-pptx로 .pptx 파일 생성 |
| deck-reviewer | 과학적 정확성, 디자인, 타이밍 검토 + 발표 코칭 |

## 실행 흐름

```
연구 결과 입력
    │
    ▼
content-extractor → story-architect → slide-composer → pptx-engineer → deck-reviewer
                                                                          │
                                                             ┌────────────┤
                                                          REVISE        PASS
                                                             │            │
                                                             ▼            ▼
                                                      slide-composer    최종 PPTX +
                                                      (수정, 최대 2회)  발표 코칭
```

---

## 작업 공간 구조

```
{작업경로}/
├── 01_content_brief.md       # 콘텐츠 추출 결과
├── 02_story_structure.md     # 스토리 구성
├── 03_slide_deck.md          # 슬라이드 구성안
├── 04_make_ppt.py            # PPTX 생성 코드
├── 05_review_report.md       # 검토 결과
├── 06_speaker_guide.md       # 발표 코칭
├── figures/                  # Figure 원본
└── output/                   # 최종 .pptx 파일
```
