from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from backend.models.database import get_db
from backend.models.user import User
from backend.schemas.user import UserCreate, UserResponse
from backend.middleware.auth import create_access_token, pwd_context, verify_token
from backend.logger import get_logger

router  = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger  = get_logger("auth")

@router.post("/register", response_model=UserResponse)
@limiter.limit("5/minute")
def register(request: Request, payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        username        = payload.username,
        email           = payload.email,
        hashed_password = pwd_context.hash(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"New user registered: {user.username}")
    return user

@router.post("/token")
@limiter.limit("10/minute")
def login(
    request  : Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db       : Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")
    token = create_access_token({"sub": user.username, "user_id": str(user.id)})
    logger.info(f"User logged in: {user.username}")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    user = db.query(User).filter(User.username == token.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user