# SSWL 연구실을 위한 하네스 100가지 아이디어

> **참조**: [revfactory/harness-100](https://github.com/revfactory/harness-100) 의 패턴을
> SSWL(태양 및 우주환경연구실) 도메인에 맞게 변환·확장.
> 연구실 논문 51편(2019~2026)의 연구 분야를 기반으로 구성.

> **주의: 아래 100가지는 샘플(초안)입니다.**
> 실제 납품을 위해서는 연구실의 **기존 코드 헤리티지**를 분석하여
> 코드 기반의 하네스를 자동 생성해야 합니다.
> 해당 절차는 본 문서 하단의 [코드 → 하네스 자동 생성 절차](#코드--하네스-자동-생성-절차)를 참조하세요.

---

## 카테고리 1: 태양 데이터 처리 & 분석 (01~15)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 01 | `aia-multichannel-analyzer` | AIA 7채널 EUV 이미지 일괄 다운로드, 보정(aiapy), 정렬, 시각화 파이프라인 | Data-Fetcher, Calibrator, Aligner, Visualizer |
| 02 | `hmi-magnetogram-processor` | HMI 자기장 데이터 다운로드, 노이즈 제거, 활동영역 식별, 물리량 추출 | Data-Fetcher, Denoiser, AR-Detector, Physics-Extractor |
| 03 | `synoptic-map-builder` | Carrington Rotation 단위 synoptic map 자동 생성 (HMI/PHI 데이터) | Data-Fetcher, Preprocessor, Map-Generator, Visualizer |
| 04 | `solo-eui-pipeline` | Solar Orbiter EUI/FSI 데이터 수집, LL→L2 보정, SDO 대응 매핑 | SOAR-Fetcher, Calibrator, Cross-Calibrator, QA-Validator |
| 05 | `solo-phi-pipeline` | Solar Orbiter PHI/FDT 자기장 데이터 수집, 보정, HMI 비교 분석 | SOAR-Fetcher, Calibrator, Comparator, Report-Writer |
| 06 | `multi-source-data-merger` | SDO+Solar Orbiter+STEREO 다중 소스 관측 데이터 시공간 정합 및 병합 | Multi-Fetcher, Coordinate-Aligner, Temporal-Matcher, Merger |
| 07 | `fits-quality-inspector` | FITS 파일 배치 검증 (헤더, NaN, 크기, 시간 연속성) + 품질 보고서 | File-Scanner, Header-Validator, Data-Checker, Report-Writer |
| 08 | `solar-event-detector` | AIA/HMI 이미지에서 플레어, CME, 코로나홀, 필라멘트 자동 탐지 | Image-Analyzer, Flare-Detector, CH-Detector, Event-Logger |
| 09 | `coronal-hole-tracker` | 코로나홀 경계 자동 탐지 + 시계열 면적/위치 추적 + 태양풍 연결 | CH-Detector, Tracker, SW-Linker, Visualizer |
| 10 | `active-region-monitor` | NOAA AR 번호 기반 활동영역 데이터 자동 수집, 자기장 진화 추적 | AR-Identifier, Data-Fetcher, Evolution-Tracker, Report-Writer |
| 11 | `solar-wind-dashboard` | NOAA SWPC 실시간 태양풍 데이터 수집, 시각화, 트렌드 분석 대시보드 | SWPC-Fetcher, Plotter, Trend-Analyzer, Dashboard-Builder |
| 12 | `flare-catalog-builder` | GOES X선 플레어 목록 수집, AR 매칭, 통계 분석, 카탈로그 생성 | Flare-Fetcher, AR-Matcher, Statistician, Catalog-Writer |
| 13 | `stereo-euvi-processor` | STEREO/EUVI 데이터 수집, 보정, SDO/AIA와 시점 비교 분석 | SSC-Fetcher, Calibrator, Viewpoint-Comparator, Visualizer |
| 14 | `historical-data-restorer` | 역사적 태양 관측(갈릴레오 드로잉, 필름 등) → 현대 데이터 형식 변환 | Image-Digitizer, DL-Restorer, Validator, Archive-Manager |
| 15 | `data-gap-analyzer` | 특정 기간/기기의 데이터 가용성 조사, 갭 식별, 대체 소스 제안 | Availability-Checker, Gap-Identifier, Alternative-Finder, Report-Writer |

---

## 카테고리 2: 우주기상 예보 & 모니터링 (16~28)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 16 | `geomag-storm-forecaster` | 태양풍 파라미터 → 지자기폭풍(Kp/Dst) 예보 + 한국어 예보문 생성 | Data-Fetcher, Model-Runner, Forecast-Writer, Notifier |
| 17 | `solar-wind-predictor` | AIA EUV 이미지 → 태양풍 속도 3일 예측 (DL 모델) | AIA-Fetcher, Preprocessor, DL-Predictor, Visualizer |
| 18 | `imf-bz-predictor` | 6시간 IMF Bz 프로파일 예측 (강한 남향 케이스 특화) | SW-Fetcher, DL-Predictor, Uncertainty-Estimator, Alerter |
| 19 | `flare-probability-forecaster` | 활동영역 벡터 자기장 → 일일 M/X급 플레어 확률 예보 | HMI-Fetcher, Feature-Extractor, Flare-Predictor, Report-Writer |
| 20 | `sep-event-forecaster` | GOES X선 + 플레어 위치 → SEP 강도/도착시간 예측 | Flare-Analyzer, SEP-Predictor, Timeline-Generator, Alerter |
| 21 | `cme-arrival-predictor` | 코로나그래프 이미지 + CME 파라미터 → 지구 도달 시간 예측 | Coronagraph-Analyzer, CME-Parametrizer, Arrival-Predictor, Report-Writer |
| 22 | `tec-forecaster` | 전리층 TEC 1일 예측 (글로벌 맵) | GNSS-Fetcher, DL-Predictor, Map-Generator, Validator |
| 23 | `electron-density-modeler` | 전리층 3D 전자밀도 모델 구축 (COSMIC RO 데이터 기반) | RO-Fetcher, Model-Builder, 3D-Visualizer, Validator |
| 24 | `space-weather-bulletin` | 종합 우주기상 현황 보고서 자동 생성 (일일/주간/월간) | Multi-Fetcher, Condition-Assessor, Bulletin-Writer, Publisher |
| 25 | `alert-threshold-optimizer` | 과거 이벤트 분석 → 최적 알림 임계값 도출 (과탐/미탐 최소화) | Event-Historian, Threshold-Tester, ROC-Analyzer, Config-Writer |
| 26 | `ensemble-forecast-combiner` | 복수 예측 모델 결과 → 앙상블 예보 생성 + 불확실도 정량화 | Model-Runner(×N), Ensemble-Combiner, Uncertainty-Quantifier, Report-Writer |
| 27 | `forecast-verification` | 예보 vs 실측 비교 분석 (Kp, Dst, 태양풍, 플레어) + 성능 리포트 | Observation-Fetcher, Forecast-Fetcher, Comparator, Performance-Reporter |
| 28 | `nowcast-dashboard` | 현재 우주기상 상태 실시간 종합 대시보드 (태양풍/자기장/플레어/전리층) | Multi-Fetcher, Status-Assessor, Dashboard-Builder, Alert-Manager |

---

## 카테고리 3: 딥러닝 모델 개발 & 실험 (29~43)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 29 | `image-translation-trainer` | Pix2Pix/CycleGAN 태양 이미지 변환 모델 학습 파이프라인 (AIA↔HMI 등) | Data-Preparer, Architecture-Selector, Trainer, Evaluator |
| 30 | `channel-synthesizer` | EUI 2채널 → 합성 AIA 5채널 생성 (Pix2PixCC) 학습/추론 파이프라인 | Pix2PixCC-Trainer, Channel-Generator, Quality-Assessor, DEM-Validator |
| 31 | `super-resolution-trainer` | HMI/AIA 초해상도 모델 학습 (저해상도→고해상도) | Data-Augmentor, SR-Trainer, PSNR-Evaluator, Visual-Comparator |
| 32 | `farside-magnetogram-generator` | STEREO/EUV → 태양 뒷면 자기장 생성 DL 모델 학습/추론 | STEREO-Fetcher, DL-Trainer, Magnetogram-Generator, Validator |
| 33 | `dem-inversion-pipeline` | 다채널 EUV → DEM 역산 파이프라인 (정규화 역산 / DL 기반) | Channel-Preparer, DEM-Calculator, Error-Estimator, Visualizer |
| 34 | `nlfff-extrapolator` | 벡터 자기장 → NLFFF 외삽 (Physics-informed Neural Operator) | HMI-Fetcher, PINO-Runner, Field-Validator, 3D-Visualizer |
| 35 | `pfss-simulator` | Synoptic map → PFSS 코로나 자기장 시뮬레이션 + 시각화 | Map-Fetcher, PFSS-Runner, Open/Closed-Classifier, 3D-Renderer |
| 36 | `model-benchmark-suite` | 연구실 DL 모델 벤치마크 자동 수행 (CC, RMSE, SSIM 등) | Model-Loader, Test-Data-Preparer, Metric-Calculator, Leaderboard-Writer |
| 37 | `hyperparameter-tuner` | DL 모델 하이퍼파라미터 탐색 자동화 (Grid/Random/Bayesian) | Config-Generator, Trainer, Evaluator, Optimizer |
| 38 | `xai-solar-analyzer` | 태양 DL 모델 설명 가능성 분석 (Grad-CAM, SHAP, 물리 파라미터 연결) | Model-Loader, XAI-Calculator, Physics-Linker, Report-Writer |
| 39 | `ml-experiment-tracker` | DL 실험 기록 관리 (데이터, 하이퍼파라미터, 결과, 모델 체크포인트) | Experiment-Logger, Artifact-Manager, Comparison-Viewer, Report-Writer |
| 40 | `training-data-curator` | SDO/AIA/HMI 학습 데이터셋 큐레이션 (품질 필터링, 분할, 버전 관리) | Data-Scanner, Quality-Filter, Splitter, Version-Manager |
| 41 | `model-deployment-pipeline` | 학습 완료 모델 → 추론 서버 배포 (Docker, API 래핑, 모니터링) | Model-Packager, Docker-Builder, API-Wrapper, Monitor |
| 42 | `ablation-study-runner` | DL 모델 ablation study 자동 수행 (컴포넌트별 기여도 분석) | Config-Modifier, Batch-Trainer, Result-Comparator, Report-Writer |
| 43 | `transfer-learning-adapter` | SDO로 학습한 모델 → Solar Orbiter/STEREO 데이터에 전이 학습 | Source-Model-Loader, Target-Data-Preparer, Fine-Tuner, Performance-Comparator |

---

## 카테고리 4: 코로나/자기장 물리 연구 (44~53)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 44 | `coronal-3d-reconstructor` | 다시점 관측(SDO+STEREO+SolO) → 코로나 3D 밀도/온도 복원 | Multi-Fetcher, Tomography-Runner, 3D-Renderer, Validator |
| 45 | `mhd-simulation-runner` | MAS/Enlil 등 MHD 시뮬레이션 실행 + 결과 시각화 | Input-Preparer, MHD-Runner, Output-Processor, 3D-Visualizer |
| 46 | `magnetic-energy-calculator` | 활동영역 3D 자기 자유 에너지 계산 + 플레어 활동 상관 분석 | NLFFF-Runner, Energy-Calculator, Flare-Correlator, Report-Writer |
| 47 | `coronal-oscillation-analyzer` | 코로나 루프/플룸 진동 탐지, 주기 분석, 코로나 진동학 물리량 도출 | Time-Series-Extractor, Oscillation-Detector, Period-Analyzer, Physics-Calculator |
| 48 | `flux-transport-modeler` | Surface Flux Transport 모델로 다음 Carrington Rotation 자기장 예측 | SFT-Runner, Prediction-Generator, Validation-Comparator, Report-Writer |
| 49 | `open-field-mapper` | PFSS로 열린/닫힌 자기장 영역 매핑 → 코로나홀 경계 비교 | PFSS-Runner, Open/Closed-Mapper, CH-Boundary-Comparator, Visualizer |
| 50 | `cme-3d-reconstructor` | 다시점 코로나그래프 → CME 3D 형태 복원 (GCS 모델 등) | Multi-Coronagraph-Fetcher, GCS-Fitter, 3D-Renderer, Parameter-Extractor |
| 51 | `sep-source-tracer` | SEP 이벤트 → 자기력선 추적 → 소스 활동영역 역추적 | SEP-Fetcher, PFSS-Runner, Field-Line-Tracer, Source-Identifier |
| 52 | `spectral-line-analyzer` | 분광 데이터(Hα, Ca II 등) 역산, 물리량 추출, 시각화 | Spectral-Fetcher, Inversion-Runner, Physics-Extractor, Visualizer |
| 53 | `solar-cycle-analyzer` | 태양 주기별 활동 통계 (흑점, 플레어, CME, 우주기상 스케일 빈도) | Long-Term-Fetcher, Statistician, Cycle-Comparator, Report-Writer |

---

## 카테고리 5: 논문 & 연구 지원 (54~66)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 54 | `paper-draft-writer` | 실험 결과 → 학술 논문 초안 자동 생성 (IMRaD 구조) | Intro-Writer, Method-Writer, Result-Writer, Discussion-Writer |
| 55 | `literature-reviewer` | 키워드/주제 → ADS/arXiv 검색 → 선행연구 요약 및 분류 | ADS-Searcher, Abstract-Summarizer, Classifier, Review-Writer |
| 56 | `reference-manager` | BibTeX 참고문헌 자동 수집, 중복 제거, 포맷 변환, 인용 관리 | DOI-Resolver, BibTeX-Builder, Deduplicator, Format-Converter |
| 57 | `figure-generator` | 논문용 그래프/플롯 자동 생성 (matplotlib/sunpy 기반, 저널 스타일) | Data-Loader, Plot-Designer, Style-Applier, Multi-Panel-Arranger |
| 58 | `paper-proofreader` | 논문 영문 교정 (문법, 스타일, 학술 표현, 일관성 검토) | Grammar-Checker, Style-Reviewer, Consistency-Validator, Suggestion-Writer |
| 59 | `submission-preparer` | 저널 투고 준비 (포맷팅, 커버레터, 응답서, 체크리스트) | Format-Converter, Cover-Letter-Writer, Response-Drafter, Checklist-Validator |
| 60 | `proposal-writer` | 연구과제 제안서 작성 지원 (연구 배경, 방법, 일정, 예산) | Background-Researcher, Method-Writer, Timeline-Designer, Budget-Planner |
| 61 | `poster-designer` | 학회 포스터 내용 구성 (제목, 핵심 결과, 그래프 배치 설계) | Content-Organizer, Layout-Designer, Figure-Selector, Text-Writer |
| 62 | `presentation-builder` | 학회 발표 슬라이드 내용 구성 + 발표 스크립트 생성 | Storyboarder, Slide-Content-Writer, Script-Writer, Q&A-Preparer |
| 63 | `research-idea-brainstormer` | 연구 분야 + 최신 트렌드 → 새로운 연구 아이디어 브레인스토밍 | Trend-Analyzer, Gap-Identifier, Idea-Generator, Feasibility-Assessor |
| 64 | `paper-impact-tracker` | 연구실 논문 인용 추적, h-index, 공동연구 네트워크 분석 | ADS-Fetcher, Citation-Tracker, Network-Analyzer, Report-Writer |
| 65 | `lab-publication-dashboard` | 연구실 논문 현황 대시보드 (연도별, 분야별, 저자별 통계) | Publication-Fetcher, Statistician, Chart-Builder, Dashboard-Writer |
| 66 | `peer-review-assistant` | 논문 리뷰 지원 (방법론 검토, 통계 확인, 리뷰 코멘트 초안) | Method-Reviewer, Statistical-Checker, Comment-Drafter, Summary-Writer |

---

## 카테고리 6: 데이터 관리 & 인프라 (67~76)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 67 | `data-archive-manager` | 연구실 데이터 아카이브 관리 (메타데이터, 검색, 용량 관리) | Indexer, Metadata-Writer, Search-Builder, Storage-Monitor |
| 68 | `model-registry-manager` | 연구실 모델 레지스트리 관리 (등록, 카드 생성, 버전 관리) | Code-Analyzer, Card-Writer, Wrapper-Generator, Version-Manager |
| 69 | `environment-replicator` | Python 실행 환경 복제 (requirements.txt, conda env, Docker) | Dependency-Scanner, Environment-Builder, Test-Runner, Doc-Writer |
| 70 | `backup-scheduler` | 연구 데이터/코드/모델 백업 자동화 + 무결성 검증 | Backup-Planner, Executor, Integrity-Checker, Report-Writer |
| 71 | `disk-space-optimizer` | 워크스페이스 디스크 사용량 분석, 중복/불필요 파일 식별, 정리 제안 | Usage-Analyzer, Duplicate-Finder, Cleanup-Advisor, Report-Writer |
| 72 | `api-endpoint-monitor` | JSOC, SWPC, SOAR 등 외부 API 가용성 모니터링 + 장애 알림 | Health-Checker, Response-Timer, Alert-Manager, Status-Reporter |
| 73 | `notebook-to-script` | Jupyter notebook → 정리된 Python 스크립트/모듈 변환 | Code-Extractor, Refactorer, Docstring-Writer, Test-Generator |
| 74 | `code-documentation-generator` | 연구 코드에 자동 docstring, README, 사용 예제 생성 | Code-Analyzer, Docstring-Writer, README-Writer, Example-Generator |
| 75 | `gpu-job-scheduler` | GPU 서버 작업 큐 관리 (학습 작업 스케줄링, 리소스 모니터링) | Queue-Manager, Resource-Monitor, Job-Scheduler, Notifier |
| 76 | `reproducibility-checker` | 논문의 실험 재현성 검증 (데이터/코드/환경/결과 일치 확인) | Code-Runner, Data-Validator, Result-Comparator, Report-Writer |

---

## 카테고리 7: 시각화 & 커뮤니케이션 (77~85)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 77 | `solar-image-animator` | AIA/EUI 시계열 이미지 → 동영상(MP4/GIF) 자동 생성 | Image-Fetcher, Frame-Processor, Animator, Annotator |
| 78 | `multi-panel-figure-maker` | 복수 관측 데이터를 논문용 멀티패널 그래프로 자동 배치 | Data-Loader, Layout-Designer, Panel-Renderer, Label-Manager |
| 79 | `outreach-content-creator` | 태양 관측 이미지/영상을 대중 과학 콘텐츠(SNS, 블로그)로 변환 | Image-Selector, Caption-Writer, Format-Adapter, Hashtag-Generator |
| 80 | `weekly-lab-report` | 연구실 주간 보고서 자동 생성 (진행 현황, 관측 하이라이트, 논문 현황) | Activity-Collector, Highlight-Selector, Report-Writer, Publisher |
| 81 | `event-timeline-builder` | 태양 이벤트(플레어, CME) 타임라인 + 다중 관측 데이터 정합 시각화 | Event-Identifier, Timeline-Builder, Multi-Data-Aligner, Visualizer |
| 82 | `3d-corona-viewer` | 코로나 자기장/밀도 3D 인터랙티브 시각화 (VTK/Plotly) | Data-Loader, 3D-Renderer, Interactive-Builder, Export-Manager |
| 83 | `infographic-generator` | 우주기상 이벤트를 인포그래픽으로 자동 요약 | Event-Summarizer, Layout-Designer, Icon-Selector, Renderer |
| 84 | `comparison-plot-maker` | 두 데이터셋/모델 결과를 나란히 비교하는 플롯 자동 생성 | Data-Loader, Alignment-Checker, Comparison-Plotter, Annotation-Writer |
| 85 | `color-map-standardizer` | 태양 이미지 색상맵 표준화 (SDO 공식 색상, 논문 일관성) | Color-Map-Library, Image-Processor, Consistency-Checker, Batch-Applier |

---

## 카테고리 8: 교육 & 온보딩 (86~92)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 86 | `new-member-onboarding` | 신규 연구자 온보딩 (연구실 소개, 도구 사용법, 데이터 접근 가이드) | Content-Organizer, Tutorial-Writer, Quiz-Creator, Progress-Tracker |
| 87 | `sunpy-tutorial-generator` | sunpy/astropy/drms 사용법 튜토리얼 자동 생성 (예제 코드 포함) | Library-Analyzer, Tutorial-Writer, Code-Example-Generator, Tester |
| 88 | `model-usage-guide-writer` | 등록된 모델별 상세 사용 가이드 자동 생성 (입출력 예제, FAQ) | Model-Card-Reader, Guide-Writer, Example-Generator, FAQ-Builder |
| 89 | `journal-club-preparer` | 논문 읽기 모임 준비 자료 자동 생성 (요약, 핵심 질문, 토론 포인트) | Paper-Summarizer, Question-Generator, Context-Researcher, Handout-Writer |
| 90 | `coding-exercise-creator` | 태양 데이터 처리 코딩 연습 문제 자동 생성 (난이도별, 해답 포함) | Problem-Designer, Data-Selector, Solution-Writer, Grader |
| 91 | `research-method-explainer` | DEM, PFSS, NLFFF 등 연구 방법론을 초보자용으로 설명 문서 생성 | Method-Analyzer, Simplifier, Diagram-Creator, Example-Writer |
| 92 | `seminar-content-generator` | 연구실 세미나 발표 자료 + 질의응답 예상 + 핸드아웃 자동 생성 | Topic-Researcher, Slide-Writer, Q&A-Preparer, Handout-Writer |

---

## 카테고리 9: 위성 미션 & 관측 지원 (93~97)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 93 | `observation-planner` | 관측 캠페인 계획 (대상, 기기, 시간, 데이터량, 다운링크 예산) | Target-Selector, Instrument-Planner, Schedule-Optimizer, Budget-Calculator |
| 94 | `satellite-conjunction-finder` | SDO-Solar Orbiter-STEREO 정렬/대향 시점 자동 탐색 + 관측 기회 안내 | Orbit-Calculator, Conjunction-Detector, Opportunity-Assessor, Calendar-Writer |
| 95 | `instrument-channel-optimizer` | 위성 미션 EUV 채널 조합 최적화 (DL 기반 정보량 분석) | Channel-Analyzer, Information-Scorer, Combination-Tester, Recommendation-Writer |
| 96 | `l4-mission-science-planner` | L4 미션 과학 목표별 관측 시나리오 설계 + 기대 데이터 시뮬레이션 | Science-Objective-Mapper, Scenario-Designer, Data-Simulator, Report-Writer |
| 97 | `telemetry-analyzer` | 위성 텔레메트리 데이터 분석 (기기 상태, 온도, 전력, 이상 탐지) | Telemetry-Parser, Health-Checker, Anomaly-Detector, Alert-Manager |

---

## 카테고리 10: 연구실 운영 & 관리 (98~100)

| # | 하네스명 | 설명 | 핵심 에이전트 |
|---|---------|------|-------------|
| 98 | `lab-knowledge-base` | 연구실 지식 베이스 구축 (논문, 모델, 데이터, 노하우 통합 검색) | Knowledge-Collector, Taxonomy-Designer, Search-Builder, Maintenance-Manager |
| 99 | `meeting-minutes-writer` | 연구실 미팅 내용 → 회의록 + 액션 아이템 + 후속 추적 | Note-Organizer, Action-Extractor, Follow-Up-Tracker, Minutes-Writer |
| 100 | `research-roadmap-planner` | 연구실 중장기 연구 로드맵 설계 (트렌드 분석, 역량 매핑, 우선순위) | Trend-Researcher, Capability-Mapper, Priority-Ranker, Roadmap-Writer |

---

## 카테고리 분포 요약

| 카테고리 | 범위 | 개수 |
|---------|------|------|
| 태양 데이터 처리 & 분석 | 01~15 | 15 |
| 우주기상 예보 & 모니터링 | 16~28 | 13 |
| 딥러닝 모델 개발 & 실험 | 29~43 | 15 |
| 코로나/자기장 물리 연구 | 44~53 | 10 |
| 논문 & 연구 지원 | 54~66 | 13 |
| 데이터 관리 & 인프라 | 67~76 | 10 |
| 시각화 & 커뮤니케이션 | 77~85 | 9 |
| 교육 & 온보딩 | 86~92 | 7 |
| 위성 미션 & 관측 지원 | 93~97 | 5 |
| 연구실 운영 & 관리 | 98~100 | 3 |
| **합계** | | **100** |

---

## 현재 이미 구축된 하네스 (v2.0)

현재 SSWL-harness-ops v2.0에 포함된 기능과의 매핑:

| 현재 스킬/에이전트 | 관련 하네스 번호 |
|---|---|
| research-task (연구 업무 수행) | 03, 09, 33, 35 등 다수 |
| model-archive (모델 아카이빙) | 68 |
| idea-to-experiment (아이디어→실험) | 29~43 영역 |
| paper-draft (논문 초안) | 54 |
| data-acquisition (데이터 수집) | 01~06, 11 등 |
| notification (알림) | 16, 24, 28 등 |

> **다음 단계**: 위 100개 중 우선순위를 정하여 순차적으로 구축.
> 현재 v2.0의 범용 파이프라인(research-task)으로 상당수를 커버하지만,
> 특화 하네스는 더 정확하고 효율적인 결과를 제공할 수 있음.

---

# 현재 하네스의 구조적 한계: 툴체인 실행 레이어 부재

## 문제 인식

현재 SSWL-harness-ops v2.0의 구조:

```
.claude/agents/*.md    ← "역할 설명서" (이 에이전트는 이런 일을 한다)
.claude/skills/*.md    ← "워크플로우 설명" (이 순서로 진행한다)
```

**없는 것**: 실제 코드를 실행하는 **Tool(도구)** 과 **Flow(툴체인)** 레이어.

| 있는 것 | 없는 것 |
|---|---|
| "data-fetcher는 JSOC에서 데이터를 수집한다" (설명) | JSOC에서 AIA 193 다운로드하는 **실행 가능한 도구** |
| "model-runner는 모델을 실행한다" (설명) | `python3 run_dem.py --input X --output Y` 를 **자동으로 체이닝**하는 로직 |
| "task-executor가 순차 실행한다" (설명) | Step1 출력 → Step2 입력으로 **자동 연결**하는 파이프라인 |

**결과**: AI가 매번 즉흥적으로 코드를 작성하거나 찾아서 실행. 연구실의 기존 코드를 정확히 호출하지 못함.

## 어시웍스(AssiWorks) 참고: Tool → Flow → Agent → Team

[어시웍스](https://aifactory.space/guide/8/14)의 4계층 구조:

```
Layer 1: Tool (도구)         ← 실행 가능한 최소 단위 (API 호출, Python 스크립트, LLM 프롬프트)
Layer 2: Flow (툴체인)       ← Tool들을 순차/조건/병렬로 연결한 워크플로우
Layer 3: Agent (에이전트)    ← 자연어를 이해하고 적절한 Tool/Flow를 선택·실행
Layer 4: Team (팀)           ← 여러 Agent가 협업
```

**핵심 차이점**: 어시웍스는 **실행 가능한 Tool을 먼저 정의**하고, 그 위에 AI를 얹는다.
우리는 **AI 설명서만 있고**, 실행 가능한 Tool이 없다.

## 해결 방향: 3계층 하네스 아키텍처

현재 2계층(에이전트 + 스킬)에서 **3계층**으로 확장:

```
┌─────────────────────────────────────────────────────┐
│  Layer 3: Skills (오케스트레이터)                      │
│  "사용자 요청 → 어떤 Flow를 실행할지 판단"             │
│  .claude/skills/*/skill.md                           │
├─────────────────────────────────────────────────────┤
│  Layer 2: Agents (지능형 판단)                        │
│  "Flow 실행 중 예외 처리, 대안 탐색, 사용자 소통"       │
│  .claude/agents/*.md                                 │
├─────────────────────────────────────────────────────┤
│  Layer 1: Tools & Flows (실행 가능한 도구/툴체인)  ← 신규 │
│  "실제 코드를 래핑한 실행 단위 + 체이닝 정의"           │
│  .claude/skills/*/scripts/   (실행 가능한 도구)        │
│  .claude/skills/*/flows/     (툴체인 정의)            │
│  _workspace/model_registry/  (등록된 모델)            │
└─────────────────────────────────────────────────────┘
```

### Layer 1: Tool 정의 형식

각 Tool은 **실행 가능한 래퍼 스크립트** + **메타데이터**:

```yaml
# tools/fetch_aia.yaml
name: fetch_aia
description: "JSOC에서 AIA EUV 이미지를 다운로드한다"
type: python_script
script: scripts/fetch_aia.py
inputs:
  - name: wavelength
    type: int
    required: true
    description: "파장 (94, 131, 171, 193, 211, 304, 335)"
  - name: time_start
    type: string
    required: true
    description: "시작 시각 (ISO 형식)"
  - name: time_end
    type: string
    required: true
  - name: cadence
    type: string
    default: "15min"
  - name: output_dir
    type: path
    required: true
outputs:
  - name: fits_files
    type: directory
    description: "다운로드된 FITS 파일 디렉토리"
  - name: manifest
    type: json
    description: "다운로드 결과 매니페스트"
dependencies:
  - drms>=0.6.0
  - astropy>=5.0
timeout: 30min
```

```python
# scripts/fetch_aia.py
"""AIA EUV 이미지 다운로드 도구."""
import argparse
import drms
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wavelength", type=int, required=True)
    parser.add_argument("--time_start", required=True)
    parser.add_argument("--time_end", required=True)
    parser.add_argument("--cadence", default="15min")
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()

    client = drms.Client()
    query = f"aia.lev1_euv_12s[{args.time_start}/{args.time_end}@{args.cadence}][{args.wavelength}]{{image}}"
    # ... 실제 다운로드 로직 ...

    # 결과 매니페스트 출력 (다음 Tool의 입력)
    manifest = {"files": downloaded, "count": len(downloaded), "status": "success"}
    with open(Path(args.output_dir) / "manifest.json", "w") as f:
        json.dump(manifest, f)

if __name__ == "__main__":
    main()
```

### Layer 1: Flow (툴체인) 정의 형식

Tool들을 체이닝하는 **Flow 정의**:

```yaml
# flows/dem_pipeline.yaml
name: dem_pipeline
description: "EUI/FSI 데이터로 DEM을 계산하는 전체 파이프라인"
trigger_keywords:
  - "DEM 만들어"
  - "DEM 계산"
  - "differential emission measure"

steps:
  - name: fetch_data
    tool: fetch_aia
    params:
      wavelength: [171, 304]
      time_start: "{{user.time_start}}"
      time_end: "{{user.time_end}}"
      output_dir: "{{workspace}}/step1_data/"

  - name: preprocess
    tool: preprocess_aia
    depends_on: [fetch_data]
    params:
      input_dir: "{{steps.fetch_data.outputs.fits_files}}"
      output_dir: "{{workspace}}/step2_preprocessed/"
      target_resolution: 1024

  - name: generate_channels
    tool: pix2pixcc_inference
    depends_on: [preprocess]
    params:
      input_dir: "{{steps.preprocess.outputs.processed_dir}}"
      checkpoint_dir: "{{model_registry}}/pix2pixcc/checkpoints/"
      output_dir: "{{workspace}}/step3_generated/"
      channels: [94, 131, 193, 211, 335]

  - name: compute_dem
    tool: dem_inversion
    depends_on: [generate_channels]
    params:
      input_dir: "{{steps.generate_channels.outputs.channel_dir}}"
      output_dir: "{{workspace}}/step4_dem/"
      method: "hannah_kontar_2012"
      temp_range: [5.5, 7.5]

  - name: visualize
    tool: dem_visualizer
    depends_on: [compute_dem]
    params:
      dem_file: "{{steps.compute_dem.outputs.dem_fits}}"
      output_dir: "{{workspace}}/output/"

error_handling:
  fetch_data_failed: "대체 소스(VSO)로 재시도"
  generate_channels_failed: "체크포인트 확인 후 사용자에게 보고"

estimated_time: "40~60분"
```

### Tool과 Flow가 있으면 뭐가 달라지는가

| 현재 (설명서만) | Tool+Flow 도입 후 |
|---|---|
| AI가 "drms를 써서 다운로드해야지" → 즉석 코드 작성 | `fetch_aia` Tool 호출 → **검증된 코드** 즉시 실행 |
| Step간 데이터 전달을 AI가 매번 추론 | `{{steps.fetch_data.outputs.fits_files}}` → **자동 연결** |
| 같은 작업을 매번 다르게 실행 | Flow 정의로 **재현성 보장** |
| 에러 시 AI가 상황 판단부터 다시 | `error_handling` 미리 정의 → **일관된 복구** |
| 연구실 코드를 모르면 범용 코드로 시도 | Tool이 연구실 코드를 **직접 래핑** |

## Code Profile → Tool + Flow 변환

Phase 1(코드 분석)에서 생성한 **Code Profile**을 Tool과 Flow로 변환하는 추가 단계:

```
Code Profile
    │
    ├── 각 실행 step → Tool YAML + 래퍼 스크립트
    │   (prepare_data.py → tools/preprocess_aia.yaml + scripts/preprocess_aia.py)
    │
    ├── 전체 파이프라인 → Flow YAML
    │   (prepare→train→generate→dem → flows/dem_pipeline.yaml)
    │
    └── 모델/가중치 → model_registry 등록
        (checkpoints/*.pt → model_registry/pix2pixcc/)
```

---

# 코드 → 하네스 자동 생성 절차 (개정)

위 100가지 아이디어는 **도메인 지식 기반 샘플**이다.
실제로 연구실에 납품할 하네스는 연구실의 **기존 코드를 읽고** 자동 생성해야 의미가 있다.
코드를 모르는 상태에서 만든 하네스는 껍데기일 수 밖에 없기 때문이다.

아래는 "코드 헤리티지 → 하네스 자동 생성"까지의 전체 절차를 정리한 것이다.
**Tool/Flow(툴체인) 레이어 생성**이 추가되었다.

---

## 왜 코드를 먼저 읽어야 하는가

| 샘플 하네스 (현재) | 코드 기반 하네스 (목표) |
|---|---|
| "synoptic map 만드는 하네스" (일반적 설명) | `lab_code/synoptic/make_synmap.py`의 실제 인자, 의존성, 출력 형식을 반영한 하네스 |
| 에이전트가 "sunpy를 쓸 것이다" (추측) | 실제 코드가 `drms` + 커스텀 보간을 쓰는 것을 반영 |
| 입력이 "HMI 자기장" (모호) | `hmi.synoptic_mr_polfil_720s[CR]/Br` 시리즈, FITS 헤더 `CRLN_OBS` 필요 |

**코드를 읽지 않으면**: 사용자가 "synoptic map 만들어줘"라고 했을 때 AI가 일반적인 방법을 시도한다.
**코드를 읽으면**: 연구실의 `make_synmap.py`를 정확히 호출하고, 해당 코드의 인자/형식에 맞춘다.

---

## 전체 절차 개요

```
Phase 0        Phase 1           Phase 2          Phase 2.5          Phase 3          Phase 4
코드 수집  ──▶  코드 분석   ──▶  하네스 설계  ──▶  Tool/Flow 생성 ──▶ 에이전트 생성 ──▶ 검증/배포

(어디에       (뭘 하는       (어떤 하네스로   (실행 가능한     (에이전트/     (테스트 +
 뭐가 있나)    코드인가)       묶을 것인가)     도구+툴체인)     스킬 .md 생성)  피드백 루프)
```

> **Phase 2.5가 핵심 추가사항**: Code Profile의 각 실행 step을 **Tool YAML + 래퍼 스크립트**로,
> 전체 파이프라인을 **Flow YAML**로 변환한다. 이것이 있어야 에이전트가 "설명"이 아닌 "실행"을 한다.

---

## Phase 0: 코드 수집 — "연구실에 뭐가 있는가"

### 목표
연구실의 모든 코드 자산을 한 곳에서 파악할 수 있게 한다.

### 절차

1. **코드 저장소 목록화**
   - GitHub/GitLab 조직 내 모든 repo 목록
   - 개인 PC/서버에 있는 비버전관리 코드 (이것이 핵심 — 대부분 여기에 있음)
   - 공유 서버 (`/home/lab/`, `/data/models/` 등)의 스크립트

2. **코드 인벤토리 작성**
   ```
   _workspace/code_inventory/
   ├── inventory.json          # 전체 코드 목록
   ├── repo_map.md             # 저장소별 개요
   └── orphan_scripts.md       # 버전관리 안 된 코드 목록
   ```

3. **접근 권한 확보**
   - 각 연구자의 코드 경로에 읽기 권한
   - 필요 시 연구자에게 코드 위치/용도 인터뷰

### 산출물
```json
{
  "repositories": [
    {
      "path": "/home/researcher_a/dem_inversion/",
      "owner": "윤준무",
      "description": "EUI→합성 채널→DEM 파이프라인",
      "last_modified": "2025-12-15",
      "vcs": "git",
      "related_papers": ["Youn et al. 2025 A&A"]
    },
    {
      "path": "/home/researcher_b/flare_forecast/",
      "owner": "이강우",
      "description": "플레어 예보 강화학습 모델",
      "last_modified": "2023-08-20",
      "vcs": "none",
      "related_papers": ["Yi et al. 2023 ApJS"]
    }
  ]
}
```

> **현실적 문제**: 연구실 코드의 80%는 개인 PC에 있고, README도 없고,
> 개발자만 실행 방법을 안다. 이것이 바로 이 절차가 필요한 이유이다.

---

## Phase 1: 코드 분석 — "이 코드가 뭘 하는가"

### 목표
각 코드의 입력, 출력, 의존성, 실행 방법, 도메인 역할을 파악한다.

### 자동 분석 항목

AI(Claude Code)가 각 코드를 읽고 다음을 추출한다:

| 분석 항목 | 방법 | 예시 |
|---|---|---|
| **진입점(entry point)** | `if __name__`, `argparse`, `click` 탐색 | `main.py --input_dir X --output_dir Y` |
| **입력 데이터** | `open()`, `fits.open()`, `pd.read_csv()`, `argparse` 인자 | AIA 193 A FITS 파일, 디렉토리 경로 |
| **출력 데이터** | `savefig()`, `fits.writeto()`, `to_csv()`, `print()` | DEM map FITS + PNG |
| **의존성** | `import` 문, `requirements.txt`, `setup.py` | sunpy, astropy, torch, demregpy |
| **데이터 소스** | `drms.Client()`, `Fido.search()`, `requests.get()` URL 패턴 | JSOC `aia.lev1_euv_12s`, SOAR TAP |
| **모델/가중치** | `torch.load()`, `model.load_state_dict()`, `.h5`, `.pt` 파일 | `checkpoints/pix2pixcc_94A.pt` |
| **실행 환경** | GPU 사용(`torch.cuda`), 메모리 패턴, 멀티프로세싱 | GPU 필수, ~8GB VRAM |
| **도메인 분류** | import 패턴 + 변수명 + 주석으로 추론 | DEM, 플레어 예보, 자기장 외삽 등 |

### 분석 결과 형식: Code Profile

각 코드에 대해 **Code Profile**을 생성한다:

```markdown
# Code Profile: dem_inversion

## 기본 정보
- **경로**: /home/youn_j/dem_inversion/
- **소유자**: 윤준무
- **관련 논문**: Youn et al. 2025, A&A, 695, A125
- **마지막 수정**: 2025-12-15
- **코드 규모**: 12개 파일, 2,400줄

## 파이프라인 구조
```
prepare_data.py  →  train_pix2pixcc.py  →  generate_channels.py  →  compute_dem.py
(데이터 전처리)     (모델 학습)             (채널 합성)               (DEM 계산)
```

## 입력
| 입력 | 형식 | 소스 | 필수 |
|---|---|---|---|
| AIA 171 A 이미지 | FITS (4096x4096) | JSOC `aia.lev1_euv_12s` | 예 |
| AIA 304 A 이미지 | FITS (4096x4096) | JSOC `aia.lev1_euv_12s` | 예 |
| AIA 94/131/193/211/335 A | FITS | JSOC | 학습 시에만 |

## 출력
| 출력 | 형식 | 설명 |
|---|---|---|
| 합성 채널 (5개) | FITS (1024x1024) | AI 생성 AIA 등가 채널 |
| DEM map | FITS | 온도별 EM 분포 |
| DEM 시각화 | PNG | 온도 맵 |

## 의존성
```
torch>=1.9.0
sunpy>=5.0.0
astropy>=5.0
demregpy>=1.0
aiapy>=0.7.0
```

## 실행 방법
```bash
# 1. 데이터 준비
python prepare_data.py --start_date 2021-01-01 --end_date 2021-12-31

# 2. 학습 (GPU 필요)
python train_pix2pixcc.py --target_channel 94 --epochs 200 --gpu 0

# 3. 채널 생성
python generate_channels.py --input_dir data/test/ --checkpoint checkpoints/best.pt

# 4. DEM 계산
python compute_dem.py --input_dir generated/ --output_dir dem_results/
```

## 주의사항
- 학습 데이터는 2011~2021 (1일 1장, 00:00 UT)
- 이미지는 1024x1024로 리사이즈
- 94 A 채널은 CC가 가장 낮음 (0.87)
- FSI 174→AIA 171 intercalibration에 0.7 factor 필요
```

### 분석 도구: `code-profiler` 에이전트

이 분석을 자동화하는 전용 에이전트를 만든다:

```markdown
---
name: code-profiler
description: >
  연구 코드를 분석하여 Code Profile을 자동 생성하는 에이전트.
  진입점, 입출력, 의존성, 실행 방법, 도메인 분류를 추출한다.
---
```

**분석 전략**:
1. 디렉토리 구조 스캔 (`*.py`, `*.ipynb`, `requirements.txt`, `README*`)
2. 각 Python 파일의 import, 함수 시그니처, argparse 인자 추출
3. 데이터 I/O 패턴 탐지 (FITS, CSV, JSON, HDF5)
4. DL 모델 패턴 탐지 (PyTorch/TF load/save)
5. 실행 순서 추론 (파일 간 의존성, 넘버링, README 참조)
6. 도메인 분류 (변수명 `aia`, `hmi`, `dem`, `flare` 등 + 논문 매칭)

---

## Phase 2: 하네스 설계 — "어떤 하네스로 묶을 것인가"

### 목표
분석된 Code Profile들을 하네스 단위로 그루핑하고, 에이전트/스킬 구조를 설계한다.

### 그루핑 기준

| 기준 | 설명 | 예시 |
|---|---|---|
| **파이프라인 단위** | 하나의 end-to-end 워크플로우 | `prepare→train→generate→dem` = 1 하네스 |
| **공유 입력** | 같은 데이터를 쓰는 코드끼리 | AIA 193 쓰는 코드들 → 코로나홀/DEM/플레어 |
| **공유 출력** | 한 코드의 출력이 다른 코드의 입력 | synoptic map → PFSS → open field mapping |
| **논문 단위** | 같은 논문에 속하는 코드 | Youn et al. 2025의 전체 코드 = 1 하네스 |
| **도메인 클러스터** | 같은 연구 분야 | 플레어 예보 관련 코드 3개 → 1 하네스 |

### 설계 결정 사항

각 하네스에 대해 결정할 것:

```
1. 실행 모드 선택
   ├── Sub-agent (단순 순차 실행) — 코드 1~2개, 파이프라인 단순
   └── Agent Team (협업 실행) — 코드 3개 이상, 병렬/분기 존재

2. 에이전트 분리 기준
   ├── 코드 파일 1개 = 에이전트 1개? (너무 세분화)
   └── 파이프라인 단계 = 에이전트 1개 (권장)
       예: data-fetch / preprocess / model-run / postprocess

3. 기존 범용 에이전트 재사용 vs 전용 에이전트 생성
   ├── data-fetcher, model-runner → 재사용 (코드 래퍼만 추가)
   └── 도메인 특화 로직 → 전용 에이전트 (dem-calculator 등)

4. 스킬 구성
   ├── 오케스트레이터 스킬 (워크플로우 정의)
   └── 참조 스킬 (코드 사용법, 데이터 형식 등)
```

### 설계 산출물: Harness Blueprint

```markdown
# Harness Blueprint: eui-dem-pipeline

## 출처 코드
- /home/youn_j/dem_inversion/ (Code Profile 참조)

## 사용자 시나리오
"Solar Orbiter EUI 데이터로 DEM 만들어줘"

## 에이전트 구성
| 에이전트 | 역할 | 출처 코드 | 기존 재사용 |
|---|---|---|---|
| data-fetcher | AIA/EUI 데이터 수집 | - | 재사용 |
| eui-preprocessor | EUI→AIA 보정, 리사이즈 | prepare_data.py | 신규 |
| pix2pixcc-runner | 합성 채널 생성 | generate_channels.py | 신규 (model-runner 확장) |
| dem-calculator | DEM 역산 | compute_dem.py | 신규 |
| result-reporter | 결과 보고 | - | 재사용 |

## 워크플로우
data-fetcher → eui-preprocessor → pix2pixcc-runner → dem-calculator → result-reporter

## 모델 레지스트리 등록
- pix2pixcc_94A.pt, pix2pixcc_131A.pt, ... (5개 체크포인트)
- model_card.md 자동 생성
```

---

## Phase 3: 자동 생성 — "에이전트/스킬 .md를 자동 작성"

### 목표
Blueprint를 바탕으로 `.claude/agents/*.md`, `.claude/skills/*/skill.md` 파일을 자동 생성한다.

### 생성 대상

| 생성물 | 내용 | 생성 방법 |
|---|---|---|
| **에이전트 .md** | 역할, 원칙, 입출력 프로토콜, 실행 명령어 | Code Profile → 템플릿 채우기 |
| **스킬 .md** | 오케스트레이터 워크플로우, Phase 정의 | Blueprint → 템플릿 채우기 |
| **model_card.md** | 모델 카드 (입출력, 의존성, 실행법) | Code Profile에서 직접 추출 |
| **run.sh** | 실행 래퍼 스크립트 | argparse/실행 명령어에서 생성 |

### 에이전트 자동 생성 템플릿

Code Profile의 각 단계를 에이전트 .md로 변환하는 규칙:

```
Code Profile의 "실행 방법" 각 step
    ↓
---
name: {step_name}
description: >
  {Code Profile의 해당 step 설명}.
  {입력 데이터 요약}을 받아 {출력 데이터 요약}을 생성한다.
---

# {Step Name}

## 핵심 역할
{Code Profile 설명에서 추출}

## 실행 명령어
```bash
{Code Profile의 실행 방법에서 해당 step}
```

## 입력
{Code Profile의 입력 테이블에서 해당 step 관련 항목}

## 출력
{Code Profile의 출력 테이블에서 해당 step 관련 항목}

## 의존성
{Code Profile의 의존성에서 해당 step import에 사용되는 것만}
```

### 생성 도구: `harness-generator` 에이전트

```markdown
---
name: harness-generator
description: >
  Code Profile과 Harness Blueprint를 읽어
  에이전트/스킬 .md 파일을 자동 생성하는 에이전트.
---
```

---

## Phase 4: 검증 & 배포 — "실제로 돌아가는가"

### 검증 단계

```
1. 정적 검증 (즉시)
   ├── 생성된 .md 파일의 YAML frontmatter 유효성
   ├── 참조하는 코드 경로가 실제 존재하는지
   ├── 의존성 패키지가 설치되어 있는지
   └── 실행 명령어 문법 오류 없는지

2. 드라이런 검증 (수 분)
   ├── 샘플 데이터(소량)로 파이프라인 실행
   ├── 각 단계의 출력이 다음 단계 입력과 호환되는지
   └── 에러 없이 end-to-end 통과하는지

3. 사용자 검증 (피드백)
   ├── 코드 소유자(개발자)에게 생성된 하네스 리뷰 요청
   ├── "이 하네스가 당신 코드를 정확히 반영하는가?"
   └── 피드백 → Phase 2로 돌아가 수정
```

### 배포

검증 통과 시:
1. `.claude/agents/`에 에이전트 .md 추가
2. `.claude/skills/`에 스킬 .md 추가
3. `_workspace/model_registry/`에 모델 카드 + 래퍼 등록
4. `CLAUDE.md` 업데이트 (새 하네스 목록 반영)

---

## 전체 프로세스를 자동화하는 메타-하네스

위 Phase 0~4 전체를 **하나의 하네스**로 만들 수 있다:

```
harness-factory/
├── skill.md                    # 오케스트레이터
├── agents/
│   ├── code-profiler.md        # Phase 1: 코드 분석
│   ├── harness-designer.md     # Phase 2: 하네스 설계
│   ├── harness-generator.md    # Phase 3: .md 파일 생성
│   └── harness-validator.md    # Phase 4: 검증
```

### 사용 시나리오

```
사용자: "연구실 코드를 하네스로 만들어줘"

  [harness-factory 오케스트레이터]

  Phase 0: "코드가 어디에 있나요?"
  사용자: "/home/youn_j/dem_inversion/"

  Phase 1: [code-profiler]
  → 코드 읽기: 12개 파일 분석
  → Code Profile 생성
  → "이 코드는 EUI DEM 파이프라인입니다. 4단계로 구성됩니다."

  Phase 2: [harness-designer]
  → Blueprint 생성
  → "다음과 같이 하네스를 설계했습니다: ..."
  → 사용자 승인

  Phase 3: [harness-generator]
  → 에이전트 3개 + 스킬 1개 + 모델 카드 5개 자동 생성
  → "생성 완료. .claude/agents/에 3개 파일, .claude/skills/에 1개 추가."

  Phase 4: [harness-validator]
  → 정적 검증 통과
  → 드라이런: 샘플 1일 데이터로 파이프라인 테스트
  → "검증 완료. 모든 단계 정상 통과."

  → 배포 완료!
```

---

## 현실적 고려사항

### 연구실 코드의 전형적인 상태

| 상태 | 빈도 | 대응 |
|---|---|---|
| README 없음 | 매우 높음 | code-profiler가 코드에서 직접 추론 |
| argparse 없음 (하드코딩) | 높음 | 하드코딩된 경로/파라미터를 식별하여 인자화 제안 |
| requirements.txt 없음 | 높음 | import 문에서 자동 생성 |
| Jupyter notebook만 존재 | 중간 | notebook→스크립트 변환 후 분석 |
| 코드가 깨져있음 (구버전 의존성) | 중간 | 의존성 충돌 식별, 수정 제안 |
| 개발자가 졸업/퇴사 | 높음 | 코드만으로 분석해야 하므로 Phase 1이 핵심 |

### 우선순위 결정 기준

모든 코드를 한꺼번에 하네스로 만들 수는 없다. 우선순위:

```
1순위: 현재 활발히 사용 중인 코드 (연구자 요청 빈도 높음)
2순위: 논문에 공개된 코드 (재현성 요구)
3순위: 여러 연구자가 공통으로 쓰는 유틸리티
4순위: 역사적 코드 (졸업생 코드 보존)
```

---

## 요약: 납품까���의 로드맵

```
Step 1. ���드 수집        연구자 인터뷰 + 서버 스캔 → inventory.json
        (1~2일)

Step 2. 코드 분석        code-profiler로 각 ���드 → Code Profile 생성
        (코드��� 10~30분)  연구실 전체 예상: 2~3일

Step 3. 하네스 설계      Code Profile → Blueprint 그루핑
        (1일)            연구자 리뷰 + 피드백

Step 4. Tool/Flow 생성   각 코드 step → Tool YAML + 래퍼 스크립트   ← 신규
        (코드당 15~30분)  파이프라인 → Flow YAML
                         연구실 전체 예상: 2~3일

Step 5. 에이전트 생성    Blueprint → 에이전트/스킬 .md + model_card
        (코드당 5~10분)   연구실 전체 ��상: 1일

Step 6. 검증/���포        Tool 단위 테스트 + Flow 드라이런 +
        (2~3��)          사용자 검증 + 피드백 반영

총 예상: 2~3주 (코드 규모에 따라 변동)
```

### Tool/Flow 레이어가 추가된 최종 디렉토리 구조

```
SSWL-harness-ops/
├── CLAUDE.md
├── scenarios.md
├── pamphlet.md
├── publications.md
├── .claude/
│   ���── agents/                    # Layer 2: 지능형 판단
│   │   ├── query-planner.md
│   │   ├── data-fetcher.md
│   │   ├── model-runner.md
│   │   ├── task-executor.md
│   │   ├── result-reporter.md
│   │   ├── skill-archivist.md
│   │   └── research-assistant.md
│   └── skills/                    # Layer 3: 오케스트레이터
│       ├── research-task/
│       │   ├��─ skill.md           # 워크플로우 설명
│       │   ├── tools/             # ← 신규: Layer 1 실행 도구
│       │   │   ├── fetch_aia.yaml
│       ��   │   ├── fetch_hmi.yaml
│       │   │   ├── preprocess.yaml
│       │   │   └── ...
│       │   ├── flows/             # ← ���규: Layer 1 툴체인 정의
│       │   │   ├── synoptic_map_pipeline.yaml
│       │   │   ├── pfss_pipeline.yaml
│       │   │   └── ...
│       │   └── scripts/           # ← 신규: 실행 가능한 래퍼 스크립트
│       │       ├── fetch_aia.py
│       │       ├── fetch_hmi.py
│       │       ├── preprocess.py
│       │       └── ...
│       ├── model-archive/
│       │   ├── skill.md
│       │   ├── tools/
│       │   └── scripts/
│       ├── idea-to-experiment/
│       │   ├── skill.md
���       │   ├── flows/
│       │   └── scripts/
│       └── ...
└── _workspace/
    └── model_registry/            # 등록된 모델 (Tool로 래핑됨)
        ├── pix2pixcc/
        ��   ├── model_card.md
        │   ├── tool.yaml          # ← 신규: Tool 정의
        │   ├── run.sh
        │   └── checkpoints/
        └── ...
```
