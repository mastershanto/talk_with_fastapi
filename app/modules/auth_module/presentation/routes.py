from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db, Base, engine
from app.core.security import get_password_hash, verify_password, create_access_token
from app.modules.auth_module.data.repository import SQLAlchemyUserRepository
from app.modules.auth_module.data.models import UserDB
from app.modules.auth_module.presentation import schemas
from app.modules.auth_module.domain.models import User

router = APIRouter()

Base.metadata.create_all(bind=engine)


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    repo = SQLAlchemyUserRepository(db)
    user = repo.get_by_username(username)
    if not user:
        return None
    user_db = db.query(UserDB).filter(UserDB.username == username).first()
    if not user_db or not verify_password(password, user_db.hashed_password):
        return None
    return user


@router.post('/register', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    existing = repo.get_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already registered')
    user = repo.create(payload.username, payload.email, get_password_hash(payload.password))
    return user


@router.post('/token', response_model=schemas.Token)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password', headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expires_minutes)
    access_token = create_access_token({'sub': str(user.id), 'username': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
