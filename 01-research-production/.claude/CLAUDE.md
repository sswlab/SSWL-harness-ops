# 01-Research-Production — SSWL 연구 생산 하네스

태양 및 우주환경연구실(SSWL)의 **연구 아이디어 → 논문** 전 과정을 자동화하는 AI 하네스.
사용자가 연구 주제를 제시하면, 문헌조사부터 실험 실행, 논문 초안, 피어 리뷰까지 에이전트 팀이 협력하여 수행한다.

## 에이전트 팀 구성표

| 에이전트 | 역할 | 설명 |
|---|---|---|
| **literature-reviewer** | 문헌조사 | arXiv/ADS 검색, 선행연구 요약, 중복 판별, 연구 갭 식별 |
| **research-designer** | 연구설계 | 가설 수립, 데이터/모델/실험 계획, 평가 지표 설계 |
| **research-executor** | 실험실행 | Python 코드 작성/실행, 데이터 처리, Figure/Table 생성 |
| **paper-writer** | 논문작성 | 논문/초록/리포트 작성, Figure+Table 5개 이내 선별 |
| **reviewer** | 품질검토 | 설계 vs 결과 대조 검토, PASS/REVISE 판정, 레퍼리 심사 |

## 실행 모드: 에이전트 팀

```
사용자 요청
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

## 작업 경로 정책

- **하네스 내 `_workspace/`는 빈 스캐폴드**(디렉토리 구조 템플릿)이다. 실행 결과물을 여기에 저장하지 않는다.
- 파이프라인 시작 시 사용자에게 **작업 경로를 질문**한다. 사용자가 쿼리에 경로를 명시했으면 그대로 사용한다.
- 이후 모든 `_workspace/` 참조는 사용자가 지정한 `{작업경로}`로 치환된다.

## 데이터 전달 규칙

에이전트 간 모든 데이터는 사용자가 지정한 `{작업경로}` 하위 파일로 전달한다.

| 에이전트 | 출력 파일 |
|---|---|
| literature-reviewer | `{작업경로}/01_literature_review.md`, `{작업경로}/references.bib` |
| research-designer | `{작업경로}/02_research_design.md` |
| research-executor | `{작업경로}/code/`, `{작업경로}/figures/`, `{작업경로}/tables/`, `{작업경로}/03_execution_log.md` |
| paper-writer | `{작업경로}/04_paper_draft.md` |
| reviewer | `{작업경로}/05_review_report.md`, `{작업경로}/06_referee_report.md` |
| 공통 | `{작업경로}/research-note.md` (전 과정 생각의 흐름 누적 기록) |

**전달 규칙:**
1. 각 에이전트는 자신의 지정 파일에만 쓴다
2. 다른 에이전트의 출력은 읽기 전용으로 참조한다
3. 모든 중간 산출물은 삭제하지 않고 보존한다
4. `{작업경로}/research-note.md`에 모든 에이전트가 자기 판단 과정을 누적 기록한다

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
2. **결과 투명성**: 성공이든 실패든, 과정과 결과를 명확히 보고
3. **품질 게이트**: reviewer가 PASS 판정해야 다음 단계로 진행
4. **생각의 흐름 기록**: 모든 판단 과정을 research-note.md에 누적
5. **재현성**: 코드, 데이터 경로, 파라미터를 명시하여 제3자가 재현 가능
