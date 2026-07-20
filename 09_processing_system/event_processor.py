# ============================================================================
# 2025. 07. 20.
# 빅데이터 저장시스템 개발

# 09_processing_system\event_processor.py
#   - "이벤트 처리(Event Processing)" 단계 모듈
#   - 숫자형 컬럼(buG1fAccTime)에 임계값(Threshold <= 75.0초)을 적용하여 저장
# ============================================================================

from database import horse_race_engine, check_required_tables, execute_sql

def create_horse_race_event() -> None:
    """
    경마 원본 데이터(horse_race_raw)에서 말별 평균 순위를 계산하여
    상위 10위에 드는 우수한 말들을 추출해 horse_race_event 테이블을 생성합니다.
    """
    execute_sql(
        horse_race_engine,
        '''
        DROP TABLE IF EXISTS horse_race_event;

        CREATE TABLE horse_race_event AS 
        SELECT
            "hrNo" AS race_id,
            "hrNameEn" AS horse,
            ROUND(AVG("buG1fOrd")::numeric, 1) AS avg_rank,
            'EXCELLENT' AS event_type
        FROM horse_race_raw
        WHERE "buG1fOrd" > 0
        GROUP BY "hrNo", "hrNameEn"
        HAVING COUNT(*) >= 3
        ORDER BY avg_rank ASC
        LIMIT 10;

        CREATE INDEX idx_horse_race_event_race_id
        ON horse_race_event(race_id);
        '''
    )
    print('[event] 우수 말 상위 10위 탐지 완료: horse_race_event')

def run_event_processing() -> None:
    """
    이벤트 처리 전체 흐름을 실행하는 엔트리 포인트 함수
    """
    print('[event] 필수 입력 테이블 확인')
    check_required_tables()
    create_horse_race_event()
    print('[event] 이벤트 처리 완료')

if __name__ == '__main__':
    run_event_processing()

