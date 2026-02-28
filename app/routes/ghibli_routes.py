from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List, Dict

from app.db.session import get_db
from app.services import user_service, ghibli_service

router = APIRouter(
    prefix="/ghibli",
    tags=["Studio Ghibli"]
)

@router.get("/", response_model=List[Dict[str, Any]])
def get_ghibli_content(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el contenido de Studio Ghibli basado en el rol del usuario proporcionado.
    En una aplicacion con autenticacion JWT, el user_id se extraeria del token.
    """
    user = user_service.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado. Se requiere un usuario valido."
        )
    
    # user.role es un Enum
    return ghibli_service.fetch_data_by_role(user.role.value)