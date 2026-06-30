# FastAPI 복습 - 공식 튜토리얼로 다시 다지는 FastAPI 핵심

## 실습 순서
|단계|내용|
|---|---|
|① sql_databases| User + Item 두 테이블, 1:N, crud.py 분리|
|② bigger_applications|routers/폴더 분리 구조
|③ app_testing | TestClient로 엔트포인트 자동 테스트 - pytest|
<!-- 'ㅇ' + 한자키 --> ①


## 실습 환경
- python 3.11
- 패키지관리 : `uv`
- DB : PostgreSQL 17
    -DB명 : `reviewdb`
- IDE : VS Code
- **터미널** : Git Bash

## 1. sql_databases --> User + Item, 1:N  관계 CRUD
- 공식 FastAPI 튜토리얼 예제를 PostgreSQL로 변환한 버전이다.
-`User`(사용자가)가 여러 개의 `Item`(아이템)을 소유하는 **1:N 관계** 구조
- `crud.py`를 별도로 분리하여 DB 조작 로직과 라우터 로직을 나눈다.


<!-- 
확장 -> 검색: tree -> file-tree-generator 설치 -> 좌측 원하는 폴더에서 마우스 우클릭 -> generator to Tree 
--> 

```
─fastapi_review
  │  crud.py
  │  database.py
  │  dependencies.py
  │  main.py
  │  models.py
  │  README.md
  │  schemas.py
  │  
  ├─routers
  │  │  items.py
  │  │  users.py
  │  │  __init__.py
  │  │  
  │  └─__pycache__
  │          items.cpython-311.pyc
  │          users.cpython-311.pyc
  │          __init__.cpython-311.pyc
  │          
  └─__pycache__
          crud.cpython-311.pyc
          database.cpython-311.pyc
          dependencies.cpython-311.pyc
          main.cpython-311.pyc
          models.cpython-311.pyc
          schemas.cpython-311.pyc
```


