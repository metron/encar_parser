import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mark_translates import MARK_TRANSLATES

app = FastAPI()

# Указываем папку с шаблонами
templates = Jinja2Templates(directory="templates")
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    with open("database.json", "r") as f:
        res = json.load(f)

    res = {id_: {
        **item,
        "mark": MARK_TRANSLATES.get(item["mark"], item["mark"])
    } for id_, item in res.items()}
    return templates.TemplateResponse(
        request,
        "index.html",
        {"data": res}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
