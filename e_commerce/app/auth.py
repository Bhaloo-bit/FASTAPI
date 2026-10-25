"""auth.py - JWT auth + password hashing for the e-commerce API (FastAPI + SQLModel).

Install: pip install "python-jose[cryptography]" "passlib[bcrypt]" "bcrypt==4.0.1" python-multipart
Set SECRET_KEY in env (generate: openssl rand -hex 32).
"""
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select

# Adjust these imports to your project layout
from database import get_session   # yields a Session
from models import User            # needs: id, email, hashed_password, is_active

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterIn(BaseModel):
    email: str
    password: str


# ---------- helpers ----------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# ---------- dependencies ----------
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise credentials_error

    user = session.get(User, user_id)
    if not user or not user.is_active:
        raise credentials_error
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


# ---------- routes ----------
@router.post("/register", status_code=201)
def register(data: RegisterIn, session: Annotated[Session, Depends(get_session)]):
    if session.exec(select(User).where(User.email == data.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "email": user.email}


@router.post("/login", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
):
    user = authenticate_user(session, form.username, form.password)  # username = email
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return Token(access_token=create_access_token(user.id))


@router.get("/me")
def me(user: CurrentUser):
    return {"id": user.id, "email": user.email}