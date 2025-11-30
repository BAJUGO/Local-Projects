from pydantic import BaseModel, Field


class MoviePost(BaseModel):
    title: str
    director: str
    description: str
    year: int = Field(ge=1900, le=2025)


class MovieCreate(MoviePost):
    pass


class Movie(MoviePost):
    id: int

    class Config:
        from_attribute = True



class SeriesPost(BaseModel):
    title: str
    seasons: int
    episodes: int
    description: str
    year: int


class SeriesCreate(SeriesPost):
    pass


class Series(SeriesCreate):
    id: int

    class Config:
        from_attribute=True