# ===================================================================
# fastapi\2026_07_10_test\pipeline.py
# 2026. 07. 10. by 홍은경
#
# 한국마사회_농어촌형 승마시설정보 수집 데이터를 저장하는 파이프라인 통합 실행
#  --> 처리단계를 지정(각각의 모듈들 함수들 호출)
# ===================================================================
print("1")

from database import init_db
print("2")

from loader import load_from_csv
print("3")

from verify import verify
print("4")

from database import init_db
from loader import load_from_csv
from verify import verify

def main():
    print('1) 저장 구조 재설계 (기본키 + UNIQUE 제약조건 적용 )')
    init_db() # 함수 호출

    print()
    print('2) 결과(horse_long.csv) 배치 적재')
    load_from_csv() # 함수 호출

    print('3) 적재 검증')
    verify() # 검증 함수 호출

if __name__ == '__main__':
    main()