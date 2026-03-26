from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.modules.auth.presentation.schemas import LoginRequest, Token, UserResponse
from app.modules.auth.services.auth_service import authenticate_user, create_token_for_user, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: LoginRequest) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_token_for_user(user)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def read_users_me(token: str = Depends(oauth2_scheme)) -> UserResponse:
    user = get_current_user(token)
    return UserResponse(username=user.username, full_name=user.full_name, email=user.email)
