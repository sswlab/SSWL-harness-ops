# 07-IDL2Python — IDL→Python 코드 변환 하네스

IDL(Interactive Data Language) `.pro` 파일을 Python으로 변환하고, 테스트를 통해 정확성을 검증하는 자동화 파이프라인.

## 참고 프로젝트

이 하네스는 [dnidever/idl2py](https://github.com/dnidever/idl2py)를 참고하여 구성하였다. `idl2py`는 IDL→Python 구문 변환의 "jump start"를 제공하는 유틸리티로, 패턴 기반 변환 규칙과 지원/미지원 IDL 구문 목록이 본 하네스의 매핑 레퍼런스 설계에 참고가 되었다. 단, `idl2py`가 커버하지 못하는 영역(FITS I/O, SSW/SolarSoft 매핑, 배열 인덱싱 자동 전치, 테스트 자동 생성 등)을 본 하네스에서 에이전트 팀 기반으로 확장하였다.

## 빠른 시작

```
사용자: "solar_prep.pro를 Python으로 변환해줘"

→ 하네스가 자동으로:
  1. IDL 코드 분석 (구조, 의존성, 변환 난이도)
  2. 변환 계획 제시 → 사용자 승인
  3. Python 코드 생성
  4. 테스트 데이터 확보 + 테스트 실행
  5. 품질 검토 (PASS/REVISE)
  6. 최종 결과 전달
```

## 에이전트 팀

| 에이전트 | 역할 | 핵심 기능 |
|---|---|---|
| **idl-analyzer** | IDL 코드 분석 | .pro 파싱, 의존성 그래프, IDL 특유 구문 식별, 변환 계획 수립 |
| **python-translator** | Python 변환 | IDL→Python 구문 변환, 라이브러리 매핑, 배열 인덱싱 전치 |
| **test-engineer** | 테스트 설계/실행 | 테스트 작성, 데이터 확보(합성/쿼리), 병렬 테스트 실행 |
| **conversion-reviewer** | 품질 검토 | 변환 정확성 검증, 인덱싱 확인, PASS/REVISE 판정 |

## 스킬

| 스킬 | 역할 |
|---|---|
| **idl2python-orchestrator** | 파이프라인 총괄, 에이전트 실행 순서, 병렬 처리, 루프백 관리 |
| **idl-python-mapping** | IDL↔Python 구문 매핑 레퍼런스, SSW→SunPy/Astropy 대응표 |
| **test-protocol** | 테스트 방법론, 데이터 확보 전략, 수치 비교 기준, 병렬 실행법 |

## 변환 모드

| 모드 | 설명 |
|---|---|
| **단일 변환** | .pro 파일 1개 변환 |
| **배치 변환** | 디렉토리 내 모든 .pro 파일 변환 (독립 파일 병렬 처리) |
| **선택적 변환** | 지정 파일 목록만 변환 |

## 파이프라인 흐름

```
idl-analyzer → [사용자 승인] → python-translator → test-engineer → conversion-reviewer
                                                                          │
                                                                 ┌───────┴───────┐
                                                                 │               │
                                                              REVISE           PASS
                                                                 │               │
                                                                 ▼               ▼
                                                          python-translator    완료
                                                          (최대 2회 루프백)
```

## 핵심 특징

- **인덱싱 자동 전치**: IDL column-major → Python row-major 배열 인덱싱 변환
- **SSW 매핑**: SolarSoft 루틴 → SunPy/Astropy 자동 매핑
- **테스트 자동 생성**: pytest 기반 테스트 + 합성/실제 데이터 자동 확보
- **병렬 처리**: 독립 파일 동시 변환/테스트
- **품질 게이트**: PASS/REVISE 판정으로 변환 품질 보장

## 필수 입력

| 항목 | 설명 |
|---|---|
| IDL 파일 경로 | 변환 대상 .pro 파일 또는 디렉토리 |
| 변환 목적 | 레거시 마이그레이션, 프로젝트 통합 등 |
| 작업 경로 | 결과물 저장 위치 |
| 변환 모드 | 단일/배치/선택적 |

## 작업 공간 구조

```
{작업경로}/
├── inbox/          # 원본 .pro 파일 복사본 (읽기 전용)
├── analysis/       # IDL 분석 결과 (인벤토리, 의존성, 변환 계획)
├── converted/      # 변환된 Python 코드 + requirements.txt
├── tests/          # pytest 테스트 코드
├── data/           # 테스트 데이터 (합성/다운로드)
├── reports/        # 품질 검토 보고서
└── logs/           # conversion-note.md (판단 과정 기록)
```

## 기술 스택

- **Python 3.10+**, NumPy, SciPy, Astropy, SunPy, Matplotlib
- **테스트**: pytest, numpy.testing
- **병렬**: concurrent.futures, pytest-xdist

## 지원 소스 유형

Git 저장소뿐 아니라, SolarSoft FTP 같은 **웹 디렉토리**에서도 직접 .pro 파일을 수집할 수 있다.

| 소스 유형 | 예시 | 처리 |
|---|---|---|
| 로컬 파일 | `/home/user/code.pro` | inbox/로 복사 |
| 로컬 디렉토리 | `/home/user/idl_codes/` | .pro 추출 |
| Git 저장소 | `https://github.com/user/repo` | clone → .pro 추출 |
| **웹 URL** | `https://sohoftp.nascom.nasa.gov/.../idl/` | **HTML 파싱 → .pro 다운로드** |
| 단일 URL | `https://example.com/code.pro` | 직접 다운로드 |

## 사용 예시

### 단일 파일 변환

```
"solar_prep.pro를 Python으로 변환해줘.
 목적: SunPy 기반 프로젝트에 통합
 경로: ~/workspace/solar_prep_conversion"
```

### 프로젝트 전체 변환

```
"/home/youn_j/idl_codes/ 디렉토리의 모든 IDL 파일을 Python으로 변환해줘.
 목적: 레거시 IDL 코드 마이그레이션
 경로: ~/workspace/idl_migration"
```

### Git 저장소 변환

```
"https://github.com/njuguoyang/magnetic_modeling_codes 의
 fieldline, null_point 모듈을 Python으로 변환해줘.
 경로: ~/workspace/magnetic_modeling"
```

### 웹 URL에서 변환 (SolarSoft 등)

```
"https://sohoftp.nascom.nasa.gov/solarsoft/packages/dem_sites/idl/ 의
 IDL 코드를 Python으로 변환해줘.
 목적: DEM 분석 코드를 Python 파이프라인에 통합
 경로: ~/workspace/dem_sites_conversion"
```

---

## IDL→Python 변환 시 근본적 주의사항

[njuguoyang/magnetic_modeling_codes](https://github.com/njuguoyang/magnetic_modeling_codes) (25개 .pro, ~3000행)를 실제 변환·시연한 경험에서 도출된 사항들이다. 구문 치환 도구(idl2py 등)로는 해결할 수 없는 **언어 간 의미론적 차이**에 해당한다.

### 1. 배열 인덱싱 — "항상 전치"는 틀렸다

| | IDL | Python/NumPy |
|---|---|---|
| 메모리 순서 | Column-major (Fortran) | Row-major (C) |
| `FLTARR(3,4)` | 3열 × 4행 | — |
| `np.zeros((3,4))` | — | 3행 × 4열 |

흔히 "IDL→Python은 모든 배열을 전치해야 한다"고 알려져 있으나, 이는 **코드별로 판단**해야 한다.

- `bx[i,j,k]` 형태의 논리적 인덱싱이 코드 전체에서 일관되면, `np.zeros((nx,ny,nz))`로 동일하게 만들고 전치하지 않아도 된다. 실제로 magnetic_modeling_codes 전체가 이 경우였다.
- `REFORM`, `REBIN`, `TOTAL(arr, dim)` 등 차원 축을 명시하는 연산에서는 축 번호가 달라지므로 반드시 확인해야 한다.
- `size(bx)`가 반환하는 인덱스 오프셋만 다르다: IDL `ss[1]` → Python `shape[0]`.

**결론**: 맹목적 전치보다 원본 코드의 인덱싱 패턴을 먼저 분석하라.

### 2. COMMON 블록 — Python에 대응 개념이 없다

IDL의 `COMMON` 블록은 여러 함수가 전역 변수를 공유하는 메커니즘이다. Python에 직접 대응하는 개념이 없으며, 두 가지 패턴으로 변환해야 한다:

| 패턴 | 적용 상황 | 예시 |
|---|---|---|
| **매개변수 전달** | 함수 간 읽기 전용 공유 | `differential3(s, coords, bx, by, bz, orig, delx, ...)` |
| **반환값으로 전달** | 함수가 공유 변수를 수정 | `bx, by, bz, sub_l = prepro(bx, by, bz, ...)` |

이 변환은 함수 시그니처를 근본적으로 바꾸므로, 호출하는 쪽 코드도 모두 수정해야 한다.

### 3. 출력 매개변수 — Python 함수는 호출자의 변수를 바꿀 수 없다

IDL의 PRO는 인자를 참조(reference)로 받아 호출자의 변수를 직접 수정한다:

```idl
; IDL: xv가 수정되어 호출자에 반영됨
PRO CORNER, n1, n2, n3, Bx, By, Bz, xv
  xv[0,0] = Bx[n1,n2,n3]
  ...
END
```

Python에서는 이것이 불가능하다. **반환값**으로 바꿔야 한다:

```python
# Python: xv를 return
def corner(n1, n2, n3, bx, by, bz):
    xv = np.zeros((3, 8))
    xv[0, 0] = bx[n1, n2, n3]
    ...
    return xv
```

다수의 출력 매개변수가 있으면 튜플로 반환한다: `return posi, matr, note`

### 4. 경계 체크 — IDL에서 안 터지던 코드가 Python에서 터진다

IDL의 반복 알고리즘(Newton-Raphson, Runge-Kutta 등)에서 좌표가 격자 밖으로 이탈할 때:
- **IDL**: 배열 경계 밖 접근 시 에러를 내지만, 원본 코드가 경계 체크를 포함한 경우가 많다
- **Python**: `field_interp` 같은 저수준 보간 함수에 경계 체크가 없으면 `IndexError`가 발생

실전에서 발견된 구체적 사례:
- Newton-Raphson 반복 중 좌표가 격자 밖으로 이탈 → `corner()` IndexError
- 다수 시드의 **중앙값(median)**이 격자 밖 → `matrix_interp()` IndexError
- 유한 차분 스텐실 `xindex ± delta`가 격자 경계를 넘음

**대응**: 보간/접근 함수에 경계 체크를 반드시 삽입하고, 범위 밖이면 `[0,0,0]` 반환.

### 5. 함수 이름을 문자열로 전달 — Python에서 불가

IDL의 `rk4(coords, dydx, s, h, 'differential3')` 처럼 함수 이름을 **문자열**로 전달하는 패턴은 Python에서 직접 대응이 없다. 함수 객체(callable)를 직접 전달하거나, RK4를 직접 구현해야 한다.

```python
# IDL: rk4(y, dydx, s, h, 'function_name')
# Python: callable 전달
result = rk4(y, dydx, s, h, differential3, **kwargs)
```

### 6. IDL SAVE/RESTORE — 파일 포맷 호환 불가

IDL의 `.sav` 바이너리 포맷은 IDL 전용이다.

| 상황 | 대응 |
|---|---|
| 새로 저장 | `np.savez()` (.npz) 또는 HDF5 사용 |
| 기존 .sav 읽기 | `scipy.io.readsav()` (읽기 전용, 일부 타입 미지원) |

기존 IDL 파이프라인과 데이터를 주고받아야 하는 경우, FITS나 ASCII 같은 중간 포맷을 고려해야 한다.

### 7. GUI/위젯 코드 — 1:1 변환 불가

IDL의 `WIDGET_BASE`, `WIDGET_DRAW`, `XMANAGER` 등 위젯 코드는 Python에 1:1 대응이 없다. 원본의 `footpoints.pro`(마우스 클릭으로 발점 선택)를 그대로 옮길 수 없으며, **프로그래밍 인터페이스**로 재설계해야 한다:

```python
# GUI 대신 좌표 배열을 직접 입력
results = fieldline3d(bx, by, bz,
                      xindex=[10.0, 20.0, 30.0],
                      yindex=[15.0, 15.0, 15.0])
```

필요하다면 PyQt5, tkinter, matplotlib의 `ginput()` 등으로 별도 GUI를 구성할 수 있으나, 이는 변환이 아닌 재구현에 해당한다.

### 8. 원본 IDL 코드의 잠재적 버그가 전파된다

IDL은 미정의 변수를 0으로 취급하지만, Python은 `NameError`를 발생시킨다. 실전에서 발견된 예:

```idl
; poincare.pro 원본 — 변수명 불일치
direction0 = sgn(...)    ; direction0으로 정의
angle0 = angle0 * direction  ; direction을 사용 (IDL: 0으로 처리)
```

원본을 맹목적으로 번역하면 Python에서 `NameError`가 발생한다. **의도를 파악하여** 올바른 변수명으로 수정해야 한다.

### 9. WHERE 반환값 의미가 다르다

| | 결과 없을 때 |
|---|---|
| IDL `WHERE(cond)` | `-1` (스칼라) 반환 |
| Python `np.where(cond)` | 빈 배열 `(array([]),)` 반환 |

IDL 코드에서 `if idx[0] eq -1 then ...` 패턴이 있으면, Python에서는 `if len(idx[0]) == 0:` 로 바꿔야 한다.

### 10. 수치 정밀도 차이

| 항목 | IDL | Python |
|---|---|---|
| `STDDEV(arr)` | ddof=1 (N-1) | `np.std(arr)` = ddof=0 **(다르다!)** |
| `MACHAR()` | 기계 정밀도 조회 | `np.finfo(np.float64).eps` |
| `sgn(x)` | 부호 함수 | `np.sign(x)` |
| 정수 나눗셈 `5/2` | `2` (정수) | `2.5` (실수, `//` 써야 정수) |

`STDDEV`는 특히 위험하다. `np.std(arr, ddof=1)`로 명시하지 않으면 전혀 다른 값이 나온다.

### 11. 성능 — IDL 루프를 그대로 옮기면 느리다

IDL의 3중 루프를 Python for-loop로 그대로 번역하면 극심한 성능 저하가 발생한다. NumPy 벡터 연산으로 대체해야 한다:

```python
# IDL 직역 (느림) — testfield 200^3 = 수 분
for i in range(200):
    for j in range(200):
        for k in range(200):
            r = np.array([i,j,k]) * pixel - origin
            bx[i,j,k] = ...

# NumPy 벡터화 (빠름) — testfield 200^3 = 수 초
ii, jj, kk = np.mgrid[0:n, 0:n, 0:n]
rx = (ii - origin[0]) * pixel
# ... 벡터 연산
```

### 요약 체크리스트

변환 전 아래를 먼저 확인하라:

- [ ] 배열 인덱싱 패턴 분석 — 전치 필요 여부 판단
- [ ] COMMON 블록 목록 — 매개변수/반환값 전환 설계
- [ ] 출력 매개변수 목록 — return 튜플로 변환
- [ ] 반복 알고리즘 식별 — 경계 체크 삽입 위치 결정
- [ ] GUI/위젯 코드 — 프로그래밍 인터페이스로 재설계
- [ ] WHERE 패턴 — `-1` 체크를 빈 배열 체크로 변환
- [ ] STDDEV — `ddof=1` 명시
- [ ] 성능 병목 루프 — NumPy 벡터화 대상 식별
