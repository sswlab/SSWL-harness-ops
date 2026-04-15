# 08-DEM-calc — DEM(Differential Emission Measure) 계산 하네스

6개 파장(예: SDO/AIA 94, 131, 171, 193, 211, 335 Å)의 이미지와
해당 온도 응답 함수(temperature response function)를 입력받아
DEM 맵을 계산하고 시각화하는 자동화 파이프라인.

## 프로젝트 개요

태양 코로나의 열적 구조를 이해하기 위해 다파장 EUV 관측 데이터로부터
DEM(Differential Emission Measure)을 역산(inversion)한다.
사용자가 6개 파장 데이터와 응답 함수를 `_workspace`에 제공하면,
에이전트 팀이 데이터 검증 → DEM 역산 → 시각화 → 품질 검토까지 수행한다.

**지원 기기:**
- **SDO/AIA**: 94, 131, 171, 193, 211, 335 Å
- **Solar Orbiter/EUI**: 94, 131, **174**, 193, 211, 335 Å (FSI 174가 AIA 171 대체)
- 파일명에서 파장 자동 감지 → AIA/EUI 자동 판별 → 해당 응답 함수 자동 선택

**지원 역산 방법:**
- **DEMreg**: 정규화 기반 GSVD 역산 (Hannah & Kontar 2013)
- **SITES**: 반복적 가중 역산 + 그리드 가속 (Morgan 2019, Pickering & Morgan 2019)

**핵심 코드 위치:** 하네스 내 `core/` 디렉토리에 번들
- DEMreg: `core/demreg/` (원본: `/home/youn_j/99_server/SOTA/05_DEM/demregpy_core/`)
- SITES: `core/sites/` (원본: `/home/youn_j/99_server/SOTA/05_DEM/dem_sites/converted/`)

## 에이전트 팀 구성표

| 에이전트 | 역할 | 핵심 기능 |
|---|---|---|
| **data-validator** | 입력 데이터 검증 | 6채널 이미지 로드/검증, 응답 함수 확인, 온도 범위 설정, 에러 추정 |
| **dem-calculator** | DEM 역산 실행 | DEMreg 또는 SITES 방법으로 DEM 계산, 파라미터 튜닝, 배치 처리 |
| **result-visualizer** | 결과 시각화 | DEM 맵 플롯, EM loci 곡선, chi-squared 맵, 온도별 DEM 슬라이스 |
| **quality-reviewer** | 품질 검토 | chi-sq 분포, 음수 DEM 비율, 합성 DN 비교, PASS/REVISE 판정 |

## 실행 모드: 에이전트 팀

```
사용자 요청 (6채널 데이터 + 응답 함수)
    │
    ▼
data-validator  →  dem-calculator  →  result-visualizer  →  quality-reviewer
                                                                │
                                                       ┌───────┴───────┐
                                                       │               │
                                                    REVISE           PASS
                                                       │               │
                                                       ▼               ▼
                                                dem-calculator      최종 결과
                                                (파라미터 조정,      전달
                                                 최대 2회)
```

## 필수 입력 정책

**파이프라인 시작 전, 아래 항목을 반드시 사용자에게 질문하여 확보한다.**
**절대 자동 추정/자동 감지하지 않는다. 모든 항목을 명시적으로 확인받은 후 진행한다.**

| # | 항목 | 변수 | 용도 |
|---|---|---|---|
| 1 | 관측 날짜 | `{날짜}` | 데이터 식별, 로그 기록 |
| 2 | 기기/파장 | `{기기}`, `{파장}` | AIA (171) / EUI-FSI (174) / 직접 입력 |
| 3 | 데이터 위치 | `{데이터경로}` | 6개 파장 이미지 디렉토리 |
| 4 | 데이터 포맷 | `{포맷}` | .npy / .npz / .fits |
| 5 | 응답 함수 | `{응답함수}` | 번들 AIA / 번들 EUI / 직접 제공 (경로) |
| 6 | 역산 방법 | `{방법}` | DEMreg / SITES / 양쪽 비교 |
| 7 | 온도 범위 | `{온도범위}` | 기본: log T = 5.6–7.0 |
| 8 | 작업 경로 | `{작업경로}` | 중간/최종 결과물 저장 위치 |

### 데이터 입력 형태

`core.loader` 모듈이 3가지 포맷을 지원한다. **사용자가 확인한 파장/포맷을 명시적으로 전달한다.**

| 방식 | 파일 예시 |
|---|---|
| **개별 .npy x6** | `aia_94.npy`, `data_131.npy`, ... (파일명에 파장 포함) |
| **단일 .npz** | `aia_6ch.npz` (키: `'94'`, `'131'`, ... 또는 `'dn_cube'`+`'wavelengths'`) |
| **개별 .fits x6** | `aia_94.fits`, `sdo_131.fits`, ... (파일명 또는 `WAVELNTH` 헤더) |

**에러 파일 (선택)**: `err_94.npy` 등 prefix+파장. 없으면 FITS는 Boerner 모델, npy/npz는 sqrt(DN)으로 추정.

### 번들 응답 함수

| 기기 | 파일 | 파장 | shape |
|---|---|---|---|
| AIA | `core/response/aia_response.npz` | 94, 131, **171**, 193, 211, 335 | (81, 6), log T = 4.0–8.0 |
| EUI-FSI | `core/response/eui_response.npz` | 94, 131, **174**, 193, 211, 335 | (81, 6), log T = 4.0–8.0 |

사용자가 직접 제공할 경우: `tresp.npy` + `tresp_logt.npy` 또는 `.npz`

```python
from core.loader import load_data, load_response

data = load_data('{작업경로}/data/')       # → dn_cube (ny,nx,6), edn_cube, wavelengths, headers
resp = load_response('{작업경로}/response/')  # → tresp, tresp_logt, temps, logt, delta_temp
```

## 역산 방법 상세

### DEMreg (정규화 기반)

**진입점**: `core.demreg.dn2dem_pos()`

```python
from core.demreg import dn2dem_pos

dem, edem, elogt, chisq, dn_reg = dn2dem_pos(
    dn_in,          # (ny, nx, 6) — DN [DN/px/s]
    edn_in,         # (ny, nx, 6) — 에러
    tresp,          # (nt_resp, 6) — 온도 응답 함수
    tresp_logt,     # (nt_resp,) — log10(T)
    temps,          # (nt+1,) — 온도 빈 경계
    reg_tweak=1.0,
    max_iter=10,
    rgt_fact=1.5,
    nmu=42
)
```

**출력:**
- `dem` — (ny, nx, nt) DEM [cm⁻⁵ K⁻¹]
- `edem` — (ny, nx, nt) 수직 에러
- `elogt` — (ny, nx, nt) 온도 분해능
- `chisq` — (ny, nx) 축소 카이제곱
- `dn_reg` — (ny, nx, 6) 합성 DN

**핵심 파라미터:**
| 파라미터 | 기본값 | 설명 |
|---|---|---|
| `reg_tweak` | 1.0 | 목표 정규화 카이제곱 |
| `max_iter` | 10 | 양수 보장 최대 반복 |
| `rgt_fact` | 1.5 | 반복당 카이제곱 증가 비율 |
| `nmu` | 42 (맵), 500 (단일) | 정규화 파라미터 샘플 수 |
| `gloci` | 0 | EM loci 곡선 사용 여부 |

### SITES (반복적 가중 역산)

**단일 픽셀**: `core.sites.dem_sites()`
**그리드 가속**: `core.sites.dem_gridsites()`

```python
from core.sites import dem_gridsites

# Grid-SITES (다중 픽셀 효율적 처리)
result = dem_gridsites(
    obs_in,         # (npix, 6) — DN [DN/s]
    err_in,         # (npix, 6) — 에러
    response,       # (nt, 6) — 온도 응답 함수
    response_err,   # (6,) — 상대 응답 불확실성
    logt,           # (nt,) — log10(T) 빈 중심
    delta_temp,     # (nt,) — 온도 빈 폭 [K]
    wavel,          # (6,) — 파장 [Å]
    convergence=0.02
)
```

**출력 (dict):**
- `dem` — (npix, nt) DEM [cm⁻⁵]
- `demerr` — (npix, nt) DEM 에러
- `obsmod` — (npix, 6) 합성 DN
- `goodoffit` — (npix,) 카이제곱

**핵심 파라미터:**
| 파라미터 | 기본값 | 설명 |
|---|---|---|
| `convergence` | 0.02 | 수렴 기준 (잔차 상대 비율) |
| `response_err` | [0.25,...] | 채널별 상대 응답 불확실성 |

## 데이터 전달 규칙

에이전트 간 모든 데이터는 사용자가 지정한 `{작업경로}` 하위 파일로 전달한다.

| 에이전트 | 출력 디렉토리 |
|---|---|
| data-validator | `{작업경로}/data/`, `{작업경로}/response/` |
| dem-calculator | `{작업경로}/results/` |
| result-visualizer | `{작업경로}/figures/` |
| quality-reviewer | `{작업경로}/reports/` |
| 공통 | `{작업경로}/logs/dem-note.md` |

**전달 규칙:**
1. 각 에이전트는 자신의 지정 디렉토리에만 쓴다
2. 다른 에이전트의 출력은 읽기 전용으로 참조한다
3. 모든 중간 산출물은 삭제하지 않고 보존한다
4. 원본 데이터는 수정 금지 — 전처리된 데이터를 `{작업경로}/data/`에 별도 저장
5. `{작업경로}/logs/dem-note.md`에 모든 에이전트가 판단 과정을 누적 기록한다

## 에이전트별 입출력 프로토콜

| Phase | 에이전트 | 입력 | 출력 |
|---|---|---|---|
| 1 | data-validator | 원본 6채널 이미지, 응답 함수 | `data/dn_cube.npy`, `data/edn_cube.npy`, `response/tresp.npy`, `response/tresp_logt.npy`, `data/00_data_report.md` |
| 2 | dem-calculator | `data/*`, `response/*` | `results/dem.npy`, `results/edem.npy`, `results/chisq.npy`, `results/dn_reg.npy`, `results/01_calc_report.md` |
| 3 | result-visualizer | `results/*`, `data/*` | `figures/dem_map_*.png`, `figures/em_loci_*.png`, `figures/chisq_map.png`, `figures/02_figure_index.md` |
| 4 | quality-reviewer | `results/*`, `figures/*`, `data/*` | `reports/03_quality_report.md` |

## 작업 경로 정책

- 하네스 내 `_workspace/`는 빈 스캐폴드(디렉토리 구조 템플릿)이다
- 실행 결과물은 사용자가 지정한 `{작업경로}`에 저장한다
- 이후 모든 `_workspace/` 참조는 사용자가 지정한 `{작업경로}`로 치환된다

## 기술 스택

| 범주 | 도구 |
|---|---|
| 언어 | Python 3.10+ |
| 수치 계산 | numpy, scipy |
| 태양물리 | sunpy, astropy, aiapy |
| DEM 역산 | core.demreg (DEMreg), core.sites (SITES) — 하네스 내 번들 |
| 시각화 | matplotlib, astropy.visualization |
| 데이터 I/O | astropy.io.fits, numpy |
| 병렬 처리 | concurrent.futures |

## DEMreg vs SITES 비교

| 특성 | DEMreg | SITES |
|---|---|---|
| 알고리즘 | GSVD + Tikhonov 정규화 | 반복적 가중 역산 + 스무딩 |
| 양수 보장 | 반복 루프 (chi-sq 완화) | 누적 구조로 자동 보장 |
| 다중 픽셀 | ProcessPoolExecutor 병렬화 | Grid-SITES 비닝 가속 |
| 에러 종류 | 수직(DEM) + 수평(온도 분해능) | 수직(DEM)만 |
| 속도 | 중간 (정밀) | 빠름 (대규모 처리) |
| 참고 문헌 | Hannah & Kontar 2013 | Morgan 2019, Pickering & Morgan 2019 |

**선택 가이드:**
- 정밀 분석, 에러 특성 상세 필요 → DEMreg
- 대규모 이미지, 빠른 처리 → SITES (Grid-SITES)
- 두 방법 비교 → 양쪽 모두 실행 후 비교 보고서 생성

## 핵심 원칙

1. **데이터 검증 필수**: DEM 역산 전 반드시 입력 데이터의 shape, 단위, NaN, 음수 등을 검증한다
2. **응답 함수 정확성**: 응답 함수의 온도 범위가 DEM 계산 온도 범위를 포함해야 한다
3. **에러 추정**: DN 에러는 포아송 노이즈 + 기기 노이즈로 추정한다. 에러가 0이면 역산이 실패한다
4. **단위 일관성**: DN은 [DN/px/s], 응답은 [DN cm⁵ px⁻¹ s⁻¹], DEM은 [cm⁻⁵ K⁻¹]
5. **원본 불변**: 원본 데이터 파일은 절대 수정하지 않는다
6. **재현성**: 모든 파라미터와 계산 과정을 dem-note.md에 기록한다
7. **품질 게이트**: quality-reviewer가 PASS/REVISE 판정. REVISE 시 파라미터 조정 루프백 (최대 2회)
8. **시각화 필수**: DEM 맵은 반드시 시각화하여 물리적 타당성을 육안 확인한다

## 스킬 구성

| 스킬 | 역할 |
|---|---|
| **dem-pipeline** | 전체 파이프라인 조율, 에이전트 실행 순서, 방법 선택, 파라미터 관리 |

## 사용 언어

- 사용자 대면: 한국어
- 코드/설정/변수명: 영어
- 보고서: 한국어
