# 빅데이터 플랫폼 테스트 실습

FastAPI와 pytest를 이용하여
빅데이터 플랫폼 테스트 평가 내용을 실습한다.


## 프로젝트 구조

```text
bigdata_platform_test/
├── main.py
├── test_main.py
├── requirements.txt
└── README.md
```


## 가상환경 생성

```bash
python -m venv .venv
```


## 가상환경 실행

Windows:

```bash
.venv\Scripts\activate
```


## 라이브러리 설치

```bash
pip install -r requirements.txt
```


## pytest 실행

```bash
pytest -v
```


## FastAPI 실행

```bash
uvicorn main:app --reload
```


## Swagger 접속

```text
http://127.0.0.1:8000/docs
```


## 테스트 항목

1. 정상 도서 검색 → 200
2. 빈 검색어 → 400
3. 중복 ISBN → 409
4. 비밀번호 정상값
5. 비밀번호 경계값 8자
6. 비밀번호 예외값 7자