from fastapi import Request, FastAPI
from fastapi.templating import Jinja2Templates

# app 객체 생성
app = FastAPI() 

# templates 객체 생성 : templates 폴더 안에서 템플릿 파일을 찾겠다는 설정
#                       uvicorn을 실행하는 위치(현재 작업 폴더) 기준 상대경로
templates = Jinja2Templates(directory="templates")

# localhost/docs를 사용하지 않고 바로 접속
# {name} --> 경로 파리미터: URL의 이 위치에 들어온 값이 name인자로 전달된다.
@app.get("/hello/{name}")

# async (비동기) : fastapi에서 주로 사용, 속도가 조금 느려질수는 있다.
async def hello(request: Request, name: str):   # 매개변수: 자료형
    
    return templates.TemplateResponse(
        request=request, 
        name="hello.html",  # templates/hello.html 렌더링할 파일 이름
        context={"name": name,  # 경로에서 받은 이름
                 "items": ["사과", "바나나", "오렌지"]      # 템플릿에서 {% for %}로 반복할 리스트
        }
    )

@app.get('/products')
async def product_list(request: Request):
    # 실습용 더미 데이터 --> 실제로는 DB 조회 결과(ex: db.scalars(select(Product)).all())
    products = [
        {"id": 1, "name": "티셔츠", "price": 29000, "stock": 50},
        {"id": 2, "name": "청바지", "price": 59000, "stock": 30},
        {"id": 3, "name": "모자", "price": 15000, "stock": 0},
    ]
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"products": products},
    )