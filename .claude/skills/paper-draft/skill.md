---
name: paper-draft
description: >
  논문 및 연구 보고서 초안 작성 스킬.
  실험 결과를 바탕으로 학술 논문 구조(Introduction, Method,
  Results, Discussion)의 초안을 작성한다.
  키워드: 논문 초안, 논문 써줘, paper draft, 보고서 작성,
  introduction, method, results, discussion,
  abstract, 학술 논문, 연구 보고서, 초안 작성
---

# Paper-Draft — 논문/보고서 초안 작성 스킬

## 개요

실험 결과를 바탕으로 **학술 논문 구조**의 초안을 작성한다. 완성된 논문이 아닌 **초안(draft)**을 제공하며, 연구자가 수정·보완하여 완성하도록 골격을 제공한다.

## 논문 초안 구조

### 표준 학술 논문 형식

```markdown
# {논문 제목}

## Abstract
{150~250 단어. 배경-방법-결과-결론 4문장 구조}

## 1. Introduction
### 1.1 Background
{연구 분야 배경. 왜 이 연구가 중요한가.}

### 1.2 Previous Work
{선행 연구. 기존 방법의 한계.}

### 1.3 Motivation
{이 연구의 동기. 어떤 갭을 채우는가.}

### 1.4 Contribution
{이 논문의 기여점. 무엇이 새로운가.}

## 2. Data and Method
### 2.1 Data
{사용한 데이터. 소스, 기간, 해상도, 전처리.}

### 2.2 Method
{실험 방법. Baseline, Experiment 설계.}

### 2.3 Evaluation Metrics
{평가 지표. 어떻게 비교/측정했는가.}

## 3. Results
### 3.1 {결과 섹션 1}
{핵심 결과. 수치, 그래프 설명.}

### 3.2 {결과 섹션 2}
{추가 분석. 세부 비교.}

## 4. Discussion
### 4.1 Interpretation
{결과의 과학적 의미.}

### 4.2 Limitations
{한계점.}

### 4.3 Future Work
{향후 연구 방향.}

## 5. Conclusion
{핵심 결론 3~5문장.}

## References
{관련 참고문헌 목록.}
```

## 작성 원칙

1. **객관적 서술**: 결과를 과장하지 않는다. "dramatically improved" 대신 "improved by 12%".
2. **수치 기반**: 주장에는 반드시 수치적 근거를 포함한다.
3. **그래프 참조**: 본문에서 Figure/Table을 명시적으로 참조한다.
4. **한계 투명성**: 실험의 한계를 솔직히 기술한다.
5. **초안 명시**: 이것은 초안이며, 연구자의 수정이 필요함을 명시한다.

## 입력

실험 결과를 포함한 컨텍스트:

```json
{
  "experiment_id": "exp_20260327_...",
  "research_question": "핵심 연구 질문",
  "experiment_design": "실험 설계 요약",
  "results": {
    "baseline": {},
    "experiment": {},
    "comparison": {}
  },
  "figures": ["fig1.png", "fig2.png"],
  "language": "en | ko"
}
```

## 출력

- `_workspace/papers/draft_{timestamp}.md`: 논문 초안 (Markdown)
- `_workspace/papers/draft_{timestamp}_figures/`: 참조 그래프

## 언어

- **기본**: 영어 (국제 학술지 대상)
- **한국어**: 사용자 요청 시 한국어로 작성
- 사용자가 명시하지 않으면 영어로 작성하되, 확인한다.

## 참고문헌

초안에 포함할 참고문헌은:
1. 실험에서 사용한 데이터/모델의 원본 논문
2. 비교 대상이 된 선행 연구
3. 분석 방법론의 출처

형식: APA 또는 학회별 표준 (사용자 지정 시)

## 에러 핸들링

| 상황 | 대응 |
|---|---|
| 실험 결과 부족 | 가용한 결과만으로 부분 초안 작성, 빈 섹션 표시 |
| 그래프 미생성 | Figure 위치만 표시하고 "[Figure TBD]" 삽입 |
| 연구 질문 불명확 | 사용자에게 핵심 질문 확인 요청 |
| 참고문헌 불확실 | "[REF]" 플레이스홀더로 표시 |
