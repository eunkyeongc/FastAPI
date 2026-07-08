# ===============================================================
# fastpai/football//test_crud.py
#
# pytest로 단위테스트
#===============================================================

import pytest
from database import date

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

import models
import crud
from database import SessionLocal

# min_last_changed_date필터 테스트를 위한 기준 날짜(2024-04-01)
test_date = date(2024, 4, 1)

@pytest.fixture(scope="function")
def db_session():
    """ 
        테스트 함수마다 새 DB 세션을 열고, 테스트가 끝나면 닫는다. 
        scope="function" ---> 테스트 하나당 세션을 새로 만든다.
        세션을 공유하지 않기 때문에 테스트 간 서로 오염될 걱정이 적다.
    """

    session = SessionLocal()
    yield session
    session.close()


def test_get_player(db_session):
    """ player_id = 1001 인 선수를 정확히 가져오는지 확인 """
    player =crud.get_player(db_session, player_id=1001)
    assert player.player_id == 1001


def test_get_players(db_session):    
    """ 202-04-01 이후 변경된 선수 수가 seed 데이터 기준 1018명인지 확인 """    
    players = crud.get_player(db_session, skip=0, limi=10000, min_last_changed_date=test_date)
    assert len(players) == 1018

def test_get_all_performances(db_session):
    """ 전체 성적 기록수가 17306건인지 확인 """
    
    



""" 리그 하나를 league_id로 조회한다. """
def get_league(db: Session, league_id: int = None):
   
    return db.query(models.League).filter(models.League.league_id == league_id).first()


""" 
    리그 목록을 조회, 각 리그에 속한 teams까지 한 번에 즉시 로딩(eager load)
    joinedload(models.League.teams)를 사용하면 League를 조회할때 SQL JOIN으로  Team까지 한번의 쿼리로 같이 가져온다.
"""
def get_leagues(db: Session, skip: int = 0, limit: int = 100, min_last_changed_date: date = None, league_name: str = None):
   
    query = db.query(models.League).options(joinedload(models.League.teams))
    if min_last_changed_date:
        query = query.filter(models.League.last_changed_date >= min_last_changed_date)
    
    if league_name:
        query = query.filter(models.League.league_name == league_name)
    
    return query.offset(skip).limit(limit).all()
   

""" 팀 목록을 조회한다. league_id를 주면 특정 리스 소속 팀만 필터링한다. """
def get_teams(db: Session, skip: int = 0, limit: int = 100, min_last_changed_date: date = None, team_name: str = None, league_id: int = None):
    
    query = db.query(models.Team)
    if min_last_changed_date:
        query = query.filter(models.Team.last_changed_date >= min_last_changed_date)
    
    if league_id:
        query =query.filter(models.Team.league_id == league_id)
    
    return query.offset(skip).limit(limit).all()


# 분석 쿼리 (단순 카운트) -----------------------------------

""" 전체 선수 수를 센다. """
def get_player_count(db: Session):

    query = db.query(models.Player)
    return query.count()


""" 전체 팀 수를 센다. """
def get_team_count(db: Session):

    query = db.query(models.Team)
    return query.count()


""" 전체 리그 수를 센다. """
def get_league_count(db: Session):

    query = db.query(models.League)
    return query.count()

