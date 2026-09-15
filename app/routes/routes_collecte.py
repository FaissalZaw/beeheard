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
    RoleContributeur.PATIENT: {
        "fr": "Patient", "en": "Patient",
        "de": "Patientin oder Patient", "it": "Paziente",
    },
    RoleContributeur.PROCHE: {
        "fr": "Proche d'un patient", "en": "Relative of a patient",
        "de": "Angehörige oder Angehöriger", "it": "Familiare di un paziente",
    },
    RoleContributeur.PROFESSIONNEL: {
        "fr": "Professionnel de santé", "en": "Healthcare professional",
        "de": "Fachperson im Gesundheitswesen", "it": "Professionista sanitario",
    },
    RoleContributeur.ASSOCIATION: {
        "fr": "Représentant d'association", "en": "Association representative",
        "de": "Vertretung eines Vereins", "it": "Rappresentante di associazione",
    },
}

NIVEAUX_GRAVITE = [
    (1, {
        "fr": ("Gênant", "Situation contraignante, sans conséquence durable"),
        "en": ("Inconvenient", "Constraining situation, no lasting consequence"),
        "de": ("Störend", "Belastende Situation ohne dauerhafte Folgen"),
        "it": ("Fastidioso", "Situazione difficile, senza conseguenze durature"),
    }),
    (2, {
        "fr": ("Pénalisant", "A retardé ou compliqué la prise en charge"),
        "en": ("Detrimental", "Delayed or complicated the care pathway"),
        "de": ("Nachteilig", "Hat die Versorgung verzögert oder erschwert"),
        "it": ("Penalizzante", "Ha ritardato o complicato la presa in carico"),
    }),
    (3, {
        "fr": ("Important", "A eu des répercussions notables sur la situation"),
        "en": ("Significant", "Had notable repercussions on the situation"),
        "de": ("Erheblich", "Hatte spürbare Auswirkungen auf die Situation"),
        "it": ("Importante", "Ha avuto ripercussioni notevoli sulla situazione"),
    }),
    (4, {
        "fr": ("Grave", "A compromis l'accès au traitement"),
        "en": ("Serious", "Compromised access to treatment"),
        "de": ("Schwerwiegend", "Hat den Zugang zur Behandlung gefährdet"),
        "it": ("Grave", "Ha compromesso l'accesso al trattamento"),
    }),
    (5, {
        "fr": ("Critique", "A eu des conséquences majeures sur la santé"),
        "en": ("Critical", "Had major consequences for health"),
        "de": ("Kritisch", "Hatte gravierende gesundheitliche Folgen"),
        "it": ("Critico", "Ha avuto conseguenze maggiori sulla salute"),
    }),
]

CANTONS = [
    "Argovie", "Appenzell", "Bâle-Campagne", "Bâle-Ville", "Berne",
    "Fribourg", "Genève", "Glaris", "Grisons", "Jura", "Lucerne",
    "Neuchâtel", "Nidwald", "Obwald", "Saint-Gall", "Schaffhouse",
    "Schwytz", "Soleure", "Tessin", "Thurgovie", "Uri", "Valais",
    "Vaud", "Zoug", "Zurich",
]


def _contexte_formulaire(
    session: Session, langue: str = "fr", erreur: str | None = None
) -> dict:
    """Assemble les données nécessaires à l'affichage du formulaire."""
    depot = DepotObstacle(session)
    return {
        "langue_courante": langue,
        "categories": depot.lister_categories(),
        "maladies": depot.lister_maladies(),
        "roles": [
            (r.value, LIBELLES_ROLES[r].get(langue, LIBELLES_ROLES[r]["fr"]))
            for r in RoleContributeur
        ],
        "niveaux_gravite": [
            (
                valeur,
                libelles.get(langue, libelles["fr"])[0],
                libelles.get(langue, libelles["fr"])[1],
            )
            for valeur, libelles in NIVEAUX_GRAVITE
        ],
        "cantons": CANTONS,
        "donnees_fictives": DONNEES_FICTIVES,
        "erreur": erreur,
    }


@routeur.get("/temoignage", response_class=HTMLResponse)
def afficher_formulaire(
    request: Request,
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> HTMLResponse:
    """Affiche le formulaire de dépôt d'un témoignage."""
    return gabarits.TemplateResponse(
        request=request,
        name="formulaire.html",
        context=_contexte_formulaire(session, langue),
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
    langue: str = Depends(obtenir_langue),
):
    """Traite la soumission du formulaire de dépôt."""
    if not obstacles:
        return gabarits.TemplateResponse(
            request=request,
            name="formulaire.html",
            context=_contexte_formulaire(
                session, langue, "Veuillez sélectionner au moins un obstacle rencontré."
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
                session, langue, "Le dépôt requiert votre consentement explicite."
            ),
            status_code=400,
        )

    return RedirectResponse(
        url=(
            f"/temoignage/confirmation"
            f"?reference={temoignage.contributeur.pseudonyme}"
            f"&code={temoignage.code_acces_en_clair}"
        ),
        status_code=303,
    )


@routeur.get("/temoignage/confirmation", response_class=HTMLResponse)
def afficher_confirmation(
    request: Request, reference: str = "", code: str = ""
) -> HTMLResponse:
    """Confirme l'enregistrement et communique les références du dépôt."""
    return gabarits.TemplateResponse(
        request=request,
        name="confirmation.html",
        context={
            "reference": reference,
            "code": code,
            "donnees_fictives": DONNEES_FICTIVES,
        },
    )
