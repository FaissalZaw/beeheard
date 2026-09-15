"""Routes des pages d'information et d'accueil."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.config import DONNEES_FICTIVES, RACINE
from app.depots.depot_obstacle import DepotObstacle
from app.services.service_statistiques import ServiceStatistiques

routeur = APIRouter(tags=["information"])
gabarits = Jinja2Templates(directory=str(RACINE / "app" / "templates"))


@routeur.get("/", response_class=HTMLResponse)
def afficher_accueil(
    request: Request, session: Session = Depends(obtenir_session)
) -> HTMLResponse:
    """Présente l'outil et oriente vers les deux parcours principaux."""
    statistiques = ServiceStatistiques(session)
    return gabarits.TemplateResponse(
        request=request,
        name="accueil.html",
        context={
            "nombre_temoignages": statistiques.compter_temoignages(),
            "nombre_obstacles": statistiques.compter_obstacles(),
            "donnees_fictives": DONNEES_FICTIVES,
        },
    )


@routeur.get("/a-propos", response_class=HTMLResponse)
def afficher_a_propos(
    request: Request, session: Session = Depends(obtenir_session)
) -> HTMLResponse:
    """Explique la démarche, la nomenclature et le cadre du projet."""
    depot = DepotObstacle(session)
    return gabarits.TemplateResponse(
        request=request,
        name="a_propos.html",
        context={
            "categories": depot.lister_categories(),
            "donnees_fictives": DONNEES_FICTIVES,
        },
    )


@routeur.get("/protection-des-donnees", response_class=HTMLResponse)
def afficher_protection_donnees(request: Request) -> HTMLResponse:
    """Détaille le traitement des données et les droits des contributeurs."""
    return gabarits.TemplateResponse(
        request=request,
        name="protection_donnees.html",
        context={"donnees_fictives": DONNEES_FICTIVES},
    )


@routeur.get("/mentions-legales", response_class=HTMLResponse)
def afficher_mentions_legales(request: Request) -> HTMLResponse:
    """Identifie le responsable du prototype et son cadre."""
    return gabarits.TemplateResponse(
        request=request,
        name="mentions_legales.html",
        context={"donnees_fictives": DONNEES_FICTIVES},
    )
