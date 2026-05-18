# 10-Paper-Finder — 논문 탐색·우선순위화 하네스

주제를 받아 관련 논문을 **얕고 넓게 정찰**하고, 읽어야 할 순서를 정해 보고서를 작성하는 AI 하네스.
1편 깊이 분석은 `04-paper-mate`의 영역이다. 이 하네스는 거기에 넘기기 직전까지의 **선별 단계**를 담당한다.

## 에이전트 팀 구성표

| 에이전트 | 역할 | 설명 |
|---|---|---|
| **query-planner** | 검색 전략 수립 | 사용자 주제를 키워드/연도/저자/필터로 분해하고, 소스별(arXiv, Semantic Scholar) 쿼리를 작성 |
| **paper-hunter** | 다중 소스 검색 | NASA ADS + arXiv + Semantic Scholar API 병렬 호출, 중복 제거(bibcode/DOI/arXivID), 메타데이터 정규화, 사용자 확인 후 PDF 다운로드 |
| **chunk-analyst** | 병렬 청크 분석 | PDF/초록을 섹션 단위로 쪼개 병렬 분석 (논문 × 섹션 2D 팬아웃) |
| **synthesizer** | 논문별 카드 합성 | 청크 결과를 논문 1편 1장 요약 카드로 통합 |
| **prioritizer** | 우선순위화 + 보고서 | 관련성·인용수·최신성·핵심도 점수화, 읽기 순서 제안, Markdown + PDF 컴파일 |

## 실행 흐름

```
사용자 요청 (주제 + 필터 + 분량)
    │
    ▼
query-planner (검색 전략 수립)
    │
    ▼
paper-hunter ×N (소스별 병렬 검색 → 통합 후보 목록)
    │
    ▼
[다운로드 결정 — 사용자에게 매번 묻기]
    │
    ▼
chunk-analyst (2D 병렬: 논문 M편 × 섹션 K개 = M×K 동시 분석)
    │
    ▼
synthesizer ×M (논문별 1장 요약 카드)
    │
    ▼
prioritizer (점수화 + 읽기 순서 + 보고서 컴파일)
```

## 필수 입력 정책

파이프라인 시작 전 아래 항목을 확보한다. 누락 시 되물어 확보한다.

| 항목 | 변수 | 용도 | 기본값 |
|---|---|---|---|
| 연구 주제 | `{주제}` | 검색 대상 | 필수 |
| 연도 범위 | `{연도}` | 검색 필터 | 최근 5년 |
| 분량 상한 | `{상한}` | 후보 논문 수 (정찰 대상) | 15편 |
| 작업 경로 | `{작업경로}` | 결과물 저장 위치 | `_workspace/` |
| 다운로드 정책 | `{다운로드}` | 매번 확인 (Phase 2 직후) | `ask` |

## 다운로드 정책

`{다운로드}`는 **매번 사용자에게 묻는다**(b 정책). 자동 다운로드하지 않는다.

옵션:
- `all` — 모든 후보 PDF 다운로드
- `top N` — 상위 N편만 다운로드 (관련성 점수 기준)
- `none` — 메타데이터+초록만으로 분석 (PDF 없이 진행)
- `pick #3 #5 #7` — 사용자가 번호로 명시 선택

다운로드하지 않은 논문은 chunk-analyst가 초록·메타데이터로만 카드를 만든다(필드에 `(abstract-only)` 명시).

## 작업 경로 정책

- 하네스 내 `_workspace/`는 빈 스캐폴드이다. 실행 결과물을 여기에 두지 않는다.
- 모든 `_workspace/` 참조는 사용자가 지정한 `{작업경로}`로 치환된다.
- 작업 경로 미지정 시 하네스 루트의 `_workspace/`를 사용한다.

## 데이터 전달 규칙

에이전트 간 모든 데이터는 `{작업경로}` 하위 파일로 전달한다.

| 에이전트 | 출력 파일 |
|---|---|
| query-planner | `{작업경로}/00_query_plan.md` |
| paper-hunter | `{작업경로}/01_search_results.md`, `{작업경로}/papers/*.pdf` (선택적) |
| chunk-analyst | `{작업경로}/chunks/{paper_id}/{section}.md` (분할), `{작업경로}/02_chunk_analyses/{paper_id}/{section}.md` (분석) |
| synthesizer | `{작업경로}/03_paper_cards/{paper_id}.md` |
| prioritizer | `{작업경로}/04_priority_report.md`, `{작업경로}/04_priority_report.tex`, `{작업경로}/04_priority_report.pdf` |

**전달 규칙:**
1. 각 에이전트는 자신의 지정 파일에만 쓴다
2. 다른 에이전트의 출력은 읽기 전용으로 참조한다
3. 모든 중간 산출물은 삭제하지 않고 보존한다 (사후 감사·재실행)

## 검색 소스 정책

SSWL은 태양·우주환경 도메인이므로 **NASA ADS를 1순위**로 사용한다. ADS가 천체물리 저널·프리프린트·bibcode 인용그래프까지 가장 넓게 커버한다. arXiv는 직접 PDF 링크용, Semantic Scholar는 비천체물리 영역 보강용으로 보조 운용한다.

| 소스 | 우선순위 | 인증 | 용도 | 엔드포인트 |
|---|---|---|---|---|
| **NASA ADS** | 1순위 | 필수 (`ADS_API_TOKEN` Bearer) | 천체물리 저널·프리프린트·bibcode 인용그래프 | `${ADS_API_BASE}/search/query` |
| **arXiv** | 2순위 | 없음 | 프리프린트, 전문 PDF 직접 접근 | `http://export.arxiv.org/api/query` |
| **Semantic Scholar** | 3순위 | 선택 (`S2_API_KEY`) | 비천체물리 영역 보강, 광범위 인용수 | `https://api.semanticscholar.org/graph/v1/...` |

**중복 제거 키 우선순위**: `bibcode` (ADS) > `DOI` > `arXivID` > (제목+1저자 정규화). 한 논문이 여러 소스에 있으면 메타데이터를 병합:
- 인용수: ADS `citation_count` 우선 → S2 `citationCount` → 없으면 0
- bibcode: ADS 출처만 보유 (paper-mate 연계 시 유용)
- 본문 PDF: arXiv 직접 PDF 링크 우선 → S2 `openAccessPdf.url` → ADS `esources`(있으면)
- 초록: ADS 우선 (학회/저널 공식 초록), 없으면 arXiv/S2

**API 키 관리**:
- 환경변수는 `.claude/settings.local.json`의 `env` 블록에 정의 (Claude Code가 Bash 호출 시 자동 주입)
- 또는 `.env` 파일 + `source .env` 방식도 지원
- `.claude/settings.local.json.example`과 `.env.example`을 템플릿으로 둠
- **`ADS_API_TOKEN` 미설정 시**: ADS 호출을 스킵하고 arXiv + S2만으로 진행. 보고서에 "ADS 미사용" 명시.
- **`S2_API_KEY` 미설정 시**: 무인증 호출로 진행하되 rate limit (1초당 1회 안팎) 때문에 직렬화.

## 청크 분할 정책 (둘 다 폴백)

1차: **섹션 인식** — `pdftotext -layout` 후 정규식으로 헤딩(`^\d+\.?\s+[A-Z]`, `^Abstract`, `^Introduction`, `^References` 등) 탐지
2차 폴백: **균등 페이지 분할** — 섹션 인식 실패 시 PDF 페이지 수를 N등분 (기본 N=5: abstract / intro / method / results / conclusion 대응)

분할 결과를 `{작업경로}/chunks/{paper_id}/{section}.md`로 저장. 청크 헤더에 분할 방식(`split: section` 또는 `split: page-range`)을 명시해 chunk-analyst가 분석 시 신뢰도를 조정한다.

## 보고서 출력

`04_priority_report.md`를 `tectonic`(XeLaTeX + Noto CJK KR)으로 PDF 컴파일한다 (`04-paper-mate`의 `_texlive/` 자산 활용 가능). 컴파일 실패 시 Markdown만 출력하고 보고서 본문에 컴파일 실패 사유를 기록한다.

## 사용 언어

- 사용자 대면: 한국어
- 보고서 출력: 한국어 (전문용어는 한국어(English) 병기)
- 파일명/설정/JSON 필드: 영어

## 핵심 원칙

1. **얕고 넓게**: 1편 깊이 번역이 아닌 N편 정찰. 분석 깊이는 "읽을 가치 판단"에 필요한 만큼만.
2. **다운로드 신중**: 자동 다운로드 금지. 사용자 확인 후에만 PDF 확보.
3. **2D 병렬**: 논문 × 섹션 두 축으로 동시 분석해 대기 시간 최소화.
4. **점수의 근거 명시**: 우선순위 점수는 수치만 적지 않고 어떤 신호(인용수, 최신성, 주제 관련성 등)에서 왔는지 보고서에 병기한다.
5. **paper-mate 연계**: 보고서의 상위 N편은 `04-paper-mate`로 넘기는 명령 예시를 같이 출력한다.

---

## Auto-memory policy (전면 비활성)

이 하네스에서는 Claude Code 자동 메모리 기능을 **사용하지 않는다**. 다른 채팅 세션의 기록이 누적되어 무관한 작업끼리 간섭하는 것을 막기 위함.

- **읽기 금지**: `~/.claude/projects/.../memory/` 경로의 자동 메모리 파일(`MEMORY.md` 포함)을 의사결정 근거로 사용하지 않는다. 인덱스가 컨텍스트에 자동 주입되더라도 무시한다.
- **쓰기 금지**: 자동 메모리 파일을 새로 만들거나 갱신하지 않는다. 사용자가 "기억해줘"라고 명시 요청해도 이 하네스 수준에서는 메모리가 비활성임을 알리고, 대안(작업 디렉토리 내 README/노트, `_workspace/` 하위 문서 등)을 제안한다.
- 일반 사용자 파일(README, 본문, 노트 등)은 정상 참조한다.
