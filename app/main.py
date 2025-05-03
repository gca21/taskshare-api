from fastapi import FastAPI
from app.routers import users
from app import models
from app.database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def root():
    return {"Hello": "World"}