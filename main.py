import os
import json
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

# Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials
from firebaseAuth import verify_firebase_token

app = FastAPI()

# 🔐 Initialize Firebase from environment variable
firebase_config = os.getenv("FIREBASE_CONFIG")
if not firebase_config:
    raise RuntimeError("FIREBASE_CONFIG environment variable not set")

cred = credentials.Certificate(json.loads(firebase_config))
firebase_admin.initialize_app(cred)

# Static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "statics")
app.mount("/statics", StaticFiles(directory=STATIC_DIR), name="statics")

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

@app.get("/protected")
def protected_route(user_data=Depends(verify_firebase_token)):
    return {"message": "You are authorized", "user": user_data}
