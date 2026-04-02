# SSWL-harness-ops

태양 및 우주환경연구실(SSWL) AI 하네스 운용 저장소.

## 개요

연구실에서 개발된 모델들을 아카이빙·관리하고, 연구자의 요청에 따라 데이터 수집·모델 실행·결과 보고를 수행하며, 연구 아이디어를 빠른 실험 결과로 전환하는 AI 하네스.

## 저장소 구조

```
SSWL-harness-ops/
├── .claude/                           ← 루트 하네스 (연구 업무 범용)
│   ├── CLAUDE.md
│   ├── agents/  (5개)
│   └── skills/  (3개)
│
├── 01-research-production/            ← 연구 생산 하네스 (논문 파이프라인)
│   └── .claude/
│       ├── CLAUDE.md
│       ├── agents/  (5개)
│       └── skills/  (3개)
│
├── 02-conference-presentation-generator/  ← 학회 발표 PPT 생성 하네스
│   └── .claude/
│       ├── CLAUDE.md
│       ├── agents/  (5개)
│       └── skills/  (3개)
│
├── 03-paper-writer/                   ← 논문 작성 및 피어리뷰 하네스
│   └── .claude/
│       ├── CLAUDE.md
│       ├── agents/  (4개)
│       └── skills/  (4개)
│
├── docs/                              # 프로젝트 참고 문서
└── PPT/                               # 팜플렛/발표 자료
```

## 하네스 사용법

Claude Code는 **`claude` 명령을 실행한 디렉토리의 `.claude/`만 읽습니다.**
`cd` 위치에 따라 다른 하네스가 활성화됩니다.

### 루트 하네스 — 연구 업무 범용

```bash
cd /home/youn_j/SSWL-harness-ops
claude
```

데이터 수집, 모델 실행, 모델 아카이빙 등 **범용 연구 업무**를 처리합니다.

| 에이전트 | 역할 |
|---|---|
| research-planner | 요청 분석, 실험 설계, 실행 계획 |
| data-engineer | 데이터 수집/검증, 모델 등록 |
| research-executor | 파이프라인 실행, 모델 실행 |
| paper-writer | 결과 보고, 논문 초안 |
| reviewer | 품질 검토, 교차 검증 |

```
> "최근 1달 SDO/HMI 데이터로 synoptic map 만들어줘"
> "코로나홀 탐지 모델을 등록해줘"
```

### 02-conference-presentation-generator — 학회 발표 PPT 생성

```bash
cd /home/youn_j/SSWL-harness-ops/02-conference-presentation-generator
claude
```

연구 결과를 입력하면 **콘텐츠 추출 → 스토리 설계 → 슬라이드 구성 → PPTX 생성 → 발표 코칭**까지 수행합니다.

| 에이전트 | 역할 |
|---|---|
| content-extractor | 논문/결과에서 핵심 메시지, Figure 추출 |
| story-architect | 발표 내러티브 설계, 시간 배분 |
| slide-composer | 슬라이드별 콘텐츠/레이아웃 구성 |
| pptx-engineer | python-pptx로 실제 .pptx 파일 생성 |
| deck-reviewer | 품질 검토 + 발표자 가이드/Q&A 준비 |

```
> "01-research-production의 태양 플레어 연구 결과로 15분 AGU 발표 PPT 만들어줘"
```

### 03-paper-writer — 논문 작성 및 피어리뷰

```bash
cd /home/youn_j/SSWL-harness-ops/03-paper-writer
claude
```

연구 결과를 입력하면 **논문 초안 작성 → 에디터 접수 → 리뷰어 병렬 심사 → 리비전 → 판정**까지 실제 저널 피어리뷰 프로세스를 시뮬레이션합니다. 최대 3회 리비전 후 Accept 시 저널 템플릿 기반 LaTeX + PDF를 생성합니다.

| 에이전트 | 역할 |
|---|---|
| researcher | 연구 결과 정리, 논문 초안 + 커버레터 작성, 리비전 수행 |
| editor | 논문 접수, 리뷰어 배정(전문분야/성격), 리뷰 취합, 판정 |
| reviewer-1 | 한줄씩 팩트체크, 전문분야 중심 리뷰 |
| reviewer-2 | 한줄씩 팩트체크, reviewer-1과 다른 전문분야 중심 리뷰 (병렬) |

```
> "이 연구 결과로 ApJ에 투고할 논문 써줘"
> "01-research-production의 태양 플레어 연구 결과로 논문 만들어줘"
```

### 01-research-production — 연구 생산 (논문 파이프라인)

```bash
cd /home/youn_j/SSWL-harness-ops/01-research-production
claude
```

연구 주제를 던지면 **문헌조사 → 설계 → 실행 → 검토 → 논문**까지 자동 수행합니다.

| 에이전트 | 역할 |
|---|---|
| literature-reviewer | arXiv/ADS 문헌조사, 연구 갭 식별 |
| research-designer | 가설/실험/평가지표 설계 |
| research-executor | Python 코드 작성/실행, Figure/Table |
| paper-writer | 논문 초안 (Figure+Table 5개 이내) |
| reviewer | PASS/REVISE 판정, 레퍼리 심사 |

```
> "GOES XRS 데이터를 이용한 태양 플레어 전구체 패턴 분석 연구를 해줘"
```

산출물은 모두 `_workspace/` 하위에 생성됩니다:

```
_workspace/
├── 01_literature_review.md    # 문헌조사
├── 02_research_design.md      # 연구 설계
├── 03_execution_log.md        # 실행 로그
├── 04_paper_draft.md          # 논문 초안
├── 05_review_report.md        # 검토 보고서
├── 06_referee_report.md       # 레퍼리 심사
├── research-note.md           # 전 과정 생각의 흐름
├── references.bib             # 참고문헌
├── code/                      # 실행 코드
├── figures/                   # Figure (DPI=300)
└── tables/                    # Table (CSV + Markdown)
```

## 사전 준비

```bash
pip install sunpy astropy aiapy drms pandas numpy scipy matplotlib scikit-learn
```

## 상세

- 루트 하네스: `.claude/CLAUDE.md`
- 연구 생산 하네스: `01-research-production/.claude/CLAUDE.md`
- 학회 발표 PPT 하네스: `02-conference-presentation-generator/.claude/CLAUDE.md`
- 논문 작성 하네스: `03-paper-writer/.claude/CLAUDE.md`
- 프로젝트 시나리오: `docs/scenarios.md`
