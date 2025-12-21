from datetime import datetime, timedelta
from app.models.user import User
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, TypeVar
from pydantic import BaseModel
import bcrypt
import time

from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import Session, sessionmaker
from app.database.config import Config

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1500"))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não configurado no ambiente")
if not ALGORITHM:
    raise RuntimeError("ALGORITHM não configurado no ambiente")
security = HTTPBearer()
# Optional bearer (does not auto error if header missing)
bearer_optional = HTTPBearer(auto_error=False)
DATABASE_URL = Config.DATABASE_URL

# Shared HTTP Bearer scheme (no OAuth2 flow)
from app.middleware.security import http_bearer

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    # RFC: `sub` deve ser string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"]) if to_encode["sub"] is not None else None
    if expires_delta:
        expire_dt = datetime.utcnow() + expires_delta
    else:
        expire_dt = datetime.utcnow() + timedelta(minutes=1500)
    # NumericDate (segundos desde epoch)
    to_encode["exp"] = int(expire_dt.timestamp())
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login(data):
    identifier = data.get('identifier')
    password = data.get('password')

    if not identifier or not password:
        raise HTTPException(status_code=400, detail="Identifier and password are required")

    identifier = identifier.strip()
    
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(User).filter(User.is_active == True)
    # Heurística: se parecer email, busca por email (case-insensitive), senão por username
    looks_like_email = '@' in identifier
    if looks_like_email:
        user = query.filter(func.lower(User.email) == identifier.lower()).first()
    else:
        user = query.filter(User.username == identifier).first()

    if not user:
        session.close()
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(password, user.hashed_password):
        session.close()
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # preferir ID numérico no token
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    session.close()
    return {"access_token": access_token, "token_type": "bearer"}

def decode_jwt(token: str) -> dict:
    try:
        # jose validates exp automatically; returns payload if valid
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except Exception:
        return {}
    
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # garante que seja int (alguns tokens antigos podem ter 'sub' como string)
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise credentials_exception
        # Aqui você pode buscar mais dados no banco se quiser
        return {"id": user_id}
    except JWTError:
        raise credentials_exception
    

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_optional),
    token: Optional[str] = None,
):
    provided_token: Optional[str] = None
    if credentials and getattr(credentials, "credentials", None):
        provided_token = credentials.credentials
    elif token:
        provided_token = token

    if not provided_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não fornecido",
        )

    payload = decode_jwt(provided_token)
    if not payload or not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )
    return payload
