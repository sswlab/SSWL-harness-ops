# 04-Paper-Mate — 논문 읽어주는 하네스

> 영어 논문이 어려운 연구자를 위한 AI 논문 번역 & 분석 도우미

## 개요

Paper Mate는 영어 학술 논문을 **완전히 한국어로 번역**하고, 인용 논문을 **중요도별로 분류**하며, 번역된 내용을 기반으로 **후속 질문에 답변**하는 Claude Code 하네스입니다.

## 주요 기능

- **논문 확보**: DOI 주소, 논문 제목, 또는 직접 파일 제공
- **완전 번역**: 요약이나 생략 없이 논문 전체를 한국어로 번역
- **병렬 번역**: 챕터별로 동시에 번역하여 속도 확보 → 통합 시 문맥 조정
- **그림 분석**: 논문의 그림(Figure)을 시각적으로 분석하여 내용·맥락·인사이트를 한국어로 상세 설명
- **전문용어 병기**: 학술용어는 한국어(English) 형태로 표기
- **참고문헌 분석**: 인용 논문을 필수/권장/참고 3단계로 분류
- **필수 논문 요약**: 꼭 읽어야 할 논문을 별도로 요약·정리
- **Q&A 지원**: 번역 완료 후 논문 내용 및 그림에 대한 질문 응답

## 사용 방법

### 1. 하네스 디렉토리에서 Claude Code 실행

```bash
cd /home/youn_j/SSWL-harness-ops/04-paper-mate
claude
```

### 2. 논문 제공

아래 중 하나의 방법으로 논문을 제공합니다:

```
# DOI로 제공
이 논문 읽어줘: 10.1038/s41586-021-03854-z

# 제목으로 제공
"Attention Is All You Need" 논문 번역해줘

# 파일로 제공 (_workspace/papers/ 하위에 PDF 저장 후)
_workspace/papers/my_paper.pdf 논문 읽어줘
```

### 3. 결과물 확인

번역 완료 후 `_workspace/` (또는 지정한 작업 경로)에 다음 파일이 생성됩니다:

| 파일 | 내용 |
|------|------|
| `00_paper_source.md` | 원문 정보, 메타데이터, 구조 분석, 그림 목록 |
| `01_chapter_translations/` | 챕터별 개별 번역 (번역 노트 포함) |
| `02_full_translation.md` | 통합 완성 번역문 |
| `03_reference_analysis.md` | 참고문헌 중요도 분류 |
| `04_must_read_papers.md` | 필수 논문 상세 요약 |
| `05_qa_log.md` | Q&A 기록 |
| `06_figure_analysis.md` | 그림 분석 보고서 (그림이 있는 경우) |

### 4. 질문하기

번역 완료 후 자유롭게 질문할 수 있습니다:

```
이 논문에서 사용한 방법론을 쉽게 설명해줘
Figure 3의 결과가 무엇을 의미해?
이 논문의 한계는 뭐야?
필수 논문 중에서 가장 먼저 읽어야 할 것은?
```

## 에이전트 구성

| 에이전트 | 역할 |
|---|---|
| paper-fetcher | 논문 확보 & 구조 분석 & 그림 목록 추출 |
| chapter-translator | 챕터별 병렬 번역 |
| figure-analyst | 그림 시각 분석 & 맥락 해석 & 인사이트 정리 |
| context-harmonizer | 통합 & 용어 통일 & 문맥 조정 & 그림 분석 반영 |
| reference-analyst | 인용 논문 분석 & 필수 논문 요약 |
| qa-companion | 후속 질문 답변 (그림 포함) |

## 실행 흐름

```
논문 제공 (DOI / 제목 / 파일)
    │
    ▼
[paper-fetcher] 논문 확보 & 구조 분석 & 그림 목록 추출
    │
    ├──► [chapter-translator ×N] 챕터별 병렬 번역
    ├──► [figure-analyst] 그림 분석 (번역과 병렬 실행)
    │
    ▼
[context-harmonizer] 통합 & 문맥 조정 & 그림 분석 반영
    │
    ├──► [reference-analyst] 참고문헌 분석
    │
    ▼
[qa-companion] Q&A 대기
```
