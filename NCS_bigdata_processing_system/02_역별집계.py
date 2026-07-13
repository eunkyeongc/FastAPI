# ============================================================================================
# NCS_bigdata_processing_system\02_역별집계.py
# [오늘의 복습 문제] 배치 처리 2번
#
# - 역별 인원 값 집계하기
# ============================================================================================
# ## 요구사항
    # 1. 실행 전에 `subway_raw` 테이블의 존재 여부와 데이터 건수를 확인합니다.
    # 2. `subway_raw`를 역 번호와 역 이름으로 묶습니다.
    # 3. 역별 행 수, 인원 값 합계 및 평균을 계산합니다.
    # 4. 평균은 소수점 둘째 자리까지 표시합니다.
    # 5. 결과를 `traffic_station_summary`에 저장합니다.
    # 6. 프로그램을 다시 실행해도 오류가 발생하지 않게 기존 결과 테이블을 처리합니다.
    # 7. `total_passengers` 내림차순 조회에 사용할 인덱스를 생성합니다.
    # 8. 결과 테이블 삭제·생성 및 인덱스 생성 SQL은 기존 `execute_sql()`을 이용해 하나의 트랜잭션으로 실행합니다.
    # 9. `check_subway_input()`과 `create_station_summary()`를 순서대로 호출하는 `main()`을 작성하고, `if __name__ == "__main__":`에서 `main()`을 호출합니다.
# ================================================================================================================================================================
# 실행결과: 
    # [batch] 역별 배치 처리 시작
    # [batch] 입력 테이블 확인 완료: subway_raw 1,260,000건
    # [batch] 역별 집계 완료: traffic_station_summary
    # [batch] 역별 배치 처리 완료
# ========================================================

from database import subway_engine, execute_sql, table_count

# 1. 실행 전에 `subway_raw` 테이블의 존재 여부와 데이터 건수를 확인합니다.
def check_subway_input() -> None :
    """subway_raw 테이블의 존재 여부와 데이터 건수를 확인하는 함수"""
    try:
        count =table_count(subway_engine, 'subway_raw')
    except Exception as exc:
        raise RuntimeError("subway_raw 테이블을 확인할 수 없습니다."
                            "DB 연결과 원본 데이터 적재 여부를 확인하세요.") from exc
    
    if count == 0:
        raise RuntimeError("subway_raw 테이블에 데이터가 없습니다.")
    print(f'[batch] 입력 테이블 확인 완료 : subway_raw {count:,}건')


# 2. `subway_raw`를 역 번호와 역 이름으로 묶습니다.
# 3. 역별 행 수, 인원 값 합계 및 평균을 계산합니다.
def create_station_summary() -> None:
    """ 원본 데이터를 역별로 집계 -> 결과 테이블로 만들기"""
    execute_sql(
        subway_engine, 
        """
        DROP TABLE IF EXISTS traffic_station_summary;

        CREATE TABLE traffic_station_summary AS
        SELECT 
            "역번호" AS station_no,
            "역명" AS station_name,
            COUNT(*) AS row_count, 
            SUM("인원수") AS total_passengers,
            ROUND(AVG("인원수")::numeric, 2) AS avg_passengers
        FROM subway_raw
        GROUP BY "역번호", "역명";

        CREATE INDEX idx_traffic_station_summary_total
        ON traffic_station_summary(total_passengers DESC);
        """
    )
    print('[batch] 역별 집계 완료: traffic_station_summary')

def main() -> None:
    print('[batch] 역별 배치 처리 시작')
    check_subway_input()
    create_station_summary()
    print('[batch] 역별 배치 처리 완료')

if __name__ == "__main__":
    main()




