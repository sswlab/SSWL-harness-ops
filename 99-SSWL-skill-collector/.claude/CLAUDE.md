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
7. **자격증명/이메일 분리**: 아래 "외부 서비스 자격증명 처리" 절 참조

## 외부 서비스 자격증명 처리

연구실 코드에는 종종 **외부 서비스에 등록된 이메일이나 API 키**가 하드코딩되어 있다.
스킬로 변환할 때는 이런 값을 **반드시 분리**해야 한다.

### JSOC/SDO drms 코드를 발견하면

원본 코드:
```python
import drms
client = drms.Client()
export = client.export(query, method="url", protocol="fits",
                       email="someone@university.edu")  # ← 하드코딩
```

스킬로 변환할 때:
- ❌ 원본의 이메일을 그대로 둔 채 패키징하지 말 것 (다른 사용자에게 발송 추적이 잘못 부과됨)
- ❌ `email="user@example.com"` 같은 더미값으로 대체하지 말 것 (런타임 에러)
- ✅ **스킬이 사용자에게 이메일을 묻도록 설계**:
  ```python
  def fetch_aia(query: str, email: str | None = None):
      if not email:
          raise ValueError(
              "JSOC export에는 등록된 이메일이 필요합니다. "
              "email 인수를 제공하거나 환경변수 JSOC_EMAIL을 설정하세요. "
              "등록: http://jsoc.stanford.edu/ajax/register_email.html"
          )
      ...
  ```
- ✅ **skill.md의 description에 명시**: "JSOC 등록 이메일이 필요한 작업"임을 트리거 키워드와 함께 기록
- ✅ **사용 예시에 사용자 질문 단계 포함**:
  > 1. 사용자에게 JSOC 등록 이메일을 묻는다
  > 2. (선택) 환경변수 `JSOC_EMAIL` 확인 → 있으면 그것 사용
  > 3. 둘 다 없으면 명확한 에러 메시지로 안내

### 다른 자격증명도 마찬가지

| 패턴 | 처리 |
|---|---|
| `email="..."`, `EMAIL = "..."` | 함수 인자 또는 환경변수로 분리 |
| `api_key="..."`, `TOKEN = "..."` | 환경변수 (`os.environ["XXX_API_KEY"]`) |
| `password="..."`, `passwd = "..."` | 환경변수 + 사용자 안내 |
| 학교 LDAP, KASI 내부 서버 자격 | 별도 설정 파일, .env, 키링 사용 |

**원칙**: 스킬은 **다음 사용자**가 받았을 때 자기 자격증명을 입력하여 동작해야 한다. 원본 작성자의 자격증명이 leak되면 안 된다.
