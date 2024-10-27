from fastapi import FastAPI

app = FastAPI()

@app.get('/')

def home():
    return "Hola"

@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"saludo": f"Hola, {nombre}!"}