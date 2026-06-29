# ==========================================================================
# C:\Users\Administrator\bigdata2026\fastapi\fastapi_review\router\users.py
#   2026-06-29
#   user에 관한 앤드포인트 함수들의 집합소

#   APIRouter : 미니 FastAPI처럼 동작하는 라우터 객체
# ==========================================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from dependencies import get_db


# prefix='/users' --> 이 파일의 모든 경로 앞에 /users가 자동으로 붙는다.
# tags = ['users'] --> Swagger 문서에서 이 라우터의 그룹 이름
router = APIRouter(prefix='/users',tags=['users'])

@router.post('/', response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)  # 함수 호출 - 이메일 중복 체크
    if db_user: # 같은 이메일이 존재할 때
        raise HTTPException(status_code=400, detail='이미 등록된 이메일입니다.')
    return crud.create_user(db=db, user=user) #  함수 호출 - 회원등록

@router.get('/', response_model=list[schemas.UserResponse])
def read_user(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit) #  함수 호출 - 전체 유저 조회

@router.get('/{user_id}', response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id) # 함수 호출 - 유저 조회
    if db_user is None:
        raise HTTPException(status_code=404, detail='사용자를 찾을 수 없습니다.')
    return db_user

@router.post('/{user_id}/items', response_model=schemas.ItemResponse)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user(db, user_id = user_id) # 함수 호출 -유저 조회
    if db_user is None:
        raise HTTPException(status_code=404, detail='사용자를 찾을 수가 없습니다.')
    return crud.create_user_item(db=db, item=item, user_id=user_id)  # 함수 호출 - 아이템 등록