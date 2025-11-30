from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base


DATABASE_URL = "postgresql://dimka:kiril12AZ@localhost:5432/Movies"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


BaseClass = declarative_base()


def create_table():
    BaseClass.metadata.create_all(bind=engine)

