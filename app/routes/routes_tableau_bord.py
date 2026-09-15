"""Routes du module de visualisation."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.dependances import obtenir_langue
from app.i18n import LANGUES_DISPONIBLES, contexte_langue, traduire
from app.config import DONNEES_FICTIVES, RACINE
from app.services.service_statistiques import ServiceStatistiques

routeur = APIRouter(tags=["tableau de bord"])
gabarits = Jinja2Templates(
    directory=str(RACINE / "app" / "templates"),
    context_processors=[contexte_langue],
)
gabarits.env.globals["t"] = traduire
gabarits.env.globals["langues"] = LANGUES_DISPONIBLES


@routeur.get("/tableau-de-bord", response_class=HTMLResponse)
def afficher_tableau_bord(
    request: Request,
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> HTMLResponse:
    """Affiche les indicateurs agrégés issus des témoignages validés."""
    synthese = ServiceStatistiques(session, langue).synthese()
    return gabarits.TemplateResponse(
        request=request,
        name="tableau_bord.html",
        context={"synthese": synthese, "donnees_fictives": DONNEES_FICTIVES},
    )


@routeur.get("/api/statistiques")
def obtenir_statistiques(
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> dict:
    """Expose les indicateurs au format JSON."""
    return ServiceStatistiques(session, langue).synthese()
