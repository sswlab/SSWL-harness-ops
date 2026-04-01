---
name: paper-draft
description: >
  학술 논문 작성 워크플로우 및 저널 스타일 가이드.
  논문 구조, Figure/Table 선별, 인용 규칙, ApJ/A&A/Solar Physics
  저널 스타일을 정의한다. paper-writer 에이전트가 참조한다.
  키워드: 논문, paper, draft, 작성, 초안, 원고,
  abstract, introduction, results, discussion,
  ApJ, A&A, Solar Physics, BibTeX, 인용,
  Figure, Table, 투고, 저널, 학술지
---

# Paper-Draft — 논문 작성 워크플로우

## 개요

연구 결과를 학술 논문으로 작성하기 위한 구조, 규칙, 저널별 스타일을 정의한다. paper-writer 에이전트가 이 스킬을 참조하여 일관된 품질의 논문 초안을 생성한다.

---

## 논문 구조

### 표준 태양물리 논문 구조

```
1. Abstract           (150~250 단어)
2. Introduction       (배경, 선행연구, 동기, 기여점)
3. Data and Methods   (데이터, 분석 방법, 실험 설계)
4. Results            (핵심 결과, Figure/Table 참조)
5. Discussion         (해석, 선행연구 비교, 한계, 향후 연구)
6. Conclusions        (핵심 결론 3~5문장)
7. Acknowledgments    (데이터 기관, 연구비)
8. References         (BibTeX 기반)
```

### 섹션별 작성 가이드

#### Abstract
- 4-문장 구조: 배경(1) → 목적(1) → 방법+결과(1~2) → 결론(1)
- 구체적 수치 포함 (예: "accuracy improved from 72% to 85%")
- 약어 사용 금지 (첫 사용 시 풀어쓰기)

#### Introduction
- 넓은 배경 → 좁은 문제 → 우리 기여 (깔때기 구조)
- 선행연구 인용은 `01_literature_review.md`를 참조
- 마지막 단락: "In this paper, we ..." 로 기여점 명시

#### Data and Methods
- 재현 가능하도록 상세히: 데이터 소스, 기간, 해상도, 전처리 단계
- 수식은 LaTeX 형식으로 번호 부여
- 소프트웨어 인용: sunpy (SunPy Community et al. 2020), astropy (Astropy Collaboration et al. 2022)

#### Results
- Figure/Table을 중심으로 서술
- 모든 Figure/Table은 본문에서 명시적으로 참조
- 객관적 서술: "Figure 1 shows that..." (과장 없이)

#### Discussion
- Results에서 제시한 사실의 **해석**
- 선행연구와 비교: 일치/불일치 및 이유
- 한계점: 솔직하게 (데이터 범위, 방법론 한계)
- 향후 연구: 구체적 방향 제시

#### Conclusions
- 3~5 문장으로 핵심 결론
- 새로운 내용 추가 금지 (Results/Discussion의 요약만)

---

## Figure/Table 선별 기준

### 총 5개 제한 (Figure + Table 합계)

#### 우선순위

| 순위 | 유형 | 설명 | 예시 |
|---|---|---|---|
| 1 | **핵심 결과** | 가설을 지지/반박하는 주 결과 | Baseline vs Experiment 비교 |
| 2 | **정량 비교** | 정량적 메트릭 비교 Table | 성능 지표 비교표 |
| 3 | **데이터 개요** | 입력 데이터 특성 | 시계열, 분포 |
| 4 | **방법론 설명** | 분석 과정 시각화 | 워크플로우, 중간 결과 |
| 5 | **부가 분석** | 파라미터 민감도 등 | Appendix 후보 |

#### 선별 원칙
- "이 Figure/Table 없이 논문이 성립하는가?" → Yes면 제외 후보
- 유사한 정보를 담은 Figure는 하나로 합치거나 선택
- 복잡한 Figure는 서브패널(a, b, c)로 구성하여 1개로 통합

---

## 인용 규칙

### BibTeX 형식

```bibtex
@article{author2024keyword,
    author = {Author, First and Author, Second},
    title = {Paper Title},
    journal = {The Astrophysical Journal},
    year = {2024},
    volume = {XXX},
    pages = {YYY},
    doi = {10.xxxx/xxxxx}
}
```

### BibTeX 키 네이밍

`{1저자성}_{연도}_{키워드}` (예: `chen_2024_flare_prediction`)

### NASA ADS 인용

- ADS bibcode 형식: `2024ApJ...XXX..YYYA`
- `references.bib`에서 관리, 본문에서 `\cite{key}` 참조
- 본문 인용 형식: "Author et al. (2024)" 또는 "(Author et al. 2024)"

### 필수 인용 대상

1. 사용한 데이터의 미션/기기 논문
2. 핵심 방법론의 원본 논문
3. 비교 대상 선행연구
4. 주요 소프트웨어 (sunpy, astropy 등)

---

## 저널 스타일

### The Astrophysical Journal (ApJ)

| 항목 | 규칙 |
|---|---|
| 스타일 | AASTeX v6.3.1 |
| 참고문헌 | `\bibliography{references}` |
| Figure | EPS/PDF/PNG (DPI≥300) |
| 페이지 제한 | 없음 (Letters는 4페이지) |
| 인용 | `\citet{key}`, `\citep{key}` |

### Astronomy & Astrophysics (A&A)

| 항목 | 규칙 |
|---|---|
| 스타일 | `aa.cls` |
| 참고문헌 | `\bibliographystyle{aa}` |
| Figure | EPS/PDF/PNG |
| 인용 | `\citet{key}`, `\citep{key}` |

### Solar Physics

| 항목 | 규칙 |
|---|---|
| 스타일 | Springer `solarphysics.cls` |
| 참고문헌 | `\bibliographystyle{spr-mp-sola}` |
| Figure | EPS/PDF/TIFF (DPI≥300) |
| 인용 | Author (Year) / (Author Year) |

---

## 작성 체크리스트

논문 초안 완료 후 자체 점검:

- [ ] Abstract에 구체적 수치가 포함되어 있는가
- [ ] Introduction에서 연구 갭이 명확히 제시되었는가
- [ ] Data/Methods에서 재현에 충분한 정보가 있는가
- [ ] 모든 Figure/Table이 본문에서 참조되었는가
- [ ] Figure + Table 합계가 5개 이내인가
- [ ] 결과를 과장 없이 객관적으로 서술했는가
- [ ] Discussion에 한계점이 솔직히 기술되었는가
- [ ] Conclusions에 새로운 내용이 없는가
- [ ] 모든 인용이 `references.bib`에 존재하는가
- [ ] 소프트웨어 인용이 포함되었는가 (sunpy, astropy 등)
