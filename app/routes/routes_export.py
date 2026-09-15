"""Routes du module de restitution."""

from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.dependances import obtenir_langue
from app.i18n import LANGUES_DISPONIBLES, contexte_langue, traduire
from app.config import DONNEES_FICTIVES, RACINE
from app.depots.depot_temoignage import DepotTemoignage
from app.modeles.enumerations import StatutTemoignage
from app.services.service_statistiques import ServiceStatistiques

routeur = APIRouter(tags=["restitution"])
gabarits = Jinja2Templates(
    directory=str(RACINE / "app" / "templates"),
    context_processors=[contexte_langue],
)
gabarits.env.globals["t"] = traduire
gabarits.env.globals["langues"] = LANGUES_DISPONIBLES


@routeur.get("/synthese", response_class=HTMLResponse)
def afficher_fiche_synthese(
    request: Request,
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> HTMLResponse:
    """Produit une fiche de synthèse destinée aux acteurs du plaidoyer."""
    statistiques = ServiceStatistiques(session, langue)
    depot = DepotTemoignage(session)

    temoignages = depot.lister(StatutTemoignage.VALIDE)
    illustrations = [
        t for t in temoignages if t.consentement and t.consentement.autorise_plaidoyer
    ][:3]

    return gabarits.TemplateResponse(
        request=request,
        name="synthese.html",
        context={
            "synthese": statistiques.synthese(),
            "illustrations": illustrations,
            "date_generation": datetime.now().strftime("%d.%m.%Y"),
            "donnees_fictives": DONNEES_FICTIVES,
        },
    )
