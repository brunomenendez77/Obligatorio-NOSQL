from typing import List
from fastapi import APIRouter, HTTPException
from app.model import HistorialMedico, RegistroMedico, Paciente
from app.db import pacientes_col, registros_medicos_col, historiales_medicos_col
from bson import ObjectId


router = APIRouter()

def existe_paciente(ci: str) -> bool:
    #busco paciente por ci
    paciente = pacientes_col.find_one({"_id": ci})
    return paciente is not None

# crear registro
@router.post("/registro/")
async def agregar_registro(registro: RegistroMedico, ci: str):
    existe = existe_paciente(ci)
    if not existe:
        raise HTTPException(status_code=402, detail="No existe un paciente con la cédula aportada.")

    registro_data = registro.dict()
    registro_data["_id"] = str(ObjectId())
    #registro_data["ci_paciente"] = ci  

    registros_medicos_col.insert_one(registro_data)

    historial = historiales_medicos_col.find_one({"paciente.ci": ci})

    if historial:
        historiales_medicos_col.update_one(
            {"paciente.ci": ci},
            {"$push": {"registros": registro_data}}
        )
        return {"existe_historial": True, "mensaje": "Registro agregado", "paciente": historial['paciente']}
    else:
        paciente = pacientes_col.find_one({"_id": ci})
        nuevo_historial = {
            "paciente": paciente,
            "registros": [registro_data]
        }
        historiales_medicos_col.insert_one(nuevo_historial)
        return {"existe_historial": False, "mensaje": "Historial Paciente creado", "paciente": nuevo_historial['paciente']}

