from fastapi import FastAPI
from app.routers import users, tasks
from app import models
from app.database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"Hello": "World"}