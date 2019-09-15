import os

from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.templating import Jinja2Templates

SECRET_KEY = os.environ['JWT_SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # what is `tokenUrl` for?
templates = Jinja2Templates(directory="nnio-admin/dist")


def get_db(request: Request):
    return request.state.db
