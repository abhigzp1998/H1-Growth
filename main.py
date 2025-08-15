import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "statics")

app.mount("/statics", StaticFiles(directory=STATIC_DIR), name="statics")

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}
