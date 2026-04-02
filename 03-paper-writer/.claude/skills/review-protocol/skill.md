---
name: review-protocol
description: >
  피어리뷰 프로토콜 및 팩트체크 가이드라인.
  리뷰어가 논문을 체계적으로 검토하는 방법, 팩트체크 절차,
  이슈 분류 기준, 리비전 추적 방법을 정의한다.
  리뷰어 에이전트가 리뷰를 수행할 때 반드시 참조하는 스킬이다.
  키워드: 리뷰 방법, 팩트체크, fact-check protocol,
  리뷰 가이드, 심사 기준, review criteria,
  이슈 분류, major minor, 리비전 체크
---

# Review-Protocol — 피어리뷰 프로토콜 및 팩트체크 가이드

## 개요

리뷰어가 논문을 체계적이고 일관성 있게 검토하기 위한 프로토콜.
팩트체크 절차, 이슈 분류 기준, 성격별 리뷰 가이드라인, 리비전 추적 방법을 정의한다.

---

## 팩트체크 절차 (Line-by-Line)

### Step 1: 섹션별 순차 읽기

논문을 다음 순서로 읽는다:
1. Abstract → 핵심 주장 추출
2. Introduction → 배경, 동기, 기여점 확인
3. Data and Methods → 데이터 소스, 방법론 확인
4. Results → 수치, Figure/Table과 본문 대조
5. Discussion → 해석의 논리적 타당성
6. Conclusions → Abstract/Results와 일관성

### Step 2: 주장-근거 대조

논문의 각 주장에 대해:

```
주장 → 근거 유형 확인 → 검증
```

| 주장 유형 | 근거 소스 | 검증 방법 |
|---|---|---|
| 정량적 결과 ("accuracy 92%") | 코드 출력, 로그 | 코드 실행 결과와 수치 대조 |
| Figure 해석 ("Figure 1 shows...") | Figure 파일 | Figure 내용과 서술 일치 확인 |
| Table 참조 ("Table 1 lists...") | Table 파일 | Table 수치와 본문 수치 대조 |
| 선행연구 인용 ("Smith et al. found...") | 참고문헌 | 인용 정확성 확인 (가능한 범위) |
| 물리적 해석 ("This implies...") | 도메인 지식 | 물리적 타당성 판단 |
| 비교 ("better than baseline") | 실험 결과 | 비교 수치의 정확성과 공정성 |

### Step 3: Figure/Table 검증

| 검증 항목 | 체크포인트 |
|---|---|
| 축 라벨 | 변수명, 단위 명시 |
| 범례 | 모든 데이터 시리즈 설명 |
| 캡션 | 독립적 이해 가능성 (캡션만 읽고 이해 가능해야 함) |
| 해상도 | 300 DPI 이상 |
| 본문 참조 | 모든 Figure/Table이 본문에서 참조되는지 |
| 데이터 일치 | Figure/Table의 수치가 본문 서술과 일치하는지 |

### Step 4: 논리 흐름 검증

```
Introduction (배경 + 동기)
    ↓ 논리적 연결?
Methods (목적에 적합?)
    ↓ 논리적 연결?
Results (Methods의 산출?)
    ↓ 논리적 연결?
Discussion (Results의 해석?)
    ↓ 논리적 연결?
Conclusions (전체 요약 일관?)
```

---

## 이슈 분류 기준

### Major Issues (수정 필수)

논문의 핵심 주장이나 결론에 영향을 미치는 문제.

| 분류 | 예시 |
|---|---|
| **사실 오류** | 수치 불일치, Figure/데이터 불일치 |
| **논리적 결함** | 근거 없는 결론, 비약적 해석 |
| **방법론 결함** | 부적절한 방법, 누락된 핵심 단계 |
| **재현성 문제** | 재현에 필요한 정보 누락 |
| **핵심 누락** | 중요한 비교/분석 부재 |
| **과장 주장** | 데이터가 지지하지 않는 강한 결론 |

### Minor Issues (수정 권장)

논문의 핵심을 손상하지 않지만 품질을 떨어뜨리는 문제.

| 분류 | 예시 |
|---|---|
| **표현 모호** | 불명확한 서술, 전문용어 미정의 |
| **형식 문제** | 참고문헌 형식, Figure 번호 순서 |
| **보완 가능** | 추가하면 좋을 분석, 논의 포인트 |
| **스타일** | 문법, 어색한 표현, 일관성 |
| **사소한 수치** | 반올림, 유효숫자 표기 |

### Questions (연구자 응답 필요)

| 유형 | 설명 |
|---|---|
| **Clarification** | 서술이 모호하여 의도를 확인 |
| **Justification** | 선택/결정의 근거를 설명 요청 |
| **Extension** | 추가 분석이나 논의 가능성 탐색 |

---

## 성격별 리뷰 톤 가이드

### Strict (엄격) 모드

**톤**: 정중하지만 단호함. 모든 주장에 근거를 요구함.

예시 표현:
- "This claim requires quantitative support. The current statement is not backed by the data presented."
- "The discrepancy between Figure 3 and the text (92% vs 89%) must be resolved."
- "Why was method X chosen over the widely-used method Y? A comparison is necessary."
- "The error bars are missing in Figure 2, making it impossible to assess statistical significance."

### Lenient (온화) 모드

**톤**: 건설적이고 격려적. 핵심 문제에 집중하고 사소한 문제는 부드럽게 제안.

예시 표현:
- "The results are interesting. It would strengthen the paper to add quantitative error estimates."
- "Consider clarifying the description of the preprocessing step for better reproducibility."
- "A minor suggestion: including a comparison with method Y could provide additional context."
- "The overall approach is sound. One point that might benefit from further discussion is..."

---

## 리비전 추적 프로토콜

### 리비전 라운드에서의 리뷰 절차

1. **이전 리뷰 로드**: `reviews/round{N-1}_reviewer{1,2}_report.md` 읽기
2. **Response to Reviewers 확인**: `revision/round{N-1}_response_to_reviewers.md` 읽기
3. **수정 사항 대조**: 이전 Issue별로 해결 여부 확인
4. **새 이슈 확인**: 수정 과정에서 도입된 새로운 문제 확인

### 이슈 추적 테이블

```markdown
## Revision Check

### 이전 Major Issues
| ID | 이슈 | 상태 | 비고 |
|---|---|---|---|
| M1 | {이슈 설명} | Resolved / Partially / Not addressed | {상세} |
| M2 | ... | ... | ... |

### 이전 Minor Issues
| ID | 이슈 | 상태 | 비고 |
|---|---|---|---|
| m1 | ... | ... | ... |

### 이전 Questions
| ID | 질문 | 응답 충분? | 비고 |
|---|---|---|---|
| Q1 | ... | Yes / No / Partial | ... |

### 새로 발견된 Issues (이번 라운드)
| ID | 유형 | 이슈 | 위치 |
|---|---|---|---|
| M_new1 | Major | ... | Section X.X |
| m_new1 | Minor | ... | Section X.X |
```

---

## 판정 가이드라인 (에디터 참조용)

| 조건 | 에디터 판정 |
|---|---|
| 두 리뷰어 모두 Accept 추천 | **Accept** |
| Minor Issues만, 재심 불필요 | **Accept** (minor 수정 후) |
| 한쪽 Accept, 한쪽 Minor Revision | **Minor Revision** |
| Major Issues 존재, 해결 가능 | **Major Revision** |
| 두 리뷰어 모두 Major Issue 지적 | **Major Revision** |
| 3회 리비전 후 Major Issue 잔존 | **사용자 반환** |
| 근본적 결함 (재설계 필요) | 즉시 **사용자 반환** (리비전 무의미) |
