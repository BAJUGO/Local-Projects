from fastapi import FastAPI
from .middleware import log_middleware_a, log_middleware_b
from ..Routers.users_router import router as user_router

app = FastAPI()


app.include_router(user_router)

app.middleware("http")(log_middleware_a)


app.middleware("http")(log_middleware_b)