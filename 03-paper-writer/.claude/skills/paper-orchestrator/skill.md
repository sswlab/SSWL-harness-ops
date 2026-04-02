---
name: paper-orchestrator
description: >
  논문 작성 및 피어리뷰 파이프라인 총괄 오케스트레이터.
  연구 결과가 주어지면 논문 작성→에디터 접수→리뷰어 배정→병렬 리뷰→
  리비전→재심의 전 과정을 조율한다. 최대 3회 리비전 루프를 관리한다.
  모든 논문 작성/리뷰 작업 시작 시 반드시 이 스킬이 파이프라인을 관리한다.
  키워드: 논문 써줘, paper, 논문 작성, 투고, submit,
  리뷰 시뮬레이션, peer review, 논문 만들어줘,
  저널 투고, manuscript, 원고 작성, 파이프라인 실행
---

# Paper-Orchestrator — 논문 작성/피어리뷰 파이프라인 총괄

## 개요

사용자가 연구 결과를 제공하면, 논문 초안 작성부터 가상 피어리뷰, 리비전, 최종 판정까지
전 과정을 자동으로 조율한다. 에이전트 실행 순서, 데이터 전달 경로, 리뷰어 병렬 실행,
리비전 루프(최대 3회)를 관리한다.

---

## 실행 전 안내 메시지

파이프라인 시작 시 사용자에게 다음을 안내한다:

```
논문 작성 및 피어리뷰 파이프라인을 시작합니다.

- 연구 결과를 바탕으로 논문 초안을 작성합니다.
- 가상 피어리뷰(리뷰어 2명 병렬)를 통해 논문 품질을 검증합니다.
- 최대 3회 리비전을 거쳐 논문을 완성합니다.
- 모든 과정은 _workspace/editorial-log.md에 기록됩니다.

입력 자료: {사용자 제공 자료 목록}
대상 저널: {확정 또는 "연구자가 제안 예정"}

파이프라인을 시작할까요?
```

---

## 파이프라인 흐름도

```
┌─────────────────────────────────────────────────────────────┐
│              사용자: 연구 결과 제공                            │
│  (코드, 데이터, Figure, Table, 논문초안(선택))                 │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │  Phase 1: 논문 작성     │
                │  researcher            │
                │  → 01_paper_draft.md   │
                │  → 02_cover_letter.md  │
                └───────────┬────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │  Phase 2: 에디터 접수   │
                │  editor                │
                │  → 04_reviewer_        │
                │    assignment.md       │
                └───────────┬────────────┘
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
    ┌────────────────────┐  ┌────────────────────┐
    │  Phase 3a: 리뷰     │  │  Phase 3b: 리뷰     │
    │  reviewer-1         │  │  reviewer-2         │  ← 병렬 실행
    │  → round{N}_       │  │  → round{N}_       │
    │    reviewer1_      │  │    reviewer2_      │
    │    report.md       │  │    report.md       │
    └────────┬───────────┘  └────────┬───────────┘
             │                       │
             └───────────┬───────────┘
                         ▼
                ┌────────────────────────┐
                │  Phase 4: 리뷰 취합     │
                │  editor                │
                │  → decision/round{N}_  │
                │    decision.md         │
                └───────────┬────────────┘
                            │
                   ┌────────┴────────┐
                   │                 │
                Accept         Major/Minor
                   │           Revision
                   ▼                 │
     ┌────────────────────────┐
     │  Phase 6: LaTeX 변환   │
     │  latex-compiler 스킬   │
     │  → latex/{journal}/    │
     │    paper.tex + .pdf   │
     └───────────┬───────────┘
                 │
                 ▼
              최종 결과               ▼
              사용자에게         ┌────────────────────────┐
              전달              │  Phase 5: 리비전        │
                               │  researcher            │
                               │  → round{N}_revised_   │
                               │    paper.md            │
                               │  → round{N}_response_  │
                               │    to_reviewers.md     │
                               └───────────┬────────────┘
                                           │
                                           ▼
                                      Phase 2로 돌아감
                                      (최대 3회 반복)
                                           │
                                    3회 초과 시
                                           │
                                           ▼
                                  ┌────────────────────┐
                                  │  사용자에게 반환     │
                                  │  미해결 이슈 +      │
                                  │  전체 리뷰 히스토리  │
                                  └────────────────────┘
```

---

## 에이전트별 데이터 전달 프로토콜

| Phase | 에이전트 | 입력 파일 | 출력 파일 |
|---|---|---|---|
| 1 | researcher | 사용자 제공 자료, (기존 논문초안) | `01_paper_draft.md`, `02_cover_letter.md` |
| 2 | editor | `01_paper_draft.md`, `02_cover_letter.md` | `04_reviewer_assignment.md` |
| 3a | reviewer-1 | `04_reviewer_assignment.md`, 논문, 데이터/코드 | `reviews/round{N}_reviewer1_report.md` |
| 3b | reviewer-2 | `04_reviewer_assignment.md`, 논문, 데이터/코드 | `reviews/round{N}_reviewer2_report.md` |
| 4 | editor | `reviews/round{N}_reviewer1_report.md`, `reviews/round{N}_reviewer2_report.md` | `decision/round{N}_decision.md` |
| 5 | researcher | `decision/round{N}_decision.md`, 리뷰 리포트들 | `revision/round{N}_revised_paper.md`, `revision/round{N}_response_to_reviewers.md` |
| 6 | latex-compiler | 해당 라운드 논문 (.md), `LaTeX-templet/` | `latex/{journal_name}/round{N}/paper.tex`, `latex/{journal_name}/round{N}/paper.pdf` |

**모든 파일은 `_workspace/` 하위에 위치한다.**

---

## 루프백 조건과 최대 횟수

| 루프백 유형 | 트리거 | 최대 횟수 | 초과 시 |
|---|---|---|---|
| **리비전 루프** | editor가 Major/Minor Revision 판정 | 3회 | 사용자에게 미해결 이슈 포함 반환 |
| **리뷰 보완** | editor가 리뷰 불완전 판단 | 1회 | 불완전 리뷰 상태로 진행 |
| **자료 보충** | researcher가 추가 자료 필요 보고 | 1회 | 가용 자료만으로 작성 |

---

## Phase별 실행 상세

### Phase 1: 논문 작성 (researcher)

1. 사용자 제공 자료 분석 (코드, 데이터, Figure, Table)
2. 대상 저널 결정 (사용자 미지정 시 3개 후보 제안 → 사용자 선택)
3. 논문 구조 설계 (Abstract~References)
4. 논문 초안 작성 → `01_paper_draft.md`
5. 커버레터 작성 → `02_cover_letter.md`

### Phase 2: 에디터 접수 (editor)

1. 논문/커버레터 접수 확인
2. 저널 적합성 확인
3. 논문 키워드 분석 → 리뷰어 전문분야 정의
4. 리뷰어 성격(strict/lenient) 배정
5. 리뷰어 배정 문서 생성 → `04_reviewer_assignment.md`

### Phase 3: 병렬 리뷰 (reviewer-1, reviewer-2)

**반드시 두 리뷰어를 병렬로 실행한다.**

두 리뷰어 에이전트를 동시에 실행한다:
- reviewer-1: 배정된 전문분야/성격으로 독립 리뷰
- reviewer-2: 배정된 전문분야/성격으로 독립 리뷰

각 리뷰어는:
1. 논문을 한 줄씩 읽으며 팩트체크
2. 전문분야 중심으로 깊이 있는 평가
3. Major/Minor Issues, Questions 분류
4. 리뷰 리포트 생성

### Phase 4: 리뷰 취합 및 판정 (editor)

1. 두 리뷰어 리포트 취합
2. Major/Minor Issues 통합 정리
3. 판정: Accept / Minor Revision / Major Revision
4. 판정문 생성 → `decision/round{N}_decision.md`
5. Accept 시 → Phase 6 (LaTeX 변환)으로
6. Revision 시 → Phase 5로

### Phase 5: 리비전 (researcher)

1. 에디터 판정문과 리뷰어 리포트 분석
2. 리뷰어 코멘트별 응답 작성
3. 논문 수정
4. 수정된 논문 → `revision/round{N}_revised_paper.md`
5. 리뷰어 응답 → `revision/round{N}_response_to_reviewers.md`
6. Phase 2로 루프백

### Phase 6: LaTeX 변환 및 컴파일 (매 라운드마다 실행)

**매 리비전 라운드마다** 해당 라운드의 논문을 LaTeX로 변환하고 PDF를 생성한다.
라운드별 별도 디렉토리에 저장하여 리비전 이력을 완전 보존한다.

- **round0**: 초기 제출 (`01_paper_draft.md`) → `latex/{journal}/round0/`
- **round1~3**: 리비전 (`revision/round{N}_revised_paper.md`) → `latex/{journal}/round{N}/`

실행 절차:
1. 대상 저널의 LaTeX 템플릿 확인 (`LaTeX-templet/` 디렉토리)
2. 템플릿 미보유 저널 → arXiv 형식으로 폴백
3. 라운드별 작업 디렉토리 생성: `_workspace/latex/{journal_name}/round{N}/`
4. 저널 템플릿 파일(cls, sty, bst) 복사
5. Markdown → LaTeX 변환 (latex-compiler 스킬 참조)
   - 문서 구조 변환 (# → \section 등)
   - Figure/Table 삽입 코드 생성
   - 참고문헌 BibTeX 연결
   - 저널별 프리앰블 생성
6. Figure 파일 복사 → `latex/{journal_name}/round{N}/figures/`
7. `references.bib` 생성/복사
8. pdflatex + bibtex 컴파일 (3회 실행)
9. PDF 생성 확인 + 미해결 참조 검토
10. 사용자에게 해당 라운드 산출물 경로 안내

**Phase 6 실행 시점:**
- Phase 1 완료 직후 → round0 LaTeX 생성
- Phase 5 (리비전) 완료 후 매번 → round{N} LaTeX 생성
- 즉, 리뷰어에게 보내기 전에 항상 해당 라운드의 .tex + .pdf가 존재

---

## 에러 핸들링 테이블

| Phase | 에러 유형 | 심각도 | 대응 |
|---|---|---|---|
| 1 | 연구 결과 불충분 | 중간 | 가용 자료로 부분 초안, 부족 섹션 [TBD] 표시 |
| 1 | 저널 미정 | 낮음 | 3개 후보 제안, 사용자 선택 |
| 2 | 저널 부적합 | 중간 | 적합 저널 재제안, 사용자 확인 |
| 3 | 리뷰어 팩트체크 실패 (데이터 접근 불가) | 중간 | "[데이터 미확인]" 표기, 가능 범위 리뷰 |
| 3 | 리뷰어 리포트 불완전 | 낮음 | 1회 보완 요청, 이후 그대로 진행 |
| 4 | 리뷰어 의견 상충 | 낮음 | 두 의견 모두 전달, 에디터 견해 추가 |
| 5 | 리비전 범위 과다 | 중간 | 우선순위화, 추가 작업은 사용자 판단 |
| 5 | 3회 리비전 초과 | 높음 | 사용자에게 전체 히스토리 + 미해결 이슈 반환 |
| 6 | pdflatex 미설치 | 중간 | .tex 파일만 생성, 사용자에게 로컬 컴파일 안내 |
| 6 | 컴파일 에러 | 중간 | 에러 로그 분석, 문제 줄 수정 후 재컴파일 (최대 3회) |
| 6 | Figure 파일 미발견 | 낮음 | 누락 Figure 목록 보고, placeholder 삽입 |
| 6 | 저널 템플릿 미보유 | 낮음 | arXiv 형식으로 자동 폴백 |

---

## editorial-log.md 기록 규칙

모든 에이전트는 `_workspace/editorial-log.md`에 자신의 판단 과정을 누적 기록한다.

```markdown
# Editorial Log

## [Phase 1: 논문 작성] {timestamp}
### researcher
- 저널 선정 근거: ...
- 논문 구조 결정: ...
- Figure/Table 배치 전략: ...

## [Phase 2: 에디터 접수] {timestamp}
### editor
- 키워드 분석 결과: ...
- 리뷰어 전문분야 배정 근거: ...
- 리뷰어 성격 배정 근거: ...

## [Phase 3: 리뷰 Round 1] {timestamp}
### reviewer-1
- 주요 팩트체크 판단: ...
- 의심스러운 주장: ...

### reviewer-2
- 주요 팩트체크 판단: ...
- 방법론 평가 근거: ...

## [Phase 4: 판정 Round 1] {timestamp}
### editor
- 판정 근거: ...
- 핵심 수정 사항: ...

## [Phase 5: 리비전 Round 1] {timestamp}
### researcher
- 리비전 전략: ...
- 주요 수정 내용: ...

...
```

**규칙:**
- 각 에이전트는 자기 Phase 섹션에만 추가한다
- 기존 내용을 수정하지 않고 누적만 한다
- timestamp를 반드시 포함한다
- 판단의 **이유**를 반드시 기록한다

---

## 테스트 시나리오

### 시나리오 1: 정상 흐름 — 1회 리비전 후 Accept

```
사용자: "01-research-production의 결과로 ApJ 논문 써줘"

Phase 1: researcher
  → 01-research-production/_workspace/ 자료 분석
  → ApJ 스타일 논문 초안 작성
  → 01_paper_draft.md, 02_cover_letter.md 생성

Phase 2: editor
  → 키워드: solar flare, prediction, machine learning
  → reviewer-1: Solar Physics 전문, strict
  → reviewer-2: ML/Data Science 전문, lenient
  → 04_reviewer_assignment.md 생성

Phase 3: reviewer-1, reviewer-2 (병렬)
  → reviewer-1: 물리 해석 중심, 엄격하게 팩트체크
  → reviewer-2: 방법론 중심, 건설적 피드백
  → round1_reviewer1_report.md, round1_reviewer2_report.md 생성

Phase 4: editor
  → Major Issues 2개 (reviewer-1), Minor Issues 3개 (reviewer-2)
  → 판정: Major Revision
  → decision/round1_decision.md 생성

Phase 5: researcher (리비전)
  → Major Issues 수정, Minor Issues 반영
  → revision/round1_revised_paper.md, round1_response_to_reviewers.md 생성

Phase 2~4: Round 2
  → reviewer-1: 이전 Major Issues 해결 확인
  → reviewer-2: Minor Issues 해결 확인
  → 판정: Accept

→ 최종 논문 + 커버레터를 사용자에게 전달
```

### 시나리오 2: 3회 리비전 후 사용자 반환

```
사용자: "이 코드 결과로 A&A 논문 만들어줘"

Round 1: Major Revision (데이터 해석 근본 문제)
Round 2: Major Revision (리뷰어1 미해결 이슈 지속)
Round 3: Minor Revision (일부 이슈 잔존)

→ 3회 도달: 사용자에게 반환
   - 전체 리비전 히스토리
   - 미해결 이슈 목록
   - 에디터 제안 (추가 실험 필요 등)
   - 사용자가 직접 판단하여 수정 또는 방향 전환
```

### 시나리오 3: 초기 논문 초안 제공

```
사용자: "이 논문 초안을 리뷰해줘" (기존 초안 파일 제공)

Phase 1: researcher
  → 사용자 초안을 기반으로 01_paper_draft.md 생성 (형식 정리)
  → 커버레터 작성

Phase 2~: 정상 리뷰 프로세스 진행
```
