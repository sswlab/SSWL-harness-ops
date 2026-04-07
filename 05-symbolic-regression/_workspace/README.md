# _workspace — 빈 스캐폴드

이 디렉토리는 **빈 템플릿**입니다. 실제 실행 결과는 사용자가 지정한 `{작업경로}`에 저장됩니다.

## 표준 구조

```
{작업경로}/
├── 01_diagnosis.md              # sr-planner: 데이터 진단
├── 02_routing_plan.md           # sr-planner: 도구 라우팅 + 실행 계획
├── 03_execution_log.md          # sr-executor: 실행 환경/시간/에러
├── 04_expression_analysis.md    # expression-analyst: 단순화·동등성·Pareto
├── 05_report.md                 # sr-reporter: 최종 보고서
├── research-note.md             # 공통: 모든 판단의 흐름 누적 기록
│
├── data/                        # 입력 데이터 (사용자 제공)
├── code/                        # 실행 코드
│   ├── config.py
│   ├── data_loader.py
│   ├── run_pysr.py
│   ├── run_dso.py
│   ├── run_nesymres.py
│   ├── run_kan.py
│   ├── run_feynman.py
│   ├── run_sindy.py
│   ├── run_deap.py
│   ├── collect_results.py
│   └── orchestrate.py
├── results/
│   ├── pysr/        candidates.json, hall_of_fame.csv, log.txt
│   ├── dso/         candidates.json, ...
│   ├── nesymres/    candidates.json, ...
│   ├── kan/         candidates.json, ...
│   ├── feynman/     candidates.json, ...
│   ├── sindy/       candidates.json, ...
│   ├── deap/        candidates.json, ...
│   ├── all_candidates.json       # 통합
│   ├── pareto.csv
│   └── equivalence_clusters.json
├── figures/                     # DPI=300 PNG
│   ├── fig01_pareto.png
│   ├── fig02_best_fit.png
│   ├── fig03_residual.png
│   ├── fig04_tool_comparison.png
│   └── fig05_learning_curves.png
└── tables/                      # CSV + Markdown
    ├── tab01_recommended_expressions.{csv,md}
    ├── tab02_tool_summary.{csv,md}
    └── tab03_pareto_full.{csv,md}
```
