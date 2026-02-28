from fastapi import FastAPI
from app.routes import user_routes
from app.db.session import engine, Base

# Esto crea las tablas en la base de datos si no existen
# En un entorno de producción estricto se usaría Alembic, pero para este challenge es suficiente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banpay Challenge API",
    description="API REST de usuarios con integracion a Studio Ghibli",
    version="1.0.1"
)

# Registramos las rutas de usuarios
app.include_router(user_routes.router)

@app.get("/")
def read_root():
    return {"message": "La API esta en linea"}