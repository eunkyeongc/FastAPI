from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text

from database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)

    word = Column(String(100), nullable=False)
    meaning = Column(String(200), nullable=False)
    level = Column(String(20), nullable=False)

    example_sentence = Column(Text, nullable=False)
    example_translation = Column(Text, nullable=False)


class StudyHistory(Base):
    __tablename__ = "study_history"

    id = Column(Integer, primary_key=True, index=True)

    word_id = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)

    studied_at = Column(
        DateTime,
        default=datetime.now
    )

class WrongWord(Base):
    __tablename__ = "wrong_words"

    id = Column(Integer, primary_key=True, index=True)

    word_id = Column(Integer, nullable=False)

    wrong_count = Column(
        Integer,
        default=1
    )

    correct_streak = Column(
        Integer,
        default=0
    )

    status = Column(
        String(20),
        default="learning"
    )

    last_wrong_at = Column(
        DateTime,
        default=datetime.now
    )

class LearningProgress(Base):
    __tablename__ = "learning_progress"

    id = Column(Integer, primary_key=True, index=True)

    level = Column(
        String(20),
        nullable=False
    )

    day = Column(
        Integer,
        nullable=False
    )

    study_completed = Column(
        Boolean,
        default=False
    )

    word_test_completed = Column(
        Boolean,
        default=False
    )

    sentence_test_completed = Column(
        Boolean,
        default=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )