from pydantic import BaseModel, Field
from app.enum import TipoSexo, TipoRegistro
from typing import List, Optional

class Paciente(BaseModel):
    ci: str = Field(..., alias="_id")
    nombre: str
    apellido: str
    fecha_nacimiento: str
    sexo: TipoSexo

class RegistroMedico(BaseModel):
    fecha: str
    tipo: TipoRegistro
    diagnostico: str
    medico: str
    institucion: str
    descripcion: str | None = None
    medicacion: str | None = None

class HistorialMedico(BaseModel):
    paciente: Paciente
    registros: List[RegistroMedico]
