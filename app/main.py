from fastapi import FastAPI
from app.routes import user_routes, ghibli_routes, auth_routes
from app.db.session import engine, Base

app = FastAPI(
    title="Banpay Challenge API",
    description="API REST de usuarios con integracion a Studio Ghibli",
    version="1.0.1"
)

# Registramos las rutas
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(ghibli_routes.router)

@app.get("/")
def read_root():
    return {"message": "La API esta en linea"}