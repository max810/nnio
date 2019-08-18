import logging
import os

from starlette.requests import Request
from starlette.responses import Response

import DAL
import uvicorn
from fastapi import FastAPI

from DAL import models
from routers import architecture_exporting, users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(message)s",
)

app = FastAPI()
app.include_router(
    architecture_exporting.router,
    prefix='/architecture',
    tags=['Neural network architecture exporting to code']
)

app.include_router(
    users.router,
    prefix='/user',
    tags=['User authentication and authorization']
)

SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL ']
# SQLALCHEMY_DATABASE_URL = "postgres+psycopg2://{}:{}@localhost:5432/nnio".format(
#     os.environ['NNIO_DB_USERNAME'],
#     os.environ['NNIO_DB_PASSWORD'],
# )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DAL.models.Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()

    return response


if __name__ == "__main__":
    sess: Session = SessionLocal()
    logging.info("About to create a user")
    user = sess.query(models.User).filter(models.User.email == 'admin@gmail.com').first()
    if not user:
        user = models.User(email='admin@gmail.com', hashed_password=os.environ['DB_ADMIN_DEFAULT_PASSWORD'])
        sess.add(user)
        sess.commit()
        sess.refresh(user)
    else:
        logging.info("EXISTS")
    logging.info(user.id)
    uvicorn.run(app, host="0.0.0.0", port=8000)

# TODO:
#  1) add beautifier after generating code
#  2) Add admin page to maintain supported layers and their params
#  3) DTYPE WILL NOT BE IN THE MODEL(check for dtype - it should be the same for all layer or not given at all)
