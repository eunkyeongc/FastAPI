from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from database import Base, engine, SessionLocal
from datetime import date, datetime
import models
import random


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

class StudyRequest(BaseModel):
    word_id: int
    status: str

class WrongWordRequest(BaseModel):
    word_id: int

class WrongTestResultRequest(BaseModel):
    word_id: int
    is_correct: bool

class ProgressRequest(BaseModel):
    level: str
    day: int
    progress_type: str

templates = Jinja2Templates(
    directory="templates"
)

@app.get("/")
def home(request: Request):

    db = SessionLocal()

    # =====================================
    # 1. 전체 학습 진행 상황 가져오기
    # =====================================
    progresses = (
        db.query(models.LearningProgress)
        .all()
    )

    progress_data = []

    for progress in progresses:

        progress_data.append(
            {
                "level": progress.level,
                "day": progress.day,
                "study_completed": progress.study_completed,
                "word_test_completed": progress.word_test_completed,
                "sentence_test_completed": progress.sentence_test_completed
            }
        )


    # =====================================
    # 2. 난이도 순서
    # =====================================
    levels = [
        "basic",
        "intermediate",
        "advanced"
    ]


    daily_count = 20

    continue_level = None
    continue_day = None

    all_course_completed = True


    # =====================================
    # 3. 기초 → 중급 → 고급 순서로 검사
    # =====================================
    for level in levels:

        # 해당 난이도의 전체 단어 수
        word_count = (
            db.query(models.Word)
            .filter(
                models.Word.level == level
            )
            .count()
        )


        # 해당 난이도에 단어가 하나도 없으면
        # 다음 난이도로 넘어감
        if word_count == 0:
            continue


        # 해당 난이도의 총 Day 수
        total_days = (
            word_count + daily_count - 1
        ) // daily_count


        # Day 1부터 하나씩 확인
        for day in range(
            1,
            total_days + 1
        ):

            progress = (
                db.query(models.LearningProgress)
                .filter(
                    models.LearningProgress.level == level,
                    models.LearningProgress.day == day
                )
                .first()
            )


            # 해당 Day의 기록 자체가 없다면
            # 아직 시작하지 않은 Day
            if not progress:

                continue_level = level
                continue_day = day
                all_course_completed = False

                break


            # 3개 과정이 모두 완료됐는지 검사
            day_completed = (
                progress.study_completed
                and progress.word_test_completed
                and progress.sentence_test_completed
            )


            # 하나라도 완료되지 않았다면
            # 해당 Day부터 다시 시작
            if not day_completed:

                continue_level = level
                continue_day = day
                all_course_completed = False

                break


        # 현재 난이도에서
        # 아직 해야 할 Day를 발견했다면 종료
        if continue_level is not None:
            break


    db.close()


    # =====================================
    # 4. 홈 화면으로 전달
    # =====================================
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "progresses": progress_data,
            "continue_level": continue_level,
            "continue_day": continue_day,
            "all_course_completed": all_course_completed
        }
    )

@app.get("/study")
def study(
    request: Request,
    level: str = "basic",
    day: int = 1
):

    db = SessionLocal()

    daily_count = 20

    offset_count = (day - 1) * daily_count

    db_words = (
        db.query(models.Word)
        .filter(models.Word.level == level)
        .offset(offset_count)
        .limit(daily_count)
        .all()
    )

    words = [
        {
            "id": word.id,
            "word": word.word,
            "meaning": word.meaning,
            "level": word.level,
            "example_sentence": word.example_sentence,
            "example_translation": word.example_translation
        }
        for word in db_words
    ]

    total_words = (
        db.query(models.Word)
        .filter(models.Word.level == level)
        .count()
    )

    total_days = (total_words + daily_count - 1) // daily_count

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="study.html",
        context={
            "words": words,
            "level": level,
            "day": day,
            "total_days": total_days
        }
    )

@app.post("/study-status")
def save_study_status(data: StudyRequest):

    db = SessionLocal()

    history = models.StudyHistory(
        word_id=data.word_id,
        status=data.status
    )

    db.add(history)
    db.commit()

    db.refresh(history)

    db.close()

    return {
        "message": "학습 상태 저장 완료",
        "word_id": data.word_id,
        "status": data.status
    }

@app.get("/study-history")
def get_study_history():

    db = SessionLocal()

    histories = db.query(models.StudyHistory).all()

    result = []

    for history in histories:

        word = (
            db.query(models.Word)
            .filter(models.Word.id == history.word_id)
            .first()
        )

        result.append(
            {
                "id": history.id,
                "word_id": history.word_id,
                "word": word.word if word else None,
                "status": history.status,
                "studied_at": history.studied_at
            }
        )

    db.close()

    return result


from datetime import date


@app.get("/today-progress")
def get_today_progress():

    db = SessionLocal()

    today = date.today()

    histories = db.query(models.StudyHistory).all()

    studied_word_ids = set()

    for history in histories:

        if history.studied_at.date() == today:
            studied_word_ids.add(history.word_id)

    studied_count = len(studied_word_ids)

    daily_goal = 20

    db.close()

    return {
        "studied_count": studied_count,
        "daily_goal": daily_goal,
        "remaining_count": max(daily_goal - studied_count, 0)
    }

@app.get("/word-test")
def word_test(
    request: Request,
    level: str = "basic",
    day: int = 1
):

    db = SessionLocal()

    daily_count = 20
    offset_count = (day - 1) * daily_count

    db_words = (
        db.query(models.Word)
        .filter(models.Word.level == level)
        .offset(offset_count)
        .limit(daily_count)
        .all()
    )

    all_words = (
        db.query(models.Word)
        .filter(models.Word.level == level)
        .all()
    )

    questions = []

    for word in db_words:

        wrong_candidates = [
            w.meaning
            for w in all_words
            if w.id != word.id
        ]

        wrong_options = random.sample(
            wrong_candidates,
            min(3, len(wrong_candidates))
        )

        options = wrong_options + [word.meaning]

        random.shuffle(options)

        questions.append(
            {
                "word_id": word.id,
                "word": word.word,
                "answer": word.meaning,
                "options": options
            }
        )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="word_test.html",
        context={
            "questions": questions,
            "level": level,
            "day": day
        }
    )

@app.post("/wrong-words")
def save_wrong_word(data: WrongWordRequest):

    db = SessionLocal()

    wrong_word = (
        db.query(models.WrongWord)
        .filter(
            models.WrongWord.word_id == data.word_id,
            models.WrongWord.status == "learning"
        )
        .first()
    )

    if wrong_word:

        wrong_word.wrong_count += 1
        wrong_word.correct_streak = 0

        wrong_word.last_wrong_at = datetime.now()

    else:

        wrong_word = models.WrongWord(
            word_id=data.word_id,
            wrong_count=1,
            correct_streak=0,
            status="learning"
        )

        db.add(wrong_word)

    db.commit()

    db.close()

    return {
        "message": "오답노트 저장 완료",
        "word_id": data.word_id
    }

@app.get("/wrong-words")
def get_wrong_words():

    db = SessionLocal()

    wrong_words = (
        db.query(models.WrongWord)
        .filter(
            models.WrongWord.status == "learning"
        )
        .all()
    )

    result = []

    for wrong in wrong_words:

        word = (
            db.query(models.Word)
            .filter(
                models.Word.id == wrong.word_id
            )
            .first()
        )

        if word:

            result.append(
                {
                    "word_id": word.id,
                    "word": word.word,
                    "meaning": word.meaning,
                    "wrong_count": wrong.wrong_count,
                    "correct_streak": wrong.correct_streak,
                    "status": wrong.status,
                    "last_wrong_at": wrong.last_wrong_at
                }
            )

    db.close()

    return result

@app.get("/wrong-note")
def wrong_note(request: Request):

    db = SessionLocal()

    wrong_records = (
        db.query(models.WrongWord)
        .filter(
            models.WrongWord.status == "learning"
        )
        .all()
    )

    wrong_words = []

    for record in wrong_records:

        word = (
            db.query(models.Word)
            .filter(
                models.Word.id == record.word_id
            )
            .first()
        )

        if word:

            wrong_words.append(
                {
                    "word_id": word.id,
                    "word": word.word,
                    "meaning": word.meaning,
                    "example_sentence": word.example_sentence,
                    "example_translation": word.example_translation,
                    "wrong_count": record.wrong_count,
                    "correct_streak": record.correct_streak
                }
            )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="wrong_note.html",
        context={
            "wrong_words": wrong_words
        }
    )

@app.get("/wrong-test")
def wrong_test(request: Request):

    db = SessionLocal()

    wrong_records = (
        db.query(models.WrongWord)
        .filter(
            models.WrongWord.status == "learning"
        )
        .all()
    )

    all_words = db.query(models.Word).all()

    questions = []


    for record in wrong_records:

        word = (
            db.query(models.Word)
            .filter(
                models.Word.id == record.word_id
            )
            .first()
        )

        if not word:
            continue


        # 예문에서 정답 단어를 빈칸으로 변경
        sentence = word.example_sentence.replace(
            word.word,
            "______"
        )


        wrong_candidates = [
            candidate.word
            for candidate in all_words
            if candidate.id != word.id
        ]


        wrong_options = random.sample(
            wrong_candidates,
            min(3, len(wrong_candidates))
        )


        options = wrong_options + [word.word]

        random.shuffle(options)


        questions.append(
            {
                "word_id": word.id,
                "sentence": sentence,
                "answer": word.word,
                "meaning": word.meaning,
                "options": options
            }
        )


    random.shuffle(questions)

    db.close()


    return templates.TemplateResponse(
        request=request,
        name="wrong_test.html",
        context={
            "questions": questions
        }
    )

@app.post("/wrong-test-result")
def save_wrong_test_result(
    data: WrongTestResultRequest
):

    db = SessionLocal()

    wrong_word = (
        db.query(models.WrongWord)
        .filter(
            models.WrongWord.word_id == data.word_id,
            models.WrongWord.status == "learning"
        )
        .first()
    )

    if not wrong_word:

        db.close()

        return {
            "message": "오답노트에 없는 단어입니다."
        }


    # 정답을 맞힌 경우
    if data.is_correct:

        wrong_word.correct_streak += 1

        # 3회 연속 정답이면 오답노트 졸업
        if wrong_word.correct_streak >= 3:

            wrong_word.status = "mastered"


    # 다시 틀린 경우
    else:

        wrong_word.wrong_count += 1

        wrong_word.correct_streak = 0

        wrong_word.last_wrong_at = datetime.now()


    db.commit()

    result = {
        "word_id": wrong_word.word_id,
        "wrong_count": wrong_word.wrong_count,
        "correct_streak": wrong_word.correct_streak,
        "status": wrong_word.status
    }

    db.close()

    return result

@app.get("/sentence-test")
def sentence_test(
    request: Request,
    level: str = "basic",
    day: int = 1
):

    db = SessionLocal()

    daily_count = 20

    offset_count = (day - 1) * daily_count


    db_words = (
        db.query(models.Word)
        .filter(models.Word.level == level)
        .offset(offset_count)
        .limit(daily_count)
        .all()
    )


    all_words = (
        db.query(models.Word)
        .filter(models.Word.level == level)
        .all()
    )


    questions = []


    for word in db_words:

        sentence = word.example_sentence.replace(
            word.word,
            "______"
        )


        wrong_candidates = [
            candidate.word
            for candidate in all_words
            if candidate.id != word.id
        ]


        wrong_options = random.sample(
            wrong_candidates,
            min(3, len(wrong_candidates))
        )


        options = wrong_options + [word.word]

        random.shuffle(options)


        questions.append(
            {
                "word_id": word.id,
                "sentence": sentence,
                "answer": word.word,
                "meaning": word.meaning,
                "options": options
            }
        )


    random.shuffle(questions)

    db.close()


    return templates.TemplateResponse(
        request=request,
        name="sentence_test.html",
        context={
            "questions": questions,
            "level": level,
            "day": day
        }
    )

@app.get("/progress")
def get_progress():

    db = SessionLocal()

    progresses = (
        db.query(models.LearningProgress)
        .order_by(
            models.LearningProgress.level,
            models.LearningProgress.day
        )
        .all()
    )

    result = []

    for progress in progresses:

        result.append(
            {
                "level": progress.level,
                "day": progress.day,
                "study_completed": progress.study_completed,
                "word_test_completed": progress.word_test_completed,
                "sentence_test_completed": progress.sentence_test_completed
            }
        )

    db.close()

    return result

@app.post("/progress")
def save_progress(data: ProgressRequest):

    db = SessionLocal()

    progress = (
        db.query(models.LearningProgress)
        .filter(
            models.LearningProgress.level == data.level,
            models.LearningProgress.day == data.day
        )
        .first()
    )

    if not progress:

        progress = models.LearningProgress(
            level=data.level,
            day=data.day
        )

        db.add(progress)


    if data.progress_type == "study":

        progress.study_completed = True

    elif data.progress_type == "word_test":

        progress.word_test_completed = True

    elif data.progress_type == "sentence_test":

        progress.sentence_test_completed = True

    else:

        db.close()

        return {
            "message": "잘못된 progress_type입니다."
        }


    db.commit()

    result = {
        "level": progress.level,
        "day": progress.day,
        "study_completed": progress.study_completed,
        "word_test_completed": progress.word_test_completed,
        "sentence_test_completed": progress.sentence_test_completed
    }

    db.close()

    return result