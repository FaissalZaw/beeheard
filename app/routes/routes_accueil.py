"""Routes des pages d'information et d'accueil."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.dependances import obtenir_langue
from app.i18n import LANGUES_DISPONIBLES, contexte_langue, traduire
from app.config import DONNEES_FICTIVES, RACINE
from app.depots.depot_obstacle import DepotObstacle
from app.services.service_statistiques import ServiceStatistiques

routeur = APIRouter(tags=["information"])
gabarits = Jinja2Templates(
    directory=str(RACINE / "app" / "templates"),
    context_processors=[contexte_langue],
)
gabarits.env.globals["t"] = traduire
gabarits.env.globals["langues"] = LANGUES_DISPONIBLES


@routeur.get("/", response_class=HTMLResponse)
def afficher_accueil(
    request: Request,
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> HTMLResponse:
    """Présente l'outil et oriente vers les deux parcours principaux."""
    statistiques = ServiceStatistiques(session, langue)
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
    request: Request,
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> HTMLResponse:
    """Explique la démarche, la nomenclature et le cadre du projet."""
    depot = DepotObstacle(session)
    return gabarits.TemplateResponse(
        request=request,
        name="a_propos.html",
        context={
            "categories": depot.lister_categories(),
            "langue_courante": langue,
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


@routeur.get("/langue/{code}")
def changer_langue(code: str, request: Request):
    """Enregistre la langue choisie et revient à la page précédente."""
    from app.dependances import NOM_COOKIE_LANGUE
    from app.i18n import langue_valide

    destination = request.headers.get("referer") or "/"
    reponse = RedirectResponse(url=destination, status_code=303)
    reponse.set_cookie(
        NOM_COOKIE_LANGUE,
        langue_valide(code),
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax",
    )
    return reponse
