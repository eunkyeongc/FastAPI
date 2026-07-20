# ============================================================================
# 2025. 07. 20.
# 빅데이터 저장시스템 개발

# 09_processing_system\pipeline.py
#   - 배치 및 이벤트 처리 단계를 하나로 통합 실행하는 파이프라인
# ============================================================================
import sys
from batch_processor import run_batch_processing
from event_processor import run_event_processing

def run_pipeline() -> None:
    print("=" * 60)
    print("빅데이터 처리 파이프라인 통합 실행 시작")
    print("=" * 60)

    try:
        # 1. 배치 처리 실행
        run_batch_processing()
        print("-" * 60)

        # 2. 이벤트 처리 실행
        run_event_processing()
        print("-" * 60)

        print(" 모든 데이터 처리 파이프라인이 성공적으로 수행되었습니다.")
        print("=" * 60)

    except Exception as exc:
        print(f"\n 파이프라인 실행 중 예외 발생: {exc}")
        sys.exit(1)

if __name__ == '__main__':
    run_pipeline()