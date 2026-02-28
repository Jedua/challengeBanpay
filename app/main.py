from fastapi import FastAPI

app = FastAPI(title="Banpay Challenge API")

@app.get("/")
def read_root():
    return {"message": "API is running"}