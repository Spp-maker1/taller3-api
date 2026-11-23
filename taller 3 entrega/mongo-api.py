"""
Taller 3 - Integración APEX + MongoDB (ISIS1511)
API intermedia entre Oracle APEX y MongoDB para los comentarios y eventos de los bares.

Variables de entorno (en Render: Environment):
    MONGO_URI  cadena de conexión de MongoDB (Atlas o el servidor del curso)
    MONGO_DB   nombre de la base de datos (por defecto: drinkadvisor)

Ejecutar localmente:
    uvicorn mongo-api:app --reload        (o renombrar el archivo a mongo_api.py)
"""
import os
from datetime import datetime, timezone

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import DESCENDING, MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "drinkadvisor")

client = MongoClient(MONGO_URI, tz_aware=True)  # fechas en UTC con zona horaria
db = client[MONGO_DB]

app = FastAPI(title="DrinkAdvisor NoSQL API")

# APEX llama la API desde el navegador, por eso se habilita CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def serializar(doc: dict) -> dict:
    """Convierte el ObjectId a texto para poder devolver el documento como JSON."""
    doc["_id"] = str(doc["_id"])
    return doc


@app.get("/")
def raiz():
    return {"mensaje": "API DrinkAdvisor NoSQL funcionando"}


# ---------------------------------------------------------------- comentarios
@app.get("/bares/{bar_id}/comentarios")
def obtener_comentarios(bar_id: int):
    # Punto 3: todos los comentarios del bar, del más reciente al más antiguo
    comentarios = (db["comentarios_bares"]
                   .find({"bar_id": bar_id})
                   .sort("fecha", DESCENDING))
    return [serializar(c) for c in comentarios]


@app.post("/bares/{bar_id}/comentarios", status_code=201)
def crear_comentario(bar_id: int, datos: dict = Body(...)):
    datos["bar_id"] = bar_id
    datos["fecha"] = datetime.now(timezone.utc)

    # Punto 4: la calificación es opcional, pero si viene debe ser un entero de 1 a 5
    if datos.get("calificacion") is not None:
        try:
            calificacion = int(datos["calificacion"])
        except (TypeError, ValueError):
            raise HTTPException(400, "La calificación debe ser un número entero")
        if not 1 <= calificacion <= 5:
            raise HTTPException(400, "La calificación debe estar entre 1 y 5")
        datos["calificacion"] = calificacion

    resultado = db["comentarios_bares"].insert_one(datos)
    return {"mensaje": "Comentario creado", "id": str(resultado.inserted_id)}


# -------------------------------------------------------------------- eventos
@app.get("/bares/{bar_id}/eventos")
def obtener_eventos(bar_id: int):
    # Punto 5: todos los eventos del bar, del más reciente al más antiguo
    eventos = (db["eventos"]
               .find({"bar_id": bar_id})
               .sort("fecha_creacion", DESCENDING))
    return [serializar(e) for e in eventos]


@app.post("/bares/{bar_id}/eventos", status_code=201)
def crear_evento(bar_id: int, evento: dict = Body(...)):
    # Punto 6: el documento se guarda tal como llega (cada tipo de evento
    # tiene campos distintos); solo se exige el nombre.
    if not str(evento.get("nombre", "")).strip():
        raise HTTPException(400, "El nombre del evento es obligatorio")

    evento["bar_id"] = bar_id
    evento["fecha_creacion"] = datetime.now(timezone.utc)

    resultado = db["eventos"].insert_one(evento)
    return {"mensaje": "Evento creado", "id": str(resultado.inserted_id)}
