#!/usr/bin/env bash
# chunk_pdf.sh — PDF를 섹션 단위로 분할 (1차) 또는 페이지 균등 분할 (2차 폴백)
#
# 사용법:
#   chunk_pdf.sh <paper_id> <pdf_path> <out_dir>
#
# 결과:
#   <out_dir>/<paper_id>/<section>.md 파일들
#   헤더에 paper_id, section, split (section|page-range), confidence (high|low), source_pages 명시
#
# 종속:
#   pdftotext (poppler-utils)
#   pdfinfo   (poppler-utils)

set -euo pipefail

PAPER_ID="${1:?paper_id required}"
PDF_PATH="${2:?pdf_path required}"
OUT_DIR="${3:?out_dir required}"

WORK_DIR="${OUT_DIR}/${PAPER_ID}"
mkdir -p "${WORK_DIR}"

if [[ ! -f "${PDF_PATH}" ]]; then
  echo "ERROR: PDF not found at ${PDF_PATH}" >&2
  exit 1
fi

# ---- 1차: 섹션 인식 ----
TXT_FILE="${WORK_DIR}/_fulltext.txt"
pdftotext -layout "${PDF_PATH}" "${TXT_FILE}"

# 섹션 헤딩 정규식 매칭
HEADING_RE='^[[:space:]]*(([0-9]+\.?)+[[:space:]]+)?(Abstract|Introduction|Related Work|Background|Method(s|ology)?|Approach|Experiments?|Result(s)?|Discussion|Conclusion(s)?|Acknowledg(e?)ments?|References)[[:space:]]*$'

# 헤딩 라인 번호 추출
mapfile -t HEADINGS < <(grep -niE "${HEADING_RE}" "${TXT_FILE}" || true)

if [[ "${#HEADINGS[@]}" -ge 3 ]]; then
  # ---- 섹션 분할 성공 ----
  SPLIT_MODE="section"
  CONFIDENCE="high"

  TOTAL_LINES=$(wc -l < "${TXT_FILE}")
  for i in "${!HEADINGS[@]}"; do
    LINE_NUM="${HEADINGS[$i]%%:*}"
    HEADER_TEXT=$(echo "${HEADINGS[$i]}" | cut -d: -f2- | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

    # 다음 헤딩 직전 또는 EOF
    if [[ "$((i+1))" -lt "${#HEADINGS[@]}" ]]; then
      NEXT_LINE="${HEADINGS[$((i+1))]%%:*}"
      END_LINE=$((NEXT_LINE - 1))
    else
      END_LINE="${TOTAL_LINES}"
    fi

    # 섹션 이름 정규화
    SECTION_NAME=$(echo "${HEADER_TEXT}" | tr '[:upper:]' '[:lower:]' \
      | sed 's/[0-9.]//g' | sed 's/[[:space:]]*//g' \
      | sed 's/methods/method/; s/results/result/; s/experiments/experiment/; s/conclusions/conclusion/; s/references/references/')

    # References는 분석 대상 아님 — 스킵
    if [[ "${SECTION_NAME}" == "references" ]]; then continue; fi

    OUT_FILE="${WORK_DIR}/${SECTION_NAME}.md"
    {
      echo "---"
      echo "paper_id: ${PAPER_ID}"
      echo "section: ${SECTION_NAME}"
      echo "split: ${SPLIT_MODE}"
      echo "confidence: ${CONFIDENCE}"
      echo "source_lines: ${LINE_NUM}-${END_LINE}"
      echo "---"
      echo
      sed -n "${LINE_NUM},${END_LINE}p" "${TXT_FILE}"
    } > "${OUT_FILE}"
  done
else
  # ---- 2차 폴백: 페이지 5등분 ----
  SPLIT_MODE="page-range"
  CONFIDENCE="low"

  PAGE_COUNT=$(pdfinfo "${PDF_PATH}" | awk '/^Pages:/ {print $2}')
  if [[ -z "${PAGE_COUNT}" || "${PAGE_COUNT}" -lt 1 ]]; then
    echo "ERROR: cannot determine page count for ${PDF_PATH}" >&2
    exit 1
  fi

  SECTIONS=(abstract intro method result conclusion)
  N=${#SECTIONS[@]}
  CHUNK=$(( (PAGE_COUNT + N - 1) / N ))  # ceil

  for i in "${!SECTIONS[@]}"; do
    SECTION_NAME="${SECTIONS[$i]}"
    START_PAGE=$(( i * CHUNK + 1 ))
    END_PAGE=$(( (i + 1) * CHUNK ))
    if [[ "${END_PAGE}" -gt "${PAGE_COUNT}" ]]; then END_PAGE="${PAGE_COUNT}"; fi
    if [[ "${START_PAGE}" -gt "${PAGE_COUNT}" ]]; then break; fi

    OUT_FILE="${WORK_DIR}/${SECTION_NAME}.md"
    {
      echo "---"
      echo "paper_id: ${PAPER_ID}"
      echo "section: ${SECTION_NAME}"
      echo "split: ${SPLIT_MODE}"
      echo "confidence: ${CONFIDENCE}"
      echo "source_pages: ${START_PAGE}-${END_PAGE}"
      echo "---"
      echo
      pdftotext -layout -f "${START_PAGE}" -l "${END_PAGE}" "${PDF_PATH}" -
    } > "${OUT_FILE}"
  done
fi

# 임시 풀텍스트 정리
rm -f "${TXT_FILE}"

echo "DONE: chunks at ${WORK_DIR}/"
ls "${WORK_DIR}/"
