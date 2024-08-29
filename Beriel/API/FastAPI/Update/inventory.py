from fastapi import HTTPException, APIRouter, Response
from Beriel.mongo.mongo_db import db
import asyncio

router = APIRouter()

@router.post("/api/add_to_inventory/{guild_id}/{user_id}/{item_name}/")
async def add_item_to_inventory(guild_id: str, user_id: str, item_name: str, amount: int):
    collections = db.list_collection_names()
    if guild_id not in collections:
        raise HTTPException(status_code=402, detail="Servidor no encontrado")

    collection = db[guild_id]
    user = collection.find_one({"users.user_id": user_id})

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Buscar el ítem en la base de datos
    item = collection.find_one({"items.name": item_name})

    if not item:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")

    # Revisar si el ítem ya está en el inventario del usuario
    user_inventory = next((inv for inv in user['users'] if inv['user_id'] == user_id), None)
    if not user_inventory:
        # Si el inventario no existe, inicializarlo
        collection.update_one(
            {"users.user_id": user_id},
            {"$push": {"users.$.inventory": {"itemname": item_name, "amount": amount}}}
        )
    else:
        # Si el ítem ya existe, incrementa la cantidad
        collection.update_one(
            {"users.user_id": user_id, "users.inventory.itemname": item_name},
            {"$inc": {"users.$.inventory.$[elem].amount": amount}},
            array_filters=[{"elem.itemname": item_name}]
        )

    # Si el ítem tiene una duración, esperar el tiempo especificado y luego eliminarlo
    if "duration" in item:
        await asyncio.sleep(item["duration"])
        collection.update_one(
            {"users.user_id": user_id},
            {"$pull": {"users.$.inventory": {"itemname": item_name}}}
        )

    return Response("El ítem fue agregado al inventario", status_code=200)



