from fastapi import APIRouter, Depends
from ..schemas import MovieCreate
from ..db import get_db
from sqlalchemy.orm import Session
from .. import functions





router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/")
async def read_movies(db: Session = Depends(get_db)):
    return functions.get_movies(db)


@router.post("/")
async def add_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return functions.add_movie(db, movie)


