import json

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# API эндпоинт для данных
@app.get("/api/data")
async def get_data():
    # with open("database.json", "r") as f:
    #     res = json.load(f)
    res = {
        "message": "Привет от FastAPI!",
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
    }
    return res

# Отдача статики (после сборки React)
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

# SPA роутинг
@app.get("/{path:path}")
async def serve_react(path: str):
    if path.startswith("static"):
        return FileResponse(f"backend/static/{path}")
    return FileResponse("backend/static/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
