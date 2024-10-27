from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mi_base_de_datos"]

pacientes_col = db["pacientes"]
registros_medicos_col = db["registros_medicos"]
historiales_medicos_col = db["historiales_medicos"]