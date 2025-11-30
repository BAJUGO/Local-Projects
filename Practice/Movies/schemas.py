from pydantic import BaseModel, Field, model_validator
from .custom_exceptions import custom_exc


class MoviePost(BaseModel):
    title: str
    director: str
    description: str
    year: int = Field(ge=1900, le=2025)


class MovieCreate(MoviePost):
    @model_validator(mode="after")
    def check_values(self):
        if self.title == "string":
            raise custom_exc.ModelValueError(reason="Title of the movie can't be 'string'")
        if self.description == "string":
            self.description = "None"
        if self.director == "string":
            self.director = "Anonym"
        return self


class Movie(MoviePost):
    id: int

    class Config:
        from_attribute = True
