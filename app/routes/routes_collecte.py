"""Routes du module de collecte structurée."""

from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.config import RACINE
from app.depots.depot_obstacle import DepotObstacle
from app.modeles.enumerations import NiveauAnonymisation, RoleContributeur
from app.schemas import ObstacleSaisi, TemoignageSaisi
from app.services.service_temoignage import (
    ConsentementManquantError,
    ServiceTemoignage,
)

routeur = APIRouter(tags=["collecte"])
gabarits = Jinja2Templates(directory=str(RACINE / "app" / "templates"))


@routeur.get("/temoignage", response_class=HTMLResponse)
def afficher_formulaire(
    request: Request, session: Session = Depends(obtenir_session)
) -> HTMLResponse:
    """Affiche le formulaire de dépôt d'un témoignage."""
    depot = DepotObstacle(session)
    return gabarits.TemplateResponse(
        request=request,
        name="formulaire.html",
        context={
            "categories": depot.lister_categories(),
            "maladies": depot.lister_maladies(),
            "roles": list(RoleContributeur),
            "niveaux": list(NiveauAnonymisation),
        },
    )


@routeur.post("/temoignage")
def enregistrer_temoignage(
    request: Request,
    role: str = Form(...),
    maladie_id: int = Form(...),
    titre: str = Form(...),
    recit: str = Form(...),
    region: str = Form(default=""),
    tranche_age: str = Form(default=""),
    date_evenement: str = Form(default=""),
    obstacles: list[int] = Form(default=[]),
    severite: int = Form(default=3),
    duree_jours: str = Form(default=""),
    niveau_anonymisation: str = Form(default="complet"),
    autorise_publication: bool = Form(default=False),
    autorise_plaidoyer: bool = Form(default=False),
    consentement_donne: bool = Form(default=False),
    session: Session = Depends(obtenir_session),
):
    """Traite la soumission du formulaire de dépôt."""
    depot = DepotObstacle(session)

    if not obstacles:
        return gabarits.TemplateResponse(
            request=request,
            name="formulaire.html",
            context={
                "categories": depot.lister_categories(),
                "maladies": depot.lister_maladies(),
                "roles": list(RoleContributeur),
                "niveaux": list(NiveauAnonymisation),
                "erreur": "Veuillez sélectionner au moins un obstacle rencontré.",
            },
            status_code=400,
        )

    saisie = TemoignageSaisi(
        role=RoleContributeur(role),
        region=region or None,
        tranche_age=tranche_age or None,
        maladie_id=maladie_id,
        titre=titre,
        recit=recit,
        date_evenement=date.fromisoformat(date_evenement) if date_evenement else None,
        obstacles=[
            ObstacleSaisi(
                type_obstacle_id=identifiant,
                severite=severite,
                duree_jours=int(duree_jours) if duree_jours else None,
            )
            for identifiant in obstacles
        ],
        niveau_anonymisation=NiveauAnonymisation(niveau_anonymisation),
        autorise_publication=autorise_publication,
        autorise_plaidoyer=autorise_plaidoyer,
        consentement_donne=consentement_donne,
    )

    service = ServiceTemoignage(session)

    try:
        service.deposer(saisie)
    except ConsentementManquantError:
        return gabarits.TemplateResponse(
            request=request,
            name="formulaire.html",
            context={
                "categories": depot.lister_categories(),
                "maladies": depot.lister_maladies(),
                "roles": list(RoleContributeur),
                "niveaux": list(NiveauAnonymisation),
                "erreur": "Le dépôt requiert votre consentement explicite.",
            },
            status_code=400,
        )

    return RedirectResponse(url="/temoignage/confirmation", status_code=303)


@routeur.get("/temoignage/confirmation", response_class=HTMLResponse)
def afficher_confirmation(request: Request) -> HTMLResponse:
    """Confirme l'enregistrement du témoignage."""
    return gabarits.TemplateResponse(request=request, name="confirmation.html")
