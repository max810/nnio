import os

from fastapi.security import OAuth2PasswordBearer
from starlette.templating import Jinja2Templates

SECRET_KEY = os.environ['JWT_SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # what is `tokenUrl` for?

templates = Jinja2Templates(directory="templates")
