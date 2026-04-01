---
name: scientific-figure-guide
description: >
  태양물리 학회 발표에서 과학적 Figure를 효과적으로 보여주는 가이드.
  Figure 선별, 강조, 주석 추가, 레이아웃 기법을 정의한다.
  content-extractor와 slide-composer가 참조한다.
  키워드: Figure, 그래프, 시각화, 시계열, 스펙트럼,
  태양 이미지, 자기장, 코로나, 히트맵, 컬러바,
  비교, 화살표, 주석, 강조
---

# Scientific-Figure-Guide — 학회 발표 Figure 가이드

## 개요

태양물리 학회 발표에서 자주 등장하는 Figure 유형별 슬라이드 표현 기법을 정의한다. 논문용 Figure를 발표용으로 변환할 때의 강조, 주석, 크기 조절 규칙을 포함한다.

---

## 논문 Figure vs 발표 Figure

| 항목 | 논문 Figure | 발표 Figure |
|---|---|---|
| 폰트 크기 | 8~12pt | 14~18pt (뒤에서도 보여야) |
| 정보 밀도 | 높음 (서브패널 다수) | 낮음 (핵심만) |
| 컬러바 | 작아도 됨 | 크고 명확하게 |
| 축 레이블 | 상세 | 단위만 간결하게 |
| 범례 | 내부 배치 가능 | 크게, 구분 명확하게 |
| 캡션 | Figure 아래 상세 | 슬라이드 제목으로 대체 |

---

## 태양물리 Figure 유형별 가이드

### 1. 태양 이미지 (AIA, HMI, EUI)

- **용도**: 코로나 구조, 활동 영역, 코로나홀 시각화
- **슬라이드 표현**:
  - 원본 해상도 유지, 슬라이드 60~80% 크기
  - 컬러맵 유지 (AIA: 채널별 표준 컬러맵)
  - 관심 영역(ROI)에 화살표 또는 사각형 오버레이
  - 관측 시각, 파장을 코너에 표시
- **주의**: 비율 변형 절대 금지

### 2. 시계열 (GOES XRS, 태양풍, Kp/Dst)

- **용도**: 플레어 이벤트, 태양풍 변화, 지자기 폭풍
- **슬라이드 표현**:
  - X축(시간)과 Y축(물리량+단위) 레이블 크게
  - 핵심 이벤트에 수직선 + 화살표 + 레이블 추가
  - 배경에 플레어 등급 영역 표시 (C/M/X 구간 음영)
  - 선 굵기 2~3pt (논문의 1pt보다 두껍게)
- **팁**: "여기를 보세요" 포인터를 추가하면 효과적

### 3. Synoptic Map / 자기장 맵

- **용도**: Carrington rotation 자기장 분포, 극성 분포
- **슬라이드 표현**:
  - 양/음극 명확한 빨강/파랑 컬러맵
  - 컬러바 크게 (높이 슬라이드의 50% 이상)
  - 관심 경도/위도 영역 표시
  - Carrington rotation 번호 표시

### 4. DEM (Differential Emission Measure) 맵

- **용도**: 코로나 온도 분포
- **슬라이드 표현**:
  - 온도별 서브패널: 슬라이드 1장에 3~4개 (2×2 배치)
  - 각 패널에 온도 레이블 (log T = 5.8, 6.0, 6.2, ...)
  - 통일된 컬러바 (모든 패널 공유)

### 5. 비교 그래프 (Baseline vs Experiment)

- **용도**: 성능 비교, 정확도 비교
- **슬라이드 표현**:
  - 막대그래프: Baseline(GRAY) vs Experiment(NAVY) 나란히
  - 차이값을 막대 위에 표시 (+12%, -3%)
  - 통계적 유의성: 별표(*) 표시
  - 3개 이하 메트릭만 표시 (나머지는 Table로)

### 6. 산점도 / 상관 분석

- **용도**: 두 변수 간 상관관계
- **슬라이드 표현**:
  - 데이터 포인트: 크기 8~12pt (발표에서 보이게)
  - 회귀선 + R² 값 크게 표시
  - 1:1 기준선 (대각선 점선)
  - 축 범위: 데이터 범위 + 10% 여백

---

## Figure 강조 기법

### 화살표/주석 추가

```python
import matplotlib.pyplot as plt

# 화살표 + 텍스트
ax.annotate('Flare onset',
            xy=(event_time, event_value),
            xytext=(text_x, text_y),
            fontsize=16, fontweight='bold', color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
```

### 영역 강조

```python
# 관심 영역 음영
ax.axvspan(start_time, end_time, alpha=0.2, color='yellow',
           label='Event period')

# 임계값 수평선
ax.axhline(y=threshold, color='red', linestyle='--',
           linewidth=1.5, label=f'Threshold = {threshold}')
```

### ROI 사각형 (태양 이미지)

```python
from matplotlib.patches import Rectangle

rect = Rectangle((x0, y0), width, height,
                 linewidth=2, edgecolor='lime',
                 facecolor='none', linestyle='--')
ax.add_patch(rect)
ax.text(x0, y0 - 20, 'Active Region', color='lime', fontsize=14)
```

---

## 멀티패널 Figure 규칙

| 패널 수 | 배치 | 슬라이드 크기 | 주의점 |
|---|---|---|---|
| 2 | 1×2 (가로) | 각 50% | 동일 축 범위, 공유 컬러바 |
| 3 | 1×3 | 각 33% | 3개 초과 시 분할 권장 |
| 4 | 2×2 | 각 25% | 최소 해상도 주의 |
| 6+ | 분할 | - | 2개 슬라이드로 분할 |

**원칙**: 발표에서 6개 이상 서브패널은 청중이 소화 불가. 핵심만 뽑아서 2~4개로 줄이기.

---

## 컬러맵 선택 가이드

| 데이터 유형 | 추천 컬러맵 | 비추천 |
|---|---|---|
| 연속 (온도, 밀도) | viridis, inferno, plasma | jet, rainbow |
| 발산 (양/음, 차이) | RdBu, coolwarm, bwr | - |
| 태양 이미지 (AIA) | 채널별 표준 (sdoaia193 등) | 변경 금지 |
| 카테고리 | tab10, Set2 (최대 6색) | 유사 색상 조합 |

**색맹 친화**: viridis/cividis 우선. 빨강-초록 조합 피하기. 패턴/마커로 보조 구분.

---

## 발표 전용 Figure 수정 체크리스트

- [ ] 폰트 크기: 축 레이블 ≥ 14pt, 범례 ≥ 12pt
- [ ] 선 굵기: 데이터 라인 ≥ 2pt
- [ ] 컬러바: 충분히 크고 레이블 명확
- [ ] 배경: 흰색 (슬라이드 배경과 통일)
- [ ] 주석: 핵심 포인트에 화살표/강조 추가
- [ ] 서브패널: 4개 이하
- [ ] 해상도: DPI ≥ 150 (인쇄: 300)
- [ ] 컬러맵: 색맹 친화적
