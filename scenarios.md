# SSWL AI Harness v2.0 — 운용 시나리오

> **핵심 방향 전환**: 상시운용(24시간 감시) 모드를 제거하고,
> **연구자의 요청에 따른 업무 수행**, **모델 아카이빙/활용**, **아이디어→실험 결과** 에 집중한다.

---

## 시나리오 1. 연구 업무 수행

> *"연구와 관련된 작업을 시키면 수행해서 결과 보고해주는 기능"*

연구자가 자연어로 작업을 요청하면, AI가 계획을 수립하고 승인 후 실행하여 결과를 보고한다.

### 시나리오 흐름

1. **사용자가 LLM에 업무를 요청**
   - (예) "최근 1달간 데이터로 SO/PHI와 SDO/HMI 데이터로 synoptic map을 만들어줘."

2. **LLM이 해당 쿼리를 분석, 실행 계획을 수립**
   - (LLM) "최근 1달 데이터니 Low Latency 데이터를 사용하겠군. 보정을 거친 뒤 synoptic map을 만들어야겠어."
   - 실행 계획서를 사용자에게 Markdown으로 제시: 단계, 소요 시간, 리스크

3. **사용자 승인 후, LLM이 연구실 내 도구를 이용하여 작업 수행**
   - 데이터 수집 (JSOC/SDO, SOAR/Solar Orbiter 등에서 자동 다운로드)
   - 전처리 (보정, 좌표 정합, 시간 정렬)
   - 모델/도구 실행 (synoptic map 생성, PFSS 시뮬레이션 등)

4. **결과를 저장 후 사용자에게 보고**
   - 성공: 결과 파일 경로, 핵심 수치, 시각화 제공
   - 실패: 원인 분석, 대안 제시, 부분 결과 보존

5. **사용자의 후속 요청 (피드백 루프)**
   - (사용자) "이걸로 PFSS 시뮬레이션 돌려줘."
   - 이전 결과를 자동으로 참조하여 연속 작업 수행

### 구체적 시나리오 예시

```
사용자: "최근 1달간 SO/PHI와 SDO/HMI 데이터로 synoptic map을 만들어줘."

  [query-planner]
  → 해석: Solar Orbiter PHI + SDO HMI, 최근 27일, synoptic map 생성
  → 데이터 전략: PHI는 Low Latency, HMI는 720s 시리즈
  → 계획서 작성: 4단계 (수집 → 전처리 → 생성 → 보고), 총 40~60분 예상

  [사용자 승인] "좋아, 진행해"

  [task-executor]
  → Step 1: data-fetcher로 PHI LL + HMI 자기장 데이터 수집 (병렬)
  → Step 2: PHI 보정, HMI 좌표 정합, 시간 정렬
  → Step 3: model-runner로 synoptic_map 모델 실행
  → Step 4: PNG 시각화 생성

  [result-reporter]
  → "Synoptic map 생성 완료. PHI+HMI 합성 27일 데이터 사용."
  → 파일 경로, 핵심 수치(데이터 커버리지, 자기장 통계), 시각화 제공
  → 후속 제안: "이 map으로 PFSS 시뮬레이션 가능합니다"

사용자: "이걸로 PFSS 돌려줘"
  → [Phase 1 복귀: synoptic map 경로 자동 참조]
```

---

## 시나리오 2. 모델 아카이빙 및 활용

> *"연구실에서 개발된 모델들을 스킬로 아카이빙하고 정리. 개발에 참여하지 않은 연구자들도 동일하게 사용할 수 있도록."*

연구실에서 개발한 모델들을 표준화된 형식으로 등록·관리하고, 누구나 자연어로 호출하여 결과를 얻을 수 있게 한다.

### 시나리오 흐름

1. **모델 등록 요청**
   - (개발자) "코로나홀 탐지 모델을 등록해줘. 코드는 `/home/researcher/ch_detect/` 에 있고, AIA 193A 이미지를 입력으로 받아서 코로나홀 경계와 면적을 출력해."

2. **LLM이 모델을 분석하고 표준 형식으로 아카이빙**
   - (LLM) 코드 구조 분석, 의존성 파악, 입출력 형식 확인
   - 모델 카드(model card) 작성: 용도, 입력, 출력, 실행 환경, 제한사항
   - `_workspace/model_registry/` 에 표준화된 형태로 저장
   - 실행 스크립트 래퍼(wrapper) 생성

3. **등록된 모델 목록 조회**
   - (아무 연구자) "우리 연구실에 어떤 모델들이 있어?"
   - (LLM) 등록된 모델 목록을 표/카드 형식으로 제시

4. **등록된 모델 활용 (개발 미참여 연구자도 가능)**
   - (연구자) "코로나홀 탐지 모델로 어제 AIA 193 이미지 분석해줘"
   - LLM이 모델 카드를 참조하여 필요 데이터를 수집하고, 모델을 실행하고, 결과를 보고
   - 연구자는 모델의 내부 구현을 몰라도 됨

5. **모델 업데이트/버전 관리**
   - (개발자) "코로나홀 탐지 모델 v2로 업데이트해줘. 새 코드는 여기에."
   - LLM이 기존 버전을 아카이브하고, 새 버전을 등록

### 구체적 시나리오 예시

```
[모델 등록]
개발자: "DEM 생성 모델 등록해줘. /home/lab/dem_model/ 에 있어.
         AIA 6채널 이미지 입력, DEM map 출력이야."

  [skill-archivist]
  → 코드 분석: main.py, requirements.txt, README.md 확인
  → 입력: AIA 94, 131, 171, 193, 211, 335 A (6채널 FITS)
  → 출력: DEM map (FITS + PNG)
  → 의존성: sunpy, astropy, demregpy
  → 실행: python3 main.py --input_dir {path} --output_dir {path}
  → 모델 카드 생성 → _workspace/model_registry/dem_model/model_card.md
  → 실행 래퍼 생성 → _workspace/model_registry/dem_model/run.sh

[모델 활용 — 다른 연구자]
연구자B: "DEM 모델로 2026년 3월 15일 태양 DEM 분석해줘"

  [query-planner] → 모델 카드 참조: AIA 6채널 필요
  [data-fetcher]  → JSOC에서 해당 일시 AIA 6채널 자동 다운로드
  [model-runner]  → dem_model 실행
  [result-reporter] → DEM map 시각화 + 온도 분포 통계 보고
```

---

## 시나리오 3. 아이디어 → 실험 결과

> *"교수님 아이디어 떠오를때마다 얘한테 말씀하시면 얘가 간단한 실험해서 결과 보여줄겁니다."*

연구자가 연구 아이디어를 제시하면, AI가 실험을 설계하고 실행하여 초기 결과를 보여준다. 논문 초안 작성까지 지원한다.

### 시나리오 흐름

1. **연구자가 아이디어를 제시**
   - (교수님) "Solar Orbiter로 DEM 만드는 연구에서 Magnetogram을 추가로 input으로 넣는다면 성능이 좋아질까?"

2. **LLM이 아이디어를 분석하고 실험 설계를 제안**
   - (LLM) "이 실험을 수행하려면: (1) EUI 6채널로 기존 DEM 생성, (2) PHI magnetogram을 추가 input으로 넣은 modified DEM 생성, (3) 두 결과를 SDO/AIA DEM과 비교 분석해야 합니다. 진행할까요?"

3. **연구자와 피드백으로 실험 계획을 구체화**
   - (교수님) "비교 시 온도 범위별로 나눠서 보여줘"
   - (LLM) 실험 계획을 수정하여 재제시

4. **실험 수행**
   - 필요 데이터 수집 (EUI, PHI, AIA)
   - 모델 실행 (기존 DEM, modified DEM)
   - 비교 분석 (통계, 시각화)

5. **결과 보고 + 논문 초안**
   - 실험 결과 보고서 (수치, 그래프, 비교표)
   - (요청 시) 논문 초안 작성: Introduction, Method, Results, Discussion 구조

### 구체적 시나리오 예시

```
교수님: "Solar Orbiter로 DEM 만드는 연구에서 Magnetogram을 추가로
         input으로 넣는다면 성능이 좋아질까?"

  [research-assistant]
  → 아이디어 분석:
    - 기존: EUI multi-channel → DEM inversion
    - 제안: EUI multi-channel + PHI magnetogram → DEM inversion
    - 검증 방법: SDO/AIA DEM을 ground truth로 사용

  → 실험 계획 제안:
    1. 데이터 수집: EUI 174/304, PHI/FDT, AIA 6채널 (동일 시각)
    2. Baseline: EUI만으로 DEM 생성
    3. Experiment: EUI + PHI로 DEM 생성
    4. Reference: AIA 6채널로 DEM 생성 (ground truth)
    5. 비교: 온도 범위별 (logT 5.5~7.0) EM 차이, χ² 통계

  → "이 계획으로 진행할까요?"

교수님: "좋아, 근데 비교할 때 활동영역과 조용한 영역 따로 봐줘"

  [research-assistant] → 계획 수정: 영역 분류 단계 추가

  [승인 후 실행]
  → data-fetcher: EUI, PHI, AIA 데이터 수집
  → model-runner: DEM 3회 실행 (baseline, experiment, reference)
  → 비교 분석: 영역별, 온도별 통계

  [결과 보고]
  → "Magnetogram 추가 시 활동영역에서 logT 6.0~6.5 범위 EM이
     12% 개선되었습니다. 조용한 영역은 유의미한 차이 없음."
  → 비교표, 온도별 EM 그래프, 영역별 분석 제공

교수님: "오, 이걸로 짧은 논문 초안 써줘"

  [paper-drafter]
  → Introduction: 배경 + 동기
  → Method: 데이터 + 실험 설계
  → Results: 핵심 수치 + 그래프 설명
  → Discussion: 의미 해석 + 한계
  → References: 관련 선행 연구
```

---

## 시스템 구성 요약

### 에이전트 구성 (7개)

| 에이전트 | 역할 | 활용 시나리오 |
|---|---|---|
| **query-planner** | 요청 분석, 실행 계획 수립 | 1, 2, 3 |
| **data-fetcher** | 다양한 소스에서 데이터 수집 | 1, 2, 3 |
| **model-runner** | 등록된 모델 실행 | 1, 2, 3 |
| **task-executor** | 계획에 따른 순차/병렬 작업 실행 | 1, 2, 3 |
| **result-reporter** | 결과 정리 및 사용자 보고 | 1, 2, 3 |
| **skill-archivist** | 모델 등록/관리/버전관리 | 2 |
| **research-assistant** | 아이디어 분석, 실험 설계, 논문 초안 | 3 |

### 스킬 구성 (6개)

| 스킬 | 역할 | 관련 시나리오 |
|---|---|---|
| **research-task** | 연구 업무 오케스트레이터 | 1 |
| **model-archive** | 모델 아카이빙/활용 오케스트레이터 | 2 |
| **idea-to-experiment** | 아이디어→실험 오케스트레이터 | 3 |
| **paper-draft** | 논문/보고서 초안 작성 | 3 |
| **data-acquisition** | 데이터 소스 통합 접근 | 1, 2, 3 (공통) |
| **notification** | Slack/Telegram 알림 | 1, 2, 3 (공통) |

### 구 버전 대비 변경사항

| 항목 | v1.0 (구 버전) | v2.0 (신 버전) |
|---|---|---|
| 상시운용 모드 | 있음 (24시간 자동 감시) | **제거** |
| 센티넬/예보문/사후분석 에이전트 | 있음 | **제거** |
| SW_monitor.py | 있음 | **제거** |
| 모델 아카이빙 | 없음 | **추가** |
| 아이디어→실험 | 없음 | **추가** |
| 논문 초안 작성 | 없음 | **추가** |
| 연구 업무 수행 | 있음 (보조 모드) | 있음 (**핵심 모드**) |
| 에이전트 수 | 9개 | 7개 |
| 스킬 수 | 4개 | 6개 |
