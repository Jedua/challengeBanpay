from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import User, UserCreate, UserUpdate, UserUpdateMe
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
    Crea un nuevo usuario con privilegios de administrador.
    
    Este endpoint esta estrictamente protegido. Solo un usuario que ya posea el rol 
    de 'admin' y proporcione un token valido puede ejecutar esta accion.
    """
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
        
    user.role = "admin" 
    
    return user_service.create_user(db=db, user=user)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario estandar en el sistema.
    
    Ruta publica. Permite la creacion de usuarios con roles convencionales 
    (films, people, locations, species, vehicles). Por seguridad, si se intenta 
    enviar el rol 'admin', la peticion sera rechazada.
    """
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
    """
    Obtiene la lista completa de todos los usuarios registrados.
    
    Endpoint protegido. Requiere autenticacion con rol de 'admin'.
    """
    return user_service.get_users(db)

@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user)
):
    """
    Obtiene los detalles de un usuario especifico mediante su ID.
    
    Endpoint protegido. Requiere autenticacion con rol de 'admin'.
    """
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/me", response_model=User)
def update_own_profile(
    user_in: UserUpdateMe,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza el perfil del usuario autenticado.
    
    Permite a cualquier usuario modificar su propio nombre de usuario, correo o contrasena.
    No permite modificar el rol
    """
    return user_service.update_own_profile(db=db, current_user=current_user, user_in=user_in)

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user) 
):
    """
    Actualiza la informacion de cualquier usuario en el sistema.
    
    Endpoint protegido. Requiere autenticacion con rol de 'admin'.
    Permite la modificacion de todos los campos, incluyendo el rol del usuario.
    """
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
    """
    Elimina a un usuario del sistema de forma permanente.
    
    Endpoint protegido. Requiere autenticacion con rol de 'admin'.
    """
    db_user = user_service.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_service.delete_user(db, db_user=db_user)
    return {"message": "Usuario eliminado exitosamente"}