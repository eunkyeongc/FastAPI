import csv
from pathlib import Path

from database import Base, engine, SessionLocal
from models import Word

Base.metadata.create_all(bind=engine)

DATA_DIR = Path(__file__).parent / "data"
CSV_FILES = sorted(DATA_DIR.glob("vocabulary_*.csv"))

REQUIRED_COLUMNS = {
    "word",
    "meaning",
    "level",
    "example_sentence",
    "example_translation",
}


def load_csv(path: Path) -> tuple[int, int]:
    added = 0
    updated = 0
    db = SessionLocal()

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            columns = set(reader.fieldnames or [])

            if not REQUIRED_COLUMNS.issubset(columns):
                missing = REQUIRED_COLUMNS - columns
                raise ValueError(f"{path.name}: 필요한 컬럼이 없습니다: {sorted(missing)}")

            for row in reader:
                word_text = row["word"].strip()
                level = row["level"].strip().lower()

                if not word_text:
                    continue

                word = (
                    db.query(Word)
                    .filter(Word.word == word_text, Word.level == level)
                    .first()
                )

                if word is None:
                    word = Word(word=word_text, level=level)
                    db.add(word)
                    added += 1
                else:
                    updated += 1

                word.meaning = row["meaning"].strip()
                word.example_sentence = row["example_sentence"].strip()
                word.example_translation = row["example_translation"].strip()

        db.commit()
        return added, updated
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main():
    if not CSV_FILES:
        print("data 폴더에 vocabulary_*.csv 파일이 없습니다.")
        return

    total_added = 0
    total_updated = 0

    for path in CSV_FILES:
        added, updated = load_csv(path)
        total_added += added
        total_updated += updated
        print(f"{path.name}: 추가 {added}개 / 갱신 {updated}개")

    print(f"완료: 추가 {total_added}개 / 갱신 {total_updated}개")


if __name__ == "__main__":
    main()
