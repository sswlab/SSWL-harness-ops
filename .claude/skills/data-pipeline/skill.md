---
name: data-pipeline
description: >
  데이터 수집/저장/버전관리 및 모델 아카이빙 통합 스킬.
  JSOC/SDO, NOAA SWPC, Solar Orbiter SOAR, STEREO, VSO 등
  소스별 데이터 접근법과 모델 등록/활용 절차를 정의한다.
  data-engineer 에이전트가 이 스킬을 참조하여 수행한다.
  키워드: 데이터 다운로드, JSOC, SWPC, SDO, Solar Orbiter,
  FITS, AIA, HMI, EUI, PHI, STEREO, VSO, sunpy, drms,
  SOAR, 관측 데이터, 아카이브, 모델 등록, 모델 카드,
  버전 관리, 모델 목록, 어떤 모델, 등록해줘,
  모델 업데이트, 스킬 등록
---

# Data-Pipeline — 데이터 수집/모델 아카이빙 통합 스킬

## 개요

태양 및 우주기상 연구에 필요한 관측 데이터를 다양한 아카이브 및 실시간 소스에서 수집하는 방법과, 연구실 모델을 표준화된 형식으로 등록·관리하는 절차를 정의한다. data-engineer 에이전트가 이 스킬을 참조하여 실제 작업을 수행한다.

---

## 파트 A: 데이터 소스별 접근 방법

### 1. NOAA SWPC (실시간 태양풍/우주기상)

- **URL**: `https://services.swpc.noaa.gov/`
- **인증**: 불필요 (공개 API)
- **형식**: JSON

#### 주요 엔드포인트

| 데이터 | 엔드포인트 | 갱신 주기 |
|---|---|---|
| 태양풍 플라즈마 (7일) | `/products/solar-wind/plasma-7-day.json` | 1분 |
| 태양풍 자기장 (7일) | `/products/solar-wind/mag-7-day.json` | 1분 |
| GOES X-ray 플럭스 | `/json/goes/primary/xrays-7-day.json` | 1분 |
| 플레어 목록 | `/json/goes/primary/xray-flares-latest.json` | 수시 |
| Kp 지수 | `/products/noaa-planetary-k-index.json` | 3시간 |
| Dst 지수 | `/products/kyoto-dst.json` | 1시간 |

#### 쿼리 패턴

```python
import requests

def fetch_swpc_data(endpoint: str, timeout: int = 30) -> dict:
    url = f"https://services.swpc.noaa.gov{endpoint}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()
```

---

### 2. JSOC/SDO (AIA, HMI)

- **URL**: `http://jsoc.stanford.edu/`
- **인증**: 이메일 등록 필요 (export 시)
- **형식**: FITS
- **Python**: `drms`

#### 주요 시리즈

| 시리즈 | 기기 | 내용 | 케이던스 |
|---|---|---|---|
| `aia.lev1_euv_12s` | AIA | EUV 이미지 | 12초 |
| `hmi.M_720s` | HMI | 시선방향 자기장 | 12분 |
| `hmi.B_720s` | HMI | 벡터 자기장 | 12분 |
| `hmi.synoptic_mr_polfil_720s` | HMI | Synoptic map | CR당 1장 |

#### 쿼리 패턴

```python
import drms

client = drms.Client()
query_str = "aia.lev1_euv_12s[2026.03.27_00:00:00_TAI/6h@15m][193]{image}"
keys = client.query(query_str, key=drms.const.all)
export = client.export(query_str, method="url", protocol="fits", email="user@example.com")
export.wait()
# export.download(output_dir)
```

---

### 3. Solar Orbiter (EUI, PHI) — SOAR

- **아카이브**: `https://soar.esac.esa.int/soar-sl-tap/tap/`
- **인증**: 불필요
- **형식**: FITS
- **데이터 레벨**: LL (Low Latency), L1, L2

#### 쿼리 패턴

```python
from sunpy.net import Fido, attrs as a

result = Fido.search(
    a.Time("2026-03-01", "2026-03-27"),
    a.Instrument("PHI"),
    a.Detector("FDT"),
    a.Level("LL")
)
# Fido.fetch(result, path="_workspace/data/solo/phi/")
```

---

### 4. STEREO (SECCHI)

- **아카이브**: `https://stereo-ssc.nascom.nasa.gov/`
- **인증**: 불필요
- **형식**: FITS

#### 쿼리 패턴

```python
from sunpy.net import Fido, attrs as a

result = Fido.search(
    a.Time("2026-03-27", "2026-03-27 06:00"),
    a.Source("STEREO_A"),
    a.Instrument("SECCHI"),
    a.Detector("EUVI")
)
```

---

### 5. VSO (Virtual Solar Observatory)

- **통합 검색**: 다수 소스 통합
- **Python**: `sunpy.net.Fido`

```python
from sunpy.net import Fido, attrs as a
import astropy.units as u

result = Fido.search(
    a.Time("2026-03-27 00:00", "2026-03-27 06:00"),
    a.Source("SDO"),
    a.Instrument("AIA"),
    a.Wavelength(193 * u.Angstrom, 193 * u.Angstrom)
)
```

---

## 다운로드 검증

### 파일 크기 기준

| 데이터 유형 | 최소 크기 |
|---|---|
| AIA FITS | 10 MB |
| HMI FITS | 5 MB |
| EUI/PHI FITS | 1 MB |
| SWPC JSON | 100 B |

### FITS 헤더 검증

- `NAXIS1`, `NAXIS2` 존재 확인
- `DATE-OBS` 또는 `T_OBS`가 요청 시간 범위 내
- `WAVELNTH`(AIA) 또는 `CONTENT`(HMI)가 요청과 일치

### NaN 비율 검사

이미지 데이터의 NaN 비율이 10% 초과 시 경고.

## 공통 의존성

```
requests>=2.28.0
drms>=0.6.0
sunpy>=5.0.0
astropy>=5.0
aiapy>=0.7.0
numpy>=1.21.0
```

## 소스별 제한사항

| 소스 | 제한사항 |
|---|---|
| NOAA SWPC | 7일 이상 과거 데이터 미제공 |
| JSOC | export 대기열 부하에 따라 지연 가능 |
| SOAR | LL 데이터 가용성 불규칙 |
| STEREO SSC | STEREO-B 통신 두절 (2014년~), A만 가용 |
| VSO | 개별 소스 직접 접근보다 느릴 수 있음 |

---

## 파트 B: 모델 아카이빙/활용 절차

### 워크플로우 A: 모델 등록

```
[개발자: "모델 등록해줘"]
    │
    ▼
╔═══════════════════════╗
║   Phase 1: 분석       ║
║   data-engineer       ║
║   (코드 분석, 의존성)   ║
╚════════╤══════════════╝
         │
         ▼
╔═══════════════════════╗
║   Phase 2: 표준화     ║
║   data-engineer       ║
║   (모델 카드 + 래퍼)   ║
╚════════╤══════════════╝
         │ 모델 카드 초안
         ▼
╔═══════════════════════╗
║   Phase 3: 검증       ║
║   data-engineer       ║
║   (테스트 실행)        ║
╚════════╤══════════════╝
         │ 등록 완료
         ▼
[registry_index.json 갱신]
```

### 워크플로우 B: 등록 모델 활용

등록된 모델을 사용하는 흐름은 일반 연구 작업과 동일하되, research-planner가 `model_registry`를 참조한다:

```
[연구자: "코로나홀 탐지 모델로 어제 데이터 분석해줘"]
    │
    ▼
╔═════════════════════════════╗
║   research-planner          ║
║   (model_registry 참조)     ║
╚════════╤════════════════════╝
         ▼
╔═════════════════════════════╗
║   사용자 승인               ║
╚════════╤════════════════════╝
         ▼
╔═════════════════════════════╗
║   research-executor         ║
║   ├ data-engineer (필요 시)  ║
║   └ 모델 카드 참조하여 실행  ║
╚════════╤════════════════════╝
         ▼
╔═════════════════════════════╗
║   paper-writer (결과 보고)  ║
╚═════════════════════════════╝
```

### 워크플로우 C: 모델 목록 조회

```
[연구자: "우리 연구실에 어떤 모델들이 있어?"]
    │
    ▼
[data-engineer]
    │ registry_index.json 읽기
    ▼
[모델 목록 표/카드 형식으로 제시]
```

### 워크플로우 D: 모델 업데이트

```
[개발자: "코로나홀 탐지 모델 v2로 업데이트해줘"]
    │
    ▼
[data-engineer]
    ├── 기존 버전 아카이브 (versions/v1.0/)
    ├── 새 코드 분석
    ├── 모델 카드 업데이트
    ├── 테스트 실행
    └── registry_index.json 갱신
```

### 모델 레지스트리 구조

```
_workspace/model_registry/
├── registry_index.json
├── {model_name}/
│   ├── model_card.md
│   ├── run.sh
│   ├── src/
│   └── versions/
│       └── v{N}/
```
