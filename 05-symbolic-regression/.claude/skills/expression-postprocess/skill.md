---
name: expression-postprocess
description: >
  SymPy를 사용한 SR 후보 수식의 단순화, 동등성 판정, 복잡도 평가, Pareto front
  구성, 차원 일관성 검사 가이드. expression-analyst 에이전트의 reference.
  키워드: SymPy 단순화, 동등성, Pareto, 복잡도, 차원 분석, dimensional analysis
---

# expression-postprocess — 수식 후처리 reference

이 skill은 expression-analyst 에이전트가 raw SR 후보를 정제할 때 참조하는 가이드입니다.

## 1. 안전 파싱

SR 도구마다 출력 문자열 형식이 다르므로, 통일된 변수 심볼로 파싱합니다.

```python
import sympy as sp

def make_symbols(n_vars):
    return sp.symbols(' '.join(f'x{i}' for i in range(n_vars)))

def parse_safe(expr_str, symbols):
    """문자열을 SymPy expression으로 안전하게 파싱."""
    locals_dict = {str(s): s for s in symbols}
    try:
        expr = sp.sympify(expr_str, locals=locals_dict)
        return expr
    except (sp.SympifyError, SyntaxError, TypeError) as e:
        return None
```

## 2. 단순화

```python
def simplify_pipeline(expr):
    """단계별 단순화. 실패하면 원본 반환."""
    if expr is None:
        return None
    try:
        e = sp.expand(expr)
        e = sp.simplify(e)
        e = sp.trigsimp(e)
        # 작은 계수를 합리적인 분수로
        e = sp.nsimplify(e, rational=False, tolerance=1e-3)
        return e
    except Exception:
        return expr
```

## 3. 복잡도 지표

```python
def complexity(expr):
    """SymPy count_ops를 표준 복잡도로 사용."""
    try:
        return int(sp.count_ops(expr))
    except Exception:
        return 10**6   # 파싱 불가는 매우 복잡한 것으로

def depth(expr):
    if expr is None or expr.is_Atom:
        return 0
    return 1 + max((depth(arg) for arg in expr.args), default=0)
```

## 4. 동등성 판정 (보수적)

```python
def equivalent(a, b, tol=1e-9):
    """두 expression이 수학적으로 같은지 보수적으로 판정."""
    if a is None or b is None:
        return False
    try:
        diff = sp.simplify(a - b)
        if diff == 0:
            return True
        # 수치 검증 (랜덤 포인트 평가)
        symbols = sorted(a.free_symbols | b.free_symbols, key=str)
        if not symbols:
            return abs(float(diff)) < tol
        import numpy as np
        rng = np.random.default_rng(0)
        for _ in range(20):
            subs = {s: float(rng.uniform(-2, 2)) for s in symbols}
            try:
                if abs(float(a.subs(subs)) - float(b.subs(subs))) > tol:
                    return False
            except Exception:
                return False
        return True
    except Exception:
        return False
```

## 5. 동등성 클러스터링

```python
def cluster_equivalents(candidates):
    """후보 리스트를 동등성 클러스터로 묶음."""
    clusters = []
    for c in candidates:
        placed = False
        for cl in clusters:
            if equivalent(c["sympy_expr"], cl["canonical"]):
                cl["members"].append(c)
                placed = True
                break
        if not placed:
            clusters.append({
                "canonical": c["sympy_expr"],
                "members": [c],
            })
    return clusters
```

## 6. 평가 (validation R²)

```python
import numpy as np

def evaluate(expr, X, y, symbols):
    """expr을 X에 대해 평가하고 R² 반환. 실패 시 None."""
    if expr is None:
        return None
    try:
        f = sp.lambdify(symbols, expr, modules=['numpy'])
        y_pred = f(*[X[:, i] for i in range(X.shape[1])])
        if np.isscalar(y_pred):
            y_pred = np.full_like(y, y_pred, dtype=float)
        if not np.all(np.isfinite(y_pred)):
            return None
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        if ss_tot == 0:
            return None
        return float(1 - ss_res / ss_tot)
    except Exception:
        return None
```

## 7. Pareto Front

```python
def pareto_front(candidates):
    """(complexity 작을수록, val_r2 클수록) 비지배 해 추출."""
    sorted_c = sorted(candidates, key=lambda c: (c["complexity"], -c["val_r2"]))
    front = []
    best_r2 = -float("inf")
    for c in sorted_c:
        if c["val_r2"] > best_r2:
            front.append(c)
            best_r2 = c["val_r2"]
    return front
```

## 8. 차원 일관성 검사

변수에 단위 정보가 있을 때 dimensional consistency를 검사.

```python
def check_dimensions(expr, var_units):
    """
    var_units: dict {"x0": Dim("L"), "x1": Dim("T"), ...}
    Dim은 단순 dict 또는 sympy.physics.units 사용.
    반환: (is_consistent: bool, reason: str)
    """
    # 간단한 SI 차원 7-튜플: (M, L, T, I, Theta, N, J)
    # 여기서는 placeholder. 실제 구현은 도메인에 맞춰 확장.
    try:
        # 1. atom 확인
        # 2. add/sub: 양변 dim 일치
        # 3. mul/div: dim 합/차
        # 4. sin/cos/exp/log: 인수 무차원
        # 5. pow: 지수 무차원
        ...
        return True, "ok"
    except Exception as e:
        return False, str(e)
```

`sympy.physics.units` 사용 예:
```python
from sympy.physics.units import meter, second, kilogram
from sympy.physics.units.systems import SI

# 변수에 unit을 곱한 형태로 substitute하여 dim 일관성 확인
```

## 9. LaTeX 출력

```python
def to_latex(expr):
    if expr is None:
        return ""
    try:
        return sp.latex(expr)
    except Exception:
        return str(expr)
```

## 10. 표준 후처리 파이프라인

```python
def postprocess(all_candidates, X_val, y_val, n_vars, var_units=None):
    symbols = make_symbols(n_vars)

    # 1. 파싱 + 단순화
    for c in all_candidates:
        e = parse_safe(c["expression"], symbols)
        c["sympy_expr"] = simplify_pipeline(e)
        c["complexity"] = complexity(c["sympy_expr"])
        c["latex"] = to_latex(c["sympy_expr"])

    # 2. validation 평가
    for c in all_candidates:
        c["val_r2"] = evaluate(c["sympy_expr"], X_val, y_val, symbols)

    # 3. 무효 후보 제거
    valid = [c for c in all_candidates if c["sympy_expr"] is not None and c["val_r2"] is not None]

    # 4. 차원 검사 (선택)
    if var_units:
        for c in valid:
            ok, reason = check_dimensions(c["sympy_expr"], var_units)
            c["dim_consistent"] = ok
            c["dim_reason"] = reason

    # 5. 동등성 클러스터링
    clusters = cluster_equivalents(valid)

    # 6. Pareto front
    front = pareto_front(valid)

    return {"valid": valid, "clusters": clusters, "pareto": front}
```
