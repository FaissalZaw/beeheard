"""Routes du module de collecte structurée."""

from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.dependances import obtenir_langue
from app.i18n import LANGUES_DISPONIBLES, contexte_langue, traduire
from app.config import DONNEES_FICTIVES, RACINE
from app.depots.depot_obstacle import DepotObstacle
from app.modeles.enumerations import NiveauAnonymisation, RoleContributeur
from app.schemas import ObstacleSaisi, TemoignageSaisi
from app.services.service_temoignage import (
    ConsentementManquantError,
    ServiceTemoignage,
)

routeur = APIRouter(tags=["collecte"])
gabarits = Jinja2Templates(
    directory=str(RACINE / "app" / "templates"),
    context_processors=[contexte_langue],
)
gabarits.env.globals["t"] = traduire
gabarits.env.globals["langues"] = LANGUES_DISPONIBLES

LIBELLES_ROLES = {
    RoleContributeur.PATIENT: "Patient",
    RoleContributeur.PROCHE: "Proche d'un patient",
    RoleContributeur.PROFESSIONNEL: "Professionnel de santé",
    RoleContributeur.ASSOCIATION: "Représentant d'association",
}

NIVEAUX_GRAVITE = [
    (1, "Gênant", "Situation contraignante, sans conséquence durable"),
    (2, "Pénalisant", "A retardé ou compliqué la prise en charge"),
    (3, "Important", "A eu des répercussions notables sur la situation"),
    (4, "Grave", "A compromis l'accès au traitement"),
    (5, "Critique", "A eu des conséquences majeures sur la santé"),
]

CANTONS = [
    "Argovie", "Appenzell", "Bâle-Campagne", "Bâle-Ville", "Berne",
    "Fribourg", "Genève", "Glaris", "Grisons", "Jura", "Lucerne",
    "Neuchâtel", "Nidwald", "Obwald", "Saint-Gall", "Schaffhouse",
    "Schwytz", "Soleure", "Tessin", "Thurgovie", "Uri", "Valais",
    "Vaud", "Zoug", "Zurich",
]


def _contexte_formulaire(session: Session, erreur: str | None = None) -> dict:
    """Assemble les données nécessaires à l'affichage du formulaire."""
    depot = DepotObstacle(session)
    return {
        "categories": depot.lister_categories(),
        "maladies": depot.lister_maladies(),
        "roles": [(r.value, LIBELLES_ROLES[r]) for r in RoleContributeur],
        "niveaux_gravite": NIVEAUX_GRAVITE,
        "cantons": CANTONS,
        "donnees_fictives": DONNEES_FICTIVES,
        "erreur": erreur,
    }


@routeur.get("/temoignage", response_class=HTMLResponse)
def afficher_formulaire(
    request: Request, session: Session = Depends(obtenir_session)
) -> HTMLResponse:
    """Affiche le formulaire de dépôt d'un témoignage."""
    return gabarits.TemplateResponse(
        request=request,
        name="formulaire.html",
        context=_contexte_formulaire(session),
    )


@routeur.post("/temoignage")
def enregistrer_temoignage(
    request: Request,
    role: str = Form(...),
    maladie_id: int = Form(...),
    recit: str = Form(...),
    titre: str = Form(default=""),
    region: str = Form(default=""),
    tranche_age: str = Form(default=""),
    date_evenement: str = Form(default=""),
    obstacles: list[int] = Form(default=[]),
    severite: int = Form(default=3),
    duree_jours: str = Form(default=""),
    niveau_anonymisation: str = Form(default="complet"),
    autorise_statistiques: bool = Form(default=False),
    autorise_publication: bool = Form(default=False),
    autorise_plaidoyer: bool = Form(default=False),
    consentement_donne: bool = Form(default=False),
    session: Session = Depends(obtenir_session),
):
    """Traite la soumission du formulaire de dépôt."""
    if not obstacles:
        return gabarits.TemplateResponse(
            request=request,
            name="formulaire.html",
            context=_contexte_formulaire(
                session, "Veuillez sélectionner au moins un obstacle rencontré."
            ),
            status_code=400,
        )

    saisie = TemoignageSaisi(
        role=RoleContributeur(role),
        region=region or None,
        tranche_age=tranche_age or None,
        maladie_id=maladie_id,
        titre=titre or None,
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
        autorise_statistiques=autorise_statistiques,
        autorise_publication=autorise_publication,
        autorise_plaidoyer=autorise_plaidoyer,
        consentement_donne=consentement_donne,
    )

    service = ServiceTemoignage(session)

    try:
        temoignage = service.deposer(saisie)
    except ConsentementManquantError:
        return gabarits.TemplateResponse(
            request=request,
            name="formulaire.html",
            context=_contexte_formulaire(
                session, "Le dépôt requiert votre consentement explicite."
            ),
            status_code=400,
        )

    return RedirectResponse(
        url=f"/temoignage/confirmation?reference={temoignage.contributeur.pseudonyme}",
        status_code=303,
    )


@routeur.get("/temoignage/confirmation", response_class=HTMLResponse)
def afficher_confirmation(
    request: Request, reference: str = ""
) -> HTMLResponse:
    """Confirme l'enregistrement et communique la référence du dépôt."""
    return gabarits.TemplateResponse(
        request=request,
        name="confirmation.html",
        context={"reference": reference, "donnees_fictives": DONNEES_FICTIVES},
    )
