👋 **IDL → Python 변환기 하네스**에 오신 걸 환영합니다.

IDL(`.pro`) 파일을 입력하면, **분석 → 변환 계획 → Python 코드 생성 → 테스트 자동 작성·실행 → 품질 검토(PASS/REVISE)**까지 수행합니다. SSW/SolarSoft → SunPy/Astropy 매핑과 column-major → row-major 인덱싱 전치도 자동입니다.

---

### 📋 입력 항목

| 항목 | 설명 | 예시 |
|---|---|---|
| **① IDL 파일** | `.pro` 파일 또는 디렉토리 | `/home/youn_j/idl/solar_prep.pro` |
| **② 변환 목적** | 왜 변환하는지 | `레거시 마이그레이션`, `Python 파이프라인 통합` |
| **③ 변환 모드** | `단일` / `배치` / `선택적` | `단일` |
| **④ 작업 경로** | 결과물 저장 디렉토리 | `/home/youn_j/converted/solar_prep/` |

### 🎯 변환 모드

| 모드 | 설명 |
|---|---|
| **단일 (Single)** | `.pro` 파일 1개 변환 |
| **배치 (Batch)** | 디렉토리 내 모든 `.pro` 병렬 변환 |
| **선택적 (Selective)** | 지정한 파일 목록만 변환 |

---

### 💬 그대로 복사해서 쓸 수 있는 프롬프트 템플릿

```
[IDL 파일/디렉토리]를 Python으로 변환해줘.

목적: [왜 변환하는지]
모드: [단일 / 배치 / 선택적]
작업 경로: [/저장/경로]
```

#### 실제 예시

```
solar_prep.pro를 Python으로 변환해줘.

파일: /home/youn_j/idl/solar_prep.pro
목적: SunPy 파이프라인에 통합
모드: 단일
작업 경로: /home/youn_j/converted/solar_prep/
```

```
이 디렉토리 IDL 코드 전부 변환해줘: /home/youn_j/idl/stix/
```
→ 배치 모드로 진입, 목적·경로만 되묻습니다.

---

### 🧪 품질 보장

`conversion-reviewer`가 PASS/REVISE 판정하며, REVISE 시 자동 루프백(최대 2회)으로 재변환합니다. 테스트는 합성/실제 데이터로 자동 생성됩니다.

준비되시면 위 템플릿대로 입력해 주세요. 🚀
