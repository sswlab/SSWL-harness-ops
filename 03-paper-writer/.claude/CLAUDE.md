# 03-Paper-Writer — 논문 작성 및 피어리뷰 하네스

연구자의 코드, 데이터, 결과, 논문초안(선택)을 바탕으로 **학술 논문을 작성**하고,
가상 피어리뷰 프로세스를 통해 **논문 품질을 반복 개선**하는 AI 하네스.
실제 저널 투고 프로세스(제출→심사→리비전→판정)를 시뮬레이션한다.

## 에이전트 팀 구성표

| 에이전트 | 역할 | 설명 |
|---|---|---|
| **researcher** | 논문 작성자 | 연구 결과를 정리하여 논문 초안 + 커버레터 작성, 리비전 수행 |
| **co-worker** | 내부 검토자 | researcher 초안을 한 문장씩 검토: 논리적 흐름, 용어 통일성, 팩트체크, 내부 용어 차단. 교정된 원고를 editor에게 전달 |
| **editor** | 에디터 | 논문 접수, 저널 확인, 참고문헌 최소 20개 확인, 리뷰어 배정(전문분야/성격), 리뷰 취합, 판정 |
| **reviewer-1** | 리뷰어 1 | 한줄씩 팩트체크, 에디터가 부여한 전문분야 중심 리뷰 |
| **reviewer-2** | 리뷰어 2 | 한줄씩 팩트체크, reviewer-1과 다른 전문분야 중심 리뷰 (병렬) |

## 실행 모드: 에이전트 팀

```
연구 결과 입력 (코드, 데이터, Figure, Table, 논문초안)
    │
    ▼
[researcher] 논문 초안 + 커버레터 + Figure/Table/코드 제출
    │
    ▼
[co-worker] 한 문장씩 검토
 ├─ 논리적 흐름 & 섹션 간 유기적 연결 확인
 ├─ 용어 통일성 검증 (같은 개념에 다른 표현 사용 여부)
 ├─ 팩트체크 (수치·주장을 코드/데이터와 대조)
 └─ 내부 용어 차단 (버전 코드, 내부 목표 등 유입 여부)
    │
    ├─ 이슈 발견 → researcher에게 검토 리포트 전달 → researcher 수정 후 재제출
    │
    └─ 이슈 없음 → 교정 완료 원고 생성
           │
           ▼
        [LaTeX 변환] .md → .tex + .pdf (round0) ← 매 라운드마다 별도 저장
           │
           ▼
        [editor] 논문 접수 → 저널 확인 → 리뷰어 전문분야 정의 → 리뷰어 성격 부여
           │
           ├──────────────────┐
           ▼                  ▼
        [reviewer-1]       [reviewer-2]       ← 병렬 진행
         한줄씩 팩트체크    한줄씩 팩트체크
         전문분야 중심      전문분야 중심
         오류지적/질문      오류지적/질문
           │                  │
           └──────┬───────────┘
                  ▼
               [editor] 리뷰 취합 → 연구자에게 전달
                  │
                  ▼
               [researcher] 리비전 수행 → 수정된 논문 + 리뷰 응답 제출
                  │
                  ▼
               [co-worker] 리비전 원고 재검토 (흐름/용어/팩트/내부용어)
                  │
                  ▼
               [LaTeX 변환] .md → .tex + .pdf (round{N}) ← 라운드별 별도 저장
                  │
                  ▼
               [editor] 리비전 확인 → 리뷰어에게 재심 요청
                  │
                  ├──────────────────┐
                  ▼                  ▼
               [reviewer-1]       [reviewer-2]    ← 재심 (병렬)
                  │                  │
                  └──────┬───────────┘
                         ▼
                      [editor] 판정
                         │
                         ├─── Accept → 최종 논문(.md + .tex + .pdf) + 커버레터 출력
                         │
                         └─── 미해결 (최대 3회 리비전 후) → 사용자에게 리뷰 내용 포함 전달
```

## 루프 요약: 최대 3회 반복

```
Round 1: researcher → co-worker → editor → reviewer-1,2(병렬) → editor → researcher
Round 2: researcher → co-worker → editor → reviewer-1,2(병렬) → editor → researcher
Round 3: researcher → co-worker → editor → reviewer-1,2(병렬) → editor → 판정
                                                                        ├→ Accept
                                                                        └→ 미해결 → 사용자에게 반환
```

## 작업 경로 정책

- **하네스 내 `_workspace/`는 빈 스캐폴드**(디렉토리 구조 템플릿)이다. 실행 결과물을 여기에 저장하지 않는다.
- 파이프라인 시작 시 사용자에게 **작업 경로를 질문**한다. 사용자가 쿼리에 경로를 명시했으면 그대로 사용한다.
- 이후 모든 `_workspace/` 참조는 사용자가 지정한 `{작업경로}`로 치환된다.

## 초안 규모 사전 안내

파이프라인 시작 시, researcher 에이전트에 초안 작성을 지시하기 **전에** 사용자에게 다음 정보를 예고한다:

1. **예상 분량**: 대략적인 단어 수 (예: ~8,000 words, ~12,000 words)
2. **Figure 수**: 입력 자료에서 식별된 Figure 후보 개수와 간략한 목록
3. **Table 수**: 본문 + Appendix에 들어갈 Table 후보 개수와 간략한 목록

이 예고는 사용자 승인 단계에서 서사 구성과 함께 제시하며, 사용자가 분량이나 Figure/Table 구성을 조정할 수 있도록 한다. researcher 에이전트는 승인된 규모 범위 내에서 초안을 작성한다.

## 데이터 전달 규칙

| 에이전트 | 출력 파일 |
|---|---|
| researcher | `{작업경로}/01_paper_draft.md`, `{작업경로}/02_cover_letter.md`, `{작업경로}/revision/round{N}_revised_paper.md`, `{작업경로}/revision/round{N}_response_to_reviewers.md` |
| co-worker | `{작업경로}/cowork/round{N}_coworker_report.md`, `{작업경로}/cowork/round{N}_polished_draft.md` |
| editor | `{작업경로}/03_editorial_decision.md`, `{작업경로}/04_reviewer_assignment.md`, `{작업경로}/decision/round{N}_decision.md` |
| reviewer-1 | `{작업경로}/reviews/round{N}_reviewer1_report.md` |
| reviewer-2 | `{작업경로}/reviews/round{N}_reviewer2_report.md` |
| latex-compiler | `{작업경로}/latex/{journal_name}/round{N}/paper.tex`, `{작업경로}/latex/{journal_name}/round{N}/paper.pdf` |
| 공통 | `{작업경로}/editorial-log.md` (전 과정 진행 기록 누적) |

**전달 규칙:**
1. 각 에이전트는 자신의 지정 파일에만 쓴다
2. 다른 에이전트의 출력은 읽기 전용으로 참조한다
3. 모든 중간 산출물(매 라운드)은 삭제하지 않고 보존한다. LaTeX도 라운드별 별도 디렉토리(`round0`, `round1`, ...)에 저장한다
4. `{작업경로}/editorial-log.md`에 모든 에이전트가 판단 과정을 누적 기록한다

## 입력 소스

- 사용자 직접 제공 파일 (연구 코드, 데이터, Figure 이미지, 논문 초안)
- 사용자가 지정한 경로의 연구 산출물
- 자연어 요청 ("이 연구 결과로 논문 써줘", "ApJ에 투고할 논문 만들어줘")

## 기존 논문 초안 제공 시

사용자가 기존 논문 초안(.tex, .pdf, .md)을 제공하면서 **문법 교정, 팩트체크, 모의 피어리뷰, 구조 개선** 등 편집 작업만 요청하는 경우, 이 하네스의 범위가 아님을 안내한다. 03-paper-writer는 연구 결과로부터 **새 논문을 작성**하는 하네스이다.

단, 사용자가 "전체 리라이트"를 요청하는 경우(기존 초안을 바탕으로 처음부터 재작성)에는 03-paper-writer의 기본 파이프라인(researcher → co-worker → editor → reviewer-1/2)을 그대로 사용한다.

## 내부 용어 차단 정책 (Internal Terminology Firewall)

연구 산출물을 입력으로 받을 때, **내부 용어가 논문에 유입되지 않도록** 모든 에이전트가 필터링한다. 논문은 외부 독자가 읽는 공식 문서이므로, 연구 과정의 내부 관리 용어는 일절 포함되어서는 안 된다.

### 차단 대상

| 유형 | 예시 | 논문에서의 처리 |
|---|---|---|
| **내부 버전 코드** | V1, V2, ..., V7, "version 6", "v6 모델" | 삭제 또는 "the proposed method/model" 등 학술 표현으로 대체 |
| **연구 프로덕션/버전 이력** | "V3→V5→V7로 개선", "이전 버전 대비 R² 0.5→0.7→0.8" | **삭제**. 버전 진행 이력은 논문에 포함하지 않음. 성능이 개선된 경우 **최종(최선) 모델만 보고**. 비교가 필요한 경우 model 1/model 2 등 중립적 명칭 사용 |
| **내부 목표/타겟** | "target R²=0.85", "목표 정확도 90%", "X를 목표했으나 Y 달성" | **삭제**. 달성된 결과만 baseline 대비 개선으로 positive 보고 |
| **하네스/파이프라인 용어** | "Phase 1~5", "연구 모드: 심층형", "research-executor", "literature-reviewer", "paper-writer" | 삭제 |
| **내부 코드네임/약칭** | 프로젝트 내부 약칭, 태스크 ID, 실험 코드명 | 삭제 |
| **내부 파일 참조** | "research-note.md에 따르면", "todo.md 기준", "execution_log", "02_research_design.md" | 삭제 |
| **실패한 실험 세부사항** | "V5에서는 temporal split 실패", 버린 ablation 결과 | 논문 contribution에 기여하지 않으면 삭제 |
| **내부 회의/의사결정 과정** | "사용자가 X를 요청", "에디터 판정에 따라", "리뷰어 피드백 반영" (하네스 내부 리뷰) | 삭제 |

### 에이전트별 책임

| 에이전트 | 책임 |
|---|---|
| **researcher** | 논문 초안 작성 시 입력 자료의 내부 용어를 학술 표현으로 변환. 내부 버전 대신 방법론/모델 명칭 사용. 내부 목표 미달 서술 금지. **버전 이력(V3→V5→V7 등) 없이 최종 모델만 보고. 비교 시 model 1/model 2 등 중립 명칭 사용** |
| **co-worker** | **1차 방어선**. 한 문장씩 검토하며 내부 용어 잔존 여부를 점검. 발견 시 검토 리포트에 "Internal Terminology Leak" 항목으로 기록하고 researcher에게 수정 요구 |
| **editor** | **2차 방어선**. 논문 접수 시 내부 용어 잔존 여부를 체크리스트로 확인. 위 차단 대상 7개 유형을 점검하고, 발견 시 researcher에게 수정 요구 후 리뷰어에게 배정 |
| **reviewer-1/2** | **3차 방어선**. 리뷰 시 내부 용어가 남아있으면 "Internal Terminology Leak" 항목으로 지적 |

### 변환 원칙

1. **내부 버전 → 방법론 설명**: "V7 모델" → "the BiLSTM-based sequence-to-sequence model" 또는 "the proposed model"
2. **버전 이력 → 최종 모델만 보고**: 여러 버전을 거쳐 성능이 개선된 경우, 중간 과정 없이 **최종(최선) 모델의 결과만** 보고한다. 예: "V3(R²=0.5) → V5(0.7) → V7(0.8)" → "The proposed model achieved R²=0.8"
3. **모델 비교 → 중립적 명칭**: 두 모델 이상의 비교가 논문에 필요한 경우 내부 버전명 대신 **model 1/model 2**, **Method A/Method B** 등 중립적 라벨을 사용한다. 예: "V5 vs V7" → "Model 1 vs Model 2" 또는 방법론 특성을 반영한 명칭("RF-based model" vs "BiLSTM-based model")
4. **내부 목표 → 생략**: 미달 target은 일절 언급하지 않음. 달성된 결과를 baseline 대비 개선으로 보고
5. **프로세스 용어 → 학술 표현**: "Phase 3 실행 결과" → "Experimental results", "Phase 1 문헌조사" → 삭제 (논문에서는 자연스러운 서술로)
6. **내부 파일 참조 → 삭제**: 내부 문서명(research-note.md, todo.md, execution_log 등)은 논문에 등장하지 않음
7. **실패 이력 → 선별적 보고**: 최종 채택된 방법론과 그 성능만 보고. 탈락한 approach는 contribution에 기여할 때만 간략히 언급

## 논문 작성 형식

- **작성 형식**: Markdown (.md) — 모든 논문 초안과 리비전은 .md로 작성
- **최종 출력**: LaTeX (.tex) + PDF (.pdf) — Accept 판정 후 자동 변환/컴파일
- **템플릿 경로**: `LaTeX-templet/` 디렉토리의 저널별 템플릿 사용
- **폴백 규칙**: 대상 저널의 템플릿이 없으면 arXiv 형식으로 작성

### 사용 가능한 LaTeX 템플릿

| 저널 | 템플릿 | 클래스 |
|---|---|---|
| ApJ / ApJL / ApJS | `LaTeX-templet/ApJ-ApJS-ApJL/` | `aastex701.cls` |
| A&A | `LaTeX-templet/AstronomyAstrophysics/` | `aa.cls` |
| MNRAS | `LaTeX-templet/MNRAS/` | `mnras.cls` |
| 기타 (Solar Physics, SW 등) | `LaTeX-templet/ArxXiV/` | `PRIMEarxiv.sty` |

## 기술 스택

| 범주 | 도구 |
|---|---|
| 언어 | Python 3.10+ |
| 논문 작성 | Markdown (.md) |
| 논문 변환 | LaTeX (tectonic 또는 pdflatex + bibtex) |
| 템플릿 | AASTeX v7, aa.cls, mnras.cls, arXiv |
| 시각화 | matplotlib (DPI=300) |
| 태양물리 | sunpy, astropy (필요 시) |
| 참고문헌 | BibTeX, ADS 검색 |

### LaTeX 컴파일 환경

시스템에 `pdflatex`가 없거나 conda 환경의 texlive-core가 불완전한 경우,
프로젝트 내 conda 환경에 설치된 **tectonic**을 사용한다.

- **환경 경로**: `_texlive/` (conda 환경, `conda create -p ./_texlive -c conda-forge tectonic`)
- **컴파일 명령**: `conda run -p /path/to/03-paper-writer/_texlive tectonic paper.tex`
- **장점**: sudo 불필요, 필요한 패키지 자동 다운로드, 단일 명령으로 .tex → .pdf 변환
- **폴백**: 시스템에 `pdflatex`가 있으면 `pdflatex + bibtex` 3-pass 사용

## 사용 언어

- 사용자 대면: 한국어
- 논문 초안: 영어 (사용자 요청 시 한국어)
- 리뷰 리포트: 영어
- 커버레터: 영어
- 코드/설정: 영어

## 핵심 원칙

1. **사용자 승인 필수**: 저널 선택과 실행 계획을 제시하고 승인 후 진행
2. **실제 피어리뷰 시뮬레이션**: 저널 에디터-리뷰어 프로세스를 충실히 재현
3. **리뷰어 전문성 분화**: 에디터가 논문 키워드 기반으로 각 리뷰어의 전문분야를 정의
4. **리뷰어 성격 부여**: 엄격(strict)/온화(lenient) 중 성격을 부여하여 다양한 관점 확보
5. **한줄씩 팩트체크**: 리뷰어는 논문의 각 주장을 코드/데이터와 대조 검증
6. **최대 3회 리비전**: 3회 내 미해결 시 사용자에게 반환하여 직접 판단
7. **커버레터 필수**: 모든 제출/리비전에 커버레터 포함
8. **Markdown 작성 → LaTeX 출력**: 초안은 .md로 작성, Accept 후 저널 템플릿 기반 .tex + .pdf 생성
9. **템플릿 폴백**: 저널 템플릿 미보유 시 arXiv 형식으로 자동 전환
10. **결과 투명성**: 성공이든 실패든, 과정과 결과를 명확히 보고
11. **참고문헌 최소 20개**: 에디터는 논문 접수 시 참고문헌이 최소 20개 이상인지 확인한다. 미달 시 researcher에게 보충을 요구한 후 리뷰어에게 배정한다
12. **내부 용어 차단**: 내부 버전 코드(V1~V7), 내부 목표/타겟, 하네스 파이프라인 용어, 내부 파일명 등은 논문에 포함되지 않는다. 에디터가 접수 시 점검하고, 리뷰어도 잔존 여부를 확인한다. 상세 규칙은 "내부 용어 차단 정책" 섹션 참조
