# 99-SSWL-Skill-Collector — 연구실 코드 → 스킬 변환 하네스

연구실에서 축적된 개인 코드, 스크립트, 유틸리티를 분석하고 분류하여
재사용 가능한 **Claude Code 스킬**로 변환하는 하네스.

## 프로젝트 개요

연구자가 정리되지 않은 코드 덩어리를 `inbox/`에 넣으면,
에이전트 팀이 코드를 읽고 → 기능별로 묶고 → 리팩터링하고 → 스킬로 패키징한다.
최종 산출물은 `.claude/skills/` 형식의 즉시 사용 가능한 스킬이다.

## 에이전트 팀 구성표

| 에이전트 | 역할 | 핵심 기능 |
|---|---|---|
| **code-archaeologist** | 코드 분석 | 원본 코드 읽기, 목적·의존성·I/O 패턴 파악, 인벤토리 생성 |
| **taxonomy-architect** | 분류 설계 | 기능별 클러스터링, 중복 식별, 분류 체계(taxonomy) 설계 |
| **code-refactorer** | 코드 정리 | 중복 병합, 모놀리스 분리, 모듈화, 인터페이스 표준화 |
| **skill-builder** | 스킬 패키징 | 모듈 → skill.md 변환, description 작성, references 구성 |
| **integration-tester** | 품질 검증 | 스킬 트리거 검증, 실행 테스트, 기존 스킬과 충돌 확인 |

## 실행 모드: 에이전트 팀

**기본 흐름:**
```
코드 덤프 (inbox/)
    │
    ▼
code-archaeologist  →  taxonomy-architect  →  [사용자 승인]
    │
    ▼
code-refactorer  →  skill-builder  →  integration-tester  →  최종 스킬
```

**데이터 흐름:**
```
code-archaeologist  ──(인벤토리)──▶  taxonomy-architect
taxonomy-architect  ──(분류 체계)──▶  code-refactorer
code-refactorer     ──(모듈)──▶      skill-builder
skill-builder       ──(스킬 초안)──▶  integration-tester
integration-tester  ──(피드백)──▶    skill-builder (루프백)
```

## 데이터 전달 규칙

1. **파일 기반 전달**: 에이전트 간 데이터는 `{작업경로}` 하위 파일로 전달한다
2. **원본 보존**: `inbox/`의 원본 코드는 절대 수정하지 않는다. 사본으로 작업한다
3. **중간 결과 보존**: 모든 중간 산출물은 삭제하지 않고 보존한다

| 에이전트 | 출력 디렉토리 |
|---|---|
| code-archaeologist | `{작업경로}/inventory/` |
| taxonomy-architect | `{작업경로}/clusters/` |
| code-refactorer | `{작업경로}/modules/` |
| skill-builder | `{작업경로}/skills/` |
| integration-tester | `{작업경로}/reports/` |
| 공통 | `{작업경로}/logs/collector-note.md` |

## 스킬 구성

| 스킬 | 역할 |
|---|---|
| **skill-collector-orchestrator** | 전체 파이프라인 조율, 에이전트 실행 순서, 루프백, 사용자 승인 |
| **code-analysis-protocol** | 코드 분석 절차, 인벤토리 작성 표준, 의존성 추출 규칙 |
| **skill-packaging-guide** | 모듈→스킬 변환 규칙, description 작성법, progressive disclosure |

## 핵심 운용 모드

1. **전체 변환**: 코드 덤프 전체를 분석 → 분류 → 스킬화
2. **추가 수집**: 기존 인벤토리에 새 코드 추가 → 기존 분류에 통합
3. **단일 변환**: 특정 코드 파일만 지정하여 스킬로 변환

## 작업 공간

```
_workspace/
├── inbox/          # 사용자가 원본 코드를 넣는 곳 (읽기 전용으로 취급)
├── inventory/      # 코드 인벤토리 (분석 결과)
├── clusters/       # 기능별 클러스터링 결과
├── modules/        # 리팩터링된 모듈
├── skills/         # 패키징된 스킬 초안
├── reports/        # 검증 보고서
└── logs/           # 시스템 로그, collector-note.md
```

## 사용 언어

- 사용자 대면: 한국어
- 코드/설정: 영어
- 스킬 문서 (skill.md): 한국어 (사용자 요청 시 영어)

## 핵심 원칙

1. **원본 불변**: inbox/ 코드는 절대 수정하지 않는다. 모든 작업은 사본으로 수행
2. **사용자 승인 필수**: 분류 체계 확정 전 사용자에게 제시하고 승인받는다
3. **점진적 변환**: 한 번에 모든 코드를 변환하지 않고, 클러스터 단위로 점진적 처리
4. **의도 확인**: 코드의 목적이 불분명하면 사용자에게 질문한다
5. **기존 스킬 존중**: 변환 결과가 기존 하네스 스킬과 충돌하지 않도록 확인
6. **실용성 우선**: 모든 코드를 스킬로 만들 필요 없다. 재사용 가치가 낮은 코드는 "아카이브"로 분류
