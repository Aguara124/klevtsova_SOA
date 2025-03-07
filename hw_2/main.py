from user_service import router as user_router
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Проект Клевцовой Снежаны 221"}

app.include_router(user_router)

client = TestClient(app)
