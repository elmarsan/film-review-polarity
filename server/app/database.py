from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///../test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    echo=True,
    future=True
)

Base = declarative_base()

Session = sessionmaker(engine)

def init_database():
    Base.metadata.create_all(bind=engine)
