# DEMreg — 사용 설명서

> Tikhonov 정규화 + GSVD 기반 DEM(Differential Emission Measure) 역산 모듈
> 참고문헌: **Hannah & Kontar, A&A 553, A10 (2013)**

---

## 1. DEMreg가 푸는 문제

태양 광학/EUV 관측에서 각 채널의 관측 카운트 `g(f)`는 온도 응답 함수 `K(f, T)`와
플라즈마의 DEM `ξ(T)`의 적분으로 표현됩니다.

```
g(f) = ∫ K(f, T) · ξ(T) dT      (f = 채널 인덱스)
```

이산화 후 행렬식으로 보면 `g = K · ξ`. K가 ill-conditioned이라 직접 역행렬을 취할 수
없으므로 DEMreg는 다음 정규화 문제로 푼다.

```
min || K·ξ − g ||² + λ · || L·ξ ||²
```

- **L** : 제약 행렬 (smoothness/positivity weighting)
- **λ** : 정규화 파라미터 — Morozov discrepancy principle로 자동 결정
- 해는 **K**와 **L**의 일반화 특이값 분해(GSVD)로 닫힌형으로 구함
- 음수 해가 나오면 `reg_tweak`을 `rgt_fact`배씩 키워가며 양수 해가 나올 때까지 반복

---

## 2. 모듈 구성

| 파일 | 역할 |
|---|---|
| `__init__.py` | 진입점 `dn2dem_pos` 노출 |
| `dn2dem_pos.py` | **사용자 진입점**. 0D/1D/2D 데이터 reshape, 응답함수 보간, 단위 처리 |
| `demmap_pos.py` | 픽셀별 DEM 계산. 픽셀 수 ≥ 200이면 `ProcessPoolExecutor`로 병렬 |
| `dem_inv_gsvd.py` | K와 L의 GSVD 계산 (`np.linalg.svd` 기반) |
| `dem_reg_map.py` | `λ`(정규화 파라미터) 탐색 — Morozov discrepancy |

호출 흐름:

```
dn2dem_pos  →  demmap_pos  →  dem_pix (per-pixel loop)
                                 ├─ dem_inv_gsvd  (GSVD of K, L)
                                 └─ dem_reg_map   (find optimal λ)
```

---

## 3. 진입점 API — `dn2dem_pos`

```python
from demreg import dn2dem_pos

dem, edem, elogt, chisq, dn_reg = dn2dem_pos(
    dn_in, edn_in, tresp, tresp_logt, temps,
    reg_tweak=1.0, max_iter=10, gloci=0, rgt_fact=1.5,
    dem_norm0=None, nmu=40, warn=False,
    emd_int=False, emd_ret=False, l_emd=False, non_pos=False,
)
```

### 3.1 필수 입력

| 이름 | 형상 | 의미 |
|---|---|---|
| `dn_in` | `(nf,)`, `(nx, nf)`, 또는 `(nx, ny, nf)` | 채널별 카운트 (DN/px/s) |
| `edn_in` | `dn_in`과 동일 | 카운트의 1σ 오차 |
| `tresp` | `(n_tresp, nf)` | 채널별 온도 응답 함수 |
| `tresp_logt` | `(n_tresp,)` | `tresp`의 logT 그리드 |
| `temps` | `(nt+1,)` | DEM 온도 **bin edges** (선형 K 단위, log 아님) |

> ⚠ `temps`는 bin **edges**입니다. 결과 DEM은 `nt = len(temps) - 1`개의 bin에 정의됨.

### 3.2 주요 옵션

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `reg_tweak` | 1.0 | 목표 정규화된 χ². 보통 1 (= reduced χ²) |
| `max_iter` | 10 | 양수해 탐색 반복 한도 (음수 나오면 `reg_tweak *= rgt_fact`) |
| `rgt_fact` | 1.5 | 반복마다 χ² 목표를 늘리는 비율 (>1 이어야 함) |
| `dem_norm0` | None | DEM 초기 가중치 (모양 `(..., nt)`). 절대값은 무관, 상대값만 사용 |
| `gloci` | 0 | `dem_norm0`이 None일 때 L 가중치 결정 방식. `0`: self-norm 2-pass / `1`: EM-loci 최솟값 |
| `nmu` | 40 | λ 샘플 개수. 0D면 자동 500, map이면 42 |
| `emd_int` | False | EMD(`cm⁻⁵`) 공간에서 역산. 고온부에서 도움 될 때 있음 |
| `emd_ret` | False | EMD로 결과 반환 (기본은 DEM `cm⁻⁵ K⁻¹`) |
| `l_emd` | False | L 행렬에서 `√dlogT` 제거 (EMD와 궁합) |
| `non_pos` | False | 양수 강제 X, 첫 해 반환 (= `max_iter=1`) |
| `warn` | False | 경고 출력 (0D면 자동 True) |

### 3.3 출력

| 이름 | 형상 | 의미 |
|---|---|---|
| `dem` | `(..., nt)` | DEM(T), 단위 = `tresp` 단위에 의해 결정 (보통 `cm⁻⁵ K⁻¹`) |
| `edem` | `(..., nt)` | DEM 수직 오차 |
| `elogt` | `(..., nt)` | logT 수평 오차 (HWHM/√(8ln2) → σ) |
| `chisq` | `(...,)` | 최종 reduced χ² |
| `dn_reg` | `(..., nf)` | 재구성된 DN — 입력 `dn_in`과 비교 검증용 |

---

## 4. 사용 시 주의사항

1. **온도 그리드** — DEM 그리드(`temps`)는 `tresp_logt` 범위 안에 있어야 함. 코드 내부에서
   `np.interp`로 로그-스페이스 보간함.
2. **응답함수 음수/0 처리** — `dn2dem_pos`가 자동으로 채널별 최솟값으로 치환.
3. **`dn_in`에 NaN/Inf/음수**가 섞이면 해당 픽셀은 0으로 반환 (`dem_pix`의 `np.prod(dn) > 0` 게이트).
4. **병렬 처리** — `nx*ny ≥ 200`이면 자동으로 `ProcessPoolExecutor`. 노트북에서 쓸 때
   `if __name__ == "__main__":` 가드가 없어도 동작하지만, 윈도우/일부 환경에서는
   block-script로 감싸는 게 안전.
5. **단위 스케일** — 내부에서 `sclf=1E15`로 스케일링 후 출력에서 되돌림. 사용자는 신경 X.
6. **초기 가중치** — `dem_norm0`을 알고 있다면 (예: 이전 분석 결과) 넣는 것이
   `gloci`만 쓰는 것보다 거의 항상 더 좋다.

---

## 5. 의존성

```
numpy
tqdm
threadpoolctl
concurrent.futures (stdlib)
```

> 노트북 예시는 추가로 `matplotlib` 사용.

---

## 6. 빠른 사용 예시 (0D, 단일 픽셀)

```python
import numpy as np
from demreg import dn2dem_pos

# 응답함수
tresp = np.load('../response/tresp_aia.npy')        # (81, 6)
tresp_logt = np.load('../response/tresp_logt.npy')  # (81,)

# DEM 온도 그리드 (선형, K 단위). 41 bin (응답함수 logT 범위 내 권장)
temps = np.logspace(5.7, 7.3, 42)
nt = len(temps) - 1

# 가짜 DN 측정값 (6 채널)
dn  = np.array([50., 200., 1500., 1000., 600., 100.])
edn = np.sqrt(dn) + 0.1 * dn

# 0D 단일 픽셀에서는 dem_norm0를 명시적으로 넣어주는 게 안정적
dem, edem, elogt, chisq, dn_reg = dn2dem_pos(
    dn, edn, tresp, tresp_logt, temps,
    dem_norm0=np.ones(nt),
)

print('chisq =', chisq)
print('dem shape =', dem.shape)
```

전체 동작 예시(시각화 포함)는 같은 디렉토리의 **`example_demreg.ipynb`** 참고.
