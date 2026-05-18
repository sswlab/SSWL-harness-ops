# 10-Paper-Finder — 논문 탐색·스캔·우선순위화 하네스

> 주제를 던지면 관련 논문을 찾아 모으고, 병렬로 빠르게 스캔한 뒤, 읽어야 할 순서를 정해주는 AI 하네스.

## 개요

Paper Finder는 `04-paper-mate`(1편 깊이 분석)와 짝을 이루는 **얕고 넓은 정찰(reconnaissance)** 하네스다.
사용자가 연구 주제를 제시하면:

1. **검색 전략 수립** → 키워드/연도/저자/필터 분해
2. **다중 소스 병렬 검색** → NASA ADS (1순위, 천체물리 핵심) + arXiv + Semantic Scholar (메타데이터 우선, PDF는 선택적)
3. **2D 병렬 분석** → 후보 논문 × 섹션을 동시에 청크 분석
4. **논문별 요약 카드** → Synthesizer가 청크 결과를 1논문 1카드로 통합
5. **우선순위 보고서** → 관련성·인용수·최신성·핵심도로 점수, 읽는 순서 제안 (Markdown + PDF)

논문 하나를 끝까지 번역해야 한다면 `04-paper-mate`로 넘긴다. Paper Finder의 목표는 **"무엇을 어떤 순서로 읽을지 정한다"** 까지다.

## 사용 방법

### 1. 하네스 디렉토리에서 Claude Code 실행

```bash
cd /home/youn_j/SSWL-HARNESS-MAIN/SSWL-harness-ops/10-paper-finder
claude
```

### 2. 주제 제공

```
# 자유 텍스트
태양 코로나의 가열 메커니즘 관련 최근 5년 논문 찾아줘

# 슬래시 명령
/paper-find solar coronal heating mechanism, 2020-2025, top 15
```

### 3. 다운로드 결정 (매번 묻기)

검색 결과 목록이 뜨면 다운로드 정책을 매번 확인한다:

- `all` — 모든 후보 PDF 다운로드
- `top N` — 상위 N편만 다운로드
- `none` — 메타데이터+초록만으로 분석
- `pick #3 #5 #7` — 번호로 선택

### 4. 결과물 확인

작업 경로 (기본 `_workspace/`) 하위:

| 파일 | 내용 |
|------|------|
| `00_query_plan.md` | 검색 전략 (키워드, 필터, 소스별 쿼리) |
| `01_search_results.md` | 다중 소스 통합 검색 결과 (중복 제거 + 메타데이터) |
| `papers/` | 다운로드된 PDF 원본 (선택적) |
| `chunks/{paper_id}/` | 논문별 섹션 청크 (`abstract.md`, `intro.md`, ...) |
| `02_chunk_analyses/{paper_id}/{section}.md` | 청크별 분석 노트 |
| `03_paper_cards/{paper_id}.md` | 논문 1편 요약 카드 |
| `04_priority_report.md` | 우선순위 보고서 (Markdown) |
| `04_priority_report.pdf` | 우선순위 보고서 (한글 PDF) |

## 에이전트 구성

| 에이전트 | 역할 |
|---|---|
| **query-planner** | 사용자 주제를 검색 키워드/필터/연도 범위로 분해, 소스별 쿼리 작성 |
| **paper-hunter** | arXiv + Semantic Scholar 병렬 검색, 중복 제거, 메타데이터 수집, PDF 다운로드 |
| **chunk-analyst** | PDF를 섹션 단위로 쪼개 병렬 분석 (논문 × 섹션 2D 팬아웃) |
| **synthesizer** | 청크 분석을 합쳐 논문별 1장 요약 카드 생성 |
| **prioritizer** | 관련성·인용·최신성·핵심도 점수화, 읽는 순서 제안, 보고서 컴파일 |

## 외부 의존성

- **NASA ADS API** — Bearer 토큰 필수 (`ADS_API_TOKEN`). [토큰 발급](https://ui.adsabs.harvard.edu/user/settings/token). 천체물리 도메인 1순위 소스.
- **arXiv API** — 인증 불필요
- **Semantic Scholar API** — 무인증 호출 가능 (rate limit 낮음), API 키 제공 시 (`S2_API_KEY`) rate limit 완화
- **시스템 도구**: `curl`, `pdftotext`, `pdfinfo` (poppler-utils), `pdftoppm` (이미지 미리보기용), `tectonic` (한글 PDF 컴파일)

## API 키 저장

이 서버에서만 작동하도록 키를 저장하려면 (저장소 따라가지 않게):

**권장 경로**: `~/.claude/settings.json` (이 사용자, 이 머신에만 적용)

```json
{
  "env": {
    "ADS_API_TOKEN": "여기에-토큰",
    "S2_API_KEY": "여기에-키",
    "ADS_API_BASE": "https://api.adsabs.harvard.edu/v1"
  }
}
```

Claude Code가 Bash 호출 시 이 `env`를 자동 주입한다. 사용자 홈에 있으므로 하네스를 다른 서버로 복사해도 키는 따라가지 않는다. 다른 경로 옵션은 `.claude/settings.local.json.example`, `.env.example` 참고.

## 04-paper-mate 와의 차이

| 항목 | 04-paper-mate | 10-paper-finder |
|---|---|---|
| 대상 | 사용자가 지정한 **1편** | 주제 관련 **N편** 후보 |
| 분석 깊이 | 완전 번역 + 모든 그림 | 섹션 핵심만 추출 |
| 산출물 | 한국어 전문 PDF | 우선순위 보고서 (읽기 가이드) |
| 다음 단계 | 끝 | 상위 논문을 paper-mate로 넘기기 |

## 디렉토리 구조

```
10-paper-finder/
├── .claude/
│   ├── CLAUDE.md
│   ├── agents/   (5개)
│   └── skills/
│       └── paper-find/
│           ├── skill.md
│           └── scripts/
├── _workspace/   (빈 스캐폴드)
├── harness.json
└── README.md
```
