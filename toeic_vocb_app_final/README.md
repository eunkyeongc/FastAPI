# 📘 TOEIC Vocabulary App

FastAPI와 SQLite를 이용하여 만든 **TOEIC 단어 학습 웹 애플리케이션**입니다.

매일 20개의 단어를 학습하고 단어 테스트와 문장 테스트를 진행합니다.  
틀린 단어는 자동으로 오답노트에 저장되며, 오답 단어는 문장형 문제를 통해 다시 복습할 수 있습니다.

---

## 🎯 프로젝트 목표

TOEIC 단어를 단순히 암기하는 것이 아니라 다음과 같은 반복 학습 과정을 구현하는 것을 목표로 합니다.

```text
단어 학습
   ↓
단어 테스트
   ↓
문장 테스트
   ↓
틀린 단어
   ↓
오답노트
   ↓
오답 문장 테스트
   ↓
반복 복습
```

학습 진행 상황은 SQLite DB에 저장되어 사용자가 어디까지 공부했는지 확인할 수 있습니다.

---

# 📚 주요 기능

## 1. 난이도별 단어 학습

TOEIC 단어를 세 가지 난이도로 구분합니다.

- 기초 (`basic`)
- 중급 (`intermediate`)
- 고급 (`advanced`)

하루에 **20개의 단어**를 학습하도록 구성되어 있습니다.

현재 기초 단어 데이터는:

```text
600단어
÷ 하루 20단어
= 총 30일
```

분량입니다.

---

## 2. 단어 학습

각 단어에 다음 정보를 제공합니다.

```text
영어 단어
한글 뜻
영어 예문
예문 해석
```

예:

```text
employee

직원, 종업원

The company hired a new employee.

그 회사는 새로운 직원을 고용했습니다.
```

학습을 완료하면 해당 Day의 학습 완료 상태가 DB에 저장됩니다.

---

## 3. 단어 테스트

학습한 단어를 객관식 문제로 테스트합니다.

예:

```text
employee

① 회의
② 직원, 종업원
③ 고객
④ 사무실
```

문제를 틀리면 해당 단어가 자동으로 **오답노트에 저장**됩니다.

---

## 4. 문장 테스트

학습한 단어를 문장 속에서 다시 확인합니다.

예:

```text
The company hired a new ______.

① meeting
② office
③ employee
④ customer
```

단어의 뜻뿐만 아니라 실제 문장에서 어떻게 사용되는지도 함께 학습할 수 있습니다.

---

## 5. 오답노트

단어 테스트 또는 문장 테스트에서 틀린 단어는 자동으로 오답노트에 저장됩니다.

오답노트에서는 다음 정보를 확인할 수 있습니다.

```text
단어
뜻
예문
예문 해석
틀린 횟수
연속 정답 횟수
```

---

## 6. 오답 문장 테스트

오답노트의 단어를 이용해 문장형 문제를 다시 출제합니다.

오답 단어를 반복해서 맞히면서 복습할 수 있도록 구성되어 있습니다.

```text
오답 발생
   ↓
오답노트 저장
   ↓
문장형 재시험
   ↓
연속 정답
   ↓
암기 완료
```

---

## 7. 학습 진행 상황 저장

각 난이도와 Day별로 다음 세 가지 상태를 저장합니다.

```text
단어 학습 완료
단어 테스트 완료
문장 테스트 완료
```

예:

```text
기초 Day 1

단어 학습       ✅ 완료
단어 테스트     ✅ 완료
문장 테스트     ✅ 완료
```

---

## 8. 이어서 학습하기

홈 화면에서 사용자의 학습 기록을 확인하여 다음에 공부해야 할 위치를 자동으로 추천합니다.

예:

```text
기초 Day 1 완료
        ↓
기초 Day 2

...

기초 Day 30 완료
        ↓
중급 Day 1

...

중급 완료
        ↓
고급 Day 1
```

---

# 🗂 프로젝트 구조

```text
toeic_vocb_app_final/
│
├── main.py
├── database.py
├── models.py
├── seed_csv.py
├── requirements.txt
├── README.md
│
├── data/
│   └── vocabulary_basic.csv
│
├── templates/
│   ├── index.html
│   ├── study.html
│   ├── word_test.html
│   ├── sentence_test.html
│   ├── wrong_note.html
│   └── wrong_test.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── app.js
```

---

# 📄 주요 파일 설명

| 파일 | 역할 |
|---|---|
| `main.py` | FastAPI 서버 및 API |
| `database.py` | SQLite 데이터베이스 연결 |
| `models.py` | SQLAlchemy DB 모델 |
| `seed_csv.py` | CSV 단어 데이터를 DB에 등록 |
| `requirements.txt` | Python 패키지 목록 |
| `README.md` | 프로젝트 설명 |
| `index.html` | 홈 및 학습 진행 현황 |
| `study.html` | 단어 학습 화면 |
| `word_test.html` | 단어 테스트 |
| `sentence_test.html` | 문장 테스트 |
| `wrong_note.html` | 오답노트 |
| `wrong_test.html` | 오답 문장 테스트 |
| `style.css` | 전체 화면 디자인 |
| `vocabulary_basic.csv` | 기초 TOEIC 단어 데이터 |

---

# 🗃 단어 CSV 구조

CSV 파일은 다음 컬럼으로 구성되어 있습니다.

| 컬럼 | 설명 |
|---|---|
| `word` | 영어 단어 |
| `meaning` | 한글 뜻 |
| `level` | 난이도 |
| `example_sentence` | 영어 예문 |
| `example_translation` | 예문 해석 |

예:

```csv
word,meaning,level,example_sentence,example_translation
employee,"직원, 종업원",basic,"The company hired a new employee.","그 회사는 새로운 직원을 고용했습니다."
```

난이도 값은 다음과 같이 사용합니다.

```text
basic
intermediate
advanced
```

---

# 💾 데이터베이스

SQLite를 사용합니다.

애플리케이션 실행 시 다음과 같은 DB 파일이 생성됩니다.

```text
toeic_vocab.db
```

SQLAlchemy ORM을 이용하여 데이터베이스를 관리합니다.

---

# 🛠 사용 기술

### Backend

```text
Python
FastAPI
SQLAlchemy
Uvicorn
```

### Frontend

```text
HTML
CSS
JavaScript
Jinja2
```

### Database

```text
SQLite
```

### Data

```text
CSV
```

---

# 🚀 실행 방법

## 1. 프로젝트 폴더 이동

```bash
cd toeic_vocb_app_final
```

---

## 2. 가상환경 생성

Windows 기준:

```bash
python -m venv .venv
```

---

## 3. 가상환경 활성화

Git Bash:

```bash
source .venv/Scripts/activate
```

Windows CMD:

```cmd
.venv\Scripts\activate
```

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 4. 필요한 패키지 설치

```bash
python -m pip install -r requirements.txt
```

---

## 5. CSV 단어 데이터 DB 등록

```bash
python seed_csv.py
```

정상적으로 실행되면 다음과 비슷한 메시지가 출력됩니다.

```text
vocabulary_basic.csv: 추가 600개 / 갱신 0개
완료: 추가 600개 / 갱신 0개
```

---

## 6. FastAPI 서버 실행

```bash
python -m uvicorn main:app --reload
```

정상 실행 시:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

가 표시됩니다.

---

## 7. 웹 브라우저 접속

브라우저에서 다음 주소로 접속합니다.

```text
http://127.0.0.1:8000
```

FastAPI API 문서는:

```text
http://127.0.0.1:8000/docs
```

에서 확인할 수 있습니다.

---

# 🔄 전체 학습 흐름

```text
             TOEIC Vocabulary
                    │
                    ▼
             난이도 / Day 선택
                    │
                    ▼
               단어 학습
                    │
                    ▼
              단어 테스트
                    │
                    ▼
              문장 테스트
                    │
             ┌──────┴──────┐
             │             │
           정답            오답
             │             │
             │             ▼
             │         오답노트
             │             │
             │             ▼
             │       오답 문장 테스트
             │             │
             └──────┬──────┘
                    │
                    ▼
                 복습
```

---

# 📊 학습 진행 상태

학습 상태는 `LearningProgress` 테이블에서 관리합니다.

각 Day마다 다음 정보를 저장합니다.

```text
level
day
study_completed
word_test_completed
sentence_test_completed
```

예:

```text
level = basic
day = 1

study_completed = True
word_test_completed = True
sentence_test_completed = True
```

---

# 📕 오답 관리

틀린 단어는 별도로 저장하여 반복 학습할 수 있습니다.

오답 학습 과정:

```text
단어 테스트 오답
        │
        ├─────────┐
        │         │
        ▼         ▼
    단어 테스트   문장 테스트
        │         │
        └────┬────┘
             ▼
          오답노트
             │
             ▼
      오답 문장 테스트
             │
             ▼
         반복 복습
```

---

# 📅 현재 학습 데이터

현재 제공되는 데이터:

```text
기초 basic
600 단어
30 Days
하루 20 단어
```

추후 다음 파일을 추가할 수 있습니다.

```text
data/
├── vocabulary_basic.csv
├── vocabulary_intermediate.csv
└── vocabulary_advanced.csv
```

`seed_csv.py`를 다시 실행하면 새로운 CSV 데이터를 DB에 등록할 수 있습니다.

---

# 🔮 향후 개발 계획

다음 기능을 추가하여 앱을 확장할 수 있습니다.

- 중급 TOEIC 단어 600개 추가
- 고급 TOEIC 단어 600개 추가
- 난이도별 진행률 표시
- 전체 학습 진행률 표시
- 테스트 점수 기록
- 날짜별 학습 기록
- 주간 오답 테스트
- 랜덤 문제 출제
- 문제 보기 순서 랜덤화
- 단어 검색
- 즐겨찾기 단어
- 로그인 및 사용자별 학습 기록
- 모바일 UI 개선
- 학습 통계 그래프
- 연속 학습일(Streak) 기능

---

# 🎯 최종 목표

최종적으로 다음과 같은 TOEIC 단어 학습 시스템을 목표로 합니다.

```text
기초 600단어
   ↓
30일 학습
   ↓
중급 600단어
   ↓
30일 학습
   ↓
고급 600단어
   ↓
30일 학습
   ↓

총 1,800단어
90일 TOEIC Vocabulary Course
```

단순 암기가 아니라

```text
학습
→ 테스트
→ 오답 저장
→ 문장 복습
→ 반복 학습
```

과정을 통해 단어를 반복적으로 학습할 수 있도록 구성합니다.