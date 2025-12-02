from fastapi import APIRouter, Depends


def this_router_dependency(something_from_routered: str):
    if something_from_routered.lower() != "something":
        return "пиздарики"
    return "нормальный самсинг"



router = APIRouter(
    prefix="/aditional_users_router",
    dependencies=[Depends(this_router_dependency)],
    tags=["Additional_Users"]
)


@router.get("/")
async def return_anything():
    return "additional user"