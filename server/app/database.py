from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Union
from sqlalchemy import Column, Float, String, Integer

SQLALCHEMY_DATABASE_URL = "sqlite:///../test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

class Review(Base):
    """Review holds the information of user review"""

    __tablename__ = "review"

    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    film_name: Union[str, Column] = Column(String, unique=False, nullable=False)
    title: Union[str, Column] = Column(String, nullable=False)
    body: Union[str, Column] = Column(String, nullable=False)
    author: Union[str, Column] = Column(String, nullable=False)
    score: Union[float, Column] = Column(Float, nullable=False)
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)


def create_tables():
    Base.metadata.create_all(bind=engine)