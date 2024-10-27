from pydantic import BaseModel
from app.enum import TipoSexo, TipoRegistro

class Paciente(BaseModel):
    ci: str
    nombre: str
    apellido: str
    fecha_nacimiento: str
    sexo: TipoSexo

class RegistroMedico(BaseModel):
    id: str
    fecha: str
    tipo: TipoRegistro
    diagnostico: str
    medico: str
    institucion: str
    descripcion: str | None = None
    medicacion: str | None = None