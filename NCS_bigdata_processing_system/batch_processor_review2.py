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

def explore_subway_data():

    queries = [
        ("1. 컬럼명과 데이터 형식", """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name='subway_raw'
            ORDER BY ordinal_position;
        """),

        ("2. 전체 행 수", """
            SELECT COUNT(*) AS total_rows
            FROM subway_raw;
        """),

        ("3. 지하철역 개수", """
            SELECT COUNT(DISTINCT "역명") AS station_count
            FROM subway_raw;
        """),

        ("4. 승하차 구분 종류", """
            SELECT DISTINCT "승하차"
            FROM subway_raw;
        """),

        ("5. 승하차 구분별 행 수", """
            SELECT "승하차", COUNT(*) AS row_count
            FROM subway_raw
            GROUP BY "승하차";
        """),

        ("6. 인원 값이 가장 큰 데이터 10건", """
            SELECT *
            FROM subway_raw
            ORDER BY "인원수" DESC
            LIMIT 10;
        """),

        ("7. 날짜의 최솟값과 최댓값", """
            SELECT
                MIN("날짜") AS min_date,
                MAX("날짜") AS max_date
            FROM subway_raw;
        """),

        ("8. 인원 값이 NULL인 행 수", """
            SELECT COUNT(*) AS null_count
            FROM subway_raw
            WHERE "인원수" IS NULL;
        """)
    ]

    with subway_engine.connect() as conn:
        for title, sql in queries:
            print("\n" + "=" * 60)
            print(title)
            print("=" * 60)

            result = conn.execute(text(sql))

            for row in result:
                print(row)


def main():

    print("=== 지하철 원본 데이터 탐색 ===")

    if not check_subway_input():
        return

    explore_subway_data()

    print("\n=== 탐색 완료 ===")


if __name__ == "__main__":
    main()