from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from ..middleware.auth import create_access_token, pwd_context

router = APIRouter()

DEMO_USER = {
    "username": "admin",
    "hashed_password": pwd_context.hash("admin123")
}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != DEMO_USER["username"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(form_data.password, DEMO_USER["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}