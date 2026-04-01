---
name: research-orchestrator
description: >
  SSWL 연구 파이프라인 총괄 오케스트레이터.
  에이전트 실행 순서, 데이터 전달, 루프백, 에러 핸들링, 알림을 관리한다.
  모든 연구 작업이 시작될 때 이 스킬이 파이프라인을 조율한다.
  키워드: 시작, 실행, 파이프라인, 작업 요청, 분석해줘,
  만들어줘, 돌려줘, 연구, 실험, 데이터, 모델,
  synoptic map, PFSS, 코로나홀, DEM, 자기장,
  HMI, AIA, PHI, EUI, Solar Orbiter, SDO
---

# Research-Orchestrator — 파이프라인 총괄 오케스트레이터

## 개요

SSWL 연구실의 모든 연구 작업 파이프라인을 조율한다. 에이전트 실행 순서, 데이터 전달 경로, 사용자 승인 게이트, 품질 검토 게이트, 루프백 조건, 에러 핸들링, 완료/실패 알림을 관리한다.

---

## 파이프라인 흐름도

```
┌─────────────────────────────────────────────────────┐
│                   사용자 요청                         │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │   Phase 1: 연구 설계    │
          │   research-planner     │
          │   (요청 분석/실험 설계)   │
          └───────────┬────────────┘
                      │
              ┌───────▼───────┐
              │  QA Gate (옵션) │──── reviewer (실험 설계 검토)
              └───────┬───────┘
                      │
          ┌───────────▼────────────┐
          │   Phase 2: 사용자 승인   │◀──── 수정 요청 시 Phase 1로
          │   (계획 제시/승인 대기)   │      (최대 3회)
          └───────────┬────────────┘
                      │ 승인
                      ▼
          ┌────────────────────────┐
          │   Phase 3: 데이터 준비   │
          │   data-engineer        │
          │   (데이터 수집/검증)     │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │   Phase 4: 실험 실행    │
          │   research-executor    │
          │   (전처리/모델/후처리)   │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │   Phase 5: 결과 보고    │
          │   paper-writer         │
          │   (보고서/논문 초안)     │
          └───────────┬────────────┘
                      │
              ┌───────▼───────┐
              │  QA Gate (옵션) │──── reviewer (결과/논문 검토)
              └───────┬───────┘
                      │
                      ▼
          ┌────────────────────────┐
          │   Phase 6: 피드백 루프   │
          │   - 후속 작업? → Phase 1 │
          │   - 논문 초안? → Phase 5 │
          │   - 종료? → 알림 발송    │
          └────────────────────────┘
```

---

## 에이전트 간 데이터 전달 프로토콜

모든 에이전트 간 데이터 전달은 `_workspace/` 하위 파일 기반으로 수행한다.

### 전달 경로

| From | To | 전달 데이터 | 경로 |
|---|---|---|---|
| research-planner | research-executor | 실행 계획 (JSON) | `_workspace/plans/plan_{ts}.json` |
| research-planner | reviewer | 실험 설계 (MD) | `_workspace/experiments/exp_{ts}/design.md` |
| data-engineer | research-executor | 수집 데이터 | `_workspace/data/{source}/` |
| data-engineer | research-executor | 수집 결과 (JSON) | `_workspace/data/fetch_result_{ts}.json` |
| research-executor | paper-writer | 실행 결과 (JSON) | `_workspace/tasks/plan_{ts}/status.json` |
| research-executor | reviewer | 실험 결과 | `_workspace/experiments/exp_{ts}/` |
| paper-writer | reviewer | 논문 초안 (MD) | `_workspace/papers/draft_{ts}.md` |
| reviewer | research-planner | 검토 피드백 (MD) | `_workspace/reviews/review_{ts}.md` |

### 전달 규칙

1. 각 에이전트는 자신의 지정 디렉토리에만 쓰기를 수행한다.
2. 다른 에이전트의 출력은 읽기 전용으로 참조한다.
3. 파일명에는 반드시 timestamp를 포함하여 버전 충돌을 방지한다.
4. JSON 프로토콜 파일은 UTF-8 인코딩을 사용한다.
5. 중간 결과는 삭제하지 않고 보존한다.

---

## 루프백 조건과 최대 횟수

| 루프백 유형 | 조건 | 최대 횟수 | 초과 시 |
|---|---|---|---|
| **계획 수정** | 사용자가 실행 계획 수정 요청 | 3회 | 사용자에게 범위 축소 제안 |
| **실험 설계 피드백** | 연구자가 실험 계획 정교화 요청 | 5회 | 최종 확정 요청 |
| **QA 수정** | reviewer가 "수정 요청" 판정 | 3회 | 사용자에게 현재 상태로 진행할지 확인 |
| **후속 작업** | 사용자가 결과 기반 추가 작업 요청 | 무제한 | 새로운 파이프라인으로 취급 |
| **실패 재시도** | 실행 실패 후 파라미터 조정 재시도 | 2회 | 사용자에게 실패 보고 |

---

## 에러 핸들링 테이블

| Phase | 에러 유형 | 심각도 | 대응 | 알림 |
|---|---|---|---|---|
| 1 | 요청 해석 불가 | 낮음 | 사용자에게 구체적 질문 | 없음 |
| 1 | 실현 불가능 요청 | 중간 | 불가 사유 + 대안 제시 | 없음 |
| 3 | 단일 소스 수집 실패 | 낮음 | 대체 소스 시도 | 없음 |
| 3 | 전체 데이터 수집 실패 | 높음 | 파이프라인 중단, 사용자 보고 | Slack/Telegram |
| 4 | 모델 실행 실패 | 중간 | 파라미터 조정 후 1회 재시도 | 없음 |
| 4 | 전체 실행 실패 | 높음 | 부분 결과 보존 + 실패 보고 | Slack/Telegram |
| 5 | 보고서 생성 실패 | 낮음 | 원시 JSON 직접 전달 | 없음 |
| QA | reviewer 반려 | 중간 | 수정 후 재검토 (최대 3회) | 없음 |

### 에스컬레이션 경로

1. **자동 복구 가능** → 에이전트가 자체 복구 (대체 소스, 파라미터 조정)
2. **자동 복구 실패** → 오케스트레이터가 대안 경로 탐색
3. **대안 경로 없음** → 사용자에게 보고 + 부분 결과 전달 + 알림 발송

---

## 알림 발송

작업 완료/실패 시 Slack 또는 Telegram으로 알림을 발송한다.

### Slack 연동

```python
import requests

def send_slack(webhook_url: str, message: str, channel: str = None):
    payload = {"text": message}
    if channel:
        payload["channel"] = channel
    requests.post(webhook_url, json=payload, timeout=10)
```

### Telegram 연동

```python
import requests

def send_telegram(bot_token: str, chat_id: str, message: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload, timeout=10)
```

### 알림 설정

`_workspace/config/notification_config.json`:

```json
{
  "slack": {
    "enabled": true,
    "webhook_url": "https://hooks.slack.com/services/...",
    "default_channel": "#sswl-tasks"
  },
  "telegram": {
    "enabled": false,
    "bot_token": "",
    "default_chat_id": ""
  },
  "notify_on": {
    "task_complete": true,
    "task_failed": true,
    "experiment_complete": true
  }
}
```

### 알림 메시지 형식

**완료 알림**:
```
*작업 완료*
• 요청: {원래 요청}
• 소요: {시간}분
• 결과: {결과 파일 경로}
```

**실패 알림**:
```
*작업 실패*
• 요청: {원래 요청}
• 실패 단계: {Phase N}
• 원인: {에러 요약}
```

### 재시도

- 발송 실패 시 최대 2회 재시도 (5초 간격)
- 재시도 실패 시 로그에 기록

---

## 테스트 시나리오

### 시나리오 1: 정상 흐름 — Synoptic map 생성

```
사용자: "최근 1달간 SDO/HMI 데이터로 synoptic map 만들어줘"

Phase 1: research-planner
  → 요청 파싱: synoptic map 생성, HMI 자기장, 최근 1 CR
  → 실행 계획 수립: 데이터 수집(20분) → 전처리(10분) → synoptic_map 모델 실행(30분)
  → 사용자에게 계획 제시

Phase 2: 사용자 승인
  → "좋아, 진행해"

Phase 3: data-engineer
  → JSOC에서 HMI 자기장 데이터 수집
  → 수집 완료: 28일분 데이터, completeness 96%

Phase 4: research-executor
  → 전처리: 보정, 좌표 정합
  → synoptic_map 모델 실행
  → 출력: synoptic_map.fits + synoptic_map.png

Phase 5: paper-writer
  → 결과 보고서 생성
  → 후속 제안: "PFSS 시뮬레이션", "코로나홀 분석"

Phase 6: 알림 발송
  → Slack: "작업 완료: Synoptic map 생성 (60분)"
```

### 시나리오 2: 실패 복구 — 데이터 수집 부분 실패

```
사용자: "Solar Orbiter PHI와 SDO HMI를 비교 분석해줘"

Phase 1: research-planner
  → 두 소스 데이터 수집 + 비교 분석 계획 수립

Phase 2: 사용자 승인

Phase 3: data-engineer
  → JSOC/HMI: 수집 성공 (100%)
  → SOAR/PHI: 수집 부분 실패 (LL 데이터 60%만 가용)
  → 대체 시도: ESA PSA Archive → 추가 확보, 총 80%

Phase 4: research-executor
  → 부분 데이터로 진행 (80% ≥ 70% 임계값)
  → 결과에 "PHI 데이터 80% 기반" 주석 추가

Phase 5: paper-writer
  → 결과 보고 + "데이터 커버리지 한계" 명시

Phase 6: 알림 발송
  → Slack: "작업 완료 (부분): PHI 데이터 80% 기반"
```
