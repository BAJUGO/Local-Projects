from .schemas import MovieCreate
from sqlalchemy.orm import Session
from .model import Movie
from fastapi.exceptions import HTTPException


def add_movie(db: Session, movie: MovieCreate):
    movie_to_database = Movie(**movie.model_dump())

    if movie_to_database:
        db.add(movie_to_database)
        db.commit()
        db.refresh(movie_to_database)
        return movie_to_database
    raise HTTPException(status_code=400, detail="For some reason there is no movie")


