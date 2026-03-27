---
name: notification
description: >
  알림 발송 스킬. Slack Incoming Webhook 및 Telegram Bot API를
  통해 작업 완료/실패 알림을 발송한다.
  키워드: 알림, 슬랙, 텔레그램, Slack, Telegram,
  알려줘, 공유해줘, 전송해줘, 보내줘, 메시지
---

# Notification — 알림 발송 스킬

## 개요

작업 완료/실패 시 Slack 또는 Telegram으로 알림을 발송한다.

## Slack 연동

### Incoming Webhook 방식

```python
import requests
import json

def send_slack(webhook_url: str, message: str, channel: str = None):
    payload = {"text": message}
    if channel:
        payload["channel"] = channel
    requests.post(webhook_url, json=payload, timeout=10)
```

### 메시지 형식

#### 작업 완료 알림
```json
{
  "text": "✅ 작업 완료: Synoptic map 생성",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*작업 완료*\n• 요청: Synoptic map 생성\n• 소요: 47분\n• 결과: `_workspace/tasks/.../synoptic_map.fits`"
      }
    }
  ]
}
```

#### 작업 실패 알림
```json
{
  "text": "❌ 작업 실패: 데이터 수집 실패",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*작업 실패*\n• 요청: 원본 요청\n• 실패 단계: 데이터 수집\n• 원인: JSOC 서버 무응답"
      }
    }
  ]
}
```

## Telegram 연동

### Bot API 방식

```python
import requests

def send_telegram(bot_token: str, chat_id: str, message: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload, timeout=10)
```

## 설정

알림 설정은 `_workspace/config/notification_config.json`에 저장:

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

## 재시도

- 발송 실패 시 최대 2회 재시도 (5초 간격)
- 재시도 실패 시 로그에 기록, 대체 채널 시도
