from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

import uvicorn

from configs import *
from routers import architecture_exporting, architecture_sharing, users, admin

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
