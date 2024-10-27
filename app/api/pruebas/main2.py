from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from typing import List

# Crear la app de FastAPI
app = FastAPI()

# Conexión con MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mi_base_de_datos"]  # Nombre de la base de datos
collection = db["mi_coleccion"]   # Nombre de la colección

# Modelo Pydantic para la respuesta
class Item(BaseModel):
    id: str
    nombre: str
    descripcion: str

# Ruta para obtener todos los items de la colección
@app.get("/items/", response_model=List[Item])
def get_items():
    items = []
    for item in collection.find():
        items.append(Item(
            id=str(item["_id"]),
            nombre=item["nombre"],
            descripcion=item["descripcion"]
        ))
    return items

# Ruta para obtener un item por su ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return Item(
            id=str(item["_id"]),
            nombre=item["nombre"],
            descripcion=item["descripcion"]
        )
    return {"error": "Item no encontrado"}
