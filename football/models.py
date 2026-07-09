# ============================================
# 데이터베이스의 테이블을 나태나는 클래스 만들기
# 2026. 7. 8.
# Book : Hands-On APIs for AI and Data Science
# 
# fastapi/football/models.py
#
# SQLAlchemy 모델 정의 (ORM 매핑 클래스)
# ===========================================
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from database import Base

# 테이블이 5개 ---> class도 5개
# 클래스 네임은 대문자로 시작, 테이블 네임은 소문자로 시작

""" 1) 선수 정보를 담은 테이블, 판타지 풋볼 리그에 참가하는 개별 선수 1명 = 1행 """
class Player(Base):
    __tablename__ ="player"

    # PostgreSQL에서는  String이 VARCHAR로 매핑된다.
    # 길이를 지정하지 않은 VARCHAR(=길이 무제한)을 정식으로 지원하으로 별도 길이를 주지 않아도 된다.
    player_id = Column(Integer, primary_key=True, index=True)   # 선수 고유 번호
    gsis_id = Column(String, nullable=True)                     # NFL 쪽 선수 식별자 --> id가 없는 선수도 있다.--> True
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position =Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)            # 데이터가 마지막으로 수정된 날짜

    # 1:N (일대다관계, 선수:성적 관계)
    performances = relationship("Performance", back_populates = 'player')

    # N:M (Team 사의 다대다 관계)
    # --> 선수 1명이 여러 팀에 속하고, 팀 하나에 여러 선수가 속할 수 있는 다대다 구조를 표현하는 패턴
    teams = relationship("Team", secondary="team_player", back_populates='players')


""" 2) 선수 한명의 특징을 추가(week) 판타지 포인트 기록 """
class Performance(Base):
    __tablename__ ="performance"

    performance_id = Column(Integer, primary_key=True, index=True)   # 성적 기록 고유 번호
    week_number = Column(String, nullable=False)                     # 시즌 몇 주차인지
    fantasy_points = Column(Float, nullable=False)                   # 판타지 점수
    last_changed_date = Column(Date, nullable=False)                # 데이터가 마지막으로 수정된 날짜

    # player 테이블의 player_id를 참조하는 외래키(FK)
    player_id = Column(Integer, ForeignKey('player.player_id'))

    player = relationship('Player', back_populates='performances')

""" 3) 판타지 풋볼 리그(대회) 정보"""
class League(Base):
    __tablename__ ="league"

    league_id = Column(Integer, primary_key=True, index=True) # 리그 고유 번호
    league_name = Column(String, nullable=False)
    scoring_type = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)

    # 1(리그):N(팀) 관계 - 한 리그 안에 팀이 여러개(일대다)
    teams = relationship("Team", back_populates='league')

""" 4) 리그에 속한 팀 """
class Team(Base):
    __tablename__ ="team"

    team_id	= Column(Integer, primary_key=True, index=True) # 팀 고유 번호
    team_name = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)	# 데이터가 마지막으로 수정된 날짜
    
    # league 테이블의 league_id를 참조하는 외래키(FK)
    league_id = Column(Integer, ForeignKey('league.league_id'))  # 외래키

    league = relationship('League', back_populates='teams')
    
    # secondary='team_player' : 아래 TeamPlayer 연결 테이블을 중간에 두고 조인
    players = relationship('Player', secondary='team_player', back_populates='teams')


""" 
    5) Team과 Player의 다대다 관계를 표현하는 연결(association) 테이블.
    테이블 자체는 독자적인 대리키(surrogate key)가 없고, 
    (team_id, player_id) 조합 전체를 복합 기본키로 사용한다.
    --> 같은 team_id + player_id 조합은 한 번만 존재할 수 있다.(중복 가입 방지)
"""
class TeamPlayer(Base):
    __tablename__ ="team_player"

    team_id = Column(Integer, ForeignKey('team.team_id'), primary_key=True, index=True)
    player_id =Column(Integer, ForeignKey('player.player_id'), primary_key=True, index=True)
    last_changed_date = Column(Date, nullable=False)