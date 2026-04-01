# 02-Conference-Presentation-Generator

SSWL 연구 결과를 **학회 발표용 PPT**로 자동 생성하는 하네스.
논문/실험 결과를 입력하면, 에이전트 팀이 스토리 설계 → 슬라이드 구성 → PPTX 생성 → 발표 코칭까지 수행한다.

## 에이전트 팀 구성표

| 에이전트 | 역할 | 설명 |
|---|---|---|
| **content-extractor** | 콘텐츠 추출 | 논문/결과에서 핵심 메시지, Figure, 데이터를 추출 |
| **story-architect** | 스토리 설계 | 발표 내러티브 구성, 시간 배분, 청중 맞춤 |
| **slide-composer** | 슬라이드 구성 | 슬라이드별 콘텐츠 작성, 레이아웃 지정, Figure 배치 |
| **pptx-engineer** | PPTX 생성 | python-pptx 코드 작성/실행, 실제 .pptx 파일 생성 |
| **deck-reviewer** | 발표 검토 | 과학적 정확성, 디자인, 타이밍 검토 + 발표 코칭 |

## 실행 모드: 에이전트 팀

```
연구 결과 입력
    │
    ▼
content-extractor → story-architect → slide-composer → pptx-engineer → deck-reviewer
                                                                          │
                                                             ┌────────────┤
                                                          REVISE        PASS
                                                             │            │
                                                             ▼            ▼
                                                      slide-composer    최종 PPTX +
                                                      (수정, 최대 2회)  발표 코칭
```

## 데이터 전달 규칙

| 에이전트 | 출력 파일 |
|---|---|
| content-extractor | `_workspace/01_content_brief.md` |
| story-architect | `_workspace/02_story_structure.md` |
| slide-composer | `_workspace/03_slide_deck.md` |
| pptx-engineer | `_workspace/04_make_ppt.py`, `_workspace/output/*.pptx` |
| deck-reviewer | `_workspace/05_review_report.md`, `_workspace/06_speaker_guide.md` |

**규칙:**
1. 에이전트 간 데이터는 `_workspace/` 파일로 전달한다
2. Figure 원본은 `_workspace/figures/`에, 슬라이드 삽입용은 `_workspace/output/`에 배치
3. 모든 중간 산출물을 보존한다

## 기술 스택

| 범주 | 도구 |
|---|---|
| PPT 생성 | python-pptx |
| 시각화 | matplotlib (DPI=300) |
| 폰트 | Noto Sans CJK KR |
| 슬라이드 크기 | 16:9 (13.333" × 7.5") |

## 입력 소스

- `01-research-production/_workspace/` 의 연구 산출물 (논문 초안, Figure, Table)
- 사용자 직접 제공 파일 (논문 PDF, Figure 이미지)
- 자연어 요청 ("이 연구 결과로 15분 학회 발표 PPT 만들어줘")

## 사용 언어

- 사용자 대면: 한국어
- 슬라이드: 영어 (국제 학회) 또는 한국어 (사용자 지정)
- 코드: 영어
