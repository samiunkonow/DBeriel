import json
from fastapi import HTTPException, APIRouter, Response
from pydantic import BaseModel
from Beriel.mongo.mongo_db import db

class Item(BaseModel):
    name: str
    value: int = 0
    description: str = "None"
    inventory: str = "None"
    duration: str = "None"
    stock: str = "None"
    role_required: str = "None"
    role_given: str = "None"
    role_removed: str = "None"
    required_balance: str = "None"
    reply: str = "None"

router = APIRouter()

@router.post("/api/add_item/{guild_id}/")
def add_item_to_server(guild_id: str, item: Item):
    collections = db.list_collection_names()
    if guild_id not in collections:
        raise HTTPException(detail="Servidor no encontrado", status_code=402)

    # Añadir el item al array 'items' en la colección del servidor
    collection = db[guild_id]
    collection.update_one(
        {},
        {"$push": {"items": item.dict()}},  # Usar .dict() en lugar de .json() para que sea un diccionario
        upsert=True  # Crear el documento si no existe
    )
    return Response(content={"status": 200, "data": {"message": "Se agregó el item"}}, status_code=200)
