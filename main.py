from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt
from typing import List, Optional
from users_db import USERS_DB

app = FastAPI()

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"

# ---------------- MODELE ----------------

class LoginData(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    roles: Optional[List[str]] = []

# ---------------- FUNKCJE ----------------

def create_token(username: str, roles: List[str]):
    payload = {
        "sub": username,
        "roles": roles,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(auth_header: str = Header(...)):
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(payload, role: str):
    if role not in payload.get("roles", []):
        raise HTTPException(status_code=403, detail="Forbidden")

# ---------------- ENDPOINTY ----------------

@app.post("/login")
def login(data: LoginData):
    user = USERS_DB.get(data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(data.password.encode('utf-8'), user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(data.username, user["roles"])
    return {"access_token": token, "token_type": "bearer"}

@app.post("/users")
def create_user(user: UserCreate, payload=Depends(verify_token)):
    require_role(payload, "ROLE_ADMIN")

    if user.username in USERS_DB:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    USERS_DB[user.username] = {
        "password": hashed_pw,
        "roles": user.roles
    }
    return {"msg": f"User {user.username} created."}

@app.get("/user_details")
def user_details(payload=Depends(verify_token)):
    return {
        "username": payload["sub"],
        "roles": payload.get("roles", [])
    }
