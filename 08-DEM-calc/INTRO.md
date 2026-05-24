👋 **DEM 계산기 하네스**에 오신 걸 환영합니다.

SDO/AIA 6채널 이미지(94·131·171·193·211·335 Å)와 온도 응답 함수를 입력하면, **데이터 검증 → DEM 역산 → 시각화 → 품질 검토**까지 수행합니다.

---

### 📋 입력 항목

| 항목 | 설명 | 예시 |
|---|---|---|
| **① 6채널 이미지** | FITS 디렉토리 또는 NumPy `(ny, nx, 6)` | `/home/youn_j/data/aia_fits/` |
| **② 응답 함수** *(선택)* | `(nt, 6)`. 미제공 시 `aiapy`로 자동 생성 | 자동 |
| **③ 역산 방법** | `DEMreg` / `SITES` / `양쪽 비교` | `DEMreg` |
| **④ 온도 범위** *(선택)* | logT 범위 | `5.6–7.0` *(기본)* |
| **⑤ 작업 경로** | 결과 저장 디렉토리 | `/home/youn_j/dem-output/` |

### 🔬 역산 방법 선택 가이드

| 방법 | 알고리즘 | 적합한 용도 |
|---|---|---|
| **DEMreg** | GSVD + Tikhonov 정규화 (Hannah & Kontar 2013) | 소규모 영역 정밀 분석 |
| **SITES** | 반복적 가중 역산 + Grid 가속 (Morgan 2019) | 대규모 이미지, 빠른 처리 |
| **양쪽 비교** | 두 방법 동시 실행, 결과 비교 | 방법 검증, 논문 작성용 |

---

### 💬 그대로 복사해서 쓸 수 있는 프롬프트 템플릿

```
DEM 계산해줘.

데이터: [/AIA/FITS/경로]
방법: [DEMreg / SITES / 양쪽 비교]
작업 경로: [/저장/경로]
```

#### 실제 예시

```
DEM 계산해줘.

데이터: /home/youn_j/data/aia_20240514/
방법: DEMreg
작업 경로: /home/youn_j/dem-results/20240514/
```

---

### 📦 결과물

| 파일 | 설명 |
|---|---|
| `results/dem.npy` | DEM 맵 `(ny, nx, nt)` |
| `results/edem.npy` | DEM 에러 |
| `results/chisq.npy` | Chi-squared 맵 |
| `figures/dem_summary.png` | DEM 요약 멀티 패널 |
| `reports/03_quality_report.md` | 품질 보고서 (PASS/REVISE) |

준비되시면 위 템플릿대로 입력해 주세요. 🚀
