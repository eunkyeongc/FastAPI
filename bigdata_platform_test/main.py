from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


# 테스트용 도서 데이터
books = [
    {
        "id": 1,
        "title": "파이썬 기초",
        "isbn": "9781111111111"
    },
    {
        "id": 2,
        "title": "FastAPI 실습",
        "isbn": "9782222222222"
    },
    {
        "id": 3,
        "title": "빅데이터와 파이썬",
        "isbn": "9783333333333"
    },
]


# 도서 등록 요청 데이터 구조
class BookCreate(BaseModel):
    title: str
    isbn: str


# ------------------------------------------------
# 1. 도서 검색 API
# ------------------------------------------------
@app.get("/books/search")
def search_books(keyword: str):

    # 검색어가 없는 경우
    if not keyword:
        raise HTTPException(
            status_code=400,
            detail="검색어를 입력하세요"
        )

    # 제목에 검색어가 포함된 책 검색
    results = [
        book
        for book in books
        if keyword in book["title"]
    ]

    return {
        "count": len(results),
        "results": results
    }


# ------------------------------------------------
# 2. 도서 등록 API
# ------------------------------------------------
@app.post("/books", status_code=201)
def create_book(book: BookCreate):

    # 동일한 ISBN이 이미 존재하는지 검사
    for existing_book in books:

        if existing_book["isbn"] == book.isbn:

            raise HTTPException(
                status_code=409,
                detail="이미 등록된 ISBN입니다"
            )

    # 신규 도서 생성
    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "isbn": book.isbn
    }

    books.append(new_book)

    return new_book


# ------------------------------------------------
# 3. 비밀번호 검증 함수
# ------------------------------------------------
def validate_password(password: str):

    # 비밀번호가 8자 미만인 경우
    if len(password) < 8:

        return {
            "success": False,
            "message": "비밀번호는 8자 이상이어야 합니다"
        }

    # 8자 이상인 경우
    return {
        "success": True,
        "message": "회원가입 가능"
    }