"""Count Room / Cage / Vault Automation - FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.database import init_db
from app.routers import count_room, cage, vault, tables, compliance


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables and seed data on startup."""
    init_db()
    from app.seed import seed_if_empty
    seed_if_empty()
    yield
    # shutdown if needed
    pass


app = FastAPI(
    title="Count Room / Cage / Vault Automation API",
    description="Casino count room, cage, and vault automation and reconciliation.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(count_room.router)
app.include_router(cage.router)
app.include_router(vault.router)
app.include_router(tables.router)
app.include_router(compliance.router)

# Serve dashboard
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def root():
    return {
        "message": "Count Room / Cage / Vault Automation API",
        "docs": "/docs",
        "dashboard": "/static/dashboard.html",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
