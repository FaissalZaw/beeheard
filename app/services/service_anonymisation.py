"""Génération de pseudonymes et application des règles d'anonymisation.

Conformément aux exigences identifiées en section 2.7.3 du mémoire, aucune
donnée identifiante directe n'est conservée. Le pseudonyme est généré par le
système et la localisation reste à l'échelle du canton ou de la région.
"""

import secrets
import string

from app.modeles.enumerations import NiveauAnonymisation

ALPHABET = string.ascii_uppercase + string.digits
LONGUEUR_IDENTIFIANT = 5


def generer_pseudonyme() -> str:
    """Produit un pseudonyme aléatoire non rattachable à une identité."""
    suffixe = "".join(secrets.choice(ALPHABET) for _ in range(LONGUEUR_IDENTIFIANT))
    return f"Contributeur-{suffixe}"


def appliquer_anonymisation(
    region: str | None,
    tranche_age: str | None,
    niveau: NiveauAnonymisation,
) -> tuple[str | None, str | None]:
    """Applique le niveau d'anonymisation choisi aux attributs contextuels.

    En anonymisation complète, la région et la tranche d'âge sont supprimées
    afin de réduire le risque de réidentification, particulièrement élevé
    dans le champ des maladies rares.
    """
    if niveau == NiveauAnonymisation.COMPLET:
        return None, None
    if niveau == NiveauAnonymisation.PARTIEL:
        return region, None
    return region, tranche_age
