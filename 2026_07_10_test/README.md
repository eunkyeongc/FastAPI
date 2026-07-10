# 빅데이터 저장시스템 개발 - NCS
-2026. 07. 10. by  홍은경
- 빅데이터 저장모델 설계
- 빅데이터 적재모듈 개발

---
## 한국마사회_농어촌형 승마시설정보 데이터 저장 시스템 실습

| 파일명 | 설명 |
|---|---|
|`medels.py` | SQRALchemy 테이블 모델 정의|
|`detabase.py` | DB 연결과 테이블 생성|
|`loader.py`|CSV 적재|
|`verify.py`|검증. 대상 테이블 정확히 조사|
|`pipeline.py`|통합 실행|
|`README.me`| 실행 방법과 설계 설명|


---
### pgAdmin에서 데이터베이스 준비
```sql
CREATE DATABASE horsedb;
```

### 입력 파일 준비

|폴더|필요한 파일|
|---|---|
|`C:\Users\Administrator\bigdata2026\fastapi\2026_07_10_test\input\`|`horse_info.csv`|

---

- 결과로 나온 파일 `output\horse_info.csv`를 사용한다.
- CSV 인코딩은 `utf-8-sig` 기준

#### 지하철 모델 설명
> 승마시설정보 데이터는 승마장이름, 지역명, 전화번호가 한 번만 존재해야 한다.

>`id`가 있어도 UNIQUE 제약이 별도로 필요한다.

#### 검증 설명
> `verify.py` ---> SQL을 대신 실행하는 파일