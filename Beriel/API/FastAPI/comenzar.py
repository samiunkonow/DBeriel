from fastapi import APIRouter
from fastapi.responses import Response
from Beriel.mongo.mongo_db import db
import json

router = APIRouter()

estructura = {
        "items": [],
        "min-max-payout": [{
            "minwork": 0,
            "maxwork": 20,
            "mincrime": 0,
            "maxcrime": 20,
            "minslut": 0,
            "maxslut": 20
        }],
        "min-max-fail": [{
            "mincrime": 0,
            "maxcrime": 20,
            "minslut": 0,
            "maxslut": 20
        }],
        "replys-win": [{
            "work": [],
            "crime": [],
            "slut": []
        }],
        "replys-fail": [{
            "crime": [],
            "slut": []
        }],
        "roles-income": [],
        "reply-count": 0,
        "users": [],
        "coin": ":pizza:"
    }


@router.post("/api/start-economy/{guild_id}/")
def start(guild_id: str):
    
    collections = db.list_collection_names()
    if not guild_id in collections:
        collection = db.create_collection(guild_id)
    

    collection.insert_one(estructura)
    return Response(json.dumps(obj={"status": 201, "data": {"message": "Economy started"}},indent=4), status_code=201)