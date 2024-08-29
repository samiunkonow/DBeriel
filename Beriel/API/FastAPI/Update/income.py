from fastapi import APIRouter, HTTPException
from Beriel.mongo.mongo_db import db

router = APIRouter()

@router.post("/api/income-economy/{guild_id}/{user_id}/{option}/{amount}/")
def income(guild_id: str, user_id: str, option: str, amount: int):
    opciones = ["cash", "bank"]
    if option not in opciones:
        raise HTTPException(detail="Opción no válida", status_code=401)
    
    # Verificar si la colección (guild) existe
    collections = db.list_collection_names()
    if guild_id not in collections:
        raise HTTPException(detail="Servidor no encontrado", status_code=402)
    
    collection = db[guild_id]
    
    # Buscar si el usuario ya existe en la colección
    user = collection.find_one({"users.user_id": user_id})
    
    if user:
        # Actualizar el campo correspondiente si el usuario existe
        collection.update_one(
            {"users.user_id": user_id},
            {"$inc": {f"users.$.{option}": amount}}
        )
        
        # Calcular el nuevo total después de la actualización
        updated_user = collection.find_one({"users.user_id": user_id})
        new_total = updated_user["users"][0]["cash"] + updated_user["users"][0]["bank"]
        collection.update_one(
            {"users.user_id": user_id},
            {"$set": {"users.$.total": new_total}}
        )
    else:
        # Crear un nuevo usuario si no existe, con el monto inicial en cash o bank
        new_user = {
            "user_id": user_id,
            "cash": 0,
            "bank": 0,
            "total": 0
        }
        new_user[option] = amount
        new_user["total"] = new_user["cash"] + new_user["bank"]

        collection.update_one(
            {},
            {"$push": {"users": new_user}}
        )
    
    return {"status": 200, "data": {"message": "Income updated successfully"}}


