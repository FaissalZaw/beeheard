"""Point d'entrée de l'application BeeHeard."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.base_donnees import creer_tables
from app.config import NOM_APPLICATION, RACINE, VERSION
from app.routes import routes_collecte, routes_export, routes_tableau_bord

app = FastAPI(
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

app.include_router(routes_tableau_bord.routeur)
app.include_router(routes_collecte.routeur)
app.include_router(routes_export.routeur)


@app.on_event("startup")
def au_demarrage() -> None:
    """Assure l'existence des tables au lancement."""
    creer_tables()


@app.get("/sante", tags=["technique"])
def verifier_sante() -> dict:
    """Sonde de disponibilité de l'application."""
    return {"statut": "operationnel", "version": VERSION}
