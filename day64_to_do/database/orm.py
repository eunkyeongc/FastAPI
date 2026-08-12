# sqlalchemy: 파이썬 클래스와 DB 테이블을 이어주는 ORM 라이브러리
# psycopg2-binary: PostgreSQL과 대화하기 위한 핵심 통역사(드라이버)

#====================================================================
# database/orm.py
#     역할: 모든 orm 모델(테이블 클래스)의 부모가 되는 base class 정의
# ORM(Object Relational Mapping)이란?
#    -SQL을 직접 작성하지 않고, python 클래스로  db 테이블을 다루는 방식
#    -예: Todo 클래스 --> todo 테이블 자동 생성
#=====================================================================

from sqlalchemy.orm import DeclarativeBase
# DeclarativeBase는 sqlalchemy의 모든 모델이 상속받아야 하는 기본 클래스를 생성

# Base 클래서: 이 클래스를 상속받는 모든 클래스는 DB 테이블로 취급한다는 기준점 역할
class Base(DeclarativeBase):
    pass 