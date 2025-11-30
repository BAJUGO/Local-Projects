from .db import BaseClass
from sqlalchemy import Integer, String, Column


class Movie(BaseClass):
    __tablename__ = "Movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    director = Column(String)
    description = Column(String, index=True)
    year = Column(Integer)


class Series(BaseClass):
    __tablename__ = "Series"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    seasons = Column(Integer)
    episodes = Column(Integer)
    description = Column(String, index=True)
    year = Column(Integer)
