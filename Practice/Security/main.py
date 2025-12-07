from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext



#         [System.BitConverter]::ToString((1..32 | ForEach-Object {Get-Random -Maximum 256} )).Replace("-", "").ToLower()
SECRET_KEY = "c72a89506e11e3c08b0ccc0ca96f8519bff68cb168a687d7841c4340a3a6b22b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") #! Эта зависимость проверяет header - Authorization
#! Если он выглядит примерно Authorization: Bearer {token} - то она вернёт token, так как это ну, зависимость



class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attribute = True


class UserCreate(BaseModel):
    password: str
    username: str
    role: Optional[str] = "user"


class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[str] = None


#! ФУНКЦИИ ДЛЯ АУТЕНТИФИКАЦИИ + БД

my_hasher = CryptContext(["sha256_crypt"])

fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": my_hasher.hash("secret1"),
        "role": "admin",
        "id": 1
    },
    "bob": {
        "username": "bob",
        "hashed_password": my_hasher.hash("secret2"),
        "role": "user",
        "id": 2
    }
}

def verify_password(password, hashed_password):
    return my_hasher.verify(password, hashed_password)


def get_user(username):
    user = fake_users_db.get(username)
    if not user is None:
        return user
    return None


def authenticate_user(username, password):
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user



#! СОЗДАТЬ ИЛИ РАЗДЕКОДИТЬ ТОКЕН
def create_access_token(data: dict, expires_time: Optional[timedelta] = None):
    data_to_update = data.copy()
    if expires_time:
        expire = datetime.now() + expires_time
    else:
        expire = datetime.now() + ACCESS_TOKEN_EXPIRE_MINUTES
    data_to_update["exp"] = expire
    jwt_token = jwt.encode(data_to_update, SECRET_KEY, ALGORITHM)
    return jwt_token


def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        user_id = payload.get('id')
        role = payload.get('role')
        if role is None or user_id is None:
            raise HTTPException(status_code=403, detail="Token error")
        return TokenData(id=user_id, role=role)
    except JWTError:
        raise HTTPException(status_code=403, detail="Token error")


#!DEPENDENCIES
#* Мы получаем из этой зависимости token, так как oauth2_scheme ищет header Authorization: Bearer {token}, и возвращает этот token
def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_access_token(token) #Возвращаем объект класса TokenData


def required_role(role: str):
    def current_user(current_user_token: TokenData = Depends(get_current_user)):
        if current_user_token.role == role:
            return current_user_token
        raise HTTPException(status_code=403, detail="Not enough rights")
    return current_user




#!ENDPOINTS
app = FastAPI()

@app.get("/everyone")
async def for_everyone():
    return {"msg": "this end is for everyone!"}


@app.get("/auth_user")
async def for_users(current_user: TokenData = Depends(get_current_user)):
    return {"msg": f"hello user {current_user.id}. Your role is {current_user.role}"}


@app.get("/admin_only")
async def for_admin(current_user: TokenData = Depends(required_role("admin"))):
    return {"msg": f"Hello admin {current_user.id}"}




from fastapi import Form

#! Запрос на tokenUrl должен возвращать сам access_token в хэдере access_token + тип токена (bearer)
@app.post("/token")
async def post_token(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="there was no such user")
    access_token = create_access_token(user, timedelta(minutes=5))
    return {"access_token": access_token, "token_type": "bearer"}