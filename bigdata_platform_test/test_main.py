from fastapi.testclient import TestClient

from main import app, validate_password


# FastAPI 테스트용 클라이언트 생성
client = TestClient(app)


# ==========================================================
# 실습 1
# 도서 검색 API 테스트
# ==========================================================

# 정상 테스트
def test_search_books_success():

    response = client.get(
        "/books/search",
        params={
            "keyword": "파이썬"
        }
    )

    # HTTP 상태 코드 확인
    assert response.status_code == 200

    # JSON 결과 가져오기
    data = response.json()

    # "파이썬"이 들어간 책은 2권
    assert data["count"] == 2

    # 검색 결과가 2개인지 확인
    assert len(data["results"]) == 2


# ----------------------------------------------------------
# 빈 검색어 테스트
# ----------------------------------------------------------

def test_search_books_empty_keyword():

    response = client.get(
        "/books/search",
        params={
            "keyword": ""
        }
    )

    # 400 오류가 발생해야 함
    assert response.status_code == 400

    # 오류 메시지 확인
    assert response.json()["detail"] == "검색어를 입력하세요"


# ==========================================================
# 실습 2
# ISBN 중복 등록 테스트
# ==========================================================

def test_duplicate_isbn_returns_409():

    response = client.post(
        "/books",
        json={
            "title": "중복 도서 테스트",
            "isbn": "9781111111111"
        }
    )

    # 중복 ISBN은 409
    assert response.status_code == 409

    # 오류 메시지 확인
    assert response.json()["detail"] == "이미 등록된 ISBN입니다"


# ==========================================================
# 실습 3
# 비밀번호 테스트
# ==========================================================

# 정상값
def test_password_normal():

    result = validate_password(
        "password123"
    )

    assert result["success"] is True


# ----------------------------------------------------------
# 경계값 : 정확히 8자
# ----------------------------------------------------------

def test_password_boundary():

    result = validate_password(
        "abcd1234"
    )

    assert result["success"] is True


# ----------------------------------------------------------
# 예외값 : 7자
# ----------------------------------------------------------

def test_password_exception():

    result = validate_password(
        "abc1234"
    )

    assert result["success"] is False

    assert (
        result["message"]
        == "비밀번호는 8자 이상이어야 합니다"
    )