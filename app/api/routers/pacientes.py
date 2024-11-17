from fastapi import APIRouter, status, Response
from app.db import pacientes_col
from app.model import Paciente
from typing import List
from app.enum import TipoSexo

router = APIRouter(
    prefix="/pacientes"
)

@router.get("/", response_model=List[Paciente])
def getPacientes():
    pacientes : List[Paciente] = []
    for item in pacientes_col.find():
        pacientes.append(Paciente(
            _id = str(item["_id"]),
            nombre = item["nombre"],
            apellido = item["apellido"],
            fecha_nacimiento = item["fecha_nacimiento"],
            sexo = TipoSexo[item["sexo"]]
        ))
    return pacientes

@router.post("/", status_code=status.HTTP_201_CREATED)
def addPaciente(paciente: Paciente, response: Response):
    paciente_dict = paciente.model_dump()
    paciente_dict["_id"] = paciente_dict.pop("ci")
    try:
        pacientes_col.insert_one(paciente_dict)
        return {"mensaje": "Paciente registrado con exito"}
    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "El paciente ya existe"}