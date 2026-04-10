---
name: skill-packaging-guide
description: >
  코드 모듈을 Claude Code 스킬로 변환하는 규칙과 패턴을 정의하는 스킬.
  skill.md 작성법, description 설계, progressive disclosure 적용,
  번들 리소스 구성 방법을 제공한다. skill-builder가 스킬을 생성할 때,
  description을 작성할 때, 스킬 구조를 결정할 때 이 스킬을 참조한다.
---

# Skill-Packaging-Guide — 모듈→스킬 변환 규칙

## 개요

리팩터링된 코드 모듈을 Claude Code 스킬 형식으로 변환하는 규칙을 정의한다.
연구 코드의 특성(도메인 지식 필요, 데이터 의존적, 시각화 중심)을 반영한 패키징 전략을 제공한다.

## 스킬 디렉토리 구조

```
{skill-name}/
├── skill.md          (필수) 스킬 본문
├── scripts/          (선택) 실행 코드
│   ├── main.py       핵심 실행 스크립트
│   ├── utils.py      공유 유틸리티
│   └── requirements.txt  의존성 목록
└── references/       (선택) 참조 문서
    ├── data-format.md    입력 데이터 규격
    └── examples.md       사용 예시
```

## Description 설계 규칙

description은 스킬의 유일한 트리거 메커니즘이다. 적극적으로 작성한다.

### 구조

```
{무엇을 하는지 — 핵심 기능 요약}.
{구체적 기능 나열 — 동사 중심}.
{트리거 키워드 — 사용자가 입력할 법한 다양한 표현}.
```

### 연구 코드 스킬 description 패턴

**데이터 처리 스킬:**
```
{기기명} 관측 데이터를 다운로드, 전처리, 변환하는 스킬.
원시 데이터 로딩, 시간 범위 필터, 채널 선택, 단위 변환, 결측치 처리,
리샘플링, FITS/CSV/HDF5 변환을 수행한다.
{기기명} 데이터, {기기명} 처리, 전처리, 데이터 변환, 데이터 로딩 요청 시
반드시 이 스킬을 사용할 것.
```

**분석/모델 스킬:**
```
{분석 대상}의 {분석 방법}을 수행하는 스킬.
모델 학습, 예측, 평가, 결과 시각화, 파라미터 튜닝을 포함한다.
{분석 대상} 분석, {방법} 실행, 모델 돌려줘, 예측해줘 요청 시
반드시 이 스킬을 사용할 것.
```

**시각화 스킬:**
```
{데이터 유형}의 논문 품질 Figure를 생성하는 스킬.
라이트커브, 스펙트로그램, 이미지맵, 비교 플롯, 시계열 등을 DPI 300으로
생성하며, 저널별 스타일 가이드를 적용한다.
{데이터} 플롯, 그래프, Figure 생성, 시각화 요청 시
반드시 이 스킬을 사용할 것.
```

## skill.md 본문 작성 패턴

### 연구 도구 스킬 템플릿

```markdown
---
name: {skill-name}
description: "{위 패턴에 따른 description}"
---

# {Skill Name} — {한 줄 역할 요약}

## 개요
이 스킬은 {무엇}을 수행한다.
{왜 필요한지 — 수동으로 하면 어떤 점이 비효율적인지}.

## 워크플로우

### 1. 데이터 준비
{입력 데이터 요건, 경로, 형식}

### 2. 실행
{단계별 실행 방법}

### 3. 결과 확인
{출력 파일, 형식, 확인 방법}

## 번들 스크립트

| 스크립트 | 목적 | 입력 | 출력 |
|---|---|---|---|
| scripts/main.py | 핵심 실행 | {입력} | {출력} |

## 의존성
- Python >= 3.10
- {패키지 목록}

## 알려진 제한
- {제한 1}
- {제한 2}
```

## Progressive Disclosure 적용

### 분리 기준

| 내용 | 위치 | 이유 |
|---|---|---|
| 핵심 워크플로우 | skill.md | 항상 필요 |
| 데이터 포맷 상세 | references/data-format.md | 첫 사용 시만 필요 |
| 사용 예시 | references/examples.md | 익숙해지면 불필요 |
| 알고리즘 설명 | references/algorithm.md | 커스터마이징할 때만 필요 |
| 트러블슈팅 | references/troubleshooting.md | 문제 발생 시만 필요 |

### 포인터 작성법

skill.md에서 references를 참조할 때:

```markdown
## 데이터 포맷
입력 데이터는 FITS 형식이어야 한다.
상세 필드 규격은 `references/data-format.md`를 참조하라.
→ FITS 헤더 필수 키워드가 궁금하거나 커스텀 포맷을 사용할 때 읽을 것.
```

"언제 이 파일을 읽어야 하는지"를 명시하여, 불필요한 로딩을 방지한다.

## 스크립트 번들링 규칙

### 포함 대상
- 반복 실행되는 핵심 로직
- 에이전트가 매번 새로 작성하게 두면 비효율적인 코드
- 정확성이 중요한 계산 (수식, 단위 변환 등)

### 제외 대상
- 일회성 설정/초기화 코드
- 사용자 환경에 따라 달라지는 설정
- 10줄 미만의 간단한 코드

### 스크립트 표준

```python
#!/usr/bin/env python3
"""
{스크립트 한 줄 설명}

원본: {원본 파일 경로}
용도: {어떤 스킬에서 사용하는지}
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    # 하드코딩 대신 CLI 인자로 받기
    parser.add_argument('--input', required=True, help='입력 파일 경로')
    parser.add_argument('--output', default='output/', help='출력 디렉토리')
    args = parser.parse_args()
    
    # 핵심 로직
    ...

if __name__ == '__main__':
    main()
```

## 스킬 간 충돌 방지

새 스킬이 기존 변환 완료 스킬과 충돌하지 않도록:

1. **기능 경계 확인**: 기존 스킬이 다루는 범위를 먼저 파악한다
2. **description 차별화**: 트리거 키워드가 겹치면, 범위를 좁혀서 구분한다
3. **보완 관계 명시**: 관련 스킬과의 관계를 skill.md에 기술한다

```markdown
## 관련 스킬
- `data-pipeline`: 데이터 수집 담당. 이 스킬은 수집된 데이터의 **전처리**에 집중.
```

## 네이밍 규칙

| 구분 | 규칙 | 예시 |
|---|---|---|
| 스킬명 | kebab-case, 기능 중심 | `stix-data-processing` |
| 스크립트명 | snake_case, 동사_명사 | `load_stix_data.py` |
| 참조 문서명 | kebab-case, 명사 | `stix-data-format.md` |
