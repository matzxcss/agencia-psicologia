"""
Clarear Psicologia — Entrypoint FastAPI.
"""

import pathlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import async_session, init_db
from app.routes.api import router as api_router
from app.seed import seed_depoimentos

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: cria tabelas e popula dados iniciais. Shutdown: cleanup."""
    await init_db()
    async with async_session() as session:
        await seed_depoimentos(session)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="API da landing page Clarear Psicologia",
    version="0.1.0",
    lifespan=lifespan,
)

# ── Rotas ───────────────────────────────────────────────────────
app.include_router(api_router)


# ── Landing page ───────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def landing_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


# ── Static files ───────────────────────────────────────────────
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
