#!/usr/bin/env python3
"""SSWL AI 하네스 v2.0 소개 팜플렛 — PPT 생성."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── 색상 팔레트 ──
NAVY = RGBColor(0x1A, 0x23, 0x7E)
BLUE = RGBColor(0x28, 0x35, 0x93)
INDIGO = RGBColor(0x39, 0x49, 0xAB)
LIGHT_BG = RGBColor(0xE8, 0xEA, 0xF6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x1A, 0x1A, 0x1A)
GRAY = RGBColor(0x66, 0x66, 0x66)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
GREEN = RGBColor(0x2E, 0x7D, 0x32)
TEAL = RGBColor(0x00, 0x69, 0x5C)
PURPLE = RGBColor(0x4A, 0x14, 0x8C)
LIGHT_GREEN = RGBColor(0xE8, 0xF5, 0xE9)
LIGHT_TEAL = RGBColor(0xE0, 0xF2, 0xF1)
LIGHT_PURPLE = RGBColor(0xF3, 0xE5, 0xF5)
TABLE_HEADER_BG = RGBColor(0x1A, 0x23, 0x7E)
TABLE_ROW_ALT = RGBColor(0xF5, 0xF5, 0xF5)
TABLE_BORDER = RGBColor(0xC5, 0xCA, 0xE9)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

FONT_NAME = "Noto Sans CJK KR"


# ── 헬퍼 함수 ──
def set_font(run, size=14, bold=False, color=BLACK, name=FONT_NAME, italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = name
    run.font.italic = italic


def add_textbox(slide, left, top, width, height):
    return slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))


def add_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    shape.adjustments[0] = 0.05
    return shape


def add_table(slide, rows, cols, left, top, width, height):
    return slide.shapes.add_table(rows, cols, Inches(left), Inches(top), Inches(width), Inches(height)).table


def style_table(table, headers, data, col_widths=None):
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = Inches(w)
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = ""
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = h
        set_font(run, size=12, bold=True, color=WHITE)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TABLE_HEADER_BG
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, row_data in enumerate(data):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j > 0 else PP_ALIGN.CENTER
            run = p.add_run()
            run.text = str(val)
            set_font(run, size=11, color=DARK_GRAY)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = TABLE_ROW_ALT if i % 2 == 1 else WHITE
    tblPr = table._tbl.tblPr
    if tblPr is None:
        tblPr = table._tbl._new_tblPr()
    tblPr.set("firstRow", "1")
    tblPr.set("bandRow", "1")


def add_paragraph(tf, text, size=14, bold=False, color=BLACK, align=PP_ALIGN.LEFT, space_after=6):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    run = p.add_run()
    run.text = text
    set_font(run, size=size, bold=bold, color=color)
    return run


def add_step_boxes(slide, steps, start_x, start_y, accent_color, dark_color):
    for i, (title, desc) in enumerate(steps):
        row = i // 3
        col = i % 3
        x = start_x + col * 1.9
        y = start_y + row * 2.1
        add_rect(slide, x, y, 1.7, 1.8, WHITE, accent_color)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.65), Inches(y + 0.1), Inches(0.4), Inches(0.4))
        circle.fill.solid()
        circle.fill.fore_color.rgb = accent_color
        circle.line.fill.background()
        cp = circle.text_frame.paragraphs[0]
        cp.alignment = PP_ALIGN.CENTER
        cr = cp.add_run()
        cr.text = str(i + 1)
        set_font(cr, size=13, bold=True, color=WHITE)
        tb2 = add_textbox(slide, x + 0.1, y + 0.55, 1.5, 0.4)
        p2 = tb2.text_frame.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = title
        set_font(r2, size=12, bold=True, color=dark_color)
        tb3 = add_textbox(slide, x + 0.1, y + 0.95, 1.5, 0.8)
        tb3.text_frame.word_wrap = True
        p3 = tb3.text_frame.paragraphs[0]
        p3.alignment = PP_ALIGN.CENTER
        r3 = p3.add_run()
        r3.text = desc
        set_font(r3, size=10, color=GRAY)


# ============================================================
# 슬라이드 1: 표지
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, NAVY)
add_rect(slide, 0, 0, 13.333, 0.08, INDIGO)

tb = add_textbox(slide, 1, 1.5, 11.333, 0.6)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "태양 및 우주환경연구실을 위한 연구 지원 AI 시스템"
set_font(run, size=18, color=RGBColor(0xC5, 0xCA, 0xE9))

tb = add_textbox(slide, 1, 2.2, 11.333, 1.5)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "SSWL AI Harness v2.0"
set_font(run, size=48, bold=True, color=WHITE)

add_rect(slide, 5, 3.7, 3.333, 0.04, INDIGO)

tb = add_textbox(slide, 1, 4.0, 11.333, 0.6)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "모델 아카이빙  ·  연구 업무 수행  ·  아이디어→실험 결과  ·  논문 초안"
set_font(run, size=20, color=RGBColor(0x9F, 0xA8, 0xDA))

tb = add_textbox(slide, 2, 5.0, 9.333, 0.8)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = '"연구실에서 개발된 모델을 누구나 활용하고, 아이디어를 빠르게 검증합니다."'
set_font(run, size=15, color=RGBColor(0x9F, 0xA8, 0xDA), italic=True)

tb = add_textbox(slide, 1, 6.5, 11.333, 0.5)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "2026  ·  태양 및 우주환경연구실"
set_font(run, size=13, color=RGBColor(0x79, 0x86, 0xCB))


# ============================================================
# 슬라이드 2: 왜 필요한가?
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)

tb = add_textbox(slide, 0.8, 0.4, 11, 0.7)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "이 시스템은 왜 필요한가요?"
set_font(run, size=30, bold=True, color=NAVY)
add_rect(slide, 0.8, 1.05, 2.5, 0.05, INDIGO)

headers = ["기존 방식", "문제점"]
data = [
    ["연구실 모델이 개발자 PC에만 존재", "개발자 부재 시 아무도 실행 불가"],
    ["모델 실행 방법이 구전으로 전수", "새 연구자 합류 시 재교육 필요"],
    ["데이터 수집을 사이트별로 수동", "연구 시간 상당 부분이 데이터 수집에 소요"],
    ["아이디어에서 실험까지 오래 걸림", "아이디어 → 데이터 → 실행 → 분석이 수일~수주"],
    ["모델 버전 관리 부재", "어떤 버전으로 어떤 결과를 냈는지 추적 불가"],
]
tbl = add_table(slide, 6, 2, 0.8, 1.5, 7.5, 3.0)
style_table(tbl, headers, data, col_widths=[3.5, 4.0])

box = add_rect(slide, 8.8, 1.5, 3.8, 3.0, LIGHT_BG, TABLE_BORDER)
tb = add_textbox(slide, 9.0, 1.7, 3.4, 2.6)
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
run = p.add_run()
run.text = "SSWL AI 하네스 v2.0은"
set_font(run, size=14, bold=True, color=NAVY)
add_paragraph(tf, "", size=6)
add_paragraph(tf, "모델을 표준화·아카이빙하고", size=13, color=DARK_GRAY)
add_paragraph(tf, "누구나 자연어로 실행하며", size=13, color=DARK_GRAY, space_after=2)
add_paragraph(tf, "아이디어를 빠르게 실험 결과로", size=13, color=DARK_GRAY, space_after=2)
add_paragraph(tf, "전환합니다.", size=13, color=DARK_GRAY)

box = add_rect(slide, 0.8, 5.0, 11.7, 0.9, LIGHT_BG, TABLE_BORDER)
tb = add_textbox(slide, 1.0, 5.1, 11.3, 0.7)
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "모델은 자산화  ·  누구나 활용  ·  아이디어에서 결과까지 당일 확인"
set_font(run, size=18, bold=True, color=INDIGO)


# ============================================================
# 슬라이드 3: 시스템 한눈에 보기 — 3가지 모드
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)

tb = add_textbox(slide, 0.8, 0.4, 11, 0.7)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "시스템 한눈에 보기 — 세 가지 핵심 기능"
set_font(run, size=30, bold=True, color=NAVY)
add_rect(slide, 0.8, 1.05, 2.5, 0.05, INDIGO)

# 기능 1: 연구 업무 수행
add_rect(slide, 0.5, 1.5, 3.9, 5.2, LIGHT_BG, RGBColor(0x90, 0xCA, 0xF9))
tb = add_textbox(slide, 0.6, 1.6, 3.7, 0.5)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "① 연구 업무 수행"
set_font(run, size=16, bold=True, color=BLUE)

steps = [
    ("연구자 요청", "자연어로\n작업 요청"),
    ("계획 수립", "AI가 실행계획\n자동 생성"),
    ("승인", "연구자가\n계획 검토·승인"),
    ("자동 실행", "데이터 수집 →\n모델 실행"),
    ("결과 보고", "보고서 생성\n시각화 포함"),
    ("후속 제안", "다음 분석\n자동 제안"),
]
for i, (title, desc) in enumerate(steps):
    row = i // 2
    col = i % 2
    x = 0.6 + col * 1.9
    y = 2.2 + row * 1.55
    add_rect(slide, x, y, 1.7, 1.35, WHITE, INDIGO)
    tb2 = add_textbox(slide, x + 0.1, y + 0.1, 1.5, 0.35)
    p2 = tb2.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = f"{i+1}. {title}"
    set_font(r2, size=11, bold=True, color=NAVY)
    tb3 = add_textbox(slide, x + 0.1, y + 0.5, 1.5, 0.7)
    tb3.text_frame.word_wrap = True
    p3 = tb3.text_frame.paragraphs[0]
    p3.alignment = PP_ALIGN.CENTER
    r3 = p3.add_run()
    r3.text = desc
    set_font(r3, size=10, color=GRAY)

# 기능 2: 모델 아카이빙
add_rect(slide, 4.7, 1.5, 3.9, 5.2, LIGHT_GREEN, RGBColor(0xA5, 0xD6, 0xA7))
tb = add_textbox(slide, 4.8, 1.6, 3.7, 0.5)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "② 모델 아카이빙 & 활용"
set_font(run, size=16, bold=True, color=GREEN)

archive_items = [
    ("모델 등록", "코드 분석 →\n모델 카드 자동 생성"),
    ("모델 목록", "등록된 모델\n표/카드로 조회"),
    ("모델 활용", "자연어 요청 →\n자동 실행·결과 보고"),
    ("버전 관리", "업데이트 시\n이전 버전 보존"),
]
for i, (title, desc) in enumerate(archive_items):
    row = i // 2
    col = i % 2
    x = 4.8 + col * 1.9
    y = 2.2 + row * 1.55
    add_rect(slide, x, y, 1.7, 1.35, WHITE, GREEN)
    tb2 = add_textbox(slide, x + 0.1, y + 0.1, 1.5, 0.35)
    p2 = tb2.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = title
    set_font(r2, size=11, bold=True, color=RGBColor(0x1B, 0x5E, 0x20))
    tb3 = add_textbox(slide, x + 0.1, y + 0.5, 1.5, 0.7)
    tb3.text_frame.word_wrap = True
    p3 = tb3.text_frame.paragraphs[0]
    p3.alignment = PP_ALIGN.CENTER
    r3 = p3.add_run()
    r3.text = desc
    set_font(r3, size=10, color=GRAY)

# 핵심 문구
tb = add_textbox(slide, 4.8, 5.65, 3.7, 0.9)
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "개발에 참여하지 않은\n연구자도 동일하게 사용 가능"
set_font(run, size=12, bold=True, color=GREEN)

# 기능 3: 아이디어 → 실험
add_rect(slide, 8.9, 1.5, 3.9, 5.2, LIGHT_PURPLE, RGBColor(0xCE, 0x93, 0xD8))
tb = add_textbox(slide, 9.0, 1.6, 3.7, 0.5)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "③ 아이디어 → 실험 결과"
set_font(run, size=16, bold=True, color=PURPLE)

idea_items = [
    ("아이디어 분석", "핵심 질문 추출\n가설 수립"),
    ("실험 설계", "Baseline vs\nExperiment 설계"),
    ("실험 실행", "데이터 수집 →\n모델 실행 → 비교"),
    ("결과 + 논문", "통계 분석 보고\n논문 초안 작성"),
]
for i, (title, desc) in enumerate(idea_items):
    row = i // 2
    col = i % 2
    x = 9.0 + col * 1.9
    y = 2.2 + row * 1.55
    add_rect(slide, x, y, 1.7, 1.35, WHITE, PURPLE)
    tb2 = add_textbox(slide, x + 0.1, y + 0.1, 1.5, 0.35)
    p2 = tb2.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = title
    set_font(r2, size=11, bold=True, color=PURPLE)
    tb3 = add_textbox(slide, x + 0.1, y + 0.5, 1.5, 0.7)
    tb3.text_frame.word_wrap = True
    p3 = tb3.text_frame.paragraphs[0]
    p3.alignment = PP_ALIGN.CENTER
    r3 = p3.add_run()
    r3.text = desc
    set_font(r3, size=10, color=GRAY)

# 핵심 문구
tb = add_textbox(slide, 9.0, 5.65, 3.7, 0.9)
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = '"교수님 아이디어 말씀하시면\n간단한 실험 결과 보여드립니다"'
set_font(run, size=12, bold=True, color=PURPLE, italic=True)


# ============================================================
# 슬라이드 4: 연구 업무 수행 상세
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)

tb = add_textbox(slide, 0.8, 0.4, 11, 0.7)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = '기능 1. 연구 업무 수행 — "말하면 해줍니다"'
set_font(run, size=28, bold=True, color=NAVY)
add_rect(slide, 0.8, 1.05, 3.0, 0.05, INDIGO)

# 좌측: 요청 예시
add_rect(slide, 0.8, 1.4, 5.5, 2.5, LIGHT_BG, TABLE_BORDER)
tb = add_textbox(slide, 1.0, 1.5, 5.1, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "요청 예시"
set_font(run, size=16, bold=True, color=NAVY)

examples = [
    '"최근 1달 HMI 데이터로 synoptic map 만들어줘"',
    '"AIA 193 이미지에서 코로나홀 찾아줘"',
    '"이걸로 PFSS 시뮬레이션 돌려줘"',
]
tb = add_textbox(slide, 1.0, 2.0, 5.1, 1.8)
tf = tb.text_frame
tf.word_wrap = True
for ex in examples:
    add_paragraph(tf, ex, size=13, color=DARK_GRAY, space_after=8)

# 우측: 처리 흐름
add_rect(slide, 6.8, 1.4, 5.8, 2.5, WHITE, TABLE_BORDER)
tb = add_textbox(slide, 7.0, 1.5, 5.4, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "처리 흐름"
set_font(run, size=16, bold=True, color=NAVY)

flow_steps = [
    "요청 → query-planner가 실행 계획 수립",
    "연구자 승인 (반드시 승인 후 실행)",
    "task-executor가 자동 실행 (데이터→모델→후처리)",
    "result-reporter가 결과 보고 + 후속 제안",
]
tb = add_textbox(slide, 7.0, 2.0, 5.4, 1.8)
tf = tb.text_frame
tf.word_wrap = True
for i, step in enumerate(flow_steps):
    add_paragraph(tf, f"{i+1}. {step}", size=12, color=DARK_GRAY, space_after=6)

# 하단: 시나리오 예시
add_rect(slide, 0.8, 4.2, 11.7, 2.5, RGBColor(0xFD, 0xFD, 0xE8), RGBColor(0xE0, 0xE0, 0xE0))
tb = add_textbox(slide, 1.0, 4.3, 11.3, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "시나리오: Synoptic Map → PFSS 연속 작업"
set_font(run, size=14, bold=True, color=NAVY)

tb = add_textbox(slide, 1.0, 4.7, 11.3, 1.8)
tf = tb.text_frame
tf.word_wrap = True
add_paragraph(tf, '연구자: "최근 1달 SO/PHI와 SDO/HMI 데이터로 synoptic map 만들어줘"', size=11, color=DARK_GRAY, space_after=4)
add_paragraph(tf, '→ AI: 계획 제시 (4단계, 40~60분 예상) → 승인 후 자동 실행 → 결과 보고', size=11, color=GRAY, space_after=4)
add_paragraph(tf, '→ "이 map으로 PFSS 시뮬레이션 가능합니다"', size=11, color=GRAY, space_after=4)
add_paragraph(tf, '연구자: "이걸로 PFSS 돌려줘" → 이전 결과 자동 참조하여 즉시 실행', size=11, color=DARK_GRAY, space_after=4)


# ============================================================
# 슬라이드 5: 모델 아카이빙 상세
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)

tb = add_textbox(slide, 0.8, 0.4, 11, 0.7)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = '기능 2. 모델 아카이빙 — "개발하지 않았어도 사용합니다"'
set_font(run, size=28, bold=True, color=NAVY)
add_rect(slide, 0.8, 1.05, 3.0, 0.05, INDIGO)

# 좌측: 등록 흐름
add_rect(slide, 0.8, 1.4, 5.8, 2.2, LIGHT_GREEN, RGBColor(0xA5, 0xD6, 0xA7))
tb = add_textbox(slide, 1.0, 1.5, 5.4, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "모델 등록 흐름"
set_font(run, size=16, bold=True, color=GREEN)

tb = add_textbox(slide, 1.0, 2.0, 5.4, 1.5)
tf = tb.text_frame
tf.word_wrap = True
add_paragraph(tf, '개발자: "코로나홀 탐지 모델 등록해줘. 코드는 여기에."', size=12, color=DARK_GRAY, space_after=6)
add_paragraph(tf, '→ AI가 코드 분석 (입출력, 의존성, 실행 방법 파악)', size=11, color=GRAY, space_after=4)
add_paragraph(tf, '→ 모델 카드(사용 설명서) + 실행 래퍼 자동 생성', size=11, color=GRAY, space_after=4)
add_paragraph(tf, '→ model_registry에 등록 완료 + 테스트 실행', size=11, color=GRAY)

# 우측: 활용 흐름
add_rect(slide, 7.0, 1.4, 5.8, 2.2, LIGHT_BG, TABLE_BORDER)
tb = add_textbox(slide, 7.2, 1.5, 5.4, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "모델 활용 (개발 미참여 연구자)"
set_font(run, size=16, bold=True, color=NAVY)

tb = add_textbox(slide, 7.2, 2.0, 5.4, 1.5)
tf = tb.text_frame
tf.word_wrap = True
add_paragraph(tf, '연구자B: "코로나홀 탐지 모델로 어제 AIA 193 분석해줘"', size=12, color=DARK_GRAY, space_after=6)
add_paragraph(tf, '→ 모델 카드 참조 → 필요 데이터 자동 수집 (JSOC)', size=11, color=GRAY, space_after=4)
add_paragraph(tf, '→ 모델 자동 실행', size=11, color=GRAY, space_after=4)
add_paragraph(tf, '→ 결과 시각화 및 보고', size=11, color=GRAY)

# 하단: 모델 목록 테이블
tb = add_textbox(slide, 0.8, 3.9, 5, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "등록 모델 목록 예시"
set_font(run, size=16, bold=True, color=NAVY)

headers = ["#", "모델명", "용도", "입력", "개발자"]
data = [
    ["1", "coronal_hole_detect", "코로나홀 탐지", "AIA 193 A", "김연구"],
    ["2", "dem_model", "DEM 분석", "AIA 6채널", "이연구"],
    ["3", "pix2pixcc_fsi", "EUI 채널 합성", "FSI 174+304", "윤준무"],
    ["4", "synoptic_map", "Synoptic map", "HMI 자기장", "(내장)"],
    ["5", "pfss_sim", "PFSS 시뮬레이션", "Synoptic map", "(내장)"],
]
tbl = add_table(slide, 6, 5, 0.8, 4.3, 11.7, 2.5)
style_table(tbl, headers, data, col_widths=[0.5, 2.5, 2.5, 2.5, 1.5])


# ============================================================
# 슬라이드 6: 아이디어 → 실험 결과 상세
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)

tb = add_textbox(slide, 0.8, 0.4, 11, 0.7)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = '기능 3. 아이디어 → 실험 결과 — "말하면 실험합니다"'
set_font(run, size=28, bold=True, color=NAVY)
add_rect(slide, 0.8, 1.05, 3.0, 0.05, INDIGO)

# 시나리오 예시
add_rect(slide, 0.8, 1.4, 11.7, 5.3, RGBColor(0xFD, 0xFD, 0xFD), RGBColor(0xE0, 0xE0, 0xE0))

tb = add_textbox(slide, 1.0, 1.5, 11.3, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "시나리오: EUI DEM 연구에서 Magnetogram 추가 효과 검증"
set_font(run, size=15, bold=True, color=PURPLE)

# 좌측: 대화 흐름
tb = add_textbox(slide, 1.0, 2.0, 5.5, 4.5)
tf = tb.text_frame
tf.word_wrap = True

add_paragraph(tf, '교수님:', size=12, bold=True, color=PURPLE, space_after=2)
add_paragraph(tf, '"Solar Orbiter DEM 연구에서 Magnetogram을\n DL 입력에 추가하면 합성 채널이 좋아질까?"', size=11, color=DARK_GRAY, space_after=8)

add_paragraph(tf, 'AI → 아이디어 분석:', size=12, bold=True, color=NAVY, space_after=2)
add_paragraph(tf, '배경: EUI/FSI 2채널 → Pix2PixCC → 합성 5채널 → DEM', size=10, color=GRAY, space_after=2)
add_paragraph(tf, '제안: DL 입력에 magnetogram 추가 시 품질 개선?', size=10, color=GRAY, space_after=8)

add_paragraph(tf, 'AI → 실험 설계:', size=12, bold=True, color=NAVY, space_after=2)
add_paragraph(tf, 'Baseline: AIA 171+304 → Pix2PixCC → DEM', size=10, color=GRAY, space_after=2)
add_paragraph(tf, 'Experiment: 171+304+HMI mag → Modified Pix2PixCC → DEM', size=10, color=GRAY, space_after=2)
add_paragraph(tf, 'Reference: 실제 AIA 6채널 DEM (ground truth)', size=10, color=GRAY, space_after=8)

add_paragraph(tf, '교수님: "비교할 때 활동영역과 조용한 영역 따로 봐줘"', size=11, color=DARK_GRAY, space_after=2)
add_paragraph(tf, '→ AI: 영역 분류 단계 추가하여 계획 수정', size=10, color=GRAY)

# 우측: 결과
add_rect(slide, 6.8, 2.0, 5.5, 2.5, LIGHT_PURPLE, RGBColor(0xCE, 0x93, 0xD8))
tb = add_textbox(slide, 7.0, 2.1, 5.1, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "실험 결과 (예시)"
set_font(run, size=14, bold=True, color=PURPLE)

tb = add_textbox(slide, 7.0, 2.5, 5.1, 1.8)
tf = tb.text_frame
tf.word_wrap = True
add_paragraph(tf, '합성 94 A 채널 CC: 0.87 → 0.91 개선', size=11, color=DARK_GRAY, space_after=6)
add_paragraph(tf, '활동영역 DEM:', size=11, bold=True, color=PURPLE, space_after=2)
add_paragraph(tf, '  logT 6.0~6.5 EM 오차 15% 감소', size=11, color=DARK_GRAY, space_after=6)
add_paragraph(tf, '조용한 영역:', size=11, bold=True, color=PURPLE, space_after=2)
add_paragraph(tf, '  유의미한 차이 없음', size=11, color=DARK_GRAY)

# 논문 초안 박스
add_rect(slide, 6.8, 4.8, 5.5, 1.7, LIGHT_BG, TABLE_BORDER)
tb = add_textbox(slide, 7.0, 4.9, 5.1, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = '"이걸로 논문 초안 써줘"'
set_font(run, size=14, bold=True, color=NAVY)

tb = add_textbox(slide, 7.0, 5.3, 5.1, 1.1)
tf = tb.text_frame
tf.word_wrap = True
add_paragraph(tf, '→ Introduction: EUI DEM 한계 + DL 접근 배경', size=10, color=GRAY, space_after=2)
add_paragraph(tf, '→ Method: Pix2PixCC 수정, 학습 데이터, DEM 방법론', size=10, color=GRAY, space_after=2)
add_paragraph(tf, '→ Results: 채널 품질 비교 + DEM 비교 (영역별)', size=10, color=GRAY, space_after=2)
add_paragraph(tf, '→ Discussion: 자기장 정보 기여 해석 + 한계', size=10, color=GRAY)


# ============================================================
# 슬라이드 7: 연구실 논문 아카이브
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)

tb = add_textbox(slide, 0.8, 0.4, 11, 0.7)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "연구실 논문 아카이브 (51편, 2019~2026)"
set_font(run, size=28, bold=True, color=NAVY)
add_rect(slide, 0.8, 1.05, 3.0, 0.05, INDIGO)

headers = ["연구 분야", "주요 내용", "논문 수"]
data = [
    ["딥러닝 이미지 변환/합성", "EUV↔자기장, 채널 합성, 백색광, He I", "8편"],
    ["태양 뒷면 자기장", "STEREO/EUV → farside magnetogram", "4편"],
    ["DEM 연구", "EUI 합성 채널 → DEM, Pixel-to-pixel", "2편"],
    ["우주기상 예보", "태양풍, IMF Bz, 플레어, 전리층 예측", "12편"],
    ["태양 자기장/코로나", "NLFFF, PFSS, Synoptic map, 3D 복원", "8편"],
    ["코로나 진동/파동", "플룸, 루프, Alfven 속도", "5편"],
    ["CME/SEP", "CME 질량, ICME, SEP 소스", "5편"],
    ["미션/관측 시스템", "L4 미션, 망원경 제어, 채널 최적화", "3편"],
]
tbl = add_table(slide, 9, 3, 0.8, 1.4, 7.0, 4.0)
style_table(tbl, headers, data, col_widths=[2.5, 3.5, 1.0])

# 우측: 주요 저널
add_rect(slide, 8.3, 1.4, 4.5, 2.5, LIGHT_BG, TABLE_BORDER)
tb = add_textbox(slide, 8.5, 1.5, 4.1, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "게재 저널"
set_font(run, size=16, bold=True, color=NAVY)

tb = add_textbox(slide, 8.5, 1.9, 4.1, 1.8)
tf = tb.text_frame
tf.word_wrap = True
add_paragraph(tf, "Nature Astronomy — 2편", size=12, bold=True, color=DARK_GRAY, space_after=4)
add_paragraph(tf, "ApJ / ApJS / ApJL — 다수", size=12, color=DARK_GRAY, space_after=4)
add_paragraph(tf, "A&A, Space Weather", size=12, color=DARK_GRAY, space_after=4)
add_paragraph(tf, "Solar Physics, Remote Sensing", size=12, color=DARK_GRAY, space_after=4)
add_paragraph(tf, "JKAS, JASTP, PASP", size=12, color=DARK_GRAY)

# 활용 예시
add_rect(slide, 8.3, 4.2, 4.5, 2.3, RGBColor(0xFD, 0xFD, 0xE8), RGBColor(0xE0, 0xE0, 0xE0))
tb = add_textbox(slide, 8.5, 4.3, 4.1, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "AI에게 물어보세요"
set_font(run, size=14, bold=True, color=NAVY)

tb = add_textbox(slide, 8.5, 4.7, 4.1, 1.6)
tf = tb.text_frame
tf.word_wrap = True
add_paragraph(tf, '"플레어 예보 관련 논문 뭐가 있어?"', size=11, color=DARK_GRAY, space_after=6)
add_paragraph(tf, '"태양 뒷면 자기장 연구 히스토리\n 정리해줘"', size=11, color=DARK_GRAY, space_after=6)
add_paragraph(tf, '"DEM 관련 우리 논문 참고문헌에\n 넣으려는데 찾아줘"', size=11, color=DARK_GRAY)


# ============================================================
# 슬라이드 8: 기대 효과
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)

tb = add_textbox(slide, 0.8, 0.4, 11, 0.7)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "기대 효과"
set_font(run, size=30, bold=True, color=NAVY)
add_rect(slide, 0.8, 1.05, 1.5, 0.05, INDIGO)

# 연구자 개인
headers = ["항목", "기존", "도입 후"]
data = [
    ["모델 사용", "개발자에게 의존, 구전 교육", "자연어로 누구나 즉시 실행"],
    ["데이터 수집", "여러 사이트 수동 다운로드", "AI가 자동 수집·검증"],
    ["아이디어 검증", "데이터 수집~분석까지 수일", "아이디어 제시 후 당일 결과"],
    ["모델 실행", "명령어 직접 입력, 환경 세팅", "자연어 요청으로 자동 실행"],
    ["논문 초안", "백지부터 직접 작성", "실험 결과 기반 골격 자동 생성"],
]
tbl = add_table(slide, 6, 3, 0.8, 1.3, 7.5, 2.8)
style_table(tbl, headers, data, col_widths=[1.5, 3.0, 3.0])

# 연구실 차원
add_rect(slide, 8.8, 1.3, 4.0, 2.8, LIGHT_BG, TABLE_BORDER)
tb = add_textbox(slide, 9.0, 1.4, 3.6, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "연구실 차원"
set_font(run, size=16, bold=True, color=NAVY)

tb = add_textbox(slide, 9.0, 1.8, 3.6, 2.1)
tf = tb.text_frame
tf.word_wrap = True
add_paragraph(tf, "모델 자산화", size=13, bold=True, color=NAVY, space_after=2)
add_paragraph(tf, "개인 PC에 묻히지 않고 연구실 자산으로", size=10, color=GRAY, space_after=8)
add_paragraph(tf, "지식 전수", size=13, bold=True, color=NAVY, space_after=2)
add_paragraph(tf, "신규 연구자도 등록 모델 즉시 활용", size=10, color=GRAY, space_after=8)
add_paragraph(tf, "연구 가속", size=13, bold=True, color=NAVY, space_after=2)
add_paragraph(tf, "아이디어 → 초기 결과까지 시간 대폭 단축", size=10, color=GRAY, space_after=8)
add_paragraph(tf, "재현성 확보", size=13, bold=True, color=NAVY, space_after=2)
add_paragraph(tf, "모델 버전 관리로 결과 추적 가능", size=10, color=GRAY)

# 하단: v1 vs v2 비교
tb = add_textbox(slide, 0.8, 4.4, 5, 0.4)
p = tb.text_frame.paragraphs[0]
run = p.add_run()
run.text = "v1.0 → v2.0 변경사항"
set_font(run, size=16, bold=True, color=NAVY)

headers = ["항목", "v1.0", "v2.0"]
data = [
    ["상시운용 (24h 감시)", "있음", "제거"],
    ["연구 업무 수행", "보조 모드", "핵심 모드"],
    ["모델 아카이빙", "없음", "신규 추가"],
    ["아이디어→실험", "없음", "신규 추가"],
    ["논문 초안 작성", "없음", "신규 추가"],
]
tbl = add_table(slide, 6, 3, 0.8, 4.8, 11.7, 2.3)
style_table(tbl, headers, data, col_widths=[3.5, 3.0, 3.0])


# ============================================================
# 슬라이드 9: 기술 요약 + 마무리
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, NAVY)
add_rect(slide, 0, 0, 13.333, 0.08, INDIGO)

# 기술 요약
tb = add_textbox(slide, 1, 0.5, 11.333, 0.7)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "기술 요약"
set_font(run, size=28, bold=True, color=WHITE)

# 스펙 박스들
specs = [
    ("기반 기술", "Claude Code\n(Anthropic AI)\n에이전트 프레임워크"),
    ("AI 모듈", "7개 전문 에이전트\n6개 스킬"),
    ("데이터", "NOAA, SDO, Solar Orbiter\nSTEREO, VSO"),
    ("모델 관리", "파일 기반 레지스트리\nmodel_card.md"),
    ("알림", "Slack Webhook\nTelegram Bot API"),
]

for i, (title, desc) in enumerate(specs):
    x = 0.8 + i * 2.5
    add_rect(slide, x, 1.5, 2.2, 2.2, INDIGO)
    tb2 = add_textbox(slide, x + 0.1, 1.6, 2.0, 0.4)
    p2 = tb2.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = title
    set_font(r2, size=14, bold=True, color=RGBColor(0xC5, 0xCA, 0xE9))
    tb3 = add_textbox(slide, x + 0.1, 2.1, 2.0, 1.4)
    tb3.text_frame.word_wrap = True
    p3 = tb3.text_frame.paragraphs[0]
    p3.alignment = PP_ALIGN.CENTER
    r3 = p3.add_run()
    r3.text = desc
    set_font(r3, size=12, color=WHITE)

# 구분선
add_rect(slide, 5, 4.2, 3.333, 0.04, INDIGO)

# 메인 메시지
tb = add_textbox(slide, 1, 4.5, 11.333, 1.5)
tf = tb.text_frame
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "SSWL AI Harness v2.0"
set_font(run, size=36, bold=True, color=WHITE)

add_paragraph(tf, "", size=8)
r = add_paragraph(tf, "연구실에서 개발된 모델을 누구나 활용하고,", size=16, color=RGBColor(0x9F, 0xA8, 0xDA), align=PP_ALIGN.CENTER, space_after=2)
add_paragraph(tf, "아이디어를 빠르게 검증합니다.", size=16, color=RGBColor(0x9F, 0xA8, 0xDA), align=PP_ALIGN.CENTER)

# 하단 안내문
tb = add_textbox(slide, 1, 6.5, 11.333, 0.5)
p = tb.text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "본 시스템은 연구자의 판단을 대체하지 않습니다. AI는 도구이며, 최종 의사결정은 항상 연구자에게 있습니다."
set_font(run, size=11, color=RGBColor(0x79, 0x86, 0xCB), italic=True)


# ============================================================
# 저장
# ============================================================
output_path = "/home/youn_j/SSWL-harness-ops/pamphlet.pptx"
prs.save(output_path)
print(f"PPT 저장 완료: {output_path}")
print(f"총 {len(prs.slides)} 슬라이드")
