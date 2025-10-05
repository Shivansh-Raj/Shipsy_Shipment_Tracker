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

router = APIRouter(prefix="/auth", tags=["Authentication"])

#Password Hashing
pwd_handler = CryptContext(schemes=["bcrypt"], deprecated="auto")

# extracts access token
auth_scheme = HTTPBearer()


# Helper functions
def hash_user_password(password: str) -> str:
    """Return a hashed version of the user's password"""
    return pwd_handler.hash(password.strip())


def verify_user_password(plain: str, hashed: str) -> bool:
    """Check if the plain password matches the hashed password"""
    return pwd_handler.verify(plain, hashed)


def generate_access_token(username: str, expires_minutes: int = 60) -> str:
    """Create a JWT access token for the given username"""
    expiry = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": username, "exp": expiry}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def fetch_user_from_token(token: str, db: Session) -> User:
    """Decode JWT and return the associated user from DB"""
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = decoded.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_authenticated_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
                           db: Session = Depends(get_db)) -> User:
    jwt_token = credentials.credentials
    return fetch_user_from_token(jwt_token, db)


# API Endpoints
@router.post("/register", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with hashed password"""
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    hashed = hash_user_password(user.password)
    new_user = User(username=user.username, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token"""
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_user_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = generate_access_token(db_user.username)
    return {"access_token": token, "token_type": "bearer"}
