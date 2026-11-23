"""Prueba la conexión a MongoDB con los datos de .env y crea las colecciones del taller.
Uso:  py probar_conexion.py
.env (en esta carpeta o en la carpeta de arriba; NUNCA se sube a GitHub):
    MONGO_URI=mongodb://usuario:contraseña@157.253.236.88:8087
    MONGO_DB=ISISxxxxxxx
"""
from pathlib import Path
from pymongo import MongoClient

env = {}
aqui = Path(__file__).resolve().parent
archivo = next(f for f in (aqui / ".env", aqui.parent / ".env") if f.exists())
for linea in archivo.read_text(encoding="utf-8").splitlines():
    if "=" in linea and not linea.strip().startswith("#"):
        k, v = linea.split("=", 1)
        env[k.strip()] = v.strip()

client = MongoClient(env["MONGO_URI"], serverSelectionTimeoutMS=8000)
print("Bases visibles:", client.list_database_names())
db = client[env["MONGO_DB"]]
for nombre in ("comentarios_bares", "eventos"):
    if nombre not in db.list_collection_names():
        db.create_collection(nombre)
        print("Colección creada:", nombre)
print("Colecciones en", env["MONGO_DB"], "->", db.list_collection_names())
