# ==========================================================================================================================================
# 빅데이터 저장시스템 개발(review)
# 2025. 07. 13. by 홍은경

# NCS_bigdata_processing_system\batch_processor_review.py
#   - "배치 처리(Batch Processing)" 단계 예제 실습
#   - 저장시스템에 이미 적재되어 있는 원본 테이블(subway-raw, bus_stop) 전체를 한 번에 읽어서, 집계 결과 테이블을 새로 만든다.
#   
#   --> 배치 처리의 특징 :  "전체 데이터를 대상으로, 정해진 시점에 한 번에" 처리
#       이번 예제에서는 python 코드가 데이터를 직접 계산하지 않고, PostgreSQL에게 SQL을 실행시켜 DB 엔진이 집계하도록 위임한다.
#       데이터가 매우 클 때에는 이렇게 DB(또는 Spark) 쪽에서 처리하는 것이 python 으로 한 줄씩 읽어 계산하는 것보다 휠씬 빠르고 메모리 효율적이다.
# ===========================================================================================================================================



from database import subway_engine, execute_sql, table_count
from sqlalchemy import text

def check_subway_input():
    """원본 테이블 존재 여부와 행 수 확인 """
    if table_count(subway_engine, "subway_raw") == 0:
        print('subway_raw 테이블이 없거나 테이터가 없습니다.')
        return False
    print(f"subway_raw 행수 : {table_count(subway_engine, 'subway_raw')}")
    return True

def create_summary_table():
    """집계 테이블 생성"""
    sql = """
        DROP TABLE IF EXISTS subway_summary;
        CREATE TABLE  subway_summary AS 
        SELECT
            "날짜" AS date,
            "역명" AS station_name,
            "승하차" AS ride_type,
            SUM("인원수") AS total_passengers
        FROM subway_raw
        GROUP BY "날짜", "역명", "승하차" 
        ORDER BY "날짜", "역명", "승하차" ;
        """
       
    execute_sql(subway_engine, sql)
    print('subway_summary  테이블 생성 완료')


def show_summary():
    """집계 결과 확인 """
    sql ="""
    SELECT *
    FROM subway_summary
    ORDER BY total_passengers DESC
    LIMIT 10;
    """

    with subway_engine.connect() as conn:
        result = conn.execute(text(sql))

        print("\n===== 집계 결과 상위 10건 =====")
        for row in result:
            print(row)

def main():

    print("=== 지하철 배치 처리 시작 ===")

    if not check_subway_input():
        return

    create_summary_table()
    show_summary()

    print("=== 배치 처리 종료 ===")


if __name__ == "__main__":
    main()