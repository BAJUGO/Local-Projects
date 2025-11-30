from .db import BaseClass
from sqlalchemy import Integer, String, Column


class Movie(BaseClass):
    __tablename__ = "Movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    director = Column(String)
    description = Column(String, index=True)
    year_of_issue = Column(Integer)


