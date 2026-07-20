# ============================================================================
# 2025. 07. 20.
# 빅데이터 저장시스템 개발

# 09_processing_system\batch_processor.py
#   - 배치 처리 모듈
#   - PostgreSQL에게 SQL을 실행시켜 DB 엔진이 집계를 수행하도록 함
# ============================================================================
from database import horse_race_engine, check_required_tables, execute_sql

def create_horse_race_summary() -> None:
    """
    경마 원본 데이터(horse_race_raw)를 기수("jkNameEn") 기준으로 그룹핑하여
    경주 수, 평균 경주 기록, 최고 기록, 최저 기록, 평균 순위 집계 테이블을 생성합니다.
    """
    execute_sql(
        horse_race_engine,
        '''
        DROP TABLE IF EXISTS horse_race_summary;

        CREATE TABLE horse_race_summary AS 
        SELECT
            "jkNameEn" AS race_place,
            COUNT(*) AS race_count,
            ROUND(AVG("buG1fAccTime")::numeric, 2) AS avg_time,
            ROUND(MAX("buG1fAccTime")::numeric, 2) AS max_time,
            ROUND(MIN("buG1fAccTime")::numeric, 2) AS min_time,
            ROUND(AVG("buG1fOrd")::numeric, 1) AS avg_rank
        FROM horse_race_raw
        GROUP BY "jkNameEn";

        CREATE INDEX idx_horse_race_summary_count
        ON horse_race_summary(race_count DESC);
        '''
    )
    print('[batch] 기수별 집계 완료: horse_race_summary')

def run_batch_processing() -> None:
    """
    배치 처리 전체 흐름을 순서대로 실행하는 엔트리 포인트 함수
    """
    print('[batch] 필수 입력 테이블 확인')
    check_required_tables()
    create_horse_race_summary()
    print('[batch] 배치 처리 완료')

if __name__ == '__main__':
    run_batch_processing()