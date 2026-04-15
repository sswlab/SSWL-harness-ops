# 08-DEM-calc — DEM 계산 하네스

6개 파장(SDO/AIA 94, 131, 171, 193, 211, 335 Å) 이미지와 온도 응답 함수를 입력받아
DEM(Differential Emission Measure) 맵을 계산하고 시각화하는 자동화 파이프라인.

## 지원 역산 방법

| 방법 | 알고리즘 | 참고 문헌 | 적합한 용도 |
|---|---|---|---|
| **DEMreg** | GSVD + Tikhonov 정규화 | Hannah & Kontar (2013) | 소규모 영역 정밀 분석 |
| **SITES** | 반복적 가중 역산 + Grid 가속 | Morgan (2019), Pickering & Morgan (2019) | 대규모 이미지, 빠른 처리 |

## 파이프라인

```
6채널 이미지 + 응답 함수
    │
    ▼
data-validator  →  dem-calculator  →  result-visualizer  →  quality-reviewer
(데이터 검증)     (DEM 역산)         (시각화)              (PASS/REVISE)
```

## 필수 입력

| 항목 | 설명 |
|---|---|
| 6채널 이미지 | FITS 또는 NumPy 배열 (ny, nx, 6) |
| 응답 함수 | 온도 응답 함수 (nt, 6) 또는 aiapy 자동 생성 |
| 역산 방법 | DEMreg / SITES / 양쪽 비교 |
| 온도 범위 | 기본: log T = 5.6–7.0 |

## 출력

| 파일 | 설명 |
|---|---|
| `results/dem.npy` | DEM 맵 (ny, nx, nt) |
| `results/edem.npy` | DEM 에러 |
| `results/chisq.npy` | Chi-squared 맵 |
| `figures/dem_summary.png` | DEM 요약 멀티 패널 |
| `reports/03_quality_report.md` | 품질 보고서 |

## 핵심 코드 (하네스 내 번들)

```
core/
├── __init__.py
├── demreg/           # DEMreg (Hannah & Kontar 2013)
│   ├── __init__.py
│   ├── dn2dem_pos.py       # 진입점
│   ├── demmap_pos.py       # 맵 처리 + 병렬화
│   ├── dem_inv_gsvd.py     # GSVD 분해
│   └── dem_reg_map.py      # 정규화 파라미터
└── sites/            # SITES (Morgan 2019)
    ├── __init__.py
    ├── dem_sites.py         # 단일 픽셀 SITES
    ├── dem_gridsites.py     # Grid-SITES 다중 픽셀
    ├── dem_aiainterpolresponse_sites.py  # AIA 응답 보간
    ├── dem_openaiafiles_sites.py         # AIA 파일 읽기
    └── robust_min.py        # 유틸리티
```

원본: `/home/youn_j/99_server/SOTA/05_DEM/`

## 사용법

이 하네스 디렉토리에서 Claude Code를 실행하고 DEM 계산을 요청하세요:

```
DEM 계산해줘
- 데이터: /path/to/aia_fits/
- 방법: DEMreg
- 작업 경로: /path/to/output/
```
