# import psycopg
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# #base way to connect to DB
# conn = psycopg.connect("dbname=test user=postgres password=Ih8hackers!")
# cur = conn.cursor(row_factory=dict_row)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
