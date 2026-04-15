# 08-DEM-calc TODO

## HRI 174Å 응답 함수 추가 (보류)

- **파일**: `core/response/gof_hri_174.fits`
  - 원본: `/home/youn_j/99_server/DEM/HRI/gof_hri_174_sun_coronal_2021_chianti.abund_chianti.ioneq_synthetic.fits`
  - CHIANTI abundance (sun_coronal_2021), ioneq (chianti), IDL 생성 (2023-12-15)
  - shape: (11, 81) — 11 rows x 81 temp bins (logt = linspace(4, 8, 81))
  - row 별로 스케일이 다름 (row 0 ~ 1e-23–1e-18, ... row 10 ~ 1e-3–1e+2)
    - 어떤 row가 실제 response인지, normalization/unit 확인 필요

- **현재 상태**: 파일만 `core/response/`에 넣어둔 상태. loader에 미연동.

- **추가 작업 (HRI 지원 시)**:
  1. HRI 174 response FITS에서 올바른 row 추출 + 단위 확인
  2. 보정 파라미터 (factor 등) 결정 — FSI는 0.7 적용됨, HRI는 미정
  3. `HRI_WAVELENGTHS` 정의 및 loader에 HRI 감지 로직 추가
  4. `core/response/hri_response.npz` 생성 (번들)
  5. HRI 174 에러 모델 파라미터 (gain, readnoise) 확정
  6. EUI FSI 174 vs HRI 174 차이점 문서화

- **참고**: 현재 EUI(FSI) 174는 `resp_concat_FSI_factor0.7_rev1.npy`로 지원됨.
  HRI 174는 같은 파장이지만 기기 특성(해상도, sensitivity)이 다르므로 별도 응답 함수 필요.
