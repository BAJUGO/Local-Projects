from fastapi import APIRouter, Depends
from ..schemas import MovieCreate
from ..db import get_db
from sqlalchemy.orm import Session
import Practice.Movies.functions as functions
from fastapi.exceptions import HTTPException




app = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@app.get("/")
async def read_movies(db: Session = Depends(get_db)):
    functions.get_movies(db)


@app.post("/")
async def add_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    movie_created = functions.add_movie(db, movie)
    if movie_created:
        return {"message": "movie_created"}
    raise HTTPException(status_code=400, detail="something went wrong")