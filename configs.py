import logging
import os

import DAL

from DAL import db_models
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, Session

origins = [
    "http://localhost:8080",
    'https://nnio-project-frontend.herokuapp.com',
    'https://nnio-project-frontend.herokuapp.com/',
    "https://max810.github.io"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)

SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DAL.db_models.Base.metadata.create_all(bind=engine)
