# 07-IDL2Python — IDL→Python 코드 변환 하네스

IDL(Interactive Data Language) `.pro` 파일을 Python으로 변환하고,
변환된 코드의 정확성을 테스트를 통해 검증하는 자동화 파이프라인.

## 프로젝트 개요

태양물리·우주과학 분야에서 레거시 IDL 코드가 여전히 다수 존재한다.
사용자가 `.pro` 파일을 제시하면, 에이전트 팀이 IDL 코드를 분석 → Python으로 변환 → 테스트 데이터 확보 → 정확성 검증까지 수행한다.
파일이 여러 개인 경우 **병렬 변환**을 지원한다.

## 에이전트 팀 구성표

| 에이전트 | 역할 | 핵심 기능 |
|---|---|---|
| **idl-analyzer** | IDL 코드 분석 | .pro 파일 파싱, 구조/의존성 분석, IDL 특유 구문 식별, 변환 난이도 평가 |
| **python-translator** | Python 변환 | IDL→Python 구문 변환, 라이브러리 매핑(IDL→NumPy/SunPy/Astropy), 관용적 Python 작성 |
| **test-engineer** | 테스트 설계/실행 | 테스트 케이스 작성, 테스트 데이터 쿼리/다운로드, 변환 결과 검증, 병렬 테스트 실행 |
| **conversion-reviewer** | 변환 품질 검토 | 변환 정확성 검증, 엣지 케이스 확인, 성능 비교, PASS/REVISE 판정 |

## 실행 모드: 에이전트 팀

```
사용자 요청 (.pro 파일 제시)
    │
    ▼
idl-analyzer  →  python-translator  →  test-engineer  →  conversion-reviewer
                                                              │
                                                     ┌───────┴───────┐
                                                     │               │
                                                  REVISE           PASS
                                                     │               │
                                                     ▼               ▼
                                              python-translator    최종 결과
                                              (루프백, 최대 2회)    전달
```

**다중 파일 병렬 처리:**
```
사용자 요청 (N개 .pro 파일)
    │
    ▼
idl-analyzer (전체 스캔, 의존성 그래프 생성)
    │
    ▼
의존성 기반 실행 그룹 결정
    │
    ├──▶ [그룹 A: 독립 파일들] → 병렬 변환/테스트
    ├──▶ [그룹 B: A에 의존] → A 완료 후 병렬 변환/테스트
    └──▶ [그룹 C: B에 의존] → B 완료 후 병렬 변환/테스트
    │
    ▼
conversion-reviewer (전체 통합 검토)
```

## 필수 입력 정책

파이프라인 시작 전 아래 항목을 확보한다. 누락 시 되물어서 확보한다.

| 항목 | 변수 | 용도 |
|---|---|---|
| IDL 파일 위치 | `{idl경로}` | 변환 대상 .pro 파일 소스. 아래 형태를 모두 지원한다 |
| 변환 목적 | `{목적}` | 변환 맥락 (레거시 마이그레이션, 학습용, 특정 프로젝트 통합 등) |
| 작업 경로 | `{작업경로}` | 중간/최종 결과물 저장 위치 |
| 변환 모드 | `{모드}` | 단일/배치/선택적 (아래 참조) |

### IDL 파일 소스 유형

| 유형 | 예시 | 처리 방법 |
|---|---|---|
| **로컬 파일** | `/home/user/code.pro` | 직접 inbox/로 복사 |
| **로컬 디렉토리** | `/home/user/idl_codes/` | 내부 .pro 파일 전체/선택 복사 |
| **Git 저장소** | `https://github.com/user/repo` | `git clone` 후 .pro 파일 추출 |
| **웹 URL (HTTP/FTP)** | `https://sohoftp.nascom.nasa.gov/.../idl/` | HTML 디렉토리 파싱 → .pro 다운로드 |
| **단일 파일 URL** | `https://example.com/code.pro` | 직접 다운로드 |

**웹 소스(URL)인 경우**:
1. URL이 HTML 디렉토리 인덱스면 → 목록을 파싱하여 `.pro` 파일 링크를 추출한다
2. URL이 단일 `.pro` 파일이면 → 직접 다운로드한다
3. URL에 `readme.txt` 등 문서가 있으면 → 함께 다운로드하여 분석에 활용한다
4. 다운로드한 파일은 `{작업경로}/inbox/`에 저장한다
5. 웹 다운로드 결과를 `{작업경로}/logs/download_manifest.md`에 기록한다

**대표적 웹 소스**:
- SolarSoft (SSW): `https://sohoftp.nascom.nasa.gov/solarsoft/...`
- NASA GSFC: `https://hesperia.gsfc.nasa.gov/...`
- 개인 웹서버: 연구자가 웹에 공개한 IDL 코드

## 변환 모드

| 모드 | 설명 | 병렬 처리 |
|---|---|---|
| **단일 변환** | 지정 .pro 파일 1개를 변환 | 해당 없음 |
| **배치 변환** | 디렉토리/저장소/URL 내 모든 .pro 파일을 변환 | 의존성 그래프 기반 병렬 |
| **선택적 변환** | 사용자가 지정한 파일 목록만 변환 | 의존성 그래프 기반 병렬 |

## 데이터 전달 규칙

에이전트 간 모든 데이터는 사용자가 지정한 `{작업경로}` 하위 파일로 전달한다.

| 에이전트 | 출력 디렉토리 |
|---|---|
| idl-analyzer | `{작업경로}/analysis/` |
| python-translator | `{작업경로}/converted/` |
| test-engineer | `{작업경로}/tests/`, `{작업경로}/data/` |
| conversion-reviewer | `{작업경로}/reports/` |
| 공통 | `{작업경로}/logs/conversion-note.md` |

**전달 규칙:**
1. 각 에이전트는 자신의 지정 디렉토리에만 쓴다
2. 다른 에이전트의 출력은 읽기 전용으로 참조한다
3. 모든 중간 산출물은 삭제하지 않고 보존한다
4. 원본 .pro 파일은 `{작업경로}/inbox/`에 복사 후 작업한다 (원본 수정 금지)
5. `{작업경로}/logs/conversion-note.md`에 모든 에이전트가 판단 과정을 누적 기록한다

## 에이전트별 입출력 프로토콜

| Phase | 에이전트 | 입력 | 출력 |
|---|---|---|---|
| 1 | idl-analyzer | `{작업경로}/inbox/*.pro` | `analysis/00_file_inventory.md`, `analysis/01_dependency_graph.md`, `analysis/02_construct_report.md`, `analysis/03_conversion_plan.md` |
| 2 | python-translator | `analysis/*`, `inbox/*.pro` (읽기 전용) | `converted/{module_name}.py`, `converted/requirements.txt`, `converted/conversion_log.md` |
| 3 | test-engineer | `converted/*.py`, `analysis/*` | `tests/test_{module_name}.py`, `tests/test_report.md`, `data/` (테스트 데이터) |
| 4 | conversion-reviewer | `analysis/*`, `converted/*`, `tests/*` | `reports/00_review_report.md` |

## IDL→Python 핵심 매핑 원칙

1. **배열**: IDL 배열 → NumPy ndarray. 인덱싱 전치는 코드별 판단이 필요하다. 논리적 인덱싱 `bx[i,j,k]`가 동일한 경우 전치 불필요. FLTARR(nx,ny,nz) → np.zeros((nx,ny,nz))로 동일 차원 유지. `size(bx)` → `bx.shape` 인덱스 오프셋만 수정 (ss[1]→shape[0])
2. **COMMON 블록**: 두 가지 패턴으로 변환한다:
   - 패턴 A (함수 간 공유 상태): 명시적 매개변수 전달 (differential3의 bx, by, bz, orig, delx 등)
   - 패턴 B (전역 수정): 함수가 수정된 배열을 return (prepro의 bx_out, by_out, bz_out)
3. **출력 매개변수**: IDL PRO의 출력 매개변수(corner의 xv, sub_field의 obx 등) → Python return 값 또는 return 튜플로 변환
4. **내장 함수**: IDL 내장 → Python 표준/NumPy/SciPy 등가물. 특히:
   - `machar().eps` → `np.finfo(np.float64).eps`
   - `rk4(y,dy,s,h,'func_name')` → 직접 구현 (함수 이름 문자열 → callable)
   - `LA_INVERT(m)` → `np.linalg.inv(m)`
   - `HQR/ELMHES/eigenvec` → `np.linalg.eig` (3개→1개 호출)
   - `sgn(x)` → `np.sign(x)`
5. **파일 I/O**: IDL SAVE/RESTORE → np.savez/np.load (.sav→.npz). scipy.io.readsav는 기존 .sav 파일 읽기 전용
6. **플로팅**: IDL direct graphics / object graphics / 위젯 → 제거하고 프로그래밍 인터페이스로 대체. 시각화는 사용자 책임
7. **태양물리 특화**: IDL SolarSoft (SSW) → SunPy/Astropy 매핑
8. **문자열**: IDL 문자열 함수 → Python str 메서드
9. **구조체**: IDL struct → Python dataclass 또는 dict
10. **프로시저/함수**: IDL PRO/FUNCTION → Python def
11. **키워드 인자**: IDL keyword → Python keyword argument (기본값 포함). `/KEYWORD` (boolean flag) → `keyword=False`
12. **에러 처리**: IDL CATCH/ON_ERROR → Python try/except
13. **벡터화**: IDL 3중 루프 → NumPy mgrid/vectorized 연산으로 대체 가능 (성능 대폭 향상)

## 테스트 전략

### 테스트 수준

1. **구문 검증**: 변환된 Python이 import/실행 가능한지 확인
2. **단위 테스트**: 개별 함수의 입출력 일치 확인
3. **통합 테스트**: 전체 워크플로우 실행 확인
4. **데이터 비교**: IDL 출력과 Python 출력의 수치적 일치 확인 (허용 오차 내)

### 테스트 데이터 확보

테스트에 필요한 데이터가 없을 경우, test-engineer가 임시 데이터를 쿼리/다운로드한다:
- **FITS 파일**: `sunpy.net.Fido` 또는 `astropy.io.fits` 활용
- **JSOC/SDO**: `drms` 또는 `sunpy.net.jsoc.JSOCClient` (JSOC 이메일 필요 — 사용자에게 질문)
- **NOAA SWPC**: 공개 API (인증 불필요)
- **합성 데이터**: NumPy로 테스트용 더미 데이터 생성 (외부 의존 없이)
- 다운로드한 데이터는 `{작업경로}/data/`에 저장

### 병렬 테스트

다중 파일 변환 시, 독립 모듈의 테스트는 병렬 실행한다:
```python
# test-engineer가 생성하는 병렬 테스트 러너
import concurrent.futures
with concurrent.futures.ProcessPoolExecutor() as executor:
    futures = {executor.submit(run_test, module): module for module in independent_modules}
```

## 작업 경로 정책

- 하네스 내 `_workspace/`는 빈 스캐폴드(디렉토리 구조 템플릿)이다
- 실행 결과물은 사용자가 지정한 `{작업경로}`에 저장한다
- 이후 모든 `_workspace/` 참조는 사용자가 지정한 `{작업경로}`로 치환된다

## 기술 스택

| 범주 | 도구 |
|---|---|
| 언어 | Python 3.10+ |
| 수치 계산 | numpy, scipy |
| 태양물리 | sunpy, astropy, aiapy, drms |
| 시각화 | matplotlib |
| 테스트 | pytest, numpy.testing |
| 데이터 | pandas, astropy.io.fits |
| 병렬 처리 | concurrent.futures, multiprocessing |
| IDL 호환 | scipy.io (readsav), numpy |

## 사용 언어

- 사용자 대면: 한국어
- 코드/설정/변수명: 영어
- 변환 보고서: 한국어

## 핵심 원칙

1. **원본 불변**: 원본 .pro 파일은 절대 수정하지 않는다. inbox/에 복사 후 작업
2. **사용자 승인 필수**: 변환 계획(analysis/03_conversion_plan.md) 제시 후 승인받고 진행
3. **정확성 우선**: 관용적 Python 스타일보다 기능적 정확성을 우선한다. 정확성 확보 후 리팩터링
4. **테스트 필수**: 모든 변환은 반드시 테스트를 거친다. 테스트 없이 변환 완료로 판정하지 않는다
5. **인덱싱 주의**: IDL은 column-major(Fortran 순서), Python/NumPy는 row-major(C 순서). 다차원 배열 변환 시 반드시 확인
6. **의존성 명시**: 변환된 코드의 Python 패키지 의존성을 requirements.txt에 명시
7. **품질 게이트**: conversion-reviewer가 PASS/REVISE 판정. REVISE 시 python-translator 루프백 (최대 2회)
8. **판단 과정 기록**: 모든 판단 과정을 conversion-note.md에 누적
9. **병렬 처리**: 독립 파일은 병렬로 변환/테스트. 의존성이 있는 파일은 순서를 지킨다
10. **데이터 자급**: 테스트 데이터가 없으면 임시로 쿼리/생성하여 확보한다

## 외부 서비스 인증

### JSOC/SDO 데이터 — 이메일 필수

테스트 데이터로 SDO 데이터를 다운로드할 때 JSOC 등록 이메일이 필요하다.

**규칙:**
- 절대 하드코딩 금지
- 첫 사용 전에 사용자에게 명시적으로 질문
- 세션 내 재사용 가능 (conversion-note.md에 기록)

### 기타 외부 서비스
- **NOAA SWPC, VSO, SOAR**: 인증 불필요 (공개)
- 유료/구독 서비스: 사용자에게 묻고, 하드코딩하지 않는다

## 스킬 구성

| 스킬 | 역할 |
|---|---|
| **idl2python-orchestrator** | 전체 파이프라인 조율, 에이전트 실행 순서, 병렬 처리 관리, 루프백 |
| **idl-python-mapping** | IDL↔Python 구문 매핑 레퍼런스, 라이브러리 대응표, 함정(gotcha) 목록 |
| **test-protocol** | 테스트 방법론, 데이터 쿼리 템플릿, 허용 오차 기준, 병렬 테스트 실행법 |
| **web-source-collector** | 웹 URL(HTTP/FTP)에서 .pro 파일 수집. HTML 디렉토리 파싱, 다운로드, inbox 배치 |

## 실전 시연 워크플로우 (End-to-End Validation)

변환된 코드가 과학적으로 올바른 결과를 내는지 검증하는 시연 절차.
단위 테스트(pytest)만으로는 부족하며, 실제 물리 시나리오로 end-to-end 시연을 반드시 수행한다.

### 시연 절차

```
Phase 5: End-to-End 시연
    │
    ▼
1. 합성 데이터 생성 (testfield 등)
    │
    ▼
2. 변환된 각 모듈을 순서대로 실행
   (testfield → fieldline → null_point → twist → prepro)
    │
    ▼
3. 결과가 물리적으로 타당한지 확인
   (null point 위치, 력선 형태, twist 값, force-free 수렴)
    │
    ▼
4. 런타임 에러 발생 시 → 버그 수정 → 재테스트 → 재시연 루프
    │
    ▼
5. 결과를 {작업경로}/reports/01_demo_report.md에 기록
```

### 시연 체크리스트

각 변환 프로젝트마다 아래 항목을 반드시 시연한다:

- [ ] **구문 검증**: 모든 모듈 `import` 성공
- [ ] **단위 테스트**: pytest 전체 PASS
- [ ] **End-to-End 실행**: 합성 데이터로 전체 파이프라인 실행
- [ ] **물리 검증**: 알려진 해석적 결과와 비교 (예: 나선 twist=1.5 turns)
- [ ] **경계 케이스**: 격자 경계, 빈 배열, NaN 처리 확인
- [ ] **에러 복구**: 의도적으로 잘못된 입력으로 에러 메시지 확인

### 시연 결과 보고 형식

```markdown
# End-to-End 시연 보고서

## 환경
- Python: {version}, NumPy: {version}

## 시연 결과
| # | 모듈 | 입력 | 결과 | 물리 검증 | 판정 |
|---|---|---|---|---|---|
| 1 | testfield | n=50, pixel=0.08 | (50,50,50) 생성 | 4전하 모델 | PASS |
| 2 | fieldline3d | 5개 발점 | 력선 추적 성공 | z 증가 방향 | PASS |
| 3 | find_null | 선형 필드 | (10,10,*) 수렴 | null line | PASS |
| 4 | prepro | 32×32 bipolar | force 감소 | 수렴 확인 | PASS |
| 5 | twist | 나선 1.5회전 | 1.495 turns | 오차 0.3% | PASS |

## 발견 버그 및 수정 이력
| 버그 | 원인 | 수정 | 재테스트 |
|---|---|---|---|
| field_interp IndexError | 경계 밖 좌표 접근 | 경계 체크 추가 | 43 PASS |
```

## 실전 발견 버그 패턴 (Known Gotchas)

실전 시연에서 반복적으로 발견되는 변환 버그 유형. python-translator와 conversion-reviewer가 반드시 확인해야 한다.

### 1. 경계 체크 누락 (Boundary Check Missing)

IDL은 배열 범위 밖 접근 시 에러를 내지만, 반복 알고리즘(Newton-Raphson, RK4 등)에서 좌표가 격자 밖으로 이탈할 수 있다. 보간 함수(`field_interp`, `corner`)에 반드시 경계 체크를 추가해야 한다.

```python
# 패턴: 보간 함수에 방어 코드 필수
def field_interp(bx, by, bz, xindex, yindex, zindex):
    nx, ny, nz = bx.shape
    floor_x = int(np.floor(xindex))
    # 경계 체크 — 없으면 IndexError 발생
    if floor_x < 0 or floor_x >= nx - 1:
        return np.array([0.0, 0.0, 0.0])
    ...
```

### 2. 중앙값/평균이 격자 밖 (Aggregated Position Out of Bounds)

다수 시드의 중앙값(median)이나 평균(mean)이 격자 범위 밖으로 벗어날 수 있다. Newton-Raphson 결과를 취합한 뒤 보간 함수를 호출하기 전에 반드시 경계를 확인한다.

### 3. IDL 원본 변수명 오류 전파

IDL 원본에 변수명 오류가 있을 수 있다 (예: `direction0`로 정의하고 `direction`으로 사용). IDL은 미정의 변수를 0으로 취급하지만 Python은 NameError를 발생시킨다. 원본 코드를 맹목적으로 번역하지 않고, 의도를 파악하여 올바른 변수명으로 변환해야 한다.

### 4. sub_field 슬라이싱 최적화

IDL의 element-by-element 루프로 작성된 서브큐브 추출을 NumPy 슬라이싱으로 최적화하면 성능이 대폭 향상된다.

```python
# IDL 스타일 (느림)
for di in range(2):
    for dj in range(2):
        for dk in range(2):
            obx[di, dj, dk] = bx[i+di, j+dj, k+dk]

# NumPy 스타일 (빠름)
obx = bx[i:i+2, j:j+2, k:k+2].copy()
```

### 5. matrix_interp 스텐실 경계

유한 차분 스텐실(xindex ± delta)이 격자 밖으로 나갈 수 있다. clamp 함수로 방어한다.
