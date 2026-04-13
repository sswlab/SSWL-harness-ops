---
name: data-pipeline
description: >
  태양물리 데이터 수집/전처리 절차 및 코드 템플릿.
  GOES XRS, SDO/AIA, SDO/HMI, SDO/EVE 데이터 다운로드,
  FITS 파일 처리, 전처리, publication-quality Figure 생성 기준을 정의한다.
  research-executor가 코드 작성 시 이 스킬을 참조한다.
  키워드: 데이터, 다운로드, FITS, GOES, SDO, AIA, HMI, EVE,
  sunpy, astropy, 전처리, 보정, Figure, matplotlib,
  데이터 파이프라인, 코드 구조, config
---

# Data-Pipeline — 데이터 수집/전처리 절차

## 개요

태양물리 연구에서 자주 사용하는 데이터 소스, Python 기반 수집/전처리 코드 패턴, publication-quality Figure 생성 기준을 정의한다. research-executor가 코드를 작성할 때 이 스킬을 참조하여 일관된 코드 구조와 품질을 유지한다.

---

## 태양물리 데이터 소스

### 1. GOES XRS (X-ray 플럭스)

| 항목 | 내용 |
|---|---|
| 용도 | 태양 플레어 분류, X선 플럭스 시계열 |
| Python | `sunpy.timeseries.TimeSeries`, `sunpy.net.Fido` |
| 형식 | NetCDF / CSV |
| 케이던스 | 1초 / 1분 |
| 채널 | 0.5-4 A (short), 1-8 A (long) |

```python
from sunpy.net import Fido, attrs as a
from sunpy.timeseries import TimeSeries

result = Fido.search(
    a.Time("2024-01-01", "2024-01-31"),
    a.Instrument("XRS"),
    a.goes.SatelliteNumber(16)
)
files = Fido.fetch(result, path="_workspace/data/goes_xrs/")
ts = TimeSeries(files, concatenate=True)
```

### 2. SDO/AIA (EUV 이미지)

| 항목 | 내용 |
|---|---|
| 용도 | 코로나 이미징, DEM 분석, 코로나홀 탐지 |
| Python | `sunpy.map.Map`, `aiapy`, `drms` |
| 형식 | FITS |
| 파장 | 94, 131, 171, 193, 211, 304, 335 A |
| 케이던스 | 12초 |

```python
import drms

# ⚠ JSOC export는 등록된 이메일이 필수.
# 절대 하드코딩하지 말고, 사용자에게 질문해서 받은 값을 사용할 것.
# (CLAUDE.md "외부 서비스 인증" 참조)
JSOC_EMAIL = ask_user_for_jsoc_email()  # 사용자에게 물어서 받음

client = drms.Client()
query = "aia.lev1_euv_12s[2024.01.01_00:00:00_TAI/1d@1h][171]{image}"
keys = client.query(query, key=drms.const.all)
export = client.export(query, method="url", protocol="fits",
                       email=JSOC_EMAIL)
export.wait()
```

> **사용자 질문 템플릿**:
> "JSOC 데이터 다운로드에 등록된 이메일이 필요합니다. 어떤 이메일을 사용할까요?
> (처음이면 http://jsoc.stanford.edu/ajax/register_email.html 에서 먼저 등록 필요)"

### 3. SDO/HMI (자기장)

| 항목 | 내용 |
|---|---|
| 용도 | 광구 자기장, Synoptic map, 활동영역 분석 |
| Python | `drms`, `sunpy.map.Map` |
| 형식 | FITS |
| 시리즈 | `hmi.M_720s` (시선방향), `hmi.B_720s` (벡터) |
| 케이던스 | 12분 |

### 4. SDO/EVE (EUV 분광)

| 항목 | 내용 |
|---|---|
| 용도 | EUV 방사조도, 플레어 분광 분석 |
| Python | `sunpy.timeseries`, `sunpy.net.Fido` |
| 형식 | FITS / NetCDF |
| 채널 | 다중 EUV 라인 |

---

## Python 기술 스택

| 패키지 | 용도 | 최소 버전 |
|---|---|---|
| `sunpy` | 태양 데이터 검색/로드/좌표 | 5.0 |
| `astropy` | FITS, 단위, 시간, 좌표 | 5.0 |
| `aiapy` | AIA 보정 (pointing, degradation) | 0.7 |
| `drms` | JSOC 데이터 쿼리/다운로드 | 0.6 |
| `pandas` | 시계열, 테이블 처리 | 2.0 |
| `numpy` | 수치 계산 | 1.24 |
| `scipy` | 통계, 최적화, 보간 | 1.10 |
| `matplotlib` | 시각화 | 3.7 |
| `scikit-learn` | ML (필요 시) | 1.3 |

---

## 코드 구조 가이드

코드 파일은 연구 내용에 맞게 자유롭게 구성하되, naming convention을 준수한다.

```
_workspace/code/
├── config.py                        # [필수] 모든 설정을 한 곳에
├── utils.py                         # [필수] 공통 유틸리티
├── {NN}_{동사}_{대상}.py             # 실행 스크립트 (자유 구성)
└── ...
```

### Naming Convention

- **형식**: `{NN}_{동사}_{대상}.py`
- **번호(NN)**: 실행 순서를 나타내는 2자리 정수 (01~)
- **동사**: download, preprocess, build, train, evaluate, plot, extract, merge 등
- **예시**: `01_download_goes_xrs.py`, `02_preprocess_stix.py`, `03_build_dataset.py`, `04_train_bilstm.py`, `05_evaluate.py`, `06_plot_results.py`
- **config.py, utils.py**: 번호 없이 고정 이름

### config.py 템플릿

```python
"""
연구 프로젝트 설정 파일.
모든 경로, 파라미터, 상수를 여기서 관리한다.
"""
from pathlib import Path
import astropy.units as u

# === 경로 ===
WORKSPACE = Path("_workspace")
DATA_DIR = WORKSPACE / "data"
FIGURES_DIR = WORKSPACE / "figures"
TABLES_DIR = WORKSPACE / "tables"
CODE_DIR = WORKSPACE / "code"

# 하위 데이터 디렉토리
GOES_DIR = DATA_DIR / "goes_xrs"
AIA_DIR = DATA_DIR / "sdo_aia"
HMI_DIR = DATA_DIR / "sdo_hmi"

# === 데이터 설정 ===
TIME_START = "2024-01-01"
TIME_END = "2024-12-31"
AIA_WAVELENGTHS = [94, 131, 171, 193, 211, 304, 335]  # Angstrom
CADENCE = 1 * u.hour

# === 모델 파라미터 ===
# (연구별로 커스터마이즈)
RANDOM_SEED = 42
TEST_RATIO = 0.2

# === Figure 설정 ===
FIG_DPI = 300
FIG_FORMAT = "png"  # or "pdf" for vector

# === 디렉토리 자동 생성 ===
for d in [DATA_DIR, FIGURES_DIR, TABLES_DIR, GOES_DIR, AIA_DIR, HMI_DIR]:
    d.mkdir(parents=True, exist_ok=True)
```

---

## Figure 생성 기준

### matplotlib rcParams (publication-quality)

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    # 해상도
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',

    # 폰트
    'font.size': 12,
    'font.family': 'serif',
    'mathtext.fontset': 'dejavuserif',

    # 축
    'axes.linewidth': 1.2,
    'axes.labelsize': 14,
    'axes.titlesize': 14,

    # 틱
    'xtick.major.width': 1.0,
    'ytick.major.width': 1.0,
    'xtick.minor.width': 0.6,
    'ytick.minor.width': 0.6,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': True,
    'ytick.right': True,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,

    # 범례
    'legend.frameon': False,
    'legend.fontsize': 11,

    # 기본 크기
    'figure.figsize': (8, 6),
})
```

### Figure 작성 규칙

| 규칙 | 상세 |
|---|---|
| 해상도 | DPI=300, 저널 요구 시 PDF(벡터) |
| 폰트 | serif 계열, 수식은 LaTeX 스타일 |
| 축 레이블 | 물리량 + 단위 (예: "Flux [W m$^{-2}$]") |
| 컬러맵 | 색맹 친화적: viridis, cividis, plasma |
| 범례 | 프레임 없음, 데이터에 맞게 최적 위치 |
| 파일명 | `fig{NN}_{내용}.png` (예: `fig01_goes_xrs_timeseries.png`) |
| 크기 | 단일 컬럼: 8×6, 더블 컬럼: 16×6 |

---

## FITS 파일 처리 패턴

```python
import astropy.io.fits as fits
import sunpy.map
import numpy as np

# 단일 FITS 로드
hdulist = fits.open("data.fits")
data = hdulist[0].data
header = hdulist[0].header

# SunPy Map으로 로드 (태양 이미지)
smap = sunpy.map.Map("aia_171.fits")
print(smap.date, smap.wavelength, smap.exposure_time)

# NaN 비율 검사
nan_ratio = np.isnan(data).sum() / data.size
if nan_ratio > 0.1:
    print(f"WARNING: NaN ratio = {nan_ratio:.2%}")
```

## 데이터 품질 체크리스트

- [ ] 파일 크기 검증 (AIA > 10MB, HMI > 5MB)
- [ ] FITS 헤더: NAXIS, DATE-OBS, WAVELNTH 확인
- [ ] NaN 비율 < 10%
- [ ] 시간 범위가 요청과 일치
- [ ] 케이던스 커버리지 > 70%
