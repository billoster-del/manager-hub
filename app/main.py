"""Manager Hub — FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import AppConfig
from app.routes import schedules, staff

app = FastAPI(title="Manager Hub", version="0.1.0")

config = AppConfig.load(Path("config/app_config.json"))
app.state.config = config

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(schedules.router, prefix="/api/schedules", tags=["schedules"])
app.include_router(staff.router, prefix="/api/staff", tags=["staff"])


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/schedules")
async def schedule_view(request: Request):
    return templates.TemplateResponse("schedule.html", {"request": request})
