---
name: paper-find
description: >
  논문 정찰·우선순위화 오케스트레이터. 주제를 받으면 NASA ADS·arXiv·Semantic Scholar
  병렬 검색, 사용자 확인 후 PDF 다운로드, 논문 × 섹션 2D 병렬 청크 분석, 1논문 1카드
  합성, 점수 기반 읽기 순서 결정, 한글 PDF 보고서까지 한 번에 처리한다.
  트리거: /paper-find, "논문 찾아줘", "주제로 논문 검색", "관련 논문 정리", paper find, literature scan,
  "최근 ~ 논문 모아줘", "어떤 논문부터 읽어야 해", DOI/제목 한 편 깊이 분석은 /paper-read로 위임.
---

# Paper-Find — 논문 정찰·우선순위화 오케스트레이터

## 트리거 조건

다음 상황에서 이 스킬이 활성화된다:
- 사용자가 `/paper-find` 명령을 입력
- "X 주제 논문 찾아줘", "관련 논문 정리해줘", "어떤 논문부터 읽어야 해" 같은 자연어 요청
- 주제어 + 연도 범위 + 분량을 함께 던지는 경우 (예: "코로나 가열 메커니즘 최근 5년 15편")

**트리거하지 말아야 할 경우 (paper-mate로 위임):**
- 사용자가 DOI 1개 또는 논문 제목 1개를 제공하여 **그 논문 자체**를 번역·분석 요청
- "이 PDF 읽어줘" 같은 단일 파일 요청

## 실행 모드

**에이전트 팀 모드** (기본). 팀원 5명: query-planner, paper-hunter, chunk-analyst, synthesizer, prioritizer.

## 실행 프로토콜

### Phase 0: 입력 확보

사용자로부터 다음을 확보한다 (누락 시 1회 되묻기):

| 항목 | 변수 | 기본값 |
|---|---|---|
| 연구 주제 | `{주제}` | (필수) |
| 연도 범위 | `{연도}` | 최근 5년 |
| 분량 상한 | `{상한}` | 15편 |
| 작업 경로 | `{작업경로}` | `_workspace/` |

이후의 `{작업경로}` 표기는 모두 사용자가 지정한 경로로 치환한다.

### Phase 1: 검색 전략 수립

**담당**: query-planner (단일)

1. 주제를 핵심 개념·동의어·인접 영역으로 분해
2. arXiv 쿼리 문법과 Semantic Scholar 쿼리 자연어를 각각 작성
3. 출력: `{작업경로}/00_query_plan.md`

**진행 보고**: "검색 계획을 수립했습니다: arXiv 쿼리 N개, S2 쿼리 N개. 검색을 시작합니다."

### Phase 2: 다중 소스 검색 + 중복 제거

**담당**: paper-hunter (소스별 3개 인스턴스 병렬)

1. 환경변수 확인 (`$ADS_API_TOKEN`, `$S2_API_KEY`). 없는 소스는 스킵하고 보고에 명시.
2. NASA ADS, arXiv, Semantic Scholar API를 동시에 호출
3. 응답을 통일 카드 스키마로 정규화 (ADS 필드 우선 — bibcode, citation_count, 공식 초록)
4. bibcode → DOI → arXiv ID → 제목/저자 정규화 순으로 중복 제거
5. 관련성 1차 컷오프로 상위 `{상한}`편 선정
6. 출력: `{작업경로}/01_search_results.md` (다운로드 정책 질문 포함)

**진행 보고**: "후보 {상한}편을 발견했습니다. 다운로드 정책을 선택해주세요."

### Phase 3: 다운로드 결정 (사용자 확인)

**사용자에게 매번 묻는다** (자동 다운로드 절대 금지).

선택지:
- `all` — 전부 다운로드
- `top N` — 상위 N편 (예: `top 5`)
- `none` — 다운로드 없이 초록만으로 분석 (전 논문 abstract-only 모드)
- `pick #3 #5 #7` — 번호 명시 선택

응답 수신 후 paper-hunter가 PDF 확보하고 `01_search_results.md`의 `PDF 상태`를 업데이트.

### Phase 4: 청크 분할

**담당**: 오케스트레이터 (스크립트 호출)

다운로드된 각 PDF에 대해:

1. `scripts/chunk_pdf.sh {paper_id}` 실행
   - 1차: `pdftotext -layout` + 헤딩 정규식으로 섹션 분할
   - 2차 폴백: 페이지 수 5등분
2. 결과: `{작업경로}/chunks/{paper_id}/{section}.md` (헤더에 `split`, `confidence` 명시)

다운로드되지 않은 논문은 분할 단계 스킵 (abstract-only 처리).

### Phase 5: 2D 병렬 청크 분석

**담당**: chunk-analyst (논문 M편 × 섹션 K개 = M×K 인스턴스 병렬)

병렬도 가이드:
- 후보 15편, 섹션 평균 5개 → 최대 75개 청크
- 한 번에 너무 많이 띄우면 토큰 비용·rate limit 부담. **6~8명을 한 팀으로 묶어 라운드 방식으로 처리** (팀 1: 청크 1~8, 팀 2: 청크 9~16, ...).
- 동일 paper_id의 청크들끼리는 독립적이므로 어느 라운드에 분산되어도 무관.

각 chunk-analyst는 할당 청크 1개만 분석하여 `{작업경로}/02_chunk_analyses/{paper_id}/{section}.md` 작성.

**진행 보고**: "총 N개 청크 분석 중... (라운드 i/j 완료)"

### Phase 6: 논문별 카드 합성

**담당**: synthesizer (paper_id 단위 병렬, M편)

각 synthesizer는 한 논문의 모든 청크 분석을 읽어 `{작업경로}/03_paper_cards/{paper_id}.md`를 작성.

청크 분석이 0개면 `FAILED.md`를 만들어 사유 기록.

### Phase 7: 우선순위화 + 보고서

**담당**: prioritizer (단일)

1. 모든 paper card를 읽고 4개 신호로 점수화 (관련성 40 / 신규성 25 / 인용 20 / 최신성 15)
2. 보정 적용 (abstract-only -10, low confidence -5)
3. 클러스터링 + 의존 관계 분석으로 읽기 순서 결정
4. Markdown 보고서 작성: `{작업경로}/04_priority_report.md`
5. LaTeX 변환 후 `tectonic`으로 PDF 컴파일: `{작업경로}/04_priority_report.pdf`
6. paper-mate 위임 명령 예시를 보고서에 포함

**완료 보고**: "보고서가 완성되었습니다. 권장 상위 N편을 깊이 분석하려면 `cd ../04-paper-mate`로 이동하세요."

## 팀 통신 프로토콜

- 모든 데이터 전달은 **파일 기반**(`{작업경로}` 하위).
- 진행 상황 추적은 **TaskCreate/TaskUpdate**로 (오케스트레이터가 청크 단위로 태스크를 생성하여 chunk-analyst가 claim).
- 팀원 간 실시간 소통이 필요한 경우(예: chunk-analyst가 PDF 깨짐을 발견하여 synthesizer에게 abstract-only 모드로 전환 요청)는 SendMessage 사용.

## 작업 경로 정책

- 사용자가 지정하지 않으면 `_workspace/` 사용.
- 모든 중간 산출물(00~03 파일)을 삭제하지 않고 보존 — 사후 감사·재실행 용도.
- 최종 산출물은 `04_priority_report.md`/`.pdf` 두 개.

## 에러 핸들링

| 상황 | 대응 |
|---|---|
| query-planner가 주제 모호로 재질문 필요 | 사용자에게 되묻고 재실행 |
| arXiv/S2 한쪽 API 실패 | 다른 쪽 결과로만 진행. 보고서에 누락 명시 |
| 다운로드 0건 (사용자 `none` 선택) | 모든 논문 abstract-only로 진행. 보고서에 모드 표시 |
| 청크 분석 일부 실패 | 가용 청크로 카드 작성. 누락 섹션은 `(분석 청크 없음)` 표시 |
| PDF 컴파일 실패 | Markdown만 출력. 보고서에 사유 기록 |
| 모든 카드 실패 | prioritizer가 "분석 실패 — query를 완화하여 재시도" 안내 출력 |

## 테스트 시나리오

**정상 흐름**:
- 입력: "태양 코로나 가열 메커니즘 최근 5년 10편 찾아줘"
- 예상: query-planner가 nanoflare/wave heating/MHD 관련 쿼리 작성 → paper-hunter 검색 → 사용자가 `top 5` 다운로드 선택 → chunk-analyst 25개 청크 분석 → synthesizer 10편 카드 → prioritizer 보고서(PDF)
- 검증: `04_priority_report.pdf` 생성, 상위 5편의 점수 합산이 0~100 범위, paper-mate 위임 명령 포함

**에러 흐름 (Semantic Scholar rate limit)**:
- 입력: 동일 (단, `S2_API_KEY` 미설정 상태에서 짧은 간격 호출)
- 예상: 429 에러 발생 → 5초 대기 재시도 1회 → 또 실패하면 arXiv 결과만으로 진행
- 검증: `01_search_results.md`에 "Semantic Scholar 실패 — arXiv 결과만 사용" 명시, 보고서에도 동일 명시

## 다른 하네스와의 관계

- **04-paper-mate**: 정찰 → 깊이 분석. 보고서의 상위 N편을 paper-mate로 넘기는 명령 예시를 자동 생성한다.
- **03-paper-writer**: 사용자가 작성 중인 논문의 참고문헌 보강을 원할 때, 정찰 결과를 paper-writer 입력으로 활용 가능.
- **99-SSWL-skill-collector**: 검색 과정에서 발견한 코드/데이터셋이 연구실 자산이면 skill-collector로 등록 후보 표시.
