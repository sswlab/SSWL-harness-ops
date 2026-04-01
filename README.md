# SSWL-harness-ops

태양 및 우주환경연구실(SSWL) AI 하네스 운용 저장소.

## 개요

연구실에서 개발된 모델들을 아카이빙·관리하고, 연구자의 요청에 따라 데이터 수집·모델 실행·결과 보고를 수행하며, 연구 아이디어를 빠른 실험 결과로 전환하는 AI 하네스.

## 핵심 운용 모드

1. **연구 업무 수행** — 자연어 요청 → 계획 → 실행 → 결과 보고
2. **모델 아카이빙/활용** — 연구실 모델 표준화 등록, 누구나 활용
3. **아이디어 → 실험 결과** — 아이디어 → 실험 설계 → 실행 → 논문 초안

## 구조

```
.claude/
├── CLAUDE.md              # 하네스 설정 (에이전트 팀, 데이터 규칙)
├── agents/                # 에이전트 정의 (5개)
│   ├── research-planner   # 연구설계
│   ├── data-engineer      # 데이터처리
│   ├── research-executor  # 실험실행
│   ├── paper-writer       # 논문작성
│   └── reviewer           # 품질검토(QA)
└── skills/                # 스킬 정의 (3개)
    ├── research-orchestrator  # 파이프라인 총괄
    ├── data-pipeline          # 데이터/모델 절차
    └── research-workflow      # 아이디어→실험→논문

docs/                      # 프로젝트 참고 문서
PPT/                       # 팜플렛/발표 자료
```

## 상세

하네스 구성 상세는 `.claude/CLAUDE.md`를, 프로젝트 시나리오는 `docs/scenarios.md`를 참조하세요.
