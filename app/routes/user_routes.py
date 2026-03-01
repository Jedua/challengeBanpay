from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.services import user_service
# Importamos ambas dependencias
from app.core.security import get_current_user, get_admin_user 

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/admin", response_model=User, status_code=status.HTTP_201_CREATED)
def create_admin_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user) 
):
    """
    Endpoint exclusivo para que un Administrador cree a otros Administradores.
    """
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
        
    user.role = "admin" 
    
    return user_service.create_user(db=db, user=user)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if user.role.value == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear un usuario administrador por esta via."
        )

    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
    return user_service.create_user(db=db, user=user)

@router.get("/", response_model=list[User])
def read_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user) 
):
    return user_service.get_users(db)

@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user) 
):
    db_user = user_service.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_service.update_user(db, db_user=db_user, user_update=user_update)

@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user) 
):
    db_user = user_service.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_service.delete_user(db, db_user=db_user)
    return {"message": "Usuario eliminado exitosamente"}