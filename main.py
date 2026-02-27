from fastapi import FastAPI
import models
from database import engine
from routers import user, projects, tasks

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TODO LIST",
    description="Многопользовательский менеджер задач",
    version='1.0.0'
)

app.include_router(user.router)
app.include_router(projects.router)
app.include_router(tasks.router)
@app.get("/")
def root():
    return {
        "message": "Добро пожаловать в Todo List! Перейдите на /docs для просмотра документации"
    }
