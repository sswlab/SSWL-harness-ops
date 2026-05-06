# 01-Research-Production — SSWL 연구 생산 하네스

태양 및 우주환경연구실(SSWL)의 **연구 아이디어 → 논문** 전 과정을 자동화하는 AI 하네스.
사용자가 연구 주제를 제시하면, 문헌조사부터 실험 실행, 논문 초안, 피어 리뷰까지 에이전트 팀이 협력하여 수행한다.

## 에이전트 팀 구성표

| 에이전트 | 역할 | 모델 | 설명 |
|---|---|---|---|
| **intake-interviewer** | Phase 0 인테이크 | Sonnet (claude-sonnet-4-6) | Ouroboros식 Ambiguity 점수로 모호성 해소, immutable spec 봉인 |
| **literature-reviewer** | 문헌조사 | (기본) | arXiv/ADS 검색, 선행연구 요약, 중복 판별, 연구 갭 식별 |
| **research-designer** | 연구설계 | (기본) | 가설 수립, 데이터/모델/실험 계획, 평가 지표 설계 |
| **research-executor** | 실험실행 | (기본) | Python 코드 작성/실행, 데이터 처리, Figure/Table 생성 |
| **paper-writer** | 논문작성 | (기본) | 논문/초록/리포트 작성, Figure+Table 5개 이내 선별 |
| **reviewer** | 품질검토 | (기본) | 설계 vs 결과 대조 검토, PASS/REVISE 판정, 레퍼리 심사 |

## 실행 모드: 에이전트 팀

```
사용자 요청
    │
    ▼
intake-interviewer (Phase 0, Sonnet, Ambiguity 루프) → 00_intake_spec.md (immutable)
    │
    ▼
literature-reviewer  →  research-designer  →  research-executor  →  reviewer(검토)
                                                                       │
                                                          ┌────────────┤
                                                          │            │
                                                       REVISE       PASS
                                                          │            │
                                                          ▼            ▼
                                                   research-designer  paper-writer  →  reviewer(심사)  →  최종 결과
                                                   (루프백, 최대 2회)
```

## 필수 입력 정책

파이프라인 시작 전 4가지 필수 항목을 확보한다. 누락 시 되물어서 확보한다.
**이 4항목은 Phase 0 Socratic 인테이크의 시드(seed)로 사용되며, 실제 연구 의도 명료화는 `intake-interviewer`가 수행한다.**

| 항목 | 변수 | 용도 |
|---|---|---|
| 연구 주제 | `{주제}` | 파이프라인 전체의 대상 |
| 연구 목적 | `{목적}` | 모든 에이전트의 판단 기준. "왜 이 연구를 하는가" |
| 연구 모드 | `{모드}` | Phase별 깊이/비중 결정 (탐색형/심층형/전체) |
| 작업 경로 | `{작업경로}` | 결과물 저장 위치 |

상세 안내는 `README.md` 참조.

## Phase 0: Socratic 인테이크 (Ouroboros식 모호성 해소)

`intake-interviewer` 에이전트가 Sonnet 모델로 사용자와 Q&A 라운드를 반복하여
Ambiguity 점수를 임계값 이하로 떨어뜨린 뒤 `00_intake_spec.md`를 immutable spec으로 봉인한다.

| 모드 | Ambiguity 임계값 | 의미 |
|---|---|---|
| 탐색형 (Survey) | ≤ 0.35 | 65% 명료 |
| 심층형 (Deep Dive) | ≤ 0.20 | 80% 명료 |
| 전체 (Full) | ≤ 0.20 | 80% 명료 |

- 4차원: 목적(35%) / 제약(25%) / 성공기준(30%) / 배경(10%) — 이전 버전 감지 시 배경 가중치 25%로 상향
- 하드캡: 8라운드 / 정체(0.03 미만 감소) 2회 연속 시 사용자에게 옵션 제시
- 봉인 후 `literature-reviewer`와 `research-designer`는 `00_intake_spec.md`를 단일 진실원으로 참조한다
- 봉인 후 변경은 사용자 명시 승인 시에만 "변경 이력" 추가 방식으로 허용

## 연구 모드

| 모드 | Phase 1 문헌 | Phase 3 실험 | Phase 5 논문 스타일 |
|---|---|---|---|
| **탐색형** | 30~50편, 넓은 키워드 | 최소/생략 | 리뷰 페이퍼 |
| **심층형** | 10~15편, 좁은 키워드 | 전체 수행 | 오리지널 리서치 |
| **전체** | 20~30편, 균형 | 전체 수행 | 오리지널 리서치 |

## 작업 경로 정책

- **하네스 내 `_workspace/`는 빈 스캐폴드**(디렉토리 구조 템플릿)이다. 실행 결과물을 여기에 저장하지 않는다.
- 이후 모든 `_workspace/` 참조는 사용자가 지정한 `{작업경로}`로 치환된다.

## 데이터 전달 규칙

에이전트 간 모든 데이터는 사용자가 지정한 `{작업경로}` 하위 파일로 전달한다.

| 에이전트 | 출력 파일 |
|---|---|
| intake-interviewer | `{작업경로}/00_intake_spec.md` (immutable) |
| literature-reviewer | `{작업경로}/01_literature_review.md`, `{작업경로}/references.bib` |
| research-designer | `{작업경로}/02_research_design.md` |
| research-executor | `{작업경로}/code/`, `{작업경로}/figures/`, `{작업경로}/tables/`, `{작업경로}/03_execution_log.md`, (크로스-버전 비교 시) `{작업경로}/tables/version_comparison.md` |
| paper-writer | `{작업경로}/04_paper_draft.md` |
| reviewer | `{작업경로}/05_review_report.md`, `{작업경로}/06_referee_report.md`, (PASS-WITH-FINDINGS 시) `{작업경로}/findings_for_next_version.md` |
| 공통 | `{작업경로}/research-note.md` (전 과정 생각의 흐름 누적 기록) |
| 프로젝트 수준 | `{프로젝트_루트}/project-meta.md` (선택, 버전 이력 관리) |

**전달 규칙:**
1. 각 에이전트는 자신의 지정 파일에만 쓴다
2. 다른 에이전트의 출력은 읽기 전용으로 참조한다
3. 모든 중간 산출물은 삭제하지 않고 보존한다
4. `{작업경로}/research-note.md`에 모든 에이전트가 자기 판단 과정을 누적 기록한다. **오케스트레이터가 파이프라인 시작 시 자동 생성을 보장하고, 각 Phase 완료 후 기록 여부를 확인한다**
5. `findings_for_next_version.md`는 사용자가 후속 버전에서 이전 작업경로로 제공하면 research-designer가 참조한다
6. `version_comparison.md`는 연구자 참고용이며 논문에 직접 포함하지 않는다

## 워크스페이스 네이밍 컨벤션

반복 연구 시 워크스페이스 이름의 일관성을 유지한다.

- **권장 형식**: `{프로젝트_루트}/_workspace-v{N}` (소문자 v + 정수)
- **예시**: `_workspace-v1`, `_workspace-v2`, ..., `_workspace-v13`
- 오케스트레이터가 기존 워크스페이스를 감지하여 다음 번호를 제안하나, 사용자 선택을 강제하지 않는다
- 대소문자 혼재(`_workspace-V5` vs `_workspace-v5`)를 감지하면 경고한다

## 프로젝트 메타데이터

프로젝트 루트에 `project-meta.md`를 두어 버전 간 연속성을 관리할 수 있다 (선택).

- 파이프라인 시작 시 존재하면 읽어서 컨텍스트로 활용
- 첫 실행 완료 시 없으면 생성 여부를 사용자에게 제안
- 상세 형식은 `research-orchestrator` 스킬 참조

## 기술 스택

| 범주 | 도구 |
|---|---|
| 언어 | Python 3.10+ |
| 태양물리 | sunpy, astropy, aiapy, drms |
| 데이터 | pandas, numpy, scipy |
| 시각화 | matplotlib (publication-quality, DPI=300) |
| 논문 | LaTeX, BibTeX |
| ML (필요 시) | scikit-learn, PyTorch |

## 사용 언어

- 사용자 대면: 한국어
- 코드/설정: 영어
- 논문 초안: 영어 (사용자 요청 시 한국어)

## 핵심 원칙

1. **사용자 승인 필수**: 실행 계획을 제시하고 승인 후 진행
2. **목적 의식 유지**: 모든 에이전트는 Phase 시작 시 `{목적}`을 참조하고, 결과가 목적에 부합하는지 자체 점검
3. **결과 투명성**: 성공이든 실패든, 과정과 결과를 명확히 보고
4. **품질 게이트**: reviewer가 PASS / PASS-WITH-FINDINGS / REVISE 판정. PASS-WITH-FINDINGS 시 `findings_for_next_version.md`를 생성하여 후속 연구 방향을 기록
5. **생각의 흐름 기록**: 모든 판단 과정을 research-note.md에 누적
6. **재현성**: 코드, 데이터 경로, 파라미터를 명시하여 제3자가 재현 가능
7. **외부 서비스 자격증명은 사용자에게 묻기**: 아래 "외부 서비스 인증" 절 참조
8. **내부 용어 차단**: 내부 버전 코드(V1~V13 등), 내부 목표/타겟, 하네스 용어, 내부 파일명, 버전 이력은 논문 초안에 포함하지 않는다. paper-writer가 1차 필터링하고, reviewer가 Phase 6에서 잔존 여부를 확인한다

## 외부 서비스 인증

### JSOC/SDO 데이터 다운로드 — 이메일 필수

`drms.Client.export()` 호출에는 **JSOC에 등록된 이메일 주소가 반드시 필요**하다.
이는 JSOC export 큐 추적용이며, 사전에 [http://jsoc.stanford.edu/ajax/register_email.html](http://jsoc.stanford.edu/ajax/register_email.html) 에서 등록해야 사용 가능하다.

**규칙:**
- ❌ **절대 하드코딩 금지** — `email="user@example.com"`, `email="test@test.com"` 같은 더미값 금지
- ❌ **임의 추측 금지** — 사용자 메시지나 메모리에서 본 이메일을 멋대로 사용하지 말 것
- ✅ **첫 사용 전에 사용자에게 명시적으로 질문**:
  > "JSOC 데이터 다운로드에 등록된 이메일 주소가 필요합니다. 어떤 이메일을 사용할까요? (예: name@khu.ac.kr)
  > 처음 사용하는 이메일이라면 [JSOC 등록 페이지](http://jsoc.stanford.edu/ajax/register_email.html)에서 먼저 등록해 주세요."
- ✅ **세션 내 재사용 가능**: 한 번 받은 이메일은 같은 세션 내에서 재질문 없이 재사용한다 (research-note.md에 기록)
- ✅ **다른 세션에서는 다시 질문**: 세션이 바뀌면 처음부터 다시 묻는다 (사용자가 바뀔 수 있음)

**적용 대상 도구**: `drms`, `sunpy.net.jsoc.JSOCClient`, 그리고 JSOC을 호출하는 모든 wrapper

### 기타 외부 서비스
- **NOAA SWPC, VSO, SOAR, STEREO SSC**: 인증 불필요 (공개)
- **유료/구독 서비스(향후 추가 시)**: 같은 원칙 적용 — 사용자에게 묻고, 하드코딩하지 않는다
