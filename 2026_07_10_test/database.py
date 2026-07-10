# =========================================================
# fastapi\2026_07_10_test\database.py
# 2026. 07. 10. by 홍은경
#
# PostgreSQL 연결 및 세션 관리
# (DB명 : subwaydb, 비밀번호: 1234)
# =========================================================

# 라이브러리 불러오기
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# DB URL 연결 
DB_URL = 'postgresql://postgres:1234@localhost:5432/horsedb'

# PostgreSQL과 연결할 엔진 생성
engine = create_engine(DB_URL, echo=False)

# 세션 팩토리 생성
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 테이블 재설계를 위한 함수 정의
def init_db(drop_existing: bool=True):
    
    if drop_existing:
        Base.metadata.drop_all(bind=engine)
        print('[database] 기존 horse_info 테이블 삭제(재설계를 위해)') 

    Base.metadata.create_all(bind=engine)
    print('[database] horse_raw  테이블 준비 완료(기본키 +  UNIQUE 제약 적용)')

def get_session():
   
    return SessionLocal()
