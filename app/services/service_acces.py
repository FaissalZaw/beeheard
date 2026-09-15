"""Accès d'un contributeur à son propre témoignage.

Conformément au droit de rectification prévu par la Loi fédérale sur la
protection des données, un contributeur doit pouvoir accéder aux informations
qu'il a transmises et en modifier les conditions d'usage. Aucune donnée
identifiante n'étant collectée, cet accès repose sur un couple de références
remis au moment du dépôt : un identifiant public et un code personnel connu du
seul contributeur.

Le code n'est jamais conservé en clair : seule son empreinte est stockée, ce
qui rend impossible sa reconstitution à partir de la base.
"""

import hashlib
import hmac
import secrets
import string

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modeles.entites import Contributeur, Temoignage

ALPHABET_CODE = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
LONGUEUR_CODE = 8
SEL = b"beeheard-acces-contributeur"


class AccesRefuseError(Exception):
    """Levée lorsque le couple référence et code ne correspond à rien."""


def generer_code() -> str:
    """Produit un code personnel lisible, sans caractères ambigus."""
    brut = "".join(secrets.choice(ALPHABET_CODE) for _ in range(LONGUEUR_CODE))
    return f"{brut[:4]}-{brut[4:]}"


def calculer_empreinte(code: str) -> str:
    """Retourne l'empreinte du code, seule valeur conservée en base."""
    normalise = code.replace("-", "").replace(" ", "").upper()
    return hashlib.pbkdf2_hmac(
        "sha256", normalise.encode(), SEL, 120_000
    ).hex()


def verifier_code(code: str, empreinte: str) -> bool:
    """Compare un code saisi à une empreinte stockée, en temps constant."""
    return hmac.compare_digest(calculer_empreinte(code), empreinte)


class ServiceAcces:
    """Retrouve et modifie un témoignage à partir de ses références."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def retrouver(self, reference: str, code: str) -> Temoignage:
        """Retourne le témoignage correspondant au couple fourni."""
        reference = reference.strip()

        requete = (
            select(Contributeur)
            .where(Contributeur.pseudonyme == reference)
            .options(selectinload(Contributeur.temoignages))
        )
        contributeur = self.session.execute(requete).scalar_one_or_none()

        if contributeur is None or not verifier_code(
            code, contributeur.empreinte_code
        ):
            raise AccesRefuseError(
                "Aucun témoignage ne correspond à ces références."
            )

        if not contributeur.temoignages:
            raise AccesRefuseError(
                "Aucun témoignage ne correspond à ces références."
            )

        temoignage = contributeur.temoignages[0]
        self.session.refresh(temoignage)
        return temoignage

    def modifier_consentements(
        self,
        temoignage: Temoignage,
        autorise_publication: bool,
        autorise_plaidoyer: bool,
    ) -> Temoignage:
        """Met à jour les usages autorisés par le contributeur.

        Le niveau d'anonymisation n'est pas modifiable : appliqué dès la
        collecte, il a supprimé des données qui ne peuvent être restaurées.
        """
        temoignage.consentement.autorise_publication = autorise_publication
        temoignage.consentement.autorise_plaidoyer = autorise_plaidoyer
        self.session.commit()
        self.session.refresh(temoignage)
        return temoignage

    def retirer(self, temoignage: Temoignage) -> None:
        """Supprime définitivement un témoignage à la demande du contributeur."""
        contributeur = temoignage.contributeur
        self.session.delete(temoignage)
        self.session.delete(contributeur)
        self.session.commit()
