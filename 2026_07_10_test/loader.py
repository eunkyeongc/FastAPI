# ===================================================================
# fastapi\2026_07_10_test\loader.py
# 2026. 07. 10. by 홍은경
#
# 수집한 결과로 나온 파일 horse_info.csv를 horse_raw 테이블에 적재
# ===================================================================

# 라이브러리 불러오기
import os
import pandas  as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from database import engine
from models import HorseRaw

# 경로 설정 및 기본값 설정
BASE_DIR = os.getcwd()  
INPUT_PATH = os.path.join(BASE_DIR, 'input', 'horse_info.csv') 
CHUNK_SIZE = 5000


def _prepare_chunk(chunk: pd.DataFrame) -> list[dict]:
   
    chunk = chunk.copy() 

    # 핵심 컬럼('승마장이름', '전화번호', '지역') 중 하나라도 비어있으며,
    chunk = chunk.dropna(subset=['승마장이름', '전화번호', '지역'])  

    # 필요한 컬럼만 순서대로 골라, DB 삽입에 사용할 수 있는 딕셔너리 리스트로 변환
    # SQLAlchemy Core의 insert(values=[...]) 형태로 넣기 위해서
    return chunk[['승마장이름', '주소', '전화번호', '시설유형', '휴관일', 'OPEN', 'CLOSE', '지역'
    ]].to_dict(orient='records')

# 함수 정의
def load_from_csv(path: str=INPUT_PATH, chunksize: int=CHUNK_SIZE) -> dict:
   
    # 전체 적재 결과를 누적할 카운터들
    total_success = 0  # 새로 삽입된 건수
    total_skipped = 0  # UNIQUE 제약에 걸린 중복으로 스킵된 건수
    total_failed = 0    # 배치 자체가 에러로 실패한 건수

    for i, chunk in enumerate(pd.read_csv(INPUT_PATH, encoding='utf-8-sig', chunksize=CHUNK_SIZE)):
        try:
            records = _prepare_chunk(chunk) # 함수호출

            if not records:
                continue  

            with engine.begin() as conn:
                
                stmt = pg_insert(HorseRaw).values(records)

                stmt = stmt.on_conflict_do_nothing(constraint='uq_horse_info_key')

                # 실제 SQL 실행
                result= conn.execute(stmt)            

            inserted =result.rowcount if result.rowcount is not None else 0

            skipped = len(records) - inserted

            total_success += inserted
            total_skipped += skipped

            print(f'[i+1]번째 배치 - 신구{inserted}건 / 중복스킵{skipped}건')

        except Exception as e:
           
            total_failed += len(chunk)
            print(f'{i+1}번째 배치 실패(이 배치만 롤백, 다음 배치는 계속 진행): {e}')

    # 최종 결과를 딕셔너리로 정리
    summary = {
        "success": total_success,
        "skipped_duplicate": total_skipped, 
        "failed": total_failed,
    }

    print(f'[loader] 전체 적재 완료 - 신규: {total_success:,}건 / 중복스킵: {total_skipped:,}건 / 실패: {total_failed:,}건')

    return summary

if __name__ == '__main__':
    load_from_csv()