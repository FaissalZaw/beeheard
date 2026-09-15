"""Gestion de l'espace d'administration.

L'accès à la modération repose sur un secret partagé plutôt que sur un
système de comptes. Ce choix est cohérent avec le périmètre du prototype :
il démontre le contrôle d'accès sans introduire une gestion d'identités qui
relèverait d'un travail distinct. Une exploitation réelle supposerait une
authentification nominative et une traçabilité des actions de modération.
"""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.config import DUREE_SESSION_HEURES, MOT_DE_PASSE_ADMIN
from app.modeles.entites import ObstacleSignale, Temoignage
from app.modeles.enumerations import StatutTemoignage

NOM_COOKIE_SESSION = "session_admin"
SEL_SESSION = b"beeheard-session-administration"

# Jetons de session émis, associés à leur date d'expiration
_sessions: dict[str, datetime] = {}


def verifier_mot_de_passe(saisi: str) -> bool:
    """Compare le mot de passe saisi au secret configuré, en temps constant."""
    return hmac.compare_digest(
        hashlib.sha256(saisi.encode()).hexdigest(),
        hashlib.sha256(MOT_DE_PASSE_ADMIN.encode()).hexdigest(),
    )


def ouvrir_session() -> str:
    """Émet un jeton de session à durée limitée."""
    jeton = secrets.token_urlsafe(32)
    _sessions[jeton] = datetime.now() + timedelta(hours=DUREE_SESSION_HEURES)
    return jeton


def session_valide(jeton: str | None) -> bool:
    """Vérifie qu'un jeton existe et n'a pas expiré."""
    if not jeton:
        return False

    expiration = _sessions.get(jeton)
    if expiration is None:
        return False

    if datetime.now() > expiration:
        _sessions.pop(jeton, None)
        return False

    return True


def fermer_session(jeton: str | None) -> None:
    """Révoque un jeton de session."""
    if jeton:
        _sessions.pop(jeton, None)


class ServiceAdministration:
    """Fournit les vues et les compteurs nécessaires à la modération."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def compter_par_statut(self) -> dict[str, int]:
        """Répartit les témoignages selon leur statut."""
        requete = select(
            Temoignage.statut, func.count(Temoignage.id)
        ).group_by(Temoignage.statut)

        comptes = dict(self.session.execute(requete).all())
        return {
            statut.value: comptes.get(statut.value, 0)
            for statut in StatutTemoignage
        }

    def lister(self, statut: str | None = None) -> list[Temoignage]:
        """Retourne les témoignages, filtrés par statut le cas échéant."""
        requete = (
            select(Temoignage)
            .options(
                selectinload(Temoignage.obstacles).selectinload(
                    ObstacleSignale.type_obstacle
                ),
                selectinload(Temoignage.contributeur),
                selectinload(Temoignage.maladie),
                selectinload(Temoignage.consentement),
            )
            .order_by(Temoignage.date_soumission.desc())
        )

        if statut:
            requete = requete.where(Temoignage.statut == statut)

        return list(self.session.execute(requete).scalars().all())

    def obtenir(self, identifiant: int) -> Temoignage | None:
        """Retourne un témoignage avec l'ensemble de ses relations."""
        requete = (
            select(Temoignage)
            .options(
                selectinload(Temoignage.obstacles).selectinload(
                    ObstacleSignale.type_obstacle
                ),
                selectinload(Temoignage.contributeur),
                selectinload(Temoignage.maladie),
                selectinload(Temoignage.consentement),
            )
            .where(Temoignage.id == identifiant)
        )
        return self.session.execute(requete).scalar_one_or_none()
