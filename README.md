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
│       ├── agents/  (5개)
│       └── skills/  (4개)
│
├── 04-paper-mate/                     ← 논문 번역 및 분석 하네스
│   └── .claude/
│       ├── CLAUDE.md
│       ├── agents/  (6개)
│       └── skills/  (1개)
│
├── 05-symbolic-regression/            ← Symbolic Regression 연구 하네스
│   └── .claude/
│       ├── CLAUDE.md
│       ├── agents/  (4개)
│       └── skills/  (3개)
│
├── 06-paper-editor/                   ← 논문 교정 및 모의 피어리뷰 하네스
│   └── .claude/
│       ├── CLAUDE.md
│       └── agents/  (5개)
│
├── 07-idl2python/                     ← IDL→Python 코드 변환 하네스
│   └── .claude/
│       ├── CLAUDE.md
│       ├── agents/  (4개)
│       └── skills/  (3개)
│
├── 99-SSWL-skill-collector/           ← 연구실 코드 → 스킬 변환 하네스
│   └── .claude/
│       ├── CLAUDE.md
│       ├── agents/  (6개)
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
| co-worker | 한 문장씩 검토: 논리 흐름, 용어 통일, 팩트체크, 내부 용어 차단 |
| editor | 논문 접수, 리뷰어 배정(전문분야/성격), 리뷰 취합, 판정 |
| reviewer-1 | 한줄씩 팩트체크, 전문분야 중심 리뷰 |
| reviewer-2 | 한줄씩 팩트체크, reviewer-1과 다른 전문분야 중심 리뷰 (병렬) |

```
> "이 연구 결과로 ApJ에 투고할 논문 써줘"
> "01-research-production의 태양 플레어 연구 결과로 논문 만들어줘"
```

### 04-paper-mate — 논문 번역 및 분석

```bash
cd /home/youn_j/SSWL-harness-ops/04-paper-mate
claude
```

영어 논문을 입력하면 **챕터별 병렬 번역 → 용어 통일 → 참고문헌 분석 → Q&A 답변**까지 수행합니다.

| 에이전트 | 역할 |
|---|---|
| paper-fetcher | 논문 확보, 구조 분석, 그림 목록 추출 |
| chapter-translator | 챕터/섹션을 한국어로 병렬 번역 |
| figure-analyst | 그림의 시각적 내용·인사이트를 한국어로 상세 설명 |
| context-harmonizer | 병렬 번역 챕터 통합, 용어 통일, 문맥 조정 |
| reference-analyst | 참고문헌 중요도 분류, 필수 논문 요약 |
| qa-companion | 번역 완료 후 사용자 Q&A 답변 |

```
> "이 논문 번역해줘" (DOI, 제목, 파일 경로 제공)
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

### 05-symbolic-regression — Symbolic Regression 연구

```bash
cd /home/youn_j/SSWL-harness-ops/05-symbolic-regression
claude
```

데이터와 연구 질문을 입력하면 **데이터 진단 → 도구 라우팅 → 다중 SR 도구 병렬 실행 → SymPy 후처리 → Pareto/LaTeX 보고**까지 수행합니다. PySR을 디폴트로 두고, 데이터 형태와 단위 정보 유무에 따라 PySINDy(시계열), AI Feynman(단위 정보 보유), NeSymReS·KAN·DSO(비교군) 등을 자동 라우팅합니다.

| 에이전트 | 역할 |
|---|---|
| sr-planner | 데이터 진단, 도구 라우팅, 실행 계획, 사용자 승인 |
| sr-executor | 선택 도구(PySR/DSO/NeSymReS/KAN/Feynman/SINDy/DEAP) 병렬 실행 |
| expression-analyst | SymPy 단순화, 동등성 클러스터링, Pareto front, 차원 분석 |
| sr-reporter | Figure(Pareto/fit/residual), LaTeX 수식, 한국어 해석 보고서 |

```
> "data/measurement.csv 의 y와 x1, x2 사이 관계를 찾아줘"
> "이 시계열 데이터에서 ODE를 발견해줘"
> "단위가 있는 물리 데이터로 경험식을 찾아줘 (AI Feynman 활용)"
```

설치는 `cd 05-symbolic-regression && bash install.sh` (PyPI는 requirements.txt, GitHub 기반 도구는 자동 clone).

### 06-paper-editor — 논문 교정 및 모의 피어리뷰

```bash
cd /home/youn_j/SSWL-harness-ops/06-paper-editor
claude
```

기존 논문(.tex, .pdf, .md)의 **문법 교정, 팩트체크, 모의 피어리뷰, 구조 개선**을 수행합니다. 작업 모드를 선택하면 해당 에이전트가 실행됩니다.

| 에이전트 | 역할 |
|---|---|
| grammar-editor | 문법·표현·일관성 교정 |
| fact-checker | 수치·주장을 코드/데이터/Figure와 대조 검증 |
| structure-advisor | 섹션 구성·논리 흐름·Figure/Table 배치 분석, 개선안 제시 |
| reviewer | 한줄씩 팩트체크 + 방법론/데이터/해석 평가 (모의 리뷰) |
| reference-finder | NASA ADS/arXiv에서 참고문헌 검색·추천 |

```
> "이 논문 문법 교정해줘"
> "모의 피어리뷰 돌려줘"
```

### 07-idl2python — IDL→Python 코드 변환

```bash
cd /home/youn_j/SSWL-harness-ops/07-idl2python
claude
```

IDL `.pro` 파일을 Python으로 변환하고, 테스트를 통해 정확성을 검증합니다. 배열 인덱싱 자동 전치(column-major→row-major), SSW→SunPy/Astropy 매핑, 테스트 데이터 자동 확보를 지원합니다. 다중 파일은 병렬 변환/테스트합니다. [dnidever/idl2py](https://github.com/dnidever/idl2py) 참고.

| 에이전트 | 역할 |
|---|---|
| idl-analyzer | .pro 파싱, 의존성 분석, 변환 계획 수립 |
| python-translator | IDL→Python 구문 변환, 라이브러리 매핑 |
| test-engineer | 테스트 작성, 데이터 확보, 병렬 테스트 실행 |
| conversion-reviewer | 변환 정확성 검증, PASS/REVISE 판정 |

```
> "solar_prep.pro를 Python으로 변환해줘"
> "이 디렉토리의 IDL 코드를 전부 Python으로 마이그레이션해줘"
```

### 99-SSWL-skill-collector — 연구실 코드 → 스킬 변환

```bash
cd /home/youn_j/SSWL-harness-ops/99-SSWL-skill-collector
claude
```

연구실에 축적된 코드, 스크립트, 유틸리티를 분석·분류하여 **재사용 가능한 Claude Code 스킬**로 변환합니다. 로컬 또는 원격 서버의 코드를 수집할 수 있습니다.

| 에이전트 | 역할 |
|---|---|
| remote-collector | SSH 기반 원격 서버 코드 탐색, 버전 선별, 로컬 전송 |
| code-archaeologist | 원본 코드 분석, 목적·의존성·I/O 패턴 파악 |
| taxonomy-architect | 기능별 클러스터링, 중복 식별, 분류 체계 설계 |
| code-refactorer | 중복 병합, 모듈화, 인터페이스 표준화 |
| skill-builder | 모듈 → skill.md 변환, description 작성 |
| integration-tester | 스킬 트리거 검증, 실행 테스트, 충돌 확인 |

```
> "내 연구 코드를 스킬로 변환해줘"
> "원격 서버 /home/user/scripts/ 에 있는 코드 수집해서 스킬로 만들어줘"
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
- 논문 번역 하네스: `04-paper-mate/.claude/CLAUDE.md`
- Symbolic Regression 하네스: `05-symbolic-regression/.claude/CLAUDE.md`
- 논문 교정 하네스: `06-paper-editor/.claude/CLAUDE.md`
- IDL→Python 변환 하네스: `07-idl2python/.claude/CLAUDE.md`
- 스킬 변환 하네스: `99-SSWL-skill-collector/.claude/CLAUDE.md`
- 프로젝트 시나리오: `docs/scenarios.md`
