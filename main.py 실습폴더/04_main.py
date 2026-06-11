# ============================================================
# FastAPI 핵심 기능 데모
# 실행: uvicorn main:app --reload
# Swagger 문서: http://127.0.0.1:8000/docs
# ============================================================
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

# 1. 기본 GET 엔드포인트 — 파라미터 없음. 잘 돌아가는지 확인용.
# 요청: GET http://127.0.0.1:8000/
# 요청: GET http://localhost:8000/

@app.get('/')
def root_handler():
    # 리턴되는 자료형은 dict -> 변환, 자동으로 JSON으로 변환해서 응답이 된다.
    return {'message': 'hello, FastAPI!!'}

# 2. 추가 경로 — 파라미터 없음
# 요청: GET http://localhost:8000/login

@app.get('/login')
def login_handler():
    return{'message': '로그인 페이지에 오신 것을 환영합니다.'}

# 3. 경로 변수 (Path Parameter)
# URL의 일부를 변수로 받음 → 중괄호 {변수명} 사용
# 요청: GET http://127.0.0.1:8000/users/12345
#   → user_id = 12345 (int로 자동 변환, 문자 입력 시 422 에러)

@app.get('/users/{user_id}')
def read_user_handler(user_id: int): # 타입 힌트
    return {'user_id': user_id, 'message': f'사용자 {user_id} 정보 조회'}

# 4. 쿼리 파라미터 (Query Parameter)
# URL 뒤 ?key=value 형태로 전달
# 요청: GET http://localhost:8000/items?max_price=5000
#       GET http://localhost:8000/items         ← max_price=None (Optional)

# int | None = None  →  Python 3.10+ 문법
#   = Optional[int]과 동일, 기본값 None이면 선택적 파라미터
@app.get('/items')
def read_items_handler(max_price: int | None = None):  # int or None, 초기값은 None
    return {'max_price': max_price}

# 5. Pydantic 모델 — 요청/응답 데이터 구조 정의
# BaseModel을 상속하면:
#   - 자동 유효성 검사 (잘못된 타입 → 422 에러)
#   - Swagger UI 자동 문서화
#   - JSON 직렬화/역직렬화 자동 처리
class Item(BaseModel):
    name: str
    price: int
    is_stock: bool = True # 기본값을 True로 정함. (요청시 True면 생략 가능, False면 입력)

# 6. POST — 요청 본문(Request Body) 수신
# JSON Body로 Item 데이터를 받아서 그대로 반환
#   (Item에 없는 필드가 있어도 걸러줌, 보안상 중요)
# status_code=201  → 성공 생성 시 200 대신 201 반환

# 요청 예시 (Body):
#   { "name": "노트북", "price": 1200000 }
@app.post(path='/Items', 
        response_model=Item,  # 응답 구조를 Item으로 고정
        status_code = status.HTTP_201_CREATED
)

def create_item_handler(item: Item):
    return item

# 7. PUT — 경로변수 + 쿼리파라미터 + 요청 본문 혼합
# FastAPI가 파라미터 종류를 자동으로 구분하는 규칙:
#   - {item_id}  → 경로 변수   (URL에 중괄호로 선언)
#   - assignee   → 쿼리 파라미터 (단순 타입이고 경로에 없음)
#   - item: Item → 요청 본문   (Pydantic 모델이면 Body)

# 요청: PUT http://localhost:8000/items/5?assignee=홍길동
# Body: { "name": "마우스", "price": 30000 }
@app.put('/items/{item_id}')
def update_item_handler(item_id: int, assignee: str, item:Item):
    return {
        'item_id': item_id,
        'assignee': assignee, # 담당자
        'item' : item
    }

# 8. 응답 모델 (Response Model)
# 반환되는 데이터를 OrderResponse 형태로 필터링
# 서버 내부에서 민감 데이터(비밀번호 등)가 dict에 섞여 있어도
# response_model에 정의된 필드만 클라이언트에 전달됨 → 보안

class OrderResponse(BaseModel):
    order_id: int
    Pickup: bool | None = None # 없으면 null반환

# GET
@app.get('/orders/{order_id}', response_model=OrderResponse)
def get_order_handler(order_id: int, pickup: bool | None = None):
    return {
        'order_id' : order_id,
        'pickup': pickup # bool 쿼리파라미터 ?pickup=true(자바스크립터는 소문자 true) / ?pickup=1 / ?pickup=yes 모두 True로 인식
    }