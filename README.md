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
- 프로젝트 시나리오: `docs/scenarios.md`
