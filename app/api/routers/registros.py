from fastapi import APIRouter, HTTPException, Query
from app.model import HistorialMedico, RegistroMedico, Paciente, TipoRegistro
from app.db import pacientes_col, registros_medicos_col, historiales_medicos_col
from bson import ObjectId
from typing import List, Dict, Any, Optional

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

    registro_data = registro.model_dump()
    registro_data["_id"] = str(ObjectId())  
    #agrego registro
    registros_medicos_col.insert_one(registro_data)

    #si no hay historial lo creo, si hay solo agrego el registro
    historial = historiales_medicos_col.find_one({"paciente.ci": ci})
    
    if historial:
    # si existe el historial para el paciente le agrego el registro
        historiales_medicos_col.update_one(
            {"paciente.ci": ci},
            {"$push": {"registros": { "$each": [registro.model_dump()], "$position": 0}}}
        )
        return {"existe historial": True, "mensaje": "Registro agregado", "paciente": historial['paciente']}
    else: # si no existe el historial para el paciente lo creo y asigno el registro
        paciente = pacientes_col.find_one({"_id": ci})
        nuevo_historial = HistorialMedico(paciente=paciente, registros=[registro_data])
        historiales_medicos_col.insert_one(nuevo_historial.model_dump())
        return {"existe historial": False, "mensaje": "Historial Paciente creado", "paciente": nuevo_historial.paciente}


#consultar historial de paciente
@router.get("/historial/{ci}", response_model=HistorialMedico)
async def obtener_historial(ci: str, paginado: bool = False, pagina: int = 1, paginaLimit: int = 5):
    # Buscar el historial médico en la base de datos
    historial_data: dict = historiales_medicos_col.find_one({"paciente.ci": ci})
    if not historial_data:
        raise HTTPException(status_code=402, detail="No existe un paciente con la cédula aportada o no tiene historial.")
    registrosPaginados = []
    siguiente = None
    previo = None
    hayPaginaSiguiente = False
    if paginado:
        reg = 0
        pag = 1
        for registro in historial_data.get("registros", []):
            reg += 1
            if reg > paginaLimit:
                reg = 0
                pag += 1
                if pag > pagina:
                    hayPaginaSiguiente = True
                    break
            else:
                if pag == pagina:
                    registrosPaginados.append(registro)
        siguiente = "http://localhost:8000/historial/" + ci + "?paginado=True&paginaLimit=" + str(paginaLimit) + "&pagina=" + str(pagina + 1) if hayPaginaSiguiente else None
        previo = ("http://localhost:8000/historial/" + ci + "?paginado=True&paginaLimit=" + str(paginaLimit) + "&pagina=" + str(pagina - 1)) if pagina != 1 else None
            

    # Convertir los datos a objetos HistorialMedico
    historial = HistorialMedico(
        paciente = Paciente(**{**historial_data["paciente"], "_id": historial_data["paciente"]["ci"]}),
        registros = [RegistroMedico(**registro) for registro in (historial_data.get("registros", []) if not paginado else registrosPaginados)],
        siguiente = siguiente,
        previo = previo
    )

    
    return historial


#consulta por criterio
@router.get("/registros/", response_model=List[RegistroMedico])
async def obtener_registros_por_criterios(
    tipo: Optional[TipoRegistro] = Query(None, description="Tipo de registro (consulta, examen, internacion)"),
    diagnostico: Optional[str] = Query(None, description="Diagnóstico del registro"),
    medico: Optional[str] = Query(None, description="Nombre del médico"),
    institucion: Optional[str] = Query(None, description="Nombre de la institución")
):
    filtros = {}

    #filtros
    if tipo:
        filtros["tipo"] = tipo
    if diagnostico:
        filtros["diagnostico"] = diagnostico
    if medico:
        filtros["medico"] = medico
    if institucion:
        filtros["institucion"] = institucion

    resultados = list(registros_medicos_col.find(filtros))

    if not resultados:
        raise HTTPException(status_code=402, detail="No se encontraron registros con los criterios especificados")

    return resultados