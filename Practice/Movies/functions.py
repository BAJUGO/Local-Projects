from .schemas import MovieCreate
from sqlalchemy.orm import Session
from .model import Movie
from fastapi.exceptions import HTTPException



def get_movies(db: Session):
    return db.query(Movie).all()


def get_movie_by_id(db: Session, movie_id: int):
    movie_by_id = db.query(Movie).get({"id":movie_id})
    if not movie_by_id is None:
        return movie_by_id
    raise HTTPException(status_code=404, detail="movie wasn't found")


def add_movie(db: Session, movie: MovieCreate):
    movie_to_database = Movie(**movie.model_dump())
    db.add(movie_to_database)
    db.commit()
    db.refresh(movie_to_database)
    return movie_to_database


def delete_movie(db: Session, movie_id: int):
    movie_to_delete = db.query(Movie).get({"id":movie_id})
    if not movie_to_delete is None:
        db.delete(movie_to_delete)
        db.commit()
        return {"This movie was deleted:": movie_to_delete}
    raise HTTPException(status_code=404, detail="movie wasn't found")


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


