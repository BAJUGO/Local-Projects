from .routers.movies_router import router as movies_router
from fastapi import FastAPI, Depends
from .dependencies.token_dep import check_admin_token
from .middlewares.general_middleware import log
from .handlers import custom_handlers


app = FastAPI(
    dependencies=[Depends(check_admin_token)]
)

custom_handlers.create_exceptions_handlers(app)


app.include_router(movies_router)

app.middleware("http")(log)