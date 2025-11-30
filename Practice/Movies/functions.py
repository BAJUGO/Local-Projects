from .schemas import MovieCreate
from sqlalchemy.orm import Session
from .model import Movie
from .custom_exceptions import custom_exc
from fastapi import Response



def get_movies(db: Session):
    return db.query(Movie).all()


def get_movie_by_id(db: Session, movie_id: int):
    movie_by_id = db.query(Movie).get({"id":movie_id})
    if not movie_by_id is None:
        return movie_by_id
    raise custom_exc.no_such_movie()


def add_movie(db: Session, movie: MovieCreate, response: Response):
    movie_to_database = Movie(**movie.model_dump())
    db.add(movie_to_database)
    db.commit()
    db.refresh(movie_to_database)
    response.status_code = 201
    return movie_to_database


def delete_movie(db: Session, movie_id: int):
    movie_to_delete = db.query(Movie).get({"id":movie_id})
    if not movie_to_delete is None:
        db.delete(movie_to_delete)
        db.commit()
        return {"This movie was deleted:": movie_to_delete}
    raise custom_exc.no_such_movie()


def update_movie(db: Session, movie_id: int, movie: MovieCreate):
    movie_to_update = db.query(Movie).get({"id":movie_id})
    if movie_to_update:
        for key, value in movie.model_dump().items():
            setattr(movie_to_update, key, value)
        db.commit()
        db.refresh(movie_to_update)
        return movie_to_update
    else:
        return {"There was no such a movie, so movie created:": add_movie(db, movie)}


def find_movies_by_year(db: Session, year: int):
    movies_by_year = db.query(Movie).filter(Movie.year==year).all()
    if movies_by_year:
        response.status_code=202
        return {f"Movies by {year} year:": movies_by_year}
    return custom_exc.no_such_movie()


def find_movie_by_title(db: Session, find_title: str):
    movie_by_title = db.query(Movie).filter(Movie.title==find_title).all()
    if movie_by_title:
        return movie_by_title
    raise custom_exc.no_such_movie()