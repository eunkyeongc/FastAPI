# =========================================================
# fastapi\2026_07_10_test\verify.py
# 2026. 07. 10. by 홍은경
#
# 승마장 적재 검증
#       - 필수 컬럼 NULL 여부
#       - 업무 키 조합 중복 여부  
#
# 커넥션(connection)?
#   - 파이썬 프로그램과 PostgreSQL 서버 사이에 맺어지는 연결 통로
#   - 계속 SQL을 주고 받으려면 이 연결부터 먼저 맺는다.
#        - 연결 생성 -> 쿼리 실행 -> 연결 종료 --> 낭비
#
# DB 커넥션 풀(Connection Pool) ?
#   - 프로그램이 시작될 때 (create_engine(...) 호출 시점) 연결 여러개를 미리 만들어서 "풀(Pool, 저장소)"에 담아 둔다.
#   - engine.connect()를 호출하면, 새로 연결을 만드는 게 아니라 풀에서 이미 만들어진 연결을 잠깐 빌려온다.
#   - 다 쓰고 나면(with 블록이 끝나면) 연결을 끊는게 아니라 풀에 다시 반납해서, 다음 번 요청이 그 연결을 재사용할 수 있게 한다.
#
# ===================================================================


from sqlalchemy import text   
from database import engine

def verify():
   
    with engine.connect() as conn:

        total = conn.execute(text("SELECT COUNT(*) FROM horse_info")).scalar()
        
        null_check = conn.execute(text("""
            SELECT  COUNT(*) FILTER (WHERE 승마장이름 IS NULL) AS null_horse_name,
                    COUNT(*) FILTER (WHERE 전화번호 IS NULL) AS null_tel_num,
                    COUNT(*) FILTER (WHERE 지역 IS NULL) AS null_area
            FROM horse_info """)).fetchone() 
        
             
    # --- 7. 검증 결과 출력---
    print('=== 승마장 적재 검증 결과 ===')
    print(f'전체 건수 : {total:,}')
    print(f'승마장이름 NULL 건수 : {null_check[0]}')
    print(f'전화번호 NULL 건수 : {null_check[1]}')
    print(f'주소 NULL 건수 : {null_check[2]}')
    
    # --- 8. 최종 PASS/FAIL 판정 ---
    ok = (
        total > 0 
        and all(value == 0 for value in null_check)  
    )
    print(f'검증 결과 :  {"PASS" if ok else "FAIL"}')
    return ok

if __name__ == "__main__": 
    verify()