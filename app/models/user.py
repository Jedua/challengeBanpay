from sqlalchemy import Column, Integer, String, Enum
import enum
from app.db.session import Base

# Definición de Roles para el challenge
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    FILMS = "films"
    PEOPLE = "people"
    LOCATIONS = "locations"
    SPECIES = "species"
    VEHICLES = "vehicles"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PEOPLE, nullable=False)