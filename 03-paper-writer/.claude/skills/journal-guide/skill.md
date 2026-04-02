---
name: journal-guide
description: >
  저널 선택 및 투고 가이드 스킬.
  연구 분야와 결과에 맞는 저널을 추천하고, 저널별 형식 요구사항을 안내한다.
  researcher가 저널을 선정할 때, 또는 사용자가 저널 추천을 요청할 때 사용한다.
  키워드: 저널 추천, 어디에 투고, journal selection,
  ApJ, A&A, Solar Physics, JSWSC, Nature Astronomy,
  투고 가이드, submission guide, 저널 비교, impact factor
---

# Journal-Guide — 저널 선택 및 투고 가이드

## 개요

태양물리학 및 우주환경 분야의 주요 저널 정보를 제공하고,
연구 주제와 결과 수준에 맞는 저널을 추천한다.

---

## 주요 저널 정보

### Tier 1: 고영향력 저널

| 저널 | 약칭 | 분야 | 특징 |
|---|---|---|---|
| Nature Astronomy | Nat. Astron. | 전 천문학 | 매우 높은 영향력, 혁신적 발견 필수 |
| The Astrophysical Journal | ApJ | 천체물리 전반 | 태양물리 주력 저널, AAS 발행 |
| The Astrophysical Journal Letters | ApJL | 천체물리 전반 | 빠른 출판, 중요 발견 속보 |
| The Astrophysical Journal Supplement | ApJS | 천체물리 전반 | 대규모 데이터셋/카탈로그/방법론 |

### Tier 2: 전문 저널

| 저널 | 약칭 | 분야 | 특징 |
|---|---|---|---|
| Astronomy & Astrophysics | A&A | 천문학 전반 | 유럽 중심, 태양물리 활발 |
| Solar Physics | Sol. Phys. | 태양물리 전문 | 태양물리 전문 저널, 관측/이론/모델 |
| Space Weather | SW | 우주기상 | AGU 발행, 예보/모델/영향 |
| Journal of Space Weather and Space Climate | JSWSC | 우주기상/기후 | EDP Sciences, 유럽 우주기상 |

### Tier 3: 관련 저널

| 저널 | 약칭 | 분야 | 특징 |
|---|---|---|---|
| Monthly Notices of the Royal Astronomical Society | MNRAS | 천문학 전반 | 영국 중심 |
| Journal of Geophysical Research: Space Physics | JGR-SP | 지구물리/우주 | AGU 발행, 자기권/전리층 |
| Advances in Space Research | ASR | 우주연구 전반 | COSPAR, 넓은 범위 |
| Earth, Planets and Space | EPS | 지구/행성/우주 | 일본 중심, 오픈 액세스 |

---

## 저널 선택 기준

### 연구 유형별 추천

| 연구 유형 | 추천 저널 |
|---|---|
| 태양 관측 분석 (AIA, HMI, EUI) | ApJ, A&A, Sol. Phys. |
| 태양 플레어/CME 물리 | ApJ, A&A, Sol. Phys. |
| 우주기상 예보 모델 | SW, JSWSC |
| ML 기반 태양 예측 | ApJ, SW, Sol. Phys. |
| 대규모 데이터 파이프라인 | ApJS |
| 혁신적 발견/새로운 현상 | ApJL, Nat. Astron. |
| 자기권/전리층 영향 | JGR-SP, SW |
| 방법론/알고리즘 | ApJS, Sol. Phys. |

### 결과 수준별 추천

| 수준 | 추천 저널 |
|---|---|
| 분야를 바꿀 만한 발견 | Nat. Astron., ApJL |
| 중요한 새 결과 | ApJ, A&A |
| 견실한 분석/방법론 | Sol. Phys., SW, JSWSC |
| 데이터셋/카탈로그 | ApJS, ASR |

---

## 저널별 형식 요구사항

### ApJ / ApJL / ApJS (AAS Journals)

```
- 형식: AASTeX (LaTeX)
- Abstract: 250단어 이내
- Figure: EPS/PDF (300 DPI 이상)
- 참고문헌: BibTeX (aasjournal.bst)
- 키워드: UAT (Unified Astronomy Thesaurus) 기반
- 특이사항: Data Availability Statement 필수
```

### A&A

```
- 형식: aa.cls (LaTeX)
- Abstract: 구조화 (Context, Aims, Methods, Results, Conclusions)
- Figure: EPS/PDF (300 DPI 이상)
- 참고문헌: BibTeX (aa.bst)
- 특이사항: Language editing 서비스 제공
```

### Solar Physics

```
- 형식: Springer LaTeX template
- Abstract: 150-250단어
- Figure: TIFF/EPS/PDF (300 DPI 이상)
- 참고문헌: Springer Basic style
- 특이사항: Online-only color figure 가능
```

### Space Weather (AGU)

```
- 형식: AGU LaTeX template 또는 Word
- Abstract: 150단어 이내
- Figure: TIFF/EPS (300 DPI 이상)
- 참고문헌: AGU style
- 특이사항: Key Points 3개 필수 (≤140자)
```

---

## LaTeX 템플릿 매핑

`LaTeX-templet/` 디렉토리에 보유한 템플릿과 저널의 매핑.
**템플릿이 없는 저널은 arXiv 형식(폴백)으로 작성한다.**

| 저널 | 보유 템플릿 | 디렉토리 | 클래스/스타일 |
|---|---|---|---|
| ApJ | O | `ApJ-ApJS-ApJL/` | `aastex701.cls` |
| ApJL | O | `ApJ-ApJS-ApJL/` | `aastex701.cls` |
| ApJS | O | `ApJ-ApJS-ApJL/` | `aastex701.cls` |
| A&A | O | `AstronomyAstrophysics/` | `aa.cls` |
| MNRAS | O | `MNRAS/` | `mnras.cls` |
| Solar Physics | X → arXiv 폴백 | `ArxXiV/` | `PRIMEarxiv.sty` |
| Space Weather | X → arXiv 폴백 | `ArxXiV/` | `PRIMEarxiv.sty` |
| JSWSC | X → arXiv 폴백 | `ArxXiV/` | `PRIMEarxiv.sty` |
| JGR-SP | X → arXiv 폴백 | `ArxXiV/` | `PRIMEarxiv.sty` |
| 기타 | X → arXiv 폴백 | `ArxXiV/` | `PRIMEarxiv.sty` |

---

## 사용 방법

researcher가 저널을 선정할 때:
1. 논문 키워드와 결과 수준을 분석
2. 위 기준에 따라 3개 후보 제안
3. 각 후보의 장단점 비교
4. **LaTeX 템플릿 보유 여부 안내** (보유 시 해당 템플릿, 미보유 시 arXiv 폴백 설명)
5. 사용자 선택 후 해당 저널 형식으로 논문 작성
