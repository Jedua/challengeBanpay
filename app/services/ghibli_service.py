import requests
from fastapi import HTTPException, status

BASE_URL = "https://ghibliapi.vercel.app"

def fetch_data_by_role(role: str):
    endpoints = {
        "films": "/films",
        "people": "/people",
        "locations": "/locations",
        "species": "/species",
        "vehicles": "/vehicles"
    }
    
    endpoint = endpoints.get(role)
    if not endpoint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol no valido para consumo de API: {role}"
        )
        
    url = f"{BASE_URL}{endpoint}"
    
    try:
        # El timeout es vital en integraciones
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error al conectar con la API externa de Studio Ghibli"
        )