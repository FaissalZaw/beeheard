"""Routes du module de visualisation."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.dependances import obtenir_langue
from app.i18n import LANGUES_DISPONIBLES, contexte_langue, traduire
from app.config import DONNEES_FICTIVES, RACINE
from app.depots.depot_obstacle import DepotObstacle
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
    categorie: str = "",
    region: str = "",
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> HTMLResponse:
    """Affiche les indicateurs agrégés, filtrés le cas échéant."""
    statistiques = ServiceStatistiques(session, langue, categorie, region)
    depot = DepotObstacle(session)

    return gabarits.TemplateResponse(
        request=request,
        name="tableau_bord.html",
        context={
            "synthese": statistiques.synthese(),
            "categories_disponibles": depot.lister_categories(),
            "regions_disponibles": _regions_disponibles(session),
            "categorie_active": categorie,
            "region_active": region,
            "langue_courante": langue,
            "donnees_fictives": DONNEES_FICTIVES,
        },
    )


def _regions_disponibles(session: Session) -> list[str]:
    """Liste les régions présentes dans les témoignages retenus."""
    from sqlalchemy import select

    from app.modeles.entites import Contributeur, Temoignage
    from app.modeles.enumerations import StatutTemoignage

    requete = (
        select(Contributeur.region)
        .join(Temoignage, Temoignage.contributeur_id == Contributeur.id)
        .where(Contributeur.region.isnot(None))
        .where(
            Temoignage.statut.in_(
                [StatutTemoignage.VALIDE.value, StatutTemoignage.PUBLIE.value]
            )
        )
        .distinct()
        .order_by(Contributeur.region)
    )
    return [r for (r,) in session.execute(requete).all() if r]


@routeur.get("/api/statistiques")
def obtenir_statistiques(
    categorie: str = "",
    region: str = "",
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> dict:
    """Expose les indicateurs au format JSON."""
    return ServiceStatistiques(session, langue, categorie, region).synthese()
