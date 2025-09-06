import os
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials

# Import token verifier
from firebaseAuth import verify_firebase_token

# 🔐 Initialize Firebase once
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "statics")

app.mount("/statics", StaticFiles(directory=STATIC_DIR), name="statics")

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}
@app.get("/protected")
def protected_route(user_data=Depends(verify_firebase_token)):
    return {"message": "You are authorized", "user": user_data}