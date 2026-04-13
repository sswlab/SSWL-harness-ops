---
name: remote-collection-protocol
description: >
  원격 서버 코드 수집 절차 및 버전 선별 표준을 정의하는 스킬.
  SSH 기반 파일 탐색, 버전 계보 분석, 최적 버전 선별, 범주별 정리,
  전송 절차를 제공한다. remote-collector가 원격 코드를 수집할 때,
  버전을 비교할 때, 파일을 전송할 때 이 스킬을 참조한다.
  원격 서버 코드, 코드 수집, 버전 비교, 코드 전송, SSH 스캔,
  서버 파일 탐색, 버전 선별, 코드 정리, 서버에서 가져오기
---

# Remote-Collection-Protocol — 원격 코드 수집 절차 표준

## 개요

연구 코드는 여러 서버에 흩어져 있고, 동일 코드의 여러 버전이 다양한 디렉토리에 산재한다.
이 스킬은 remote-collector 에이전트가 수백~수천 개의 파일에서 최적 버전만 선별하여
범주별로 정리·전송하는 표준 절차를 정의한다.

## 수집 4단계 절차

### 1단계: 접속 및 트리 스캔 (Connection & Tree Scan)

```bash
# SSH 접속 테스트
ssh -o ConnectTimeout=5 -o BatchMode=yes {user}@{host} "hostname && echo SSH_OK"

# 메타데이터 수집 — .py 파일
ssh {user}@{host} "find {scan_path} -name '*.py' \
  ! -path '*/anaconda3/*' ! -path '*/.local/*' ! -path '*/.cache/*' \
  ! -path '*/.vscode*' ! -path '*/__pycache__/*' ! -path '*/.git/*' \
  ! -path '*/site-packages/*' ! -path '*/.ipynb_checkpoints/*' \
  -printf '%T@ %s %p\n' 2>/dev/null | sort -rn"

# 메타데이터 수집 — .ipynb 파일 (동일 제외 패턴)
ssh {user}@{host} "find {scan_path} -name '*.ipynb' \
  [동일 제외 패턴] \
  -printf '%T@ %s %p\n' 2>/dev/null | sort -rn"
```

**수집 항목**: 타임스탬프(epoch), 파일 크기(bytes), 전체 경로
**결과**: `collection/00_scan_manifest.md`에 기록

### 2단계: 버전 계열 그룹핑 (Version Family Grouping)

파일명에서 버전 접미사를 탐지하고, 동일 base_name으로 그룹핑한다.

**버전 패턴 인식 정규식 (우선순위 순)**:

| 우선순위 | 패턴 | 정규식 | 예시 |
|---|---|---|---|
| 1 | 시맨틱 버전 | `[_-]v?(\d+)\.(\d+)\.(\d+)` | `Train_v0.6.2.py` |
| 2 | V + major.minor | `[_-][Vv](\d+)[_.](\d+)` | `DEM_V3_1.py`, `DEM_V3.1.py` |
| 3 | V + major | `[_-][Vv](\d+)` | `dem_V3.py` |
| 4 | 날짜 접미사 | `[_-](\d{6,8})` | `proc_20240315.py`, `proc_250315.py` |
| 5 | 없음 | — | `utils.py` (타임스탬프 폴백) |

**base_name 추출 규칙**:
1. 확장자 제거 (`.py`, `.ipynb`)
2. 버전 접미사 제거 (위 패턴 매칭)
3. 디렉토리 경로의 마지막 2 레벨을 포함하여 같은 이름 다른 위치 구분
4. `Copy`, `checkpoint`, `old`, `backup` 접미사가 있으면 원본의 변형으로 취급

**주의 — 에지 케이스**:
- `V3_1`은 3.1이지 31이 아니다
- `_250315`는 2025-03-15이다 (6자리 = YYMMDD, 8자리 = YYYYMMDD)
- 디렉토리명에 버전이 있을 수 있다: `Code_V2/preprocess/` → V2는 디렉토리 버전
- 같은 base_name이 다른 프로젝트에 있으면 별개 계열이다

### 3단계: 최적 버전 선별 (Best-Version Selection)

각 버전 계열에서 하나의 최적 버전을 선택한다.

**종합 점수 = 버전(0.5) + 타임스탬프(0.3) + 완성도(0.2)**

| 기준 | 가중치 | 측정 방법 |
|---|---|---|
| 버전 번호 | 0.5 | 최고 버전 = 1.0, 이하 비례 감소 |
| 수정 타임스탬프 | 0.3 | 최신 = 1.0, 이하 비례 감소 |
| 완성도 (크기 프록시) | 0.2 | 최대 크기 = 1.0, 이하 비례 감소 |

**예외 규칙**:
- 버전 패턴이 없는 단독 파일: 자동 선택 (비교 대상 없음)
- `.ipynb`와 `.py`가 동일 base_name: `.py` 우선, `.ipynb`도 참조용으로 수집
- 0바이트 파일: 무조건 제외
- `-Copy`가 붙은 파일: 원본이 있으면 제외

**선별 결과 형식** (`collection/02_selected_files.md`):

```markdown
# 수집 대상 선별 결과

## 요약
- 스캔 총 파일: N개
- 버전 계열: M개
- 선별 파일: K개
- 범주: L개

## 선별 파일 목록

### 범주: 전처리 (Preprocessing)
| # | 파일명 | 버전 | 원격 경로 | 크기 | 선별 이유 |
|---|---|---|---|---|---|
| 1 | AIA_prepV251124.py | latest | /path/to/... | 10KB | 최신 버전, 가장 완전 |

### 범주: DL Pix2Pix
...
```

### 4단계: 범주 할당 및 전송 (Category Assignment & Transfer)

**범주 할당 로직** (파일명 패턴 → import 시그니처 → 디렉토리 위치 순으로 판단):

1. 파일명에 범주 키워드가 포함되면 즉시 할당
2. 파일명 매칭 실패 시, `head -20`으로 import 문을 읽어 시그니처 매칭
3. import 매칭도 실패 시, 디렉토리 이름으로 추정 (예: `Code_DL/` → DL 관련)
4. 모두 실패 시, `[미분류]` 태그 → 사용자에게 질문

**전송 절차**:

```bash
# 1. 원격 스테이징 디렉토리 생성
ssh {user}@{host} "mkdir -p /tmp/_SOTA_staging/{category}/"

# 2. 선별 파일 복사 (원본 불변)
ssh {user}@{host} "cp {remote_path} /tmp/_SOTA_staging/{category}/"

# 3. zip 압축
ssh {user}@{host} "cd /tmp && zip -r _SOTA_staging.zip _SOTA_staging/"

# 4. scp 전송
scp {user}@{host}:/tmp/_SOTA_staging.zip {workspace}/

# 5. 로컬에서 압축 해제 → inbox/ 배치
unzip -o {workspace}/_SOTA_staging.zip -d {workspace}/inbox/

# 6. 원격 스테이징 정리
ssh {user}@{host} "rm -rf /tmp/_SOTA_staging /tmp/_SOTA_staging.zip"
```

## 노트북(.ipynb) 수집 규칙

- 노트북도 정식 수집 대상이다 (스킵하지 않는다)
- `.py`와 `.ipynb`가 동일 base_name이면: `.py`가 주(primary), `.ipynb`는 참조(reference)
- 대형 노트북(>5MB): 내장 이미지/출력 때문이므로 크기만으로 가치를 판단하지 않는다
- 50셀 이상 노트북: archaeologist 단계에서 분할 검토 대상으로 플래그

## 전송 매니페스트 형식

`collection/03_transfer_log.md`:

```markdown
# 전송 로그

- 전송일: {timestamp}
- 원격: {user}@{host}
- 로컬: {workspace}/inbox/
- 총 전송: N개 파일, X MB

| # | 원격 경로 | 로컬 경로 | 범주 | 크기 | 상태 |
|---|---|---|---|---|---|
| 1 | /remote/path/file.py | inbox/Preprocessing/file.py | 전처리 | 10KB | 완료 |
```

## 효율적 네트워크 사용

- `find` 결과를 한 번의 SSH 명령으로 수집한다 (파일당 SSH 연결을 열지 않는다)
- 내용 읽기(`head`, `cat`)는 선별된 후보에만 적용한다
- 대량 전송은 zip 1개로 묶어 scp 1회로 전송한다 (파일별 scp 금지)
- SSH 연결 재사용: `ControlMaster`가 설정되어 있으면 활용한다
