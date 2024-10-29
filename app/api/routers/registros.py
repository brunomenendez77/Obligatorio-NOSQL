from fastapi import APIRouter, HTTPException, Query
from app.model import HistorialMedico, RegistroMedico, Paciente
from app.db import pacientes_col, registros_medicos_col, historiales_medicos_col
from bson import ObjectId
from typing import List, Dict, Any

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
    #agrego registro
    registros_medicos_col.insert_one(registro_data)

    #si no hay historial lo creo, si hay solo agrego el registro
    historial = historiales_medicos_col.find_one({"paciente.ci": ci})
    
    if historial:
    # si existe el historial para el paciente le agrego el registro
        historiales_medicos_col.update_one(
            {"paciente.ci": ci},
            {"$push": {"registros": registro.dict()}}
        )
        return {"existe historial": True, "mensaje": "Registro agregado", "paciente": historial['paciente']}
    else: # si no existe el historial para el paciente lo creo y asigno el registro
        paciente = pacientes_col.find_one({"_id": ci})
        nuevo_historial = HistorialMedico(paciente=paciente, registros=[registro_data])
        historiales_medicos_col.insert_one(nuevo_historial.dict())
        return {"existe historial": False, "mensaje": "Historial Paciente creado", "paciente": nuevo_historial.paciente}


#consultar historial de paciente
