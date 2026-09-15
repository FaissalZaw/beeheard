"""Point d'entrée de l'application BeeHeard."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.base_donnees import creer_tables
from app.config import NOM_APPLICATION, RACINE, VERSION
from app.routes import (
    routes_acces,
    routes_accueil,
    routes_collecte,
    routes_export,
    routes_tableau_bord,
)

@asynccontextmanager
async def cycle_de_vie(application: FastAPI) -> AsyncGenerator[None, None]:
    """Assure l'existence des tables au démarrage de l'application."""
    creer_tables()
    yield


app = FastAPI(
    lifespan=cycle_de_vie,
    title=NOM_APPLICATION,
    version=VERSION,
    description=(
        "Prototype d'outil de documentation et de visualisation des obstacles "
        "d'accès aux traitements dans les maladies rares."
    ),
)

app.mount(
    "/static",
    StaticFiles(directory=str(RACINE / "app" / "static")),
    name="static",
)

app.include_router(routes_accueil.routeur)
app.include_router(routes_tableau_bord.routeur)
app.include_router(routes_collecte.routeur)
app.include_router(routes_export.routeur)
app.include_router(routes_acces.routeur)


@app.get("/sante", tags=["technique"])
def verifier_sante() -> dict:
    """Sonde de disponibilité de l'application."""
    return {"statut": "operationnel", "version": VERSION}
