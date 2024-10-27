from enum import Enum

class TipoSexo(str, Enum):
    masculino = "masculino"
    femenino = "femenino"

class TipoRegistro(str, Enum):
    consulta = "consulta"
    examen = "examen"
    internacion = "internacion"