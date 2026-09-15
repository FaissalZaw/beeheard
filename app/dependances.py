"""Dépendances partagées entre les routes."""

from fastapi import Request

from app.i18n import langue_valide

NOM_COOKIE_LANGUE = "langue"


def obtenir_langue(request: Request) -> str:
    """Détermine la langue d'affichage à partir du cookie ou de l'en-tête."""
    cookie = request.cookies.get(NOM_COOKIE_LANGUE)
    if cookie:
        return langue_valide(cookie)

    entete = request.headers.get("accept-language", "")
    if entete:
        preferee = entete.split(",")[0].split("-")[0].lower()
        return langue_valide(preferee)

    return langue_valide(None)
