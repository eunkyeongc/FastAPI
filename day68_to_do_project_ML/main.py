# ========================================================================================
# 2026. 08. 12. --> 8.19. 수정
# to_do_ project
# day66_to_do_project\main.py
#
# FastAPI 애플리케이션의 진입점(entry point)
# JWT 인증 토큰 방식으로.

# 앱 인스턴스를 만들고, 여러 개로 나뉜 라우터들을 하나로 조립하고, 
# 서버가 커질때/꺼질때 딱 한 번씩 해야하는 일(DB 테이블 생서, ML 모델 로드)을 처리한다.
# ========================================================================================
from pathlib import Path
import joblib
from fastapi import FastAPI
from database.db_connection import engine
from database.orm import Base
from routers.todo import router as todo_router
from routers.user import router as user_router
from contextlib import asynccontextmanager

# 모델 경로 지정
# uvicorn을 어느 폴더에서 실행하느냐에 따라 상대경로 기준이 달라져 파일을 못찾는 경우가 자주 발생--> 절대 경로 사용
MODEL_PATH = Path(__file__).resolve().parent / 'ml' / 'artifacts' / 'latest.pkl'

@asynccontextmanager
async def lifespan(app: FastAPI): # async -> 비동기, (_) -> 이름모를 저장소에 임시 저장
    # 앱 시작시 1회 실행: models.py에 정의된 테이블들을 DB에 생성
    # (이미 테이블이 있으면 아무 일도 하지 않는다.)
    Base.metadata.create_all(bind=engine) 

    # 카테고리 예측 머신러닝 모델 불러오기
    # --> 서버가 켜질 때 딱 한 번만 수행해서, app_state에 보관한다.
    #     app_state : FastAPI가 기본 제공하는 앱 영역에서 공유하는 저장공간
    if MODEL_PATH.exists():
        app.state.category_model = joblib.load(MODEL_PATH)
        print(f'[INFO] 카테고리 예측 모델 로드 완료! : {MODEL_PATH}'
              f'먼저 `python ml/train_model.py`를 실행하세요.')
        
    # yield 지점에서 FastAPI가 이제 요청을 받아도 좋다고 판단하고 실제 서비스를 시작한다.
    else:
        # 모델 파일이 없어도 서버가 안 켜지게 막지 않는다. 회원가입/로그인/Todo CRUD는 ML과 무관하게 항상 정상 동작해야 하기 때문.
        app.state.category_model = None
        print(f'[WARN] 모델 파일이 없습니다.({MODEL_PATH})')



    yield 

# FastAPI 앱 객체 생성
# lifespan에 위에 만든 함수를 연결해서 '서버 켜질 때 테이블이 자동 생성'이 실제로 작업
app = FastAPI(lifespan=lifespan)

# routers/todo.py, routers/user.py에서 만든 라우터를 app 하나에 '합체'시키는 부분
app.include_router(todo_router)
app.include_router(user_router)
app.include_router(ml_router)


