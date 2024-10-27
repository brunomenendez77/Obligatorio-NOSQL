from fastapi import FastAPI
from app.api.routers.pacientes import router as router_pacientes
from app.api.routers.registros import router as router_registros

app = FastAPI()

app.include_router(router_pacientes)
app.include_router(router_registros)

@app.get("/")
def root():
    return "Plataforma de gestion de historial medico"