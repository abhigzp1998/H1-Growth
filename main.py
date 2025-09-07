import os
import json
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # ✅ Import CORS middleware
import firebase_admin
from firebase_admin import credentials
from firebaseAuth import verify_firebase_token

app = FastAPI()

firebase_config = os.getenv("FIREBASE_CONFIG")
if not firebase_config:
    raise RuntimeError("FIREBASE_CONFIG environment variable not set")

cred = credentials.Certificate(json.loads(firebase_config))
firebase_admin.initialize_app(cred)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "statics")
STATIC_DIR2 = os.path.join(BASE_DIR, "statics2")
STATIC_DIR3 = os.path.join(BASE_DIR, "statics3")
MID_ADS=os.path.join(BASE_DIR, "midads")
app.mount("/statics", StaticFiles(directory=STATIC_DIR), name="statics")
app.mount("/statics2", StaticFiles(directory=STATIC_DIR2), name="statics2")
app.mount("/statics3", StaticFiles(directory=STATIC_DIR3), name="statics3")
app.mount("/midsads", StaticFiles(directory=MID_ADS), name="midads")
# Routes
@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

@app.get("/protected")
def protected_route(user_data=Depends(verify_firebase_token)):
    return {"message": "You are authorized", "user": user_data}
