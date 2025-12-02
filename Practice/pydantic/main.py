from pydantic import BaseModel, Field, model_validator, field_validator, EmailStr
from fastapi import FastAPI

#! Тут учить считай нечего. Сперва наперво хочу сказать, что при mode="before" мы обрабатываем модель до того, как она ей стала, то
#! есть мы на прямую работаем со словарём, который поступает в нашу модель. Поэтому здесь мы пишем Values["name_of_attr"]. Когда mode="after" -
#! Мы работаем уже с моделью, поэтому model.name_of_attr
app = FastAPI()


class Cat(BaseModel):
    cat_email: EmailStr
    name: str = Field(min_length=3, max_length=20, description="Cat description", title="model title", examples=["cotMotros"])
    age: int = Field(ge=0, le=20)
    idk: str | None = Field(default=None, max_length=500)
    listss: list[str] = Field(default_factory=list)


    @model_validator(mode="before")
    def validate_model(cls, values):
        if values["name"] == "string":
            raise Exception()
        return values

    @field_validator("name")
    def strip_name(cls, value):
        return value.strip()


    @property
    def find_cat_weight(self):
        return self.age * 20


    model_config = {"extra": "forbid"}


class ChildClass(BaseModel):
    attr_containing_cat: Cat




@app.post("/cat")
async def post_cat(cat: Cat):
    return cat