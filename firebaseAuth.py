
from fastapi import Request, HTTPException
from firebase_admin import auth

def verify_firebase_token(request: Request):
    """
    Verifies Firebase ID token from Authorization header.
    Returns decoded token if valid.
    """
    id_token = request.headers.get("Authorization")

    if not id_token:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        # Strip "Bearer " if present
        token = id_token.replace("Bearer ", "")
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
