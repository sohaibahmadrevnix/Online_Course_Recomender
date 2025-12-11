from fastapi import APIRouter, Depends
from app.db.schemas.user_schema import UserOut
from app.dep.dependencies import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_me(current_user = Depends(get_current_user)):
    return current_user
