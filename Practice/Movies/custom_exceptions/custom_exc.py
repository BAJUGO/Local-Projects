from fastapi.exceptions import HTTPException

no_such_movie = HTTPException(status_code=404, detail="There is no something you are looking for", headers={"just_check":"if_it_works"})
not_enough_rights = HTTPException(status_code=403, detail="You have not enough rights")



