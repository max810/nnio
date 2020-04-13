import logging
import os

from starlette.requests import Request
from starlette.responses import Response

import DAL
import uvicorn
from fastapi import FastAPI

from DAL import db_models
from routers import architecture_exporting, users, admin, architecture_sharing
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, Session
from starlette.middleware.cors import CORSMiddleware

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

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origin_regex=".*://localhost:.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    architecture_exporting.router,
    prefix='/architecture',
    tags=['Neural network architecture exporting to code']
)

app.include_router(
    architecture_sharing.router,
    prefix='/sharing',
    tags=['Storing created architectures on the server']
)

app.include_router(
    users.router,
    prefix='/user',
    tags=['User authentication and authorization']
)

app.include_router(
    admin.router,
    prefix='/admin',
    tags=['Layers schema editing']
)

SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DAL.db_models.Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error_message", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()

    return response


if __name__ == "__main__":
    sess: Session = SessionLocal()

    logging.info("About to create a user")
    user = sess.query(db_models.User).filter(db_models.User.email == 'admin@gmail.com').first()
    if not user:
        user = db_models.User(email='admin@gmail.com', hashed_password=os.environ['DB_ADMIN_DEFAULT_PASSWORD'])
        sess.add(user)
        sess.commit()
        sess.refresh(user)
    else:
        logging.info("EXISTS")
    logging.info(user.id)
    uvicorn.run(app, host="0.0.0.0", port=8000)

# TODO:
#  1) ? add Python beautifier after generating code
#  --DTYPE WILL NOT BE IN THE MODEL(check for dtype - it should be the same for all layer or not given at all)
