import os
import importlib.util
from fastapi import FastAPI, HTTPException, Query,APIRouter
from fastapi.responses import Response, JSONResponse, StreamingResponse
from Beriel.API.Funciones.loop import registrar_rutas_desde_directorio
app = FastAPI()


carpeta_api = os.path.join(os.path.dirname(__file__), 'Beriel')
router_principal = APIRouter()

registrar_rutas_desde_directorio(router_principal, carpeta_api)
app.include_router(router_principal)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)