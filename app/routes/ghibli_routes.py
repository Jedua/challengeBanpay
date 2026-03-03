from fastapi import APIRouter, Depends
from typing import Any

from app.core.security import get_current_user
from app.models.user import User
from app.services import ghibli_service

router = APIRouter(prefix="/ghibli", tags=["Studio Ghibli"])

@router.get("/")
def get_ghibli_content(current_user: User = Depends(get_current_user)) -> Any:
    """
    Consulta la API externa de Studio Ghibli basada en el rol del usuario.
    """
    return ghibli_service.get_ghibli_data(role=current_user.role.value)