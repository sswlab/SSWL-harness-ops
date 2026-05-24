👋 **논문 작성 및 피어리뷰 하네스**에 오신 걸 환영합니다.

연구 코드·데이터·Figure를 입력하면, **논문 초안 작성 → 내부 검토 → 피어리뷰 시뮬레이션 → 리비전 → 최종 LaTeX/PDF 생성**까지 자동으로 수행합니다. 실제 저널 투고 프로세스를 최대 3회 반복합니다.

> ⚠ 이 하네스는 **새 논문을 작성**합니다. 기존 논문 교정/리뷰는 `06-paper-editor`를 사용하세요.

---

### 📋 입력 항목

| 항목 | 설명 | 예시 |
|---|---|---|
| **① 연구 결과물** | 코드·데이터·Figure가 있는 경로 | `/home/youn_j/research/stix-goes/` |
| **② 대상 저널** | 투고할 저널 (미정이면 후보 3개 추천) | `ApJ` / `A&A` / `MNRAS` / `Solar Physics` / `미정` |
| **③ 작업 경로** | 결과물 저장 디렉토리 | `/home/youn_j/papers/stix-goes/_workspace` |

지원 LaTeX 템플릿: ApJ / ApJL / ApJS / A&A / MNRAS / arXiv(폴백)

---

### 💬 그대로 복사해서 쓸 수 있는 프롬프트 템플릿

```
[연구 주제] 연구 결과로 논문 써줘.

저널: [ApJ / A&A / 미정 등]
연구 결과: [/절대/경로]
작업 경로: [/절대/경로/_workspace]
```

#### 실제 예시

```
STIX-GOES 변환 연구 결과로 ApJ 논문 써줘.

저널: ApJ
연구 결과: /home/youn_j/research/stix-goes/
작업 경로: /home/youn_j/papers/stix-goes/_workspace
```

---

### 📝 빠뜨려도 되는 것 / 안 되는 것

- ✅ 저널 미정 — researcher가 분석 후 3개 후보 제안
- ✅ 일부 결과만 있어도 시작 가능 — 누락된 분석은 reviewer가 지적
- ⚠ 연구 결과 자체가 없으면 시작 불가 — 먼저 `01-research-production`으로 연구 수행

자세한 에이전트 구성·리비전 루프는 하네스 루트의 `README.md` 참조.

준비되시면 위 템플릿대로 입력해 주세요. 🚀
