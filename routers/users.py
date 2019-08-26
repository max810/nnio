import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import jwt
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from pydantic import BaseModel
import starlette.status as status

from DAL import schemas, users_repository, models
from routers.common import SECRET_KEY, ALGORITHM, oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES, templates

router = APIRouter()


def get_db(request: Request):
    return request.state.db


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


def authenticate_user(db: Session, email: str, password: str):
    user: models.User = users_repository.get_user_by_email(db, email)
    if not user:
        return False

    if user.hashed_password != password:
        return False

    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except PyJWTError as e:
        logging.info("JWT TOKEN LOGIN FAILED: " + str(e))
        raise credentials_exception

    user = users_repository.get_user_by_email(db, token_data.username)

    if user is None:
        raise credentials_exception

    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/test_token", response_model=str)
async def test_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        user = await get_current_user(db, token)
    except HTTPException:
        logging.info("JWT TOKEN INVALID")
        raise

    return user.email


@router.get("/admin")
def get_admin_template(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@router.get("/login_page")
def get_admin_page(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})


@router.get("/admin_page")
def get_admin_page(request: Request, token: str = Depends(oauth2_scheme)):
    return templates.TemplateResponse('admin.html',
                                      {"request": request, "layer_schemas": get_layers_schemas(request, token)})


@router.get("/layers_schemas")
def get_layers_schemas(token: str = Depends(oauth2_scheme)):
    p_layer_schemas = Path('BLL/layer_schemas')
    layer_schemas = {}
    for p_schema in p_layer_schemas.glob("*.json"):
        schema = json.load(open(p_schema))
        layer_schemas[p_schema.stem] = schema

    # TODO - don't deserialize JSON, just combine strings and return
    return layer_schemas


@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = users_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    return users_repository.create_user(db=db, user=user)
