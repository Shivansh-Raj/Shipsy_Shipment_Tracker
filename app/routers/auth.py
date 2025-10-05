from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, Token
from app.config import settings

router = APIRouter(tags=["Auth"], prefix="/auth")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token extractor
security = HTTPBearer()

# Helper functions

def hash_password(password: str) -> str:
    return pwd_context.hash(password.strip())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str, expires_minutes: int = 60) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def get_user_from_token(access_token: str, db: Session) -> User:
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    return get_user_from_token(token, db)


# Routes

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pwd = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(db_user.username)
    return {"access_token": access_token, "token_type": "bearer"}
