# Taller 3 - API DrinkAdvisor NoSQL (ISIS1511)

API en FastAPI que conecta la aplicación de Oracle APEX con MongoDB (comentarios y eventos de bares).

| Método | Ruta | Colección |
|---|---|---|
| GET  | `/bares/{bar_id}/comentarios` | `comentarios_bares` |
| POST | `/bares/{bar_id}/comentarios` | `comentarios_bares` |
| GET  | `/bares/{bar_id}/eventos`     | `eventos` |
| POST | `/bares/{bar_id}/eventos`     | `eventos` |

Variables de entorno: `MONGO_URI` (cadena de conexión) y `MONGO_DB` (nombre de la base).

Ejecutar localmente: `pip install -r requirements.txt` y `uvicorn mongo-api:app --reload`.
