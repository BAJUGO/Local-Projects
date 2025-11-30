from .routers.movies_router import router as movies_router
from fastapi import FastAPI, Depends
from .dependencies.token_dep import check_admin_token


app = FastAPI(
    dependencies=[Depends(check_admin_token)]
)


app.include_router(movies_router)
