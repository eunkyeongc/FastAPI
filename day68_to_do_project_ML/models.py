# =====================================================================
# 2026. 08. 12.
# to_do_ project
# day66_to_do_project\models.py
#
# SQLAlchemy ORM 모델 정의 파일
# 파이썬 클래스와 DB 테이블을 매핑(Mapping)하는 부분
#  
# =====================================================================

from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.orm import Base   # \database\orm.py

# --- Todo 모델 (할 일 테이블) ---
class Todo(Base):
    __tablename__ = 'todo'  # 실제 DB에 생성될 테이블 이름

    # 컬럼(열) 생성  --> 실제 컬럼 4가지(id, title, is_done, user_id)
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,   # 기본키
        autoincrement=True, # 새 행이 추가될 때마다 1씩 자동 증가
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,     # 널 가능? --> 아니(반드시 입력되어야 함)
    )
    is_done: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,     # 할 일을 했니? 안 했니?(필수사항)
        default=False,      # 새로 생성될 때마다 기본값은 '완료 안 함'
    )
    user_id: Mapped[int] = mapped_column(
        # Todo.user_id가 User.id를 참조한다.(이 할 일은 어떤 회원의 것인지 연결)
        ForeignKey('user.id'),  # user 테이블의 id를 참조하는 외래키
        nullable=True,      # 담당 회원을 지정하지 않고 생성 가능(널 가능?? -> 응 가능.)
    )

    user: Mapped['User'] = relationship(
        back_populates = 'todos',   # User.todos 속성과 양방향으로 연결
    )

# --- User 모델(회원 테이블) ---
class User(Base):
    __tablename__ = 'user' # 실제 DB에 생성될 테이블 이름

    # 컬럼(열) 생성
    id: Mapped[int] = mapped_column(
        primary_key=True    # 기본키
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,    # 같은 이메일로 중복 가입 불가
        index=True,     # 이메일로 조회가 자주 일어나므로 검색 속도 향상용 인덱스
        nullable=False, # 널 가능?? -> 아님 (필수사항)
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,     # 비밀번호는 평문이 아닌 해시코드로 저장(필수사항)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),      # 행 추가 시점에 DB가 자동으로 현재 시간을 채운다.
        nullable=False,
    )

    refresh_token: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,  # 로그인 전이거나, 로그아웃한 사용자는 None
    )
    todos: Mapped[list['Todo']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan', # 회원이 삭제되면 그 회원의 Todo들도 함께 자동삭제
    )




