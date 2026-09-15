"""Génération automatique d'un titre à partir du récit.

Le titre reste facultatif à la saisie. Lorsqu'il n'est pas renseigné, un
intitulé est dérivé du récit afin que chaque témoignage dispose d'un libellé
exploitable dans les listes et les restitutions.
"""

import re

LONGUEUR_MAXIMALE = 90
LONGUEUR_MINIMALE = 25


def generer_titre(recit: str) -> str:
    """Dérive un titre lisible de la première phrase du récit."""
    texte = " ".join(recit.split())

    if not texte:
        return "Témoignage sans titre"

    # Première phrase, délimitée par un point, un point d'exclamation
    # ou un point d'interrogation suivi d'une espace
    phrases = re.split(r"(?<=[.!?])\s+", texte)
    candidat = phrases[0].strip()

    # Une phrase trop courte n'est pas informative : on ajoute la suivante
    if len(candidat) < LONGUEUR_MINIMALE and len(phrases) > 1:
        candidat = f"{candidat} {phrases[1].strip()}"

    candidat = candidat.rstrip(".!?")

    if len(candidat) <= LONGUEUR_MAXIMALE:
        return candidat

    # Troncature au dernier mot entier
    tronque = candidat[:LONGUEUR_MAXIMALE]
    if " " in tronque:
        tronque = tronque[: tronque.rfind(" ")]
    return f"{tronque}…"
