# =========================================================
# fastapi\2026_07_10_test\models.py
# 2026. 07. 10. by 홍은경
#
# 저장 모델 설계 :\\ 기본키 + UNIQUE 제약조건 추가
#
# 직접 실행되는 파일은 아니다. 
# database.py loader.py, import해서 사용
# =========================================================

# 라이브러리 불러오기
from sqlalchemy import Column, Integer, String, Date, Boolean, UniqueConstraint
from sqlalchemy.orm import declarative_base

#모든 모델 클래스가 상속받을 선언적 베이스 클래스를 생성
# 이 Base 를 상속받으면 클래스 =테이블, 클래서 속성 = 자동으로 테이블과 매칭
Base = declarative_base()

class HorseRaw(Base):
    __tablename__ = 'horse_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    승마장이름 = Column(String(30), nullable=False)
    주소 = Column(String(100), nullable=False)
    전화번호 = Column(String(50), nullable=False)
    시설유형 = Column(String(50), nullable=False)
    휴관일 = Column(String(10), nullable=False)
    OPEN = Column(String(10), nullable=False)
    CLOSE = Column(String(10), nullable=False)
    지역 = Column(String(20), nullable=False)
  
    
    #  # 복합 UNIQUE 제약 조건
    __table_args__ = (UniqueConstraint('승마장이름', '전화번호', '지역', name='uq_horse_info_key'),)

def __repr__(self):
   
    return f'<horseRaw {self.OPEN} {self.CLOSE} >'