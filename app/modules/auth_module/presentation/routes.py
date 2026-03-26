from fastapi import APIRouter
from app.modules.auth_module.presentation.schemas import Token

router = APIRouter()

@router.post('/token', response_model=Token)
def token():
    return {'access_token': 'fake', 'token_type': 'bearer'}
