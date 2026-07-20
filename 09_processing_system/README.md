# 2026. 07. 20.
# NCS 빅데이터 처리 시스템 능력단위평가

## 한국 마사회 경주기록 정보 데이터 처리시스템 
PostgreSQL에 적재한 데이터셋을 이어받아, 배치 처리 모듈과 이벤트 처리 모듈을 설계·구현

### 1. 전제 조건
pgAdmin에 다음의 테이블이 저장되어 있어야 함.
|DB|테이블|
|---|---|
|`horse_race_db`|`horse_race_raw`|

### 2. 필요한 라이브러리
``` bash
uv add sqlalchemy psycopg2-binary
```

### 3. 환경변수
기본값은 저장시스템 실습과 같은 비밀번호    `1234`
``` bash
set HORSE_RACE_DB_URL = postgresq1://postgres:1234@localhost:5432/horse_race_db
```

### 4. 실행
```bash
python pipeline.py
```
### 5. 결과 테이블
|DB | 결과 테이블 |
|---|---|
|`horse_race_db`|`hore_race_summary`|
|`horse_race_db`|`hore_race_event`|
