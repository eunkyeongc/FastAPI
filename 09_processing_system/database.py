# ============================================================================
# 2025. 07. 20.
# 빅데이터 저장시스템 개발

# 09_processing_system\database.py
#   - engine 생성 및 공통 유틸리티(execute_sql 등)
# =====================================================================================
from sqlalchemy import create_engine, text
import os

from config import HORSE_RACE_DB_URL

# -------------------------------------------------------------------------------------
# DB Engine 생성
#
# echo=False : 실행되는 SQL을 콘솔에 출력하지 않는다.( 디버깅 시 True로 바꾸면 유용)
# future=True : SQLAlchemy 2.0 스타일 API를 사용하겠다는 의미
# -------------------------------------------------------------------------------------
horse_race_engine = create_engine(HORSE_RACE_DB_URL, echo=False, future=True) 


def table_count(engine, table_name : str) -> int: 
    """ 주어진 테이블의 전체 행(row) 개수를 반환 """
    with engine.connect() as conn:
        # scalar_one() :  결과가 정확히 1행 1열일 때, 그 값 하나만 꺼내는 메서드
        return conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar_one()
    
def check_required_tables() -> None:
    """
    배치/실시간/이벤트 처리를 시작하기 전에, 반드시 존재해야하는 원본 테이블(horse_race_db)이
    실제로 존재하고 데이터가 들어있는지 점검하는 함수
    """
    checks = [
        (horse_race_engine, "horse_race_raw", "경마경주기록 저장시스템 실습 결과가 필요합니다.")      
    ]
    for engine, table_name, hint in checks:
        try:
            count = table_count(engine, table_name)
            print(f"[check] {table_name} 테이블 데이터 확인: {count}건")
        except Exception as exc:
           raise RuntimeError(f'"{table_name}" 테이블을 확인할 수 없습니다. {hint} 원인: {exc}') from exc
        
        if count == 0: 
            # 테이블은 있지만 적재된 행이 0건 인 경우(저장시스템 실습 미완료 가능성)
            raise RuntimeError(f'"{table_name}" 테이블은 존재하지만 데이터가 없습니다. 저장시스템 적재를 먼저 확인해주세요.')

def execute_sql(engine, sql: str, params: dict | None = None) -> None:
    """
    여러 문장으로 이루어진  SQL 스크립트(세미콜론으로 구분)를 한번에 실행한다.

    동작 방식 :
        1) engine.begin() : 트랜잭션을 시작하고, with 블록이 정상 종료되면 자동으로 COMMIT, 예외가 발생하면 자동으로 ROLLBACK
        2) sql.split(';'): SQL 문자열을 세미콜론 기준으로 나눠 여러 statement로 분리
        3) 빈 문자열(공백만 있는 조각)은 제거하고, 각 statement를 순서대로 실행
    """
    with engine.begin() as conn:
        statements = [statement.strip() for statement in sql.split(';') if statement.strip()]
        for statement in statements:
            conn.execute(text(statement), params or {})


