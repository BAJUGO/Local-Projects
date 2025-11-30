from fastapi import APIRouter, Depends
from ..schemas import MovieCreate
from ..db import get_db
from sqlalchemy.orm import Session
from .. import functions



db_dep: Session = Depends(get_db)
type_of_db = "Movie"


router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/")
async def read_movies(db=db_dep):
    return functions.get_movies(db)


@router.get("/{movie_id}")
async def get_movie_by_id(movie_id: int, db=db_dep):
    return functions.get_movie_by_id(db, movie_id)



@router.post("/")
async def add_movie(movie: MovieCreate, db=db_dep):
    return functions.add_movie(db, movie)


@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, db=db_dep):
    return functions.delete_movie(db, movie_id)


@router.put("/{movie_id}")
async def update_movie(movie_id: int, movie: MovieCreate, db=db_dep):
    return functions.update_movie(db, movie_id, movie)


@router.get("/{year}")
async def movies_by_year(year:int, db=db_dep):
    return functions.find_movies_by_year(db, year)