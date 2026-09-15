"""Routes de l'espace d'administration."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.config import DONNEES_FICTIVES, DUREE_SESSION_HEURES, RACINE
from app.dependances import obtenir_langue
from app.i18n import LANGUES_DISPONIBLES, contexte_langue, traduire
from app.modeles.enumerations import StatutTemoignage
from app.services.service_administration import (
    NOM_COOKIE_SESSION,
    ServiceAdministration,
    fermer_session,
    ouvrir_session,
    session_valide,
    verifier_mot_de_passe,
)
from app.services.service_temoignage import (
    ServiceTemoignage,
    TransitionInterditeError,
)

routeur = APIRouter(prefix="/administration", tags=["administration"])
gabarits = Jinja2Templates(
    directory=str(RACINE / "app" / "templates"),
    context_processors=[contexte_langue],
)
gabarits.env.globals["t"] = traduire
gabarits.env.globals["langues"] = LANGUES_DISPONIBLES

LIBELLES_STATUTS = {
    StatutTemoignage.BROUILLON.value: "Brouillon",
    StatutTemoignage.SOUMIS.value: "En attente",
    StatutTemoignage.VALIDE.value: "Validé",
    StatutTemoignage.PUBLIE.value: "Publié",
    StatutTemoignage.REJETE.value: "Rejeté",
}


def exiger_session(request: Request) -> bool:
    """Vérifie la présence d'une session d'administration valide."""
    return session_valide(request.cookies.get(NOM_COOKIE_SESSION))


@routeur.get("", response_class=HTMLResponse)
def afficher_administration(
    request: Request,
    statut: str = "",
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
):
    """Affiche la liste des témoignages à modérer."""
    if not exiger_session(request):
        return gabarits.TemplateResponse(
            request=request,
            name="administration_connexion.html",
            context={"donnees_fictives": DONNEES_FICTIVES},
        )

    service = ServiceAdministration(session)

    return gabarits.TemplateResponse(
        request=request,
        name="administration.html",
        context={
            "temoignages": service.lister(statut or None),
            "comptes": service.compter_par_statut(),
            "statut_actif": statut,
            "libelles_statuts": LIBELLES_STATUTS,
            "langue_courante": langue,
            "donnees_fictives": DONNEES_FICTIVES,
        },
    )


@routeur.post("/connexion")
def se_connecter(
    request: Request,
    mot_de_passe: str = Form(...),
):
    """Ouvre une session d'administration."""
    if not verifier_mot_de_passe(mot_de_passe):
        return gabarits.TemplateResponse(
            request=request,
            name="administration_connexion.html",
            context={
                "erreur": "Mot de passe incorrect.",
                "donnees_fictives": DONNEES_FICTIVES,
            },
            status_code=401,
        )

    reponse = RedirectResponse(url="/administration", status_code=303)
    reponse.set_cookie(
        NOM_COOKIE_SESSION,
        ouvrir_session(),
        max_age=DUREE_SESSION_HEURES * 3600,
        httponly=True,
        samesite="lax",
    )
    return reponse


@routeur.post("/deconnexion")
def se_deconnecter(request: Request):
    """Révoque la session en cours."""
    fermer_session(request.cookies.get(NOM_COOKIE_SESSION))
    reponse = RedirectResponse(url="/administration", status_code=303)
    reponse.delete_cookie(NOM_COOKIE_SESSION)
    return reponse


@routeur.get("/temoignage/{identifiant}", response_class=HTMLResponse)
def afficher_detail(
    request: Request,
    identifiant: int,
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
):
    """Affiche le détail d'un témoignage en vue de sa modération."""
    if not exiger_session(request):
        return RedirectResponse(url="/administration", status_code=303)

    temoignage = ServiceAdministration(session).obtenir(identifiant)

    if temoignage is None:
        return RedirectResponse(url="/administration", status_code=303)

    return gabarits.TemplateResponse(
        request=request,
        name="administration_detail.html",
        context={
            "temoignage": temoignage,
            "libelles_statuts": LIBELLES_STATUTS,
            "langue_courante": langue,
            "donnees_fictives": DONNEES_FICTIVES,
        },
    )


@routeur.post("/temoignage/{identifiant}/{action}")
def appliquer_action(
    request: Request,
    identifiant: int,
    action: str,
    session: Session = Depends(obtenir_session),
):
    """Applique une transition d'état à un témoignage.

    Les transitions autorisées sont définies dans le service de témoignage :
    l'interface d'administration ne fait qu'y recourir, ce qui garantit que
    les mêmes règles s'appliquent quel que soit le point d'entrée.
    """
    if not exiger_session(request):
        return RedirectResponse(url="/administration", status_code=303)

    administration = ServiceAdministration(session)
    temoignage = administration.obtenir(identifiant)

    if temoignage is None:
        return RedirectResponse(url="/administration", status_code=303)

    service = ServiceTemoignage(session)
    actions = {
        "valider": service.valider,
        "publier": service.publier,
        "rejeter": service.rejeter,
    }

    if action in actions:
        try:
            actions[action](temoignage)
        except TransitionInterditeError:
            pass

    return RedirectResponse(
        url=f"/administration/temoignage/{identifiant}", status_code=303
    )
