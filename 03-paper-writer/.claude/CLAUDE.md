# 03-Paper-Writer — 논문 작성 및 피어리뷰 하네스

연구자의 코드, 데이터, 결과, 논문초안(선택)을 바탕으로 **학술 논문을 작성**하고,
가상 피어리뷰 프로세스를 통해 **논문 품질을 반복 개선**하는 AI 하네스.
실제 저널 투고 프로세스(제출→심사→리비전→판정)를 시뮬레이션한다.

## 에이전트 팀 구성표

| 에이전트 | 역할 | 설명 |
|---|---|---|
| **researcher** | 논문 작성자 | 연구 결과를 정리하여 논문 초안 + 커버레터 작성, 리비전 수행 |
| **editor** | 에디터 | 논문 접수, 저널 확인, 리뷰어 배정(전문분야/성격), 리뷰 취합, 판정 |
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
Round 1: researcher → editor → reviewer-1,2(병렬) → editor → researcher
Round 2: researcher → editor → reviewer-1,2(병렬) → editor → researcher
Round 3: researcher → editor → reviewer-1,2(병렬) → editor → 판정
                                                             ├→ Accept
                                                             └→ 미해결 → 사용자에게 반환
```

## 작업 경로 정책

- **하네스 내 `_workspace/`는 빈 스캐폴드**(디렉토리 구조 템플릿)이다. 실행 결과물을 여기에 저장하지 않는다.
- 파이프라인 시작 시 사용자에게 **작업 경로를 질문**한다. 사용자가 쿼리에 경로를 명시했으면 그대로 사용한다.
- 이후 모든 `_workspace/` 참조는 사용자가 지정한 `{작업경로}`로 치환된다.

## 데이터 전달 규칙

| 에이전트 | 출력 파일 |
|---|---|
| researcher | `{작업경로}/01_paper_draft.md`, `{작업경로}/02_cover_letter.md`, `{작업경로}/revision/round{N}_revised_paper.md`, `{작업경로}/revision/round{N}_response_to_reviewers.md` |
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

- `01-research-production/_workspace/` 의 연구 산출물 (논문 초안, Figure, Table, 코드)
- 사용자 직접 제공 파일 (연구 코드, 데이터, Figure 이미지)
- 자연어 요청 ("이 연구 결과로 논문 써줘", "ApJ에 투고할 논문 만들어줘")

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
