#!/usr/bin/env bash
# 05-symbolic-regression — 설치 스크립트
#
# PyPI 패키지는 requirements.txt로 설치하고,
# GitHub 기반 도구(DSO, NeSymReS, AI Feynman)는 별도로 clone/install 합니다.
#
# 사용법:
#   bash install.sh                # 전체 설치
#   bash install.sh core           # PyPI 패키지만
#   bash install.sh pysr           # PySR + Julia 백엔드
#   bash install.sh dso            # DSO만
#   bash install.sh nesymres       # NeSymReS만
#   bash install.sh feynman        # AI Feynman만
#
# 외부 가중치(NeSymReS pretrained 등)는 사용자 동의 후 다운로드됩니다.

set -e

HARNESS_DIR="$(cd "$(dirname "$0")" && pwd)"
EXT_DIR="$HARNESS_DIR/external"
mkdir -p "$EXT_DIR"

install_core() {
    echo "[1/5] PyPI 패키지 설치"
    pip install -r "$HARNESS_DIR/requirements.txt"
}

install_pysr_julia() {
    echo "[2/5] PySR Julia 백엔드 설치 (수 분 소요)"
    python -c "import pysr; pysr.install()"
}

install_dso() {
    echo "[3/5] DSO (Deep Symbolic Optimization) 설치"
    if [ ! -d "$EXT_DIR/deep-symbolic-optimization" ]; then
        git clone https://github.com/brendenpetersen/deep-symbolic-optimization.git \
            "$EXT_DIR/deep-symbolic-optimization"
    fi
    pip install -e "$EXT_DIR/deep-symbolic-optimization/dso"
}

install_nesymres() {
    echo "[4/5] NeSymReS 설치"
    if [ ! -d "$EXT_DIR/NeuralSymbolicRegressionThatScales" ]; then
        git clone https://github.com/SymposiumOrganization/NeuralSymbolicRegressionThatScales.git \
            "$EXT_DIR/NeuralSymbolicRegressionThatScales"
    fi
    pip install -e "$EXT_DIR/NeuralSymbolicRegressionThatScales"
    echo ""
    echo "  ⚠️  사전학습 가중치는 별도 다운로드가 필요합니다."
    echo "  ⚠️  처음 사용 시 sr-planner가 사용자에게 출처/라이선스를 알린 후 다운로드합니다."
    echo "  ⚠️  참고: https://github.com/SymposiumOrganization/NeuralSymbolicRegressionThatScales"
}

install_feynman() {
    echo "[5/5] AI Feynman 설치"
    if [ ! -d "$EXT_DIR/AI-Feynman" ]; then
        git clone https://github.com/SJ001/AI-Feynman.git "$EXT_DIR/AI-Feynman"
    fi
    pip install -e "$EXT_DIR/AI-Feynman"
}

case "${1:-all}" in
    core)
        install_core
        ;;
    pysr)
        install_pysr_julia
        ;;
    dso)
        install_dso
        ;;
    nesymres)
        install_nesymres
        ;;
    feynman)
        install_feynman
        ;;
    all)
        install_core
        install_pysr_julia
        install_dso       || echo "  ⚠️  DSO 설치 실패. 수동 설치 필요."
        install_nesymres  || echo "  ⚠️  NeSymReS 설치 실패. 수동 설치 필요."
        install_feynman   || echo "  ⚠️  AI Feynman 설치 실패. 수동 설치 필요."
        echo ""
        echo "✅ 설치 완료. 외부 도구는 $EXT_DIR/ 아래에 있습니다."
        ;;
    *)
        echo "Unknown target: $1"
        echo "사용법: bash install.sh [core|pysr|dso|nesymres|feynman|all]"
        exit 1
        ;;
esac
