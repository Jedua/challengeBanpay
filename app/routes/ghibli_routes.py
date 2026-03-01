from fastapi import APIRouter, Depends
from typing import Any, List, Dict
from app.core.security import get_current_user
from app.services import ghibli_service
from app.models.user import User

router = APIRouter(prefix="/ghibli", tags=["Studio Ghibli"])

@router.get("/")
def get_ghibli_content(current_user: User = Depends(get_current_user)):
    # Usamos directamente el rol del usuario que el token identifico
    return ghibli_service.fetch_data_by_role(current_user.role.value)