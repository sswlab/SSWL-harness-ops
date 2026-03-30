# SSWL 연구실을 위한 하네스 100가지 아이디어

> **참조**: [revfactory/harness-100](https://github.com/revfactory/harness-100) 의 패턴을
> SSWL(태양 및 우주환경연구실) 도메인에 맞게 변환·확장.
> 연구실 논문 51편(2019~2026)의 연구 분야를 기반으로 구성.

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
