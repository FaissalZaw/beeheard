"""Accès aux données relatives aux témoignages."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modeles.entites import Contributeur, Temoignage
from app.modeles.enumerations import StatutTemoignage


class DepotTemoignage:
    """Encapsule les opérations de persistance sur les témoignages."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def ajouter(self, temoignage: Temoignage) -> Temoignage:
        """Persiste un nouveau témoignage."""
        self.session.add(temoignage)
        self.session.commit()
        self.session.refresh(temoignage)
        return temoignage

    def ajouter_contributeur(self, contributeur: Contributeur) -> Contributeur:
        """Persiste un nouveau contributeur."""
        self.session.add(contributeur)
        self.session.commit()
        self.session.refresh(contributeur)
        return contributeur

    def obtenir_par_id(self, identifiant: int) -> Temoignage | None:
        """Retourne un témoignage avec ses relations chargées."""
        requete = (
            select(Temoignage)
            .options(
                selectinload(Temoignage.obstacles),
                selectinload(Temoignage.contributeur),
                selectinload(Temoignage.maladie),
                selectinload(Temoignage.consentement),
            )
            .where(Temoignage.id == identifiant)
        )
        return self.session.execute(requete).scalar_one_or_none()

    def lister(
        self, statut: StatutTemoignage | None = None
    ) -> list[Temoignage]:
        """Retourne les témoignages, filtrés par statut le cas échéant."""
        requete = select(Temoignage).options(
            selectinload(Temoignage.obstacles),
            selectinload(Temoignage.contributeur),
            selectinload(Temoignage.maladie),
        )
        if statut is not None:
            requete = requete.where(Temoignage.statut == statut)
        return list(self.session.execute(requete).scalars().all())

    def compter(self, statut: StatutTemoignage | None = None) -> int:
        """Compte les témoignages, filtrés par statut le cas échéant."""
        return len(self.lister(statut))

    def mettre_a_jour_statut(
        self, temoignage: Temoignage, statut: StatutTemoignage
    ) -> Temoignage:
        """Modifie le statut d'un témoignage et persiste le changement."""
        temoignage.statut = statut
        self.session.commit()
        self.session.refresh(temoignage)
        return temoignage
