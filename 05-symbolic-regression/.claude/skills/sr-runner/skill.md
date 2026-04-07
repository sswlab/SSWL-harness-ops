---
name: sr-runner
description: >
  PySR, DSO, NeSymReS, pykan, AI Feynman, PySINDy, DEAP를 표준 인터페이스로 실행하는
  방법을 정리한 reference. 각 도구의 설치, 호출 패턴, 출력 변환을 포함한다.
  키워드: PySR 사용법, DSO 사용법, NeSymReS, pykan KAN, AI Feynman, PySINDy, DEAP, SR 도구 실행
---

# sr-runner — SR 도구 실행 reference

이 skill은 sr-executor 에이전트가 각 SR 도구를 호출할 때 참조하는 가이드입니다.
**모든 도구의 출력은 다음 표준 스키마로 변환**되어 `results/<tool>/candidates.json`에 저장됩니다.

```json
{
  "tool": "<name>",
  "expression": "<sympy-parseable string>",
  "complexity": <int>,
  "train_r2": <float>,
  "val_r2": <float>,
  "train_mse": <float>,
  "val_mse": <float>,
  "wall_time_sec": <float>,
  "seed": <int>,
  "extra": { ... }
}
```

---

## 1. PySR (디폴트 워크호스)

### 설치
```bash
pip install pysr
python -c "import pysr; pysr.install()"   # Julia 백엔드 자동 설치
```

### 호출
```python
from pysr import PySRRegressor
import time

model = PySRRegressor(
    niterations=40,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["sin", "cos", "exp", "log", "sqrt"],
    extra_sympy_mappings={},
    populations=20,
    population_size=33,
    maxsize=30,
    timeout_in_seconds=600,    # 시간 예산
    random_state=42,
    deterministic=True,
    procs=0,
)

t0 = time.time()
model.fit(X_train, y_train)
wall = time.time() - t0

# 후보 수집 (Pareto front)
hof = model.equations_   # DataFrame: complexity, loss, sympy_format, ...
```

### 표준 변환
```python
candidates = []
for _, row in hof.iterrows():
    expr_str = str(row["sympy_format"])
    candidates.append({
        "tool": "pysr",
        "expression": expr_str,
        "complexity": int(row["complexity"]),
        "train_mse": float(row["loss"]),
        "wall_time_sec": wall,
        "seed": 42,
        "extra": {"score": float(row.get("score", 0))},
    })
```
val 메트릭은 collect_results 단계에서 hold-out 데이터로 별도 계산.

### 주의
- 첫 실행 시 Julia 컴파일로 1~3분 소요
- `procs=0`로 두면 가용 코어 사용
- maxsize는 표현 복잡도 상한 — 도메인에 맞게 조정

---

## 2. DSO/DSR (RL + RNN)

### 설치
```bash
pip install dso   # 또는 GitHub: brendenpetersen/deep-symbolic-optimization
```

### 호출
```python
from dso import DeepSymbolicRegressor
import time

config = {
    "task": {
        "task_type": "regression",
        "function_set": ["add", "sub", "mul", "div", "sin", "cos", "exp", "log"],
        "metric": "inv_nrmse",
        "threshold": 1e-6,
    },
    "training": {
        "n_samples": 200000,
        "batch_size": 1000,
        "epsilon": 0.05,
    },
    "controller": {"learning_rate": 0.0005},
}

model = DeepSymbolicRegressor(config)
t0 = time.time()
model.fit(X_train, y_train)
wall = time.time() - t0

best_program = model.program_   # 최적 프로그램
expr_str = str(best_program.sympy_expr)
```

### 표준 변환
DSO는 보통 best 1개를 반환. 여러 후보가 필요하면 hall_of_fame 활용:
```python
candidates = []
for prog in model.hof[:10]:
    candidates.append({
        "tool": "dso",
        "expression": str(prog.sympy_expr),
        "complexity": prog.length,
        "train_r2": prog.r,
        "wall_time_sec": wall,
        "seed": 42,
    })
```

### 주의
- RL 학습이라 시간이 김 (GPU 권장)
- 기본 config는 toy 데이터용 — 실제 데이터는 n_samples 늘릴 것

---

## 3. NeSymReS (Transformer pre-trained)

### 설치
```bash
git clone https://github.com/SymposiumOrganization/NeuralSymbolicRegressionThatScales
pip install -e .
# 사전학습 가중치 별도 다운로드 (10M / 100M)
```
**가중치는 첫 사용 시 사용자에게 다운로드 출처/라이선스를 알릴 것.**

### 호출
```python
from nesymres.architectures.model import Model
from nesymres.dclasses import FitParams, BFGSParams
import torch

bfgs = BFGSParams(activated=True, n_restarts=10, add_coefficients_if_not_existing=False)
params = FitParams(
    word2id=word2id,
    id2word=id2word,
    una_ops=una_ops,
    bin_ops=bin_ops,
    total_variables=list(eq_setting["total_variables"]),
    total_coefficients=list(eq_setting["total_coefficients"]),
    rewrite_functions=list(eq_setting["rewrite_functions"]),
    bfgs=bfgs,
    beam_size=cfg.inference.beam_size,
)
model = Model.load_from_checkpoint(ckpt_path, cfg=cfg.architecture)
model.eval()

t0 = time.time()
output = model.fitfunc(X_train, y_train)
wall = time.time() - t0
expr_str = str(output["best_bfgs_preds"][0])
```

### 표준 변환
beam의 top-k를 후보로 저장.

### 주의
- 입력 차원 D ≤ 5에서만 잘 작동 (사전학습 가정)
- 데이터 정규화 필요 (보통 [-1, 1])

---

## 4. pykan (KAN)

### 설치
```bash
pip install pykan
```

### 호출
```python
from kan import KAN
import torch
import time

model = KAN(width=[D, 5, 1], grid=5, k=3, seed=42)
dataset = {
    "train_input": torch.tensor(X_train).float(),
    "train_label": torch.tensor(y_train).float().unsqueeze(-1),
    "test_input":  torch.tensor(X_val).float(),
    "test_label":  torch.tensor(y_val).float().unsqueeze(-1),
}

t0 = time.time()
model.train(dataset, opt="LBFGS", steps=50)
# 활성 함수 후보를 SR로 자동 매칭
model.auto_symbolic(lib=["x", "x^2", "x^3", "exp", "log", "sin", "cos", "sqrt"])
formula = model.symbolic_formula()[0][0]
wall = time.time() - t0
expr_str = str(formula)
```

### 표준 변환
KAN은 단일 closed-form expression을 반환.

### 주의
- 차원이 크면 width를 [D, 5, 5, 1]처럼 늘려야 함
- auto_symbolic의 lib를 도메인에 맞게 조정

---

## 5. AI Feynman (물리 특화, 단위 정보 활용)

### 설치
```bash
git clone https://github.com/SJ001/AI-Feynman
cd AI-Feynman && pip install -e .
```

### 호출
- 데이터 파일 형식: `x1 x2 ... xD y` (공백 구분)
- 단위 파일 (선택): 각 변수의 SI 차원 벡터

```python
from aifeynman import run_aifeynman
import time

t0 = time.time()
run_aifeynman(
    pathdir="data/",
    filename="dataset.txt",
    BF_try_time=60,
    BF_ops_file_type="14ops.txt",
    polyfit_deg=4,
    NN_epochs=400,
)
wall = time.time() - t0
# 결과는 results/solution_<filename>.txt 에 후보 수식 목록으로 저장
```

### 표준 변환
solution 파일을 파싱해 후보 리스트로 변환.

### 주의
- 단위 파일이 있으면 dimensional analysis로 탐색 공간이 크게 줄어듦
- 시간 소요가 큼 (수십 분 ~ 수 시간)
- **단위 정보가 없으면 사용하지 말 것** — sr-planner에서 게이트

---

## 6. PySINDy (시계열·동역학)

### 설치
```bash
pip install pysindy
```

### 호출
```python
import pysindy as ps
import numpy as np
import time

# X: (T, D) 시계열, t: 시간 벡터
optimizer = ps.STLSQ(threshold=0.1)
feature_library = ps.PolynomialLibrary(degree=3) + ps.FourierLibrary(n_frequencies=2)
model = ps.SINDy(
    feature_library=feature_library,
    optimizer=optimizer,
    differentiation_method=ps.SmoothedFiniteDifference(),
)

t0 = time.time()
model.fit(X, t=t)
wall = time.time() - t0

# 발견된 ODE: dx_i/dt = sum_j coef_ij * lib_j(x)
model.print()
equations = model.equations()
```

### 표준 변환
각 상태변수에 대한 ODE를 별도 후보로 저장.

### 주의
- 도함수 계산이 노이즈에 민감 — SmoothedFiniteDifference 또는 spectral method 권장
- threshold가 sparsity 조절 (작을수록 더 많은 항)

---

## 7. DEAP (커스텀 GP fallback)

### 설치
```bash
pip install deap
```

### 호출
표준 GP 루프 템플릿:

```python
import operator, math, random
from deap import base, creator, gp, tools, algorithms
import numpy as np

pset = gp.PrimitiveSet("MAIN", arity=D)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(np.sin, 1)
pset.addPrimitive(np.cos, 1)
# 변수 이름 매핑
for i in range(D):
    pset.renameArguments(**{f"ARG{i}": f"x{i}"})

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def eval_expr(ind):
    func = toolbox.compile(expr=ind)
    try:
        y_pred = np.array([func(*row) for row in X_train])
        mse = np.mean((y_train - y_pred) ** 2)
        return (mse if np.isfinite(mse) else 1e9,)
    except Exception:
        return (1e9,)

toolbox.register("evaluate", eval_expr)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

pop = toolbox.population(n=300)
hof = tools.HallOfFame(20)
algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, halloffame=hof, verbose=False)

# hof의 각 개체를 sympy로 변환하려면 별도 로직 필요 (operator → sympy 매핑)
```

### 주의
- DEAP는 직접 코드를 짜야 하므로 fallback 용도
- 사용자가 명시적으로 커스텀 연산자/제약을 요청할 때만 사용

---

## 표준 출력 통합

각 도구가 `results/<tool>/candidates.json`을 생성한 후, `collect_results.py`가 통합:

```python
import json, glob

all_candidates = []
for path in glob.glob("results/*/candidates.json"):
    with open(path) as f:
        all_candidates.extend(json.load(f))

with open("results/all_candidates.json", "w") as f:
    json.dump(all_candidates, f, indent=2)
```

이후 expression-analyst가 `all_candidates.json`을 입력으로 후처리.
