from typing import List
from decimal import Decimal

from fastapi import FastAPI, HTTPException, Query, Body, Depends

from .auth.model import UserLoginSchema
from .auth.auth_handler import signJWT, USER
from .auth.auth_bearer import JWTBearer


app = FastAPI(
    title='JWT-Api',
    description='Uma API implementada com FastAPI, que possui autenticação JWT.',
    redoc_url=None
)


users = [USER]


def check_user(data: UserLoginSchema):
    for user in users:
        if user['email'] == data.email and user['password'] == data.password:
            return True
    return False


@app.post('/user/login', tags=['user'])
async def user_login(user: UserLoginSchema = Body(...)):
    '''
    Verifica credenciais do usuário e retorna um token JWT para autorizar rotas protegidas caso
    o usuário esteja autorizado a usar a API.
    '''
    if check_user(user):
        return signJWT(user.email)
    raise HTTPException(
        status_code=403,
        detail='Email ou senha incorretos.'
    )

