---
name: latex-compiler
description: >
  Markdown 논문을 LaTeX로 변환하고 PDF로 컴파일하는 스킬.
  논문 초안(.md)을 대상 저널의 LaTeX 템플릿에 맞춰 .tex 파일로 변환한다.
  LaTeX-templet/ 디렉토리의 실제 템플릿을 사용하며,
  템플릿이 없는 저널은 arXiv 형식으로 작성한다.
  키워드: LaTeX, tex, 컴파일, compile, PDF, 변환,
  논문 변환, md to tex, markdown to latex,
  AASTeX, aa.cls, mnras.cls, arXiv
---

# LaTeX-Compiler — Markdown→LaTeX 변환 및 컴파일

## 개요

논문 초안은 `.md` 형식으로 작성되지만, 최종 산출물은 저널 투고 가능한 LaTeX 파일이다.
이 스킬은 `.md` 논문을 대상 저널의 LaTeX 템플릿에 맞춰 `.tex`로 변환하고,
`pdflatex`/`bibtex`으로 컴파일하여 PDF를 생성한다.

---

## 사용 가능한 템플릿

템플릿 경로: `LaTeX-templet/`

| 저널 | 디렉토리 | 클래스 파일 | 샘플 .tex |
|---|---|---|---|
| ApJ / ApJS / ApJL | `ApJ-ApJS-ApJL/` | `aastex701.cls` | `sample701.tex` |
| A&A | `AstronomyAstrophysics/` | `macros/aa.cls` | (aa_example.zip 내) |
| MNRAS | `MNRAS/` | `mnras.cls` | `mnras_template.tex` |
| arXiv (기본) | `ArxXiV/` | `PRIMEarxiv.sty` | `templateArxiv.tex` |

**규칙: 대상 저널의 템플릿이 위 목록에 없으면 arXiv 형식으로 작성한다.**

---

## 변환 흐름

**매 리비전 라운드마다 LaTeX를 별도 디렉토리에 저장한다.**
초기 제출은 `round0`, 이후 리비전은 `round1`, `round2`, `round3`.

```
_workspace/01_paper_draft.md  (round0)
  또는 revision/round{N}_revised_paper.md  (roundN)
         │
         ▼
    [저널 확인] → 템플릿 선택
         │
         ▼
    [Markdown → LaTeX 변환]
         │
         ├── 문서 구조 변환 (# → \section 등)
         ├── Figure/Table 삽입 (\includegraphics, tabular)
         ├── 참고문헌 연결 (\bibliography)
         ├── 저널별 프리앰블 생성
         └── 메타데이터 삽입 (저자, 소속, 키워드)
         │
         ▼
    _workspace/latex/{journal_name}/round{N}/
         ├── paper.tex          (변환된 LaTeX)
         ├── references.bib     (참고문헌)
         ├── figures/            (Figure 복사)
         └── {cls/sty 파일}     (템플릿에서 복사)
         │
         ▼
    [pdflatex + bibtex 컴파일]
         │
         ▼
    _workspace/latex/{journal_name}/round{N}/paper.pdf
```

---

## Markdown → LaTeX 매핑 규칙

### 문서 구조

| Markdown | LaTeX |
|---|---|
| `# Title` | `\title{Title}` |
| `## 1. Introduction` | `\section{Introduction}` |
| `### 1.1 Background` | `\subsection{Background}` |
| `#### 1.1.1 Detail` | `\subsubsection{Detail}` |
| `## Abstract` | `\begin{abstract}...\end{abstract}` |
| `## Acknowledgments` | `\acknowledgments` (AASTeX) / `\section*{Acknowledgements}` (MNRAS) |
| `## References` | `\bibliography{references}` |

### 인라인 서식

| Markdown | LaTeX |
|---|---|
| `**bold**` | `\textbf{bold}` |
| `*italic*` | `\textit{italic}` |
| `` `code` `` | `\texttt{code}` |
| `$E = mc^2$` | `$E = mc^2$` (그대로) |
| `$$equation$$` | `\begin{equation}...\end{equation}` |

### Figure 삽입

Markdown:
```markdown
![Caption text](figures/fig1.png)
<!-- Figure 1: Detailed caption here -->
```

LaTeX (AASTeX):
```latex
\begin{figure}
\plotone{figures/fig1.png}
\caption{Detailed caption here\label{fig:fig1}}
\end{figure}
```

LaTeX (A&A / MNRAS / arXiv):
```latex
\begin{figure}
\centering
\includegraphics[width=\columnwidth]{figures/fig1.png}
\caption{Detailed caption here}
\label{fig:fig1}
\end{figure}
```

### Table 삽입

Markdown:
```markdown
| Column A | Column B | Column C |
|---|---|---|
| 1 | 2 | 3 |
<!-- Table 1: Table caption here -->
```

LaTeX:
```latex
\begin{table}
\caption{Table caption here}
\label{tab:tab1}
\begin{tabular}{lcc}
\hline
Column A & Column B & Column C \\
\hline
1 & 2 & 3 \\
\hline
\end{tabular}
\end{table}
```

### 참고문헌 인용

| Markdown | LaTeX |
|---|---|
| `(Smith et al. 2020)` | `\citep{smith2020}` |
| `Smith et al. (2020)` | `\citet{smith2020}` |
| `[REF]` | `\citep{PLACEHOLDER}` (경고 표시) |

---

## 저널별 프리앰블 생성

### ApJ / ApJS / ApJL (AASTeX v7)

```latex
\documentclass[linenumbers]{aastex701}

\newcommand{\vdag}{(v)^\dagger}

\begin{document}

\title{{TITLE}}

\correspondingauthor{{CORRESPONDING_AUTHOR}}
\email{{EMAIL}}

\author{{AUTHOR1}}
\affiliation{{AFFILIATION1}}

\author{{AUTHOR2}}
\affiliation{{AFFILIATION2}}

\begin{abstract}
{ABSTRACT}
\end{abstract}

\keywords{{KEYWORDS}}

% ... body ...

\bibliography{references}

\end{document}
```

### A&A (aa.cls)

```latex
\documentclass{aa}

\usepackage{graphicx}
\usepackage{txfonts}
\usepackage{natbib}

\begin{document}

\title{{TITLE}}

\author{{AUTHOR1}\inst{1} \and {AUTHOR2}\inst{2}}

\institute{{AFFILIATION1} \and {AFFILIATION2}}

\date{Received ; accepted }

\abstract{{ABSTRACT}}

\keywords{{KEYWORDS}}

\maketitle

% ... body ...

\bibliographystyle{aa}
\bibliography{references}

\end{document}
```

### MNRAS (mnras.cls)

```latex
\documentclass[fleqn,usenatbib]{mnras}

\usepackage{newtxtext,newtxmath}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{amsmath}

\title[Short title]{{TITLE}}

\author[{SHORT_AUTHORS}]{
{AUTHOR1},$^{1}$\thanks{E-mail: {EMAIL}}
{AUTHOR2}$^{2}$
\\
$^{1}${AFFILIATION1}\\
$^{2}${AFFILIATION2}
}

\date{Accepted XXX. Received XXX; in original form XXX}

\pubyear{\the\year}

\begin{document}
\maketitle

\begin{abstract}
{ABSTRACT}
\end{abstract}

\begin{keywords}
{KEYWORDS}
\end{keywords}

% ... body ...

\bibliographystyle{mnras}
\bibliography{references}

\end{document}
```

### arXiv (기본 폴백)

```latex
\documentclass{article}

\usepackage{PRIMEarxiv}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsfonts}
\usepackage{nicefrac}
\usepackage{microtype}
\usepackage{fancyhdr}
\usepackage{graphicx}
\graphicspath{{figures/}}

\pagestyle{fancy}
\thispagestyle{empty}
\fancyhead[LO]{{SHORT_TITLE}}

\title{{TITLE}}

\author{
  {AUTHOR1} \\
  {AFFILIATION1} \\
  \texttt{{EMAIL}} \\
}

\begin{document}
\maketitle

\begin{abstract}
{ABSTRACT}
\end{abstract}

\keywords{{KEYWORDS}}

% ... body ...

\bibliographystyle{unsrt}
\bibliography{references}

\end{document}
```

---

## 컴파일 절차

### Step 1: 파일 준비

```bash
# 라운드별 작업 디렉토리 생성
mkdir -p _workspace/latex/{journal_name}/round{N}/figures

# 템플릿 파일 복사
cp LaTeX-templet/{template_dir}/*.{cls,sty,bst} _workspace/latex/{journal_name}/round{N}/

# Figure 복사
cp _workspace/figures/* _workspace/latex/{journal_name}/round{N}/figures/
```

### Step 2: 변환 실행

1. `.md` 파일 파싱
2. 저널별 프리앰블 생성
3. 섹션, Figure, Table, 참고문헌 변환
4. `paper.tex` 출력
5. `references.bib` 생성/복사

### Step 3: PDF 컴파일

```bash
cd _workspace/latex/{journal_name}/round{N}/
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

3회 실행하는 이유: 참고문헌 번호, 교차 참조(Figure/Table 번호)가 올바르게 해결되도록.

### Step 4: 결과 확인

- `paper.pdf` 생성 확인
- 컴파일 경고/에러 로그 검토
- 미해결 참조(`??`) 확인

---

## 저널-템플릿 매핑 테이블

| 대상 저널 | 사용 템플릿 | 비고 |
|---|---|---|
| ApJ | `ApJ-ApJS-ApJL/` | AASTeX v7 |
| ApJL | `ApJ-ApJS-ApJL/` | AASTeX v7, letter 옵션 |
| ApJS | `ApJ-ApJS-ApJL/` | AASTeX v7 |
| A&A | `AstronomyAstrophysics/` | aa.cls |
| MNRAS | `MNRAS/` | mnras.cls |
| Solar Physics | `ArxXiV/` | Springer 템플릿 미보유 → arXiv 폴백 |
| Space Weather | `ArxXiV/` | AGU 템플릿 미보유 → arXiv 폴백 |
| JSWSC | `ArxXiV/` | 템플릿 미보유 → arXiv 폴백 |
| JGR-SP | `ArxXiV/` | 템플릿 미보유 → arXiv 폴백 |
| 기타 | `ArxXiV/` | 기본 폴백 |

---

## 에러 핸들링

| 에러 | 대응 |
|---|---|
| `pdflatex` 미설치 | 사용자에게 TeX Live/MiKTeX 설치 안내 |
| 컴파일 에러 | 에러 로그 분석, 문제 줄 수정 후 재컴파일 |
| 미해결 참조 (`??`) | BibTeX 키 확인, 누락된 라벨 추가 |
| Figure 파일 미발견 | 경로 확인, 누락 Figure 목록 보고 |
| 인코딩 에러 | UTF-8 확인, 특수문자 이스케이프 처리 |
| 템플릿 cls 파일 누락 | `LaTeX-templet/`에서 재복사 |

---

## 출력 디렉토리 구조

**매 라운드마다 독립된 디렉토리에 저장하여 리비전 이력을 완전 보존한다.**

```
_workspace/latex/{journal_name}/
├── round0/                    # 초기 제출 (01_paper_draft.md 기반)
│   ├── paper.tex
│   ├── paper.pdf
│   ├── paper.aux
│   ├── paper.bbl
│   ├── paper.log
│   ├── references.bib
│   ├── figures/
│   └── {cls/sty/bst}
├── round1/                    # 1차 리비전 (round1_revised_paper.md 기반)
│   ├── paper.tex
│   ├── paper.pdf
│   ├── ...
├── round2/                    # 2차 리비전
│   └── ...
└── round3/                    # 3차 리비전 (최종)
    └── ...
```

### 라운드-소스 매핑

| 라운드 | 소스 .md 파일 | LaTeX 출력 경로 |
|---|---|---|
| round0 | `_workspace/01_paper_draft.md` | `latex/{journal}/round0/paper.tex` |
| round1 | `_workspace/revision/round1_revised_paper.md` | `latex/{journal}/round1/paper.tex` |
| round2 | `_workspace/revision/round2_revised_paper.md` | `latex/{journal}/round2/paper.tex` |
| round3 | `_workspace/revision/round3_revised_paper.md` | `latex/{journal}/round3/paper.tex` |
