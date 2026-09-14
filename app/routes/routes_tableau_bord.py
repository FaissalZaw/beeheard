"""Routes du module de visualisation."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.config import DONNEES_FICTIVES, RACINE
from app.services.service_statistiques import ServiceStatistiques

routeur = APIRouter(tags=["tableau de bord"])
gabarits = Jinja2Templates(directory=str(RACINE / "app" / "templates"))


@routeur.get("/", response_class=HTMLResponse)
def afficher_tableau_bord(
    request: Request, session: Session = Depends(obtenir_session)
) -> HTMLResponse:
    """Affiche les indicateurs agrégés issus des témoignages validés."""
    synthese = ServiceStatistiques(session).synthese()
    return gabarits.TemplateResponse(
        request=request,
        name="tableau_bord.html",
        context={"synthese": synthese, "donnees_fictives": DONNEES_FICTIVES},
    )


@routeur.get("/api/statistiques")
def obtenir_statistiques(session: Session = Depends(obtenir_session)) -> dict:
    """Expose les indicateurs au format JSON."""
    return ServiceStatistiques(session).synthese()
