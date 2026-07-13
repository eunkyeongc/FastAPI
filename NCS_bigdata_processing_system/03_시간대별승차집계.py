# ============================================================================================
# NCS_bigdata_processing_system\03_시간대별승차집계.py
# [오늘의 복습 문제] 배치 처리 3번
#
# - 시간대별 승차 인원 집계하기
# ============================================================================================
# ## 요구사항
    # 1. 문제 1에서 확인한 실제 승하차 구분 컬럼을 사용합니다.
    # 2. 승차 데이터만 선택합니다.
    # 3. 시작 시간별로 데이터를 묶습니다.
    # 4. 행 수와 고유 역 개수를 각각 계산합니다.
    # 5. 승차 인원의 합계와 평균을 계산합니다.
    # 6. 결과를 `traffic_hour_summary`에 저장합니다.
    # 7. 프로그램을 다시 실행해도 오류가 발생하지 않아야 합니다.
    # 8. 평균은 소수점 둘째 자리까지 표시합니다.
    # 9. 결과 테이블 삭제·생성 및 인덱스 생성 SQL은 `create_hour_summary()` 함수에서 기존 `execute_sql()`로 실행합니다.
    # 10. `check_subway_input()`과 `create_hour_summary()`를 순서대로 호출하는 `main()`을 작성하고, `if __name__ == "__main__":`에서 `main()`을 호출합니다.
# ================================================================================================================================================================
# 실행결과: 
    # [batch] 시간대별 배치 처리 시작
    # [batch] 입력 테이블 확인 완료: subway_raw 1,260,000건
    # [batch] 시간대별 승차 집계 완료: traffic_hour_summary
    # [batch] 시간대별 배치 처리 완료
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