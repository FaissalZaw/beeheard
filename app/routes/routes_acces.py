"""Routes de consultation et de modification par le contributeur."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.base_donnees import obtenir_session
from app.config import DONNEES_FICTIVES, RACINE
from app.dependances import obtenir_langue
from app.i18n import LANGUES_DISPONIBLES, contexte_langue, traduire
from app.services.service_acces import AccesRefuseError, ServiceAcces

routeur = APIRouter(tags=["acces contributeur"])
gabarits = Jinja2Templates(
    directory=str(RACINE / "app" / "templates"),
    context_processors=[contexte_langue],
)
gabarits.env.globals["t"] = traduire
gabarits.env.globals["langues"] = LANGUES_DISPONIBLES


@routeur.get("/mon-temoignage", response_class=HTMLResponse)
def afficher_formulaire_acces(
    request: Request, langue: str = Depends(obtenir_langue)
) -> HTMLResponse:
    """Affiche le formulaire de saisie des références."""
    return gabarits.TemplateResponse(
        request=request,
        name="acces.html",
        context={"donnees_fictives": DONNEES_FICTIVES},
    )


@routeur.post("/mon-temoignage", response_class=HTMLResponse)
def consulter_temoignage(
    request: Request,
    reference: str = Form(...),
    code: str = Form(...),
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> HTMLResponse:
    """Retrouve un témoignage à partir de sa référence et de son code."""
    service = ServiceAcces(session)

    try:
        temoignage = service.retrouver(reference, code)
    except AccesRefuseError:
        return gabarits.TemplateResponse(
            request=request,
            name="acces.html",
            context={
                "erreur": traduire("acces_erreur", langue),
                "reference_saisie": reference,
                "donnees_fictives": DONNEES_FICTIVES,
            },
            status_code=404,
        )

    return gabarits.TemplateResponse(
        request=request,
        name="mon_temoignage.html",
        context={
            "temoignage": temoignage,
            "reference": reference,
            "code": code,
            "langue_courante": langue,
            "donnees_fictives": DONNEES_FICTIVES,
        },
    )


@routeur.post("/mon-temoignage/consentements", response_class=HTMLResponse)
def modifier_consentements(
    request: Request,
    reference: str = Form(...),
    code: str = Form(...),
    autorise_publication: bool = Form(default=False),
    autorise_plaidoyer: bool = Form(default=False),
    session: Session = Depends(obtenir_session),
    langue: str = Depends(obtenir_langue),
) -> HTMLResponse:
    """Met à jour les usages autorisés par le contributeur."""
    service = ServiceAcces(session)

    try:
        temoignage = service.retrouver(reference, code)
    except AccesRefuseError:
        return RedirectResponse(url="/mon-temoignage", status_code=303)

    service.modifier_consentements(
        temoignage, autorise_publication, autorise_plaidoyer
    )

    return gabarits.TemplateResponse(
        request=request,
        name="mon_temoignage.html",
        context={
            "temoignage": temoignage,
            "reference": reference,
            "code": code,
            "langue_courante": langue,
            "message": traduire("acces_modifie", langue),
            "donnees_fictives": DONNEES_FICTIVES,
        },
    )


@routeur.post("/mon-temoignage/retrait")
def retirer_temoignage(
    reference: str = Form(...),
    code: str = Form(...),
    session: Session = Depends(obtenir_session),
):
    """Supprime définitivement un témoignage à la demande du contributeur."""
    service = ServiceAcces(session)

    try:
        temoignage = service.retrouver(reference, code)
    except AccesRefuseError:
        return RedirectResponse(url="/mon-temoignage", status_code=303)

    service.retirer(temoignage)
    return RedirectResponse(url="/mon-temoignage/retire", status_code=303)


@routeur.get("/mon-temoignage/retire", response_class=HTMLResponse)
def confirmer_retrait(
    request: Request, langue: str = Depends(obtenir_langue)
) -> HTMLResponse:
    """Confirme la suppression du témoignage."""
    return gabarits.TemplateResponse(
        request=request,
        name="retrait_confirme.html",
        context={"donnees_fictives": DONNEES_FICTIVES},
    )
