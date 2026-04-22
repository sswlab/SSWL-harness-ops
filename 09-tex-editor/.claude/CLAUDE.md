# 09-TeX-Editor — LaTeX 원고 컴파일·검토·수정 하네스

사용자가 제공한 LaTeX 원고(`.tex` + 보조 파일)를 입력으로 받아,
**컴파일 → 시각·문법 검토 → 수정된 `.tex` 출력**을 수행한다.

GPT Prism 같은 AI LaTeX 편집기를 로컬 에이전트 팀으로 구현한 형태.

> **범위**: 컴파일 에러 수정 + 시각적 레이아웃 문제 + 영문 문법/오타. 내용 리뷰·팩트체크·구조 개선은 `06-paper-editor`의 영역.

## 에이전트 팀 구성표

| 에이전트 | 역할 |
|---|---|
| **latex-compiler** | `latexmk`로 컴파일, 로그 파싱(에러·경고·미해결 참조·missing figure 등), `pdftoppm`으로 페이지 PNG 렌더링 |
| **visual-inspector** | 렌더된 PNG를 **직접 보고** 시각 문제 탐지: 표 잘림, 그림 마진 벗어남, 캡션 분리, 페이지 경계 이상, 수식 줄바꿈 깨짐, 과도한 여백 |
| **grammar-checker** | 영문 문법 오류 및 오탈자만 검토. 과학적 내용은 건드리지 않음 |
| **tex-editor** | 위 3개 리포트를 받아 수정된 `.tex` 생성. 컴파일 에러 해소를 최우선으로 하며, 시각 문제와 문법 교정을 반영 |

## 실행 모드: 에이전트 팀 (파이프라인 + 팬아웃)

```
사용자 입력: 루트 .tex 경로 + 작업경로
    │
    ▼
[오케스트레이터] source/ 복사, 디렉토리 구조 준비
    │
    ▼
[latex-compiler] 컴파일 → PDF + log + PNG 렌더
    │
    ├──▶ [visual-inspector]  (병렬)
    └──▶ [grammar-checker]   (병렬)
    │
    ▼
[tex-editor] 3개 리포트 통합 → revised.tex 생성
    │
    ▼
[latex-compiler] revised.tex 재컴파일 (검증용 1회)
    │
    ▼
사용자에게 최종 보고 (수정본 경로 + 변경 요약)
```

**중요: 자동 재실행 루프 없음.** 재컴파일은 "수정본이 컴파일되는지" 확인 목적의 1회만. 추가 개선이 필요하면 사용자가 revised.tex를 입력으로 하여 재호출한다.

## 입력 수집

1. 루트 `.tex` 파일 경로 (필수)
2. 작업 경로 (필수) — 없으면 `{tex_dir}/_tex-editor/` 제안
3. 사용자가 쿼리에서 경로를 이미 제공한 경우 질문 건너뜀

## 디렉토리 준비

오케스트레이터가 파이프라인 시작 시 수행:

```bash
mkdir -p {작업경로}/{source,build,pages,reports}
cp -r {루트tex_dir}/* {작업경로}/source/
```

이후 모든 컴파일은 `{작업경로}/source/` 안에서 수행하며, 출력은 `{작업경로}/build/`로 나가게 한다.

## 데이터 전달 규칙

| 에이전트 | 입력 | 출력 |
|---|---|---|
| latex-compiler | `{작업경로}/source/{root}.tex` | `{작업경로}/build/`, `{작업경로}/pages/`, `{작업경로}/reports/compile.md` |
| visual-inspector | `{작업경로}/pages/*.png`, `{작업경로}/reports/compile.md` | `{작업경로}/reports/visual.md` |
| grammar-checker | `{작업경로}/source/*.tex` | `{작업경로}/reports/grammar.md` |
| tex-editor | `{작업경로}/source/`, `reports/compile.md`, `reports/visual.md`, `reports/grammar.md` | `{작업경로}/revised.tex` (+ 필요 시 보조 .tex) |

**전달 규칙:**
1. 각 에이전트는 자신의 지정 파일에만 쓴다
2. 다른 에이전트의 출력은 읽기 전용으로 참조한다
3. 모든 중간 산출물(`build/`, `pages/`, `reports/`)은 삭제하지 않고 보존한다
4. `{작업경로}/editorial-log.md`에 모든 에이전트가 진행 상황을 누적 기록한다

## 작업 공간 구조

```
{작업경로}/
├── source/           # 원본 복사본 (작업 대상)
├── build/            # .aux, .log, .pdf 등
├── pages/            # page-001.png, page-002.png, ...
├── reports/
│   ├── compile.md    # 컴파일 에러·경고
│   ├── visual.md     # 시각 문제
│   └── grammar.md    # 문법·오타
├── revised.tex       # 최종 수정본 (+ 보조 .tex 파일이 있다면 함께)
└── editorial-log.md
```

## 기술 스택

| 범주 | 도구 |
|---|---|
| 컴파일 | `latexmk -pdf` (pdflatex 기반) |
| 페이지 렌더링 | `pdftoppm -png -r 150` |
| 로그 파싱 | 정규식 기반 (에러/경고/overfull 등 패턴 매칭) |
| 시각 판독 | Claude의 이미지 Read 기능 (PNG 직접 관찰) |
| 언어 | Python 3.10+ (필요 시 헬퍼 스크립트) |

## 사용 언어

- 사용자 대면: 한국어
- 리포트: 논문 언어에 맞춤 (영어 논문이면 영어)
- 수정본 `.tex`: 원본 언어 그대로

## 핵심 원칙

1. **원본 비파괴**: 입력 디렉토리는 읽기 전용. `source/`에 복사해 작업한다
2. **1회 실행 후 사용자 보고**: 자동 재컴파일·재편집 루프 없음. 재컴파일은 "수정본이 통과하는지" 검증 1회만
3. **컴파일 에러 최우선**: 에러가 있으면 `revised.tex`의 첫 목표는 컴파일 통과. 그 위에서 시각/문법 수정을 얹는다
4. **시각 문제는 실제로 본다**: 로그 경고(overfull hbox)만 의존하지 않고 `pages/*.png`를 직접 관찰해 판단
5. **보수적 문법 교정**: 명백한 문법 오류와 오타만 수정. 저자 문체 존중. 과학적 내용은 손대지 않음
6. **변경 추적**: 모든 수정은 리포트에 `원문 → 수정` 형식으로 기록

## 에러 핸들링

| 상황 | 대응 |
|---|---|
| 컴파일 자체가 실패 (pdflatex 반환 코드 ≠ 0) | PDF/PNG 없이 진행. visual-inspector 건너뛰고 tex-editor가 컴파일 에러 해소에만 집중 |
| 루트 `.tex` 추정 실패 (여러 파일 중) | 사용자에게 되물음 |
| 보조 파일 누락 (graphicspath, \input) | compile.md에 명시, tex-editor는 경로 문제인지 파일 부재인지 구분해 보고 |
| 페이지 수 과다 (>50) | 전 페이지 렌더 후 visual-inspector가 섹션별로 샘플링 + 전수 스캔 혼합 |

## 테스트 시나리오

**정상 흐름:**
1. 사용자: "이 tex 편집해줘: ~/papers/test/main.tex"
2. 오케스트레이터: 작업경로 질문 → `~/papers/test/_tex-editor/` 제안
3. source/ 복사, latex-compiler 실행 → 컴파일 성공, 12페이지 PNG
4. visual-inspector + grammar-checker 병렬 실행
5. tex-editor가 revised.tex 생성
6. latex-compiler 재실행으로 revised.tex 컴파일 검증
7. 사용자에게 변경 요약 + `revised.tex` 경로 보고

**에러 흐름:**
1. 컴파일 에러 (\end{document} 누락) → latex-compiler가 로그 파싱 후 compile.md에 에러 위치 기록
2. visual-inspector 건너뜀 (PDF 없음)
3. grammar-checker는 정상 진행
4. tex-editor가 컴파일 에러 + 문법 수정을 반영한 revised.tex 생성
5. 재컴파일 시도 → 성공 또는 여전히 실패. 실패 시 사용자에게 남은 이슈 명시하여 보고
