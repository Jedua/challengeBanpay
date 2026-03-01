import os
from dotenv import load_dotenv
from app.db.session import SessionLocal
from app.models.user import User, UserRole 
from app.core.security import get_password_hash

load_dotenv()

def create_super_admin():
    db = SessionLocal()
    try:
        admin_username = os.environ.get("ADMIN_USERNAME")
        admin_email = os.environ.get("ADMIN_EMAIL")
        admin_password = os.environ.get("ADMIN_PASSWORD")
        
        if not all([admin_username, admin_email, admin_password]):
            raise ValueError("Faltan variables de administrador (USERNAME, EMAIL o PASSWORD) en el archivo .env")

        admin_exists = db.query(User).filter(User.username == admin_username).first()
        if admin_exists:
            print(f"El usuario administrador '{admin_username}' ya existe en la base de datos.")
            return

        hashed_pwd = get_password_hash(admin_password)
        admin_user = User(
            username=admin_username,
            email=admin_email,
            role=UserRole.ADMIN, 
            hashed_password=hashed_pwd
        )
        db.add(admin_user)
        db.commit()
        print(f"Usuario administrador '{admin_username}' creado exitosamente de forma segura.")
        
    except Exception as e:
        print(f"Error al crear el administrador: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Inicializando base de datos...")
    create_super_admin()