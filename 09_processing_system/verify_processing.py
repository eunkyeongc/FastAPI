# ============================================================================
# 2025. 07. 20.
# 빅데이터 저장시스템 개발

# 09_processing_system\verify_processing.py
#   - 배치 및 이벤트 처리 결과 검증
# ============================================================================
# ============================================================================
# 09_processing_system\verify_processing.py
#   - 처리시스템 결과 검증 (배치 + 이벤트)
# ============================================================================
from sqlalchemy import text
from database import horse_race_engine, table_count

# CHECKS - 검증할 DB Engine과 결과 테이블 목록
CHECKS = [
    (horse_race_engine, "horse_race_summary"),  # 배치 처리 결과 : 말별 통합 실적 집계
    (horse_race_engine, "horse_race_event"),  # 이벤트 처리 결과 : 상위 우수 말 탐지
]


def verify() -> bool:
    """
    CHECKS에 정의된 모든 테이블을 순회하며 건수를 출력하고,
    하나라도 조회에 실패하면 전체 결과를 FAIL로 판정

    반환값:
        True: 모든 테이블 조회에 성공(PASS)
        False: 하나 이상의 테이블 조회에 실패(FAIL)
    """
    print("=== 처리시스템 결과 검증(배치+이벤트) ===")

    # 처음에는 성공(True)으로 가정하고, 실패를 한 번이라도 만나면 False
    ok = True

    for engine, table_name in CHECKS:
        try:
            count = table_count(engine, table_name)  # 테이블 행 수 조회
            print(f"{table_name}: {count:,}건")

        except Exception as exc:
            ok = False
            print(f"{table_name}: 확인 실패 - {exc}")

    print(f'검증 결과: {"PASS" if ok else "FAIL"}')

    # 호출한 코드가 화면 문자열을 다시 분석하지 않고도 성공 여부를 사용할 수 있게 bool 값 반환
    return ok


if __name__ == "__main__":
    verify()  # 검증 함수 호출