from .routers.movies_router import router as movies_router
from .routers.ultra_services import router as ultra_router
from fastapi import FastAPI
from .middlewares.general_middleware import log
from .handlers import custom_handlers


app = FastAPI()

custom_handlers.create_exceptions_handlers(app)


app.include_router(movies_router)
app.include_router(ultra_router)

app.middleware("http")(log)