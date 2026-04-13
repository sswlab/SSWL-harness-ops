# SSWL Harness-Ops Plugin Audit — Action Items

Date: 2026-04-13
Harness version: v2.0 (harness.json 기준, plugin.json 부재)
Peers compared: plugin-dev (Anthropic), feature-dev@1.0.0, pr-review-toolkit (MIT), skill-creator, claude-md-management, hookify, security-guidance, code-review@1.0.0, frontend-design
Peer marketplace path: `~/.claude/plugins/marketplaces/claude-plugins-official/`

---

## Executive Summary

- **Positioning**: 태양물리 연구실(SSWL)에 특화된 멀티-하네스 연구 자동화 시스템. 연구 설계→실험→논문→리뷰의 전 과정을 에이전트 팀으로 자동화.
- **Strengths** (peer 대비 명확히 우수한 점)
  1. **도메인 특화 깊이**: 7개 하네스가 각각 연구생산, PPT, 논문작성, 논문읽기, SR, 논문편집, 코드수집이라는 명확한 단일 목적을 가짐 — peer 플러그인 중 이 수준의 도메인 깊이를 가진 것 없음
  2. **파이프라인 구조화**: 에이전트 간 파일 기반 데이터 전달, 출력 디렉토리 분리, 루프백 조건 등이 `_workspace/` 규약으로 표준화됨
  3. **내부 용어 방화벽 (03-paper-writer)**: V1–V7 버전 코드, 내부 목표치, 하네스 용어가 논문에 유출되지 않도록 3중 방어선(co-worker → editor → reviewer) 설계 — peer에 없는 독자적 기여
- **Gaps** (severity: high / medium / low)
  1. **[high]** 플러그인 표준 미준수 — `plugin.json` 부재, `skill.md` → `SKILL.md` 컨벤션 미준수, 배포 불가능 상태
  2. **[high]** 전체 39개 에이전트에 `tools:`, `model:`, `color:` 미지정 — 최소 권한 원칙 위반, 리소스 낭비
  3. **[high]** hooks/guardrails 전무 — 보안 검증, 세션 초기화, 작업 완료 확인 등 자동화된 안전장치 없음

---

## 1. Inventory

| 항목 | SSWL (전체) | SSWL (root) | plugin-dev | feature-dev | pr-review-toolkit | skill-creator | hookify |
|---|---|---|---|---|---|---|---|
| Skills | 20 | 3 | 7 | 0 (command) | 0 | 1 (내부 agents/scripts 포함) | 1 |
| Agents | 39 | 5 | 3 | 3 | 6 | 0 (skill 내부) | 1 |
| Hooks | 0 | 0 | 0 | 0 | 0 | 0 | 4 (PreToolUse, PostToolUse, Stop, UserPromptSubmit) |
| Scripts | 1 (install.sh) | 0 | 0 | 0 | 0 | 9 | 0 |
| plugin.json | 없음 | 없음 | 있음 | 있음 (README) | 있음 (README) | 없음 | 없음 |
| Docs | README + docs/3개 | CLAUDE.md | README (403줄) | README (413줄) | README (314줄) | README (4줄) | README (340줄) |

---

## 2. Scope Coherence

- **Verdict**: **focused** (개별 하네스) / **diffuse** (root 하네스)
- **Evidence**:
  - 개별 하네스(01–06, 99): 각각 단일 목적으로 잘 분리됨. `harness.json`의 name/description이 내용과 일치.
  - Root 하네스(`.claude/`): research-orchestrator, data-pipeline, research-workflow 3개 스킬이 범위가 넓고 matchPatterns가 중복됨. research-orchestrator의 키워드("분석해줘", "만들어줘", "돌려줘")가 research-workflow의 키워드("분석해줘", "만들어줘", "돌려줘")와 완전 중복.
  - 01-research-production은 root 하네스의 기능을 거의 포함하면서 더 구체적 — root 하네스의 존재 의의가 불분명.

---

## 3. Skill Design

| Skill | Frontmatter 완성도 | 단일 책임 | Description 품질 | Verdict |
|---|---|---|---|---|
| research-orchestrator (root) | name+description만. version/user-invocable 없음 | 오케스트레이터로 적절 | 키워드 나열식, peer 대비 트리거 조건 불명확 | 보완 필요 |
| data-pipeline (root) | 동일 | 수집+아카이빙 혼합 | 키워드 과다 (30+개) | 분리 검토 |
| research-workflow (root) | 동일 | orchestrator와 범위 중복 | "아이디어→실험→논문" 전 범위 | 중복 정리 필요 |
| paper-orchestrator (03) | 동일 | 적절 | 구체적 | 양호 |
| latex-compiler (03) | 동일 | 적절 | 적절 | 양호 |
| paper-read (04) | 동일 | 적절 | 트리거 패턴 구체적 | 양호 |
| sr-orchestrator (05) | 동일 | 적절 | 구체적 | 양호 |
| skill-collector-orchestrator (99) | 동일 | 적절 | 키워드 과다 | 트리거 정리 필요 |

**Peer 대비 공통 문제**:
- `version:` 필드 0개 (peer: skill-creator 0.1.0, plugin-dev skills 전부 0.1.0)
- `user-invocable:` 필드 0개 (slash command로 호출 불가 — 04-paper-mate의 `/paper-read`만 description 내에 암시)
- 파일명 `skill.md` (소문자) vs peer 표준 `SKILL.md` (대문자) — auto-discovery 호환 미확인
- description 내 "키워드:" 패턴은 비표준. peer는 description 자체를 자연어 트리거 문장으로 작성 (skill-creator: "Use when users want to create a skill from scratch...")

---

## 4. Agent Design

| Agent (대표) | tools: 지정 | model: 지정 | color: 지정 | 스킬 대체 가능성 | Verdict |
|---|---|---|---|---|---|
| research-planner (root) | 없음 | 없음 | 없음 | 아니오 | 보완 필요 |
| reviewer (root) | 없음 | 없음 | 없음 | 아니오 | 보완 필요 |
| data-engineer (root) | 없음 | 없음 | 없음 | 아니오 | 보완 필요 |
| grammar-editor (06) | 없음 | 없음 | 없음 | 스킬 대체 검토 | 과잉 |
| reference-finder (06) | 없음 | 없음 | 없음 | 스킬 대체 검토 | 과잉 |
| structure-advisor (06) | 없음 | 없음 | 없음 | 읽기 전용이면 스킬 가능 | 과잉 |
| co-worker (03) | 없음 | 없음 | 없음 | 아니오 (문장별 체크 로직) | 양호 |

**Peer 비교**:
- `feature-dev/code-reviewer`: `tools: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput` / `model: sonnet` / `color: red` — 10개 도구를 명시적으로 제한
- `pr-review-toolkit/code-reviewer`: `model: opus` / `color: green` — 높은 정확도 필요 작업에만 opus 할당
- **SSWL 39개 에이전트 전부**: tools/model/color 미지정 → 모든 에이전트가 모든 도구 접근 가능, 모델 선택 제어 불가, UI 구분 불가

**핵심 문제**: reviewer 에이전트가 Write/Edit 도구에 접근 가능 — 검토자가 원고를 직접 수정할 수 있는 구조적 위험. `tools: Read, Glob, Grep, WebSearch` 로 제한해야 함.

---

## 5. Hook Footprint

| Check | SSWL | security-guidance | hookify | Peer 평균 |
|---|---|---|---|---|
| Blocking hooks | 0 | 1 (PreToolUse: Edit/Write/MultiEdit) | 동적 (사용자 정의) | ~0.5 |
| Session hooks | 0 | 0 | 0 | ~0.3 (explanatory/learning) |
| Stop hooks | 0 | 0 | 1 | ~0.2 |
| Total hooks | 0 | 1 | 4 | ~1.0 |

**분석**:
- **guardrail 전무**: security-guidance처럼 Edit/Write 시 보안 패턴 체크하는 훅 없음
- **세션 초기화 없음**: explanatory-output-style처럼 SessionStart에서 컨텍스트를 주입하는 훅 없음
- **작업 완료 검증 없음**: Stop 훅으로 결과물 체크리스트 확인하는 기능 없음
- **settings.local.json으로 부분 대체**: root 하네스의 WebFetch 도메인 제한(SWPC/JSOC/SOAR)은 훅 대신 permission으로 구현 — 이 방식도 유효하지만, 동적 규칙에는 한계

**오탐 위험**: 해당 없음 (훅 자체가 없으므로)
**실패 모드**: 해당 없음

---

## 6. Namespacing & Distribution

| Check | Status | Detail |
|---|---|---|
| plugin.json 존재 | ❌ 없음 | `.claude-plugin/plugin.json` 디렉토리 자체가 부재 |
| name 필드 | ❌ | 플러그인 수준 이름 없음 |
| version 필드 | ❌ | 전체 버전 관리 없음 (harness.json에도 version 없음) |
| description 필드 | △ | CLAUDE.md에 서술형으로 존재하나 구조화되지 않음 |
| author 필드 | ❌ | 저자 정보 없음 |
| repository/homepage | ❌ | 없음 |
| keywords | ❌ | 없음 |
| 스킬 네이밍 | △ | kebab-case 준수 (research-orchestrator 등), 그러나 네임스페이스 접두사 없음 |
| 에이전트 네이밍 | △ | kebab-case 준수, 네임스페이스 없음 |
| CHANGELOG | ❌ | 없음 (peer: plugin-dev, feature-dev 등도 대부분 없음) |
| 파일명 컨벤션 | ❌ | `skill.md` (소문자) — peer 표준은 `SKILL.md` (대문자) |
| 배포 가능성 | ❌ | `/plugin install` 불가 — plugin.json 없이 마켓플레이스 등록 불가 |

**Peer 비교**: plugin-dev의 plugin.json은 `{"name": "plugin-dev", "description": "...", "author": {"name": "Anthropic", "email": "..."}}`. SSWL은 이에 해당하는 메타데이터가 완전히 부재.

---

## 7. Overlap Map

| SSWL 기능 | 가장 가까운 Peer | 관계 | Note |
|---|---|---|---|
| research-planner (설계) | feature-dev/code-architect | 보완 | 도메인이 다름 (연구 vs 소프트웨어). 개념적 유사 |
| reviewer (품질검토) | pr-review-toolkit/code-reviewer | 보완 | 학술 리뷰 vs 코드 리뷰. 접근 방식 유사 (confidence scoring 없음) |
| paper-writer (논문) | — | **독자** | Peer에 학술 논문 작성 기능 전무 |
| latex-compiler | — | **독자** | LaTeX 컴파일 스킬은 peer에 없음 |
| sr-orchestrator (SR) | — | **독자** | Symbolic Regression 파이프라인은 peer에 없음 |
| paper-read (번역) | — | **독자** | 논문 번역+분석 파이프라인은 peer에 없음 |
| skill-collector-orchestrator | skill-creator | **보완** | 기존 코드→스킬 변환 vs 처음부터 스킬 생성 |
| 내부용어 방화벽 (03) | — | **독자** | Peer에 없는 독자적 기여 |
| research-orchestrator (오케스트레이션) | — | **독자** | 멀티-에이전트 파이프라인 오케스트레이터는 peer에 없음 |
| 없음 (보안 훅) | security-guidance | **누락** | SSWL에 보안 패턴 검증 없음 |
| 없음 (세션 컨텍스트) | explanatory-output-style | **누락** | SessionStart 시 도메인 지식 주입 없음 |
| 없음 (코드 단순화) | pr-review-toolkit/code-simplifier | **누락** | 자동 코드 정리 없음 |

---

## 8. Documentation Parity

| Artifact | SSWL | Peer 평균 | Gap |
|---|---|---|---|
| Root README | 있음, 하네스별 설명 포함 | 있음 (300–400줄) | △ — 04, 06 하네스 누락 |
| 하네스별 README | 01–06, 99 각각 있음 | N/A (플러그인은 단일 README) | 양호 |
| CLAUDE.md (시스템 프롬프트) | 매우 상세 (03은 특히 정교) | N/A (peer는 SKILL.md에 통합) | 강점 |
| 인라인 스킬 문서 | description만 (본문은 상세) | description + SKILL.md 본문 상세 | 양호 |
| 사용 예시/시나리오 | docs/scenarios.md, docs/pamphlet.md | README 내 예시 섹션 | 양호 |
| 스크린샷/다이어그램 | ASCII 다이어그램만 | 없음 (대부분) | 동등 |
| API/Integration 문서 | 없음 | 없음 (대부분) | 동등 |

---

## 9. Real-World Utility

### Research Scenarios (주요 사용 시나리오)

| Scenario | Value (+) | Friction (-) | Net |
|---|---|---|---|
| 신규 연구 실행 (01-research-production) | 문헌조사→설계→실행→논문 자동화, 에이전트 분업 | 초기 입력 4개 항목(주제, 목적, 모드, 경로) 필수 — 진입 장벽 | + |
| 논문 작성 (03-paper-writer) | 3중 방화벽, 병렬 리뷰, max 3 리비전, LaTeX 출력 | 모든 에이전트가 전 도구 접근 가능 — 리뷰어가 원고 수정 위험 | + (tools 제한 시 ++) |
| 논문 읽기/번역 (04-paper-mate) | 챕터 병렬 번역, 용어 통일, 참고문헌 분석, Q&A | 없음 — 잘 설계됨 | ++ |
| 학회 PPT 생성 (02) | 콘텐츠→스토리→슬라이드→PPTX 자동화, 발표 코칭 | python-pptx 실행 실패 시 복구 경로 불명확 | + |
| Symbolic Regression (05) | 7개 도구 자동 라우팅, Pareto front, SymPy 후처리 | install.sh 의존성 설치 실패 시 안내 부족 | + |
| 논문 편집 (06) | 문법교정, 팩트체크, 모의리뷰 멀티모드 | 5개 에이전트 모두 도구 미제한 — grammar-editor가 Bash 접근 가능 | 0 (tools 제한 시 +) |
| 기존 코드→스킬 변환 (99) | 고유한 가치 — 연구실 코드 자산화 | 실제 사용 빈도 낮을 가능성 | 0 / + |

### Non-Research Scenarios

| Scenario | Value (+) | Friction (-) | Net |
|---|---|---|---|
| 일반 코딩 작업 | root 하네스의 research-orchestrator가 "분석해줘" 등 일반 요청도 가로챔 | 단순 코드 편집에서 연구 파이프라인 발동 가능성 | - |
| 단순 메모/문서 작성 | 하네스 개입 없음 | 없음 | 0 |
| 데이터 탐색 (비연구) | data-pipeline 스킬이 FITS/SDO 키워드에만 반응 | 일반 데이터 작업에는 도움 안 됨 | 0 |

### Dead Weight

- **root 하네스 전체** — 01-research-production이 더 구체적이고 완전한 상위 호환. root 하네스의 5개 에이전트 + 3개 스킬이 01과 대부분 중복.
- **research-workflow (root 스킬)** — research-orchestrator와 키워드·기능이 거의 완전 중복. 두 스킬의 구분이 불명확.
- **data-pipeline의 "모델 아카이빙" 파트** — `_workspace/model_registry/` 참조이지만, 실제 등록된 모델이 있는지 불확실. 빈 인프라일 가능성.

### Missing Surfaces (Peer가 제공하지만 SSWL이 놓친 자동화)

- **confidence scoring (0–100)**: pr-review-toolkit/feature-dev의 리뷰어는 이슈별 신뢰도 점수를 매기고 ≥80만 보고. SSWL reviewer는 PASS/REVISE/FAIL 3단계만 사용 — 이슈 심각도 구분 부재.
- **verification-before-completion**: 작업 완료 전 체크리스트 자동 확인 (Stop 훅 활용). SSWL에는 없음.
- **자동 코드 리뷰 트리거**: pr-review-toolkit은 코드 작성 후 자동으로 code-reviewer를 호출하도록 description에 명시. SSWL의 연구 리뷰는 오케스트레이터가 수동 호출.
- **description 최적화 도구**: skill-creator의 `improve_description.py` — 스킬 트리거 정확도를 자동 개선. SSWL 스킬의 description 품질 검증 도구 없음.
- **eval/benchmark 체계**: skill-creator의 eval 실행 → 채점 → 벤치마크 → 뷰어 생성 파이프라인. SSWL에는 스킬/에이전트 성능 측정 체계 없음.

### Friction Hotspots

- **root 하네스 키워드 충돌**: "분석해줘", "만들어줘", "돌려줘"가 research-orchestrator와 research-workflow 양쪽에 등록 — 어느 스킬이 발동할지 예측 불가.
- **에이전트 도구 과잉 접근**: reviewer가 Edit/Write로 원고를 직접 수정하거나, grammar-editor가 Bash로 시스템 명령을 실행할 수 있는 구조적 위험.
- **settings.local.json 불일치**: root(Bash 광범위 허용) vs 01(tee 2개만) vs 03(빈 배열) — 하네스 간 보안 수준 일관성 없음.
- **harness.json에 version 없음**: 어떤 버전의 하네스를 사용 중인지 추적 불가.

### Escape Hatches

- **문서화된 우회 경로 없음**: 오케스트레이터를 건너뛰고 특정 에이전트를 직접 호출하는 방법이 명시되지 않음.
- **스킬 비활성화 방법 없음**: hookify처럼 `enabled: false`로 특정 스킬을 끄는 메커니즘 없음.

---

## Action Items

### [high] — 즉시 조치 권장

- [ ] **H1. 에이전트 `tools:` 명시**: 39개 에이전트 전부에 최소 권한 원칙 적용.
  - reviewer 계열 (root/reviewer, 01/reviewer, 03/reviewer-1, 03/reviewer-2, 06/reviewer): `tools: Read, Glob, Grep, WebSearch, WebFetch`
  - planner 계열 (root/research-planner, 01/research-designer, 05/sr-planner): `tools: Read, Glob, Grep, WebSearch, WebFetch, Bash(읽기 전용)`
  - executor 계열 (root/research-executor, 01/research-executor, 05/sr-executor): `tools: Read, Glob, Grep, Bash, Write, Edit, WebFetch`
  - writer 계열 (root/paper-writer, 01/paper-writer, 03/researcher): `tools: Read, Glob, Grep, Write, Edit, WebFetch, WebSearch`
  - 06/grammar-editor, 06/structure-advisor: `tools: Read, Glob, Grep` (읽기 전용)
  - 06/fact-checker, 06/reference-finder: `tools: Read, Glob, Grep, WebSearch, WebFetch`

- [ ] **H2. 에이전트 `model:` 명시**: 작업 복잡도에 따라 모델 배정.
  - 고복잡도 (research-planner, paper-writer, editor, reviewer 계열): `model: opus` 또는 `model: sonnet` (비용-품질 균형에 따라)
  - 단순 실행 (grammar-editor, reference-finder, chapter-translator): `model: haiku` 또는 `model: sonnet`
  - 코드 실행 (research-executor, sr-executor, pptx-engineer): `model: sonnet`

- [ ] **H3. `skill.md` → `SKILL.md` 리네이밍**: 20개 스킬 파일 전부. Claude Code auto-discovery 표준 준수.
  - `find . -name 'skill.md' -path '*/.claude/skills/*' -exec bash -c 'mv "$1" "$(dirname "$1")/SKILL.md"' _ {} \;`

- [ ] **H4. root 하네스 정리**: research-orchestrator와 research-workflow의 키워드 중복 해소.
  - 옵션 A: research-workflow 삭제, research-orchestrator에 통합
  - 옵션 B: research-orchestrator = 파이프라인 흐름 제어, research-workflow = 아이디어→실험→논문 콘텐츠 가이드로 명확 분리
  - 01-research-production과의 중복도 정리 필요 — root를 "라우터"로 축소하고 실제 로직은 01에 집중

- [ ] **H5. settings.local.json 일관성 확보**: 모든 하네스에 settings.local.json 배치.
  - 02, 04, 05, 06, 99에 settings.local.json 없음 → 최소한 빈 `{"permissions": {"allow": []}}` 배치
  - root의 `Bash(python3:*)` 는 지나치게 넓음 — 하네스별로 필요한 명령만 허용

### [medium] — 다음 이터레이션에서 조치

- [ ] **M1. plugin.json 생성**: 마켓플레이스 배포를 고려한다면 각 하네스 또는 전체 프로젝트에 `.claude-plugin/plugin.json` 추가.
  ```json
  {
    "name": "sswl-harness",
    "version": "2.0.0",
    "description": "Solar & Space Weather Laboratory research automation harness",
    "author": {"name": "SSWL", "email": "..."},
    "keywords": ["solar-physics", "research", "paper-writing", "symbolic-regression"]
  }
  ```

- [ ] **M2. 스킬 frontmatter 보강**: 전 스킬에 `version:`, `user-invocable:` 추가.
  - `version: 1.0.0` (또는 현재 상태에 맞는 버전)
  - 사용자가 slash command로 호출할 수 있어야 하는 스킬에 `user-invocable: true` 명시 (최소: paper-read, sr-orchestrator, presentation-orchestrator, paper-orchestrator, skill-collector-orchestrator)

- [ ] **M3. 에이전트 `color:` 지정**: 하네스 내에서 에이전트 출력을 시각적으로 구분.
  - planner → blue, executor → green, writer → yellow, reviewer → red (peer 관례 참조)

- [ ] **M4. confidence scoring 도입 (reviewer 에이전트)**: PASS/REVISE/FAIL 외에 이슈별 0–100 신뢰도 점수.
  - peer 참조: `pr-review-toolkit/code-reviewer` — "Only report issues with confidence >= 80"
  - 학술 리뷰에 적용: Major(≥80) / Minor(60–79) / Suggestion(<60) 매핑

- [ ] **M5. harness.json에 version 필드 추가**: 각 하네스의 변경 이력 추적.
  ```json
  {"name": "...", "description": "...", "version": "1.0.0"}
  ```

- [ ] **M6. 보안 훅 도입**: security-guidance 스타일의 PreToolUse 훅.
  - 최소한 `_workspace/` 외부 파일 수정 시 경고
  - `.env`, credentials, API key 패턴 감지

- [ ] **M7. README.md 보완**: root README에서 04-paper-mate, 06-paper-editor 누락 → 추가.

- [ ] **M8. description 키워드 스타일 개선**: "키워드: X, Y, Z" 나열 방식 → peer 스타일의 자연어 트리거 문장으로 전환.
  - Before: `키워드: 분석해줘, 계획, 실험 설계, 가설, 아이디어`
  - After: `사용자가 연구 아이디어를 제시하거나 "분석해줘", "실험 설계해줘" 등의 요청을 할 때 사용한다. 가설 수립, 실험 계획, 실현 가능성 평가를 수행한다.`

### [low] — 향후 개선

- [ ] **L1. SessionStart 훅 도입**: 세션 시작 시 현재 하네스 컨텍스트, 최근 작업 상태, 주의사항을 자동 주입.
  - explanatory-output-style 참조: `hooks.json` → `SessionStart` → bash script

- [ ] **L2. Stop 훅 도입**: 작업 완료 시 `_workspace/` 산출물 체크리스트 자동 확인.
  - "plans/ 에 계획 파일이 있는가?", "figures/ 에 Figure가 DPI=300인가?" 등

- [ ] **L3. 스킬 eval 체계 구축**: skill-creator 스타일의 eval → 채점 → 벤치마크.
  - 최소한: 각 오케스트레이터 스킬에 대해 3–5개 테스트 프롬프트 + 예상 결과 정의

- [ ] **L4. 에이전트→스킬 전환 검토**: 06-paper-editor의 일부 에이전트가 단순 체크리스트형.
  - grammar-editor: "문법 교정 가이드" 스킬로 대체 가능 (에이전트 오버헤드 불필요)
  - structure-advisor: "구조 개선 가이드" 스킬로 대체 가능 (원고 수정 안 함)

- [ ] **L5. escape hatch 문서화**: 오케스트레이터를 건너뛰고 개별 에이전트를 직접 호출하는 방법, 스킬 비활성화 방법을 각 하네스 README에 추가.

- [ ] **L6. CHANGELOG.md 도입**: 하네스 변경 이력 추적. 최소한 root 수준에서 주요 변경사항 기록.

- [ ] **L7. data-pipeline 스킬 분리**: "데이터 수집" 과 "모델 아카이빙" 을 별도 스킬로 분리 — 단일 책임 원칙.

---

## 01-Research-Production 실전 개선 — V2→V13 경험 기반

> Harness-first-study에서 STIX-GOES 변환 연구를 V2부터 V13까지 13회 반복 수행한 경험에서 도출한 개선 사항.
> 기존 Action Items(H1–H5, M1–M8, L1–L7)는 구조/표준 관점이고, 아래는 **실제 연구 워크플로우에서 드러난 기능 결함**이다.

### [high] — 즉시 조치 권장

- [ ] **R1. 반복 연구(iteration) 모드 신설**: 현재 하네스는 단일 사이클(문헌→설계→실행→리뷰→논문)만 지원한다. V2→V13처럼 이전 버전 결과를 기반으로 가설을 수정하고 재실험하는 "continuation" 모드가 없다.
  - **증거**: V12 research-note.md 첫 줄이 "V11에서 BKG 완성도 향상(99.2%)으로 near-side focal MAE 10.4% 개선을 달성했으나..." — 이전 버전 참조가 필수적이었음
  - **필요한 것**:
    - 필수 입력에 `{이전 작업경로}` 항목 추가 (선택적)
    - 제공 시 literature-reviewer를 건너뛰고 research-designer가 이전 결과 + 실패 분석을 읽어 새 가설 수립
    - research-note.md에 "이전 버전 요약" 섹션을 자동 생성
    - 연구 모드에 **반복형(iterative)** 추가: 이전 결과 읽기 → 실패 분석 → 새 가설 → 실행 → 비교

- [ ] **R2. 내부 용어 차단 정책(Internal Terminology Firewall) 도입**: 01 하네스의 paper-writer에는 03-paper-writer의 내부 용어 방화벽이 전혀 없다. V2→V13까지 13개 버전 코드(V2, V5.1, V10.5 등)가 논문에 유출될 위험이 크다.
  - **증거**: 03-paper-writer에서 이 방화벽이 co-worker→editor→reviewer 3중 방어선으로 작동하여 V 코드 유출을 차단함
  - **필요한 것**:
    - paper-writer 에이전트에 차단 대상 목록 추가: 내부 버전 코드, 내부 목표/타겟, 하네스 용어, 내부 파일명, 버전 이력
    - reviewer 에이전트의 Phase 6(레퍼리 심사)에 "Internal Terminology Leak" 체크 항목 추가
    - 변환 원칙: "V12 모델" → "the proposed model", "V5→V7→V12 개선" → 최종 모델만 보고

- [ ] **R3. Figure 상한 5개 → 저널별 유동 조정**: 현재 paper-writer가 Figure+Table 합계 5개로 제한하나, 실제 ApJ 논문에서 Figure 6개 + Table 2개가 필요했다.
  - **증거**: V13 최종 논문 `latex/ApJ/round1/`에 fig1~fig6 총 6개 Figure
  - **필요한 것**:
    - 고정 상한 5개 삭제 → 저널별 가이드라인으로 대체
    - ApJ/ApJL: Figure 10개 이내 권장 / ApJL: 4개 이내 / A&A: 자유 / Solar Physics: 자유
    - paper-writer가 Figure 선별 시 저널 가이드라인을 참조하되, 사용자 승인 하에 조정 가능

### [medium] — 다음 이터레이션에서 조치

- [ ] **R4. 코드 파일명 템플릿 유연화**: 현재 스킬이 `01_data_download.py`~`06_figures.py` 고정 구조를 제시하나, 실제 연구에서는 버전마다 전혀 다른 스크립트 구조가 생성되었다.
  - **증거**: V2 `00_data_filtering.py`, V4 `00b_reextract.py`, V9 `01_composite_survey.py`, V11 `10_download_bkg_full.py`, V13 `26_farside_stiefel_hint.py` — 템플릿과 무관한 넘버링과 파일명
  - **필요한 것**:
    - 고정 템플릿 대신 **naming convention 가이드** 제공: `{NN}_{동사}_{대상}.py` (예: `20_build_v12_dataset.py`)
    - 반복 모드(R1)에서는 이전 버전의 마지막 번호 이후부터 넘버링 계속
    - `config.py`와 `utils.py`는 유지하되, 나머지는 연구 내용에 따라 자유 구성

- [ ] **R5. 크로스-버전 비교 메커니즘 추가**: 반복 연구에서 이전 버전 대비 성능 비교는 핵심인데, 하네스에 이를 지원하는 구조가 없다.
  - **증거**: V12 research-note에서 V11 대비 수치를 일일이 수작업으로 나열 (near-side MAE 0.0197→0.0190, X-class MAE 0.2775→0.1455 등)
  - **필요한 것**:
    - research-executor가 이전 버전의 평가 결과(JSON/CSV)를 자동 로드하여 비교 테이블 생성
    - 비교 Figure 자동 생성 (예: "버전별 metric 추이" 차트) — 단, 이 Figure는 내부용이며 논문에는 포함하지 않음 (R2 방화벽과 연동)
    - 비교 결과를 `{작업경로}/version_comparison.md`에 정리

- [ ] **R6. 실패 분석→새 가설 프레임워크 추가**: 현재 reviewer는 PASS/REVISE만 판정한다. 실제 연구에서는 "결과가 나왔으나 특정 부분이 기대에 미달" → "원인 분석" → "새 가설"의 사이클이 핵심이었다.
  - **증거**: V12에서 "far-side 66% flat 프로파일" 발견 → "peak hint가 uncalibrated BKG 때문" 원인 분석 → V13에서 "Stiefel catalog로 교정" 새 가설 → 검증 성공
  - **필요한 것**:
    - reviewer의 Phase 4에 "PASS-WITH-FINDINGS" 판정 추가: 핵심 결과는 유효하나 후속 연구가 필요한 발견사항 목록
    - 발견사항을 `{작업경로}/findings_for_next_version.md`로 출력
    - 반복 모드(R1)에서 research-designer가 이 파일을 읽어 새 가설 수립

- [ ] **R7. 03-paper-writer 핸드오프 프로토콜**: 01에서 연구 실행 후 논문 작성은 03-paper-writer에서 수행하는 것이 실제 패턴이었다. 두 하네스 간 핸드오프가 공식화되어 있지 않다.
  - **증거**: V12/V13 최종 논문은 03-paper-writer의 co-worker→editor→reviewer-1/2 파이프라인을 거쳐 Accept 판정
  - **필요한 것**:
    - 01의 paper-writer 결과물 또는 실행 결과를 03에 전달하는 표준 패키지 정의
    - 최소 패키지: `research-note.md`, `figures/`, `tables/`, `code/`, `references.bib`, `03_execution_log.md`
    - 01 paper-writer의 역할 재정의: "논문 초안"이 아니라 "결과 보고서 + 핵심 서사(narrative) 초안" — 정식 논문은 03에서 작성

- [ ] **R8. research-note.md 누락 방지 및 구조 강화**: 13개 버전 중 V3과 V13에서 research-note.md가 생성되지 않았다. 또한 버전별로 형식이 제각각이다.
  - **증거**: V3, V13에 research-note.md 부재. V2는 간략, V12는 매우 상세
  - **필요한 것**:
    - 파이프라인 시작 시 research-note.md를 자동 생성하고 Overview 섹션을 채우는 것을 오케스트레이터가 보장
    - 각 Phase 완료 시 해당 에이전트가 기록했는지 오케스트레이터가 확인 — 미기록 시 에이전트에게 재요청
    - 표준 섹션 구조 강제: Overview → Phase 1 → Phase 2 → ... → Summary/Next Steps

- [ ] **R9. 워크스페이스 네이밍 컨벤션 도입**: V2→V13 동안 `_workspace-V2`(대문자)와 `_workspace-v12`(소문자)가 혼재했다.
  - **증거**: `_workspace-V2`, `_workspace-V3`, ..., `_workspace-V9` vs `_workspace-v10.5`, `_workspace-v11`, `_workspace-v12`, `_workspace-v13`
  - **필요한 것**:
    - 작업 경로를 사용자가 자유롭게 지정하되, 반복 모드(R1) 사용 시 오케스트레이터가 네이밍 제안: `{프로젝트명}/_workspace-v{N}`
    - 이전 작업경로에서 버전 번호를 자동 감지하여 다음 번호 제안

### [low] — 향후 개선

- [ ] **R10. reviewer 이원화 검토**: 01 하네스는 reviewer 1명이 설계 검토(Phase 4)와 논문 심사(Phase 6)를 모두 담당한다. 03-paper-writer처럼 전문분야별 2명 리뷰어가 더 효과적일 수 있다.
  - **증거**: 03의 V12 논문 심사에서 reviewer-1(Solar Physics, strict)은 물리적 해석을 지적하고, reviewer-2(ML/DL, lenient)는 모델 아키텍처를 지적 — 분업이 효과적이었음
  - **고려사항**: 01은 논문 작성보다 연구 실행이 핵심이므로, 논문 심사는 03에 위임하고(R7) 01의 reviewer는 설계-결과 정합성 검토에 집중하는 것이 더 합리적일 수 있음

- [ ] **R11. 문헌조사 증분 업데이트 모드**: 반복 연구에서 매번 전체 문헌조사를 다시 할 필요가 없다. "마지막 조사 이후 새 논문" 만 검색하는 증분 모드가 필요하다.
  - **필요한 것**:
    - literature-reviewer에 `{이전 references.bib}` 입력 옵션 추가
    - 기존 BibTeX에 없는 새 논문만 검색하여 추가
    - 연구 모드 "반복형"(R1)에서 자동 활성화

- [ ] **R12. 프로젝트 수준 메타데이터 파일**: 13개 버전에 걸친 연구의 전체 맥락(프로젝트명, 대상 저널, 핵심 가설 변천, 데이터셋 진화)을 기록하는 프로젝트 수준 설정 파일이 없다.
  - **필요한 것**:
    - `{프로젝트_루트}/project-meta.json` 또는 `.md` 파일
    - 내용: 프로젝트명, 대상 저널, 공동 저자, 핵심 데이터셋, 버전 이력 요약, 현재 상태
    - 반복 모드(R1)에서 오케스트레이터가 이 파일을 읽어 컨텍스트 제공
    - 새 버전 시작/완료 시 자동 업데이트

---

## Appendix

### Referenced Peer Paths (재현용)

```
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/feature-dev/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/pr-review-toolkit/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/claude-md-management/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/code-review/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/frontend-design/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/explanatory-output-style/
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/learning-output-style/
```

### 부재 확인된 Peer 플러그인

- `superpowers/` — 마켓플레이스에 존재하지 않음
- `chrome-devtools-mcp/` — 마켓플레이스에 존재하지 않음
- `figma/` — 마켓플레이스에 존재하지 않음

### SSWL 전체 에이전트 목록 (39개)

| # | Harness | Agent | tools 지정 | model 지정 |
|---|---|---|---|---|
| 1 | root | research-planner | ❌ | ❌ |
| 2 | root | data-engineer | ❌ | ❌ |
| 3 | root | research-executor | ❌ | ❌ |
| 4 | root | paper-writer | ❌ | ❌ |
| 5 | root | reviewer | ❌ | ❌ |
| 6 | 01 | literature-reviewer | ❌ | ❌ |
| 7 | 01 | research-designer | ❌ | ❌ |
| 8 | 01 | research-executor | ❌ | ❌ |
| 9 | 01 | paper-writer | ❌ | ❌ |
| 10 | 01 | reviewer | ❌ | ❌ |
| 11 | 02 | content-extractor | ❌ | ❌ |
| 12 | 02 | story-architect | ❌ | ❌ |
| 13 | 02 | slide-composer | ❌ | ❌ |
| 14 | 02 | pptx-engineer | ❌ | ❌ |
| 15 | 02 | deck-reviewer | ❌ | ❌ |
| 16 | 03 | researcher | ❌ | ❌ |
| 17 | 03 | co-worker | ❌ | ❌ |
| 18 | 03 | editor | ❌ | ❌ |
| 19 | 03 | reviewer-1 | ❌ | ❌ |
| 20 | 03 | reviewer-2 | ❌ | ❌ |
| 21 | 04 | paper-fetcher | ❌ | ❌ |
| 22 | 04 | chapter-translator | ❌ | ❌ |
| 23 | 04 | figure-analyst | ❌ | ❌ |
| 24 | 04 | context-harmonizer | ❌ | ❌ |
| 25 | 04 | reference-analyst | ❌ | ❌ |
| 26 | 04 | qa-companion | ❌ | ❌ |
| 27 | 05 | sr-planner | ❌ | ❌ |
| 28 | 05 | sr-executor | ❌ | ❌ |
| 29 | 05 | expression-analyst | ❌ | ❌ |
| 30 | 05 | sr-reporter | ❌ | ❌ |
| 31 | 06 | grammar-editor | ❌ | ❌ |
| 32 | 06 | fact-checker | ❌ | ❌ |
| 33 | 06 | structure-advisor | ❌ | ❌ |
| 34 | 06 | reviewer | ❌ | ❌ |
| 35 | 06 | reference-finder | ❌ | ❌ |
| 36 | 99 | code-archaeologist | ❌ | ❌ |
| 37 | 99 | taxonomy-architect | ❌ | ❌ |
| 38 | 99 | code-refactorer | ❌ | ❌ |
| 39 | 99 | skill-builder | ❌ | ❌ |
| — | 99 | integration-tester | ❌ | ❌ |

(총 40개 — 99-SSWL-skill-collector에 integration-tester 포함)
