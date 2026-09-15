"""Entités du modèle de données BeeHeard.

La nomenclature des obstacles (CategorieObstacle, TypeObstacle) est dérivée
de la revue de littérature, en particulier de Phillips et al. (2022) pour les
niveaux de barrières perçues et de la section 2.5 du mémoire pour les quatre
catégories retenues.
"""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base_donnees import Base
from app.modeles.enumerations import (
    NiveauAnonymisation,
    RoleContributeur,
    StatutTemoignage,
)


class CategorieObstacle(Base):
    """Catégorie d'obstacle : économique, organisationnel, informationnel, social."""

    __tablename__ = "categorie_obstacle"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    libelle: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)

    types: Mapped[list["TypeObstacle"]] = relationship(back_populates="categorie")
    traductions: Mapped[list["TraductionCategorie"]] = relationship(
        back_populates="categorie", cascade="all, delete-orphan"
    )

    def libelle_dans(self, langue: str) -> str:
        """Retourne le libellé dans la langue demandée, ou le libellé source."""
        for traduction in self.traductions:
            if traduction.langue == langue:
                return traduction.libelle
        return self.libelle

    def description_dans(self, langue: str) -> str | None:
        """Retourne la description dans la langue demandée."""
        for traduction in self.traductions:
            if traduction.langue == langue and traduction.description:
                return traduction.description
        return self.description

    def __repr__(self) -> str:
        return f"<CategorieObstacle {self.code}>"


class TypeObstacle(Base):
    """Type d'obstacle précis, rattaché à une catégorie."""

    __tablename__ = "type_obstacle"

    id: Mapped[int] = mapped_column(primary_key=True)
    categorie_id: Mapped[int] = mapped_column(ForeignKey("categorie_obstacle.id"))
    code: Mapped[str] = mapped_column(String(80), unique=True)
    libelle: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)

    categorie: Mapped["CategorieObstacle"] = relationship(back_populates="types")
    signalements: Mapped[list["ObstacleSignale"]] = relationship(
        back_populates="type_obstacle"
    )
    traductions: Mapped[list["TraductionType"]] = relationship(
        back_populates="type_obstacle", cascade="all, delete-orphan"
    )

    def libelle_dans(self, langue: str) -> str:
        """Retourne le libellé dans la langue demandée, ou le libellé source."""
        for traduction in self.traductions:
            if traduction.langue == langue:
                return traduction.libelle
        return self.libelle

    def __repr__(self) -> str:
        return f"<TypeObstacle {self.code}>"


class Maladie(Base):
    """Pathologie concernée par un témoignage."""

    __tablename__ = "maladie"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(200), unique=True)
    code_orpha: Mapped[str | None] = mapped_column(String(20))
    est_rare: Mapped[bool] = mapped_column(default=True)

    temoignages: Mapped[list["Temoignage"]] = relationship(back_populates="maladie")

    def __repr__(self) -> str:
        return f"<Maladie {self.nom}>"


class Contributeur(Base):
    """Auteur d'un témoignage.

    Aucune donnée identifiante directe n'est stockée : le pseudonyme est
    généré par le système et la localisation reste à l'échelle du canton.
    """

    __tablename__ = "contributeur"

    id: Mapped[int] = mapped_column(primary_key=True)
    pseudonyme: Mapped[str] = mapped_column(String(50), unique=True)
    empreinte_code: Mapped[str] = mapped_column(String(128))
    role: Mapped[RoleContributeur] = mapped_column(String(30))
    region: Mapped[str | None] = mapped_column(String(80))
    tranche_age: Mapped[str | None] = mapped_column(String(20))
    date_creation: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    temoignages: Mapped[list["Temoignage"]] = relationship(
        back_populates="contributeur"
    )

    def __repr__(self) -> str:
        return f"<Contributeur {self.pseudonyme}>"


class Temoignage(Base):
    """Témoignage déposé par un contributeur sur les obstacles rencontrés."""

    __tablename__ = "temoignage"

    id: Mapped[int] = mapped_column(primary_key=True)
    contributeur_id: Mapped[int] = mapped_column(ForeignKey("contributeur.id"))
    maladie_id: Mapped[int] = mapped_column(ForeignKey("maladie.id"))
    titre: Mapped[str] = mapped_column(String(200))
    recit: Mapped[str] = mapped_column(Text)
    date_evenement: Mapped[date | None] = mapped_column(Date)
    date_soumission: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    statut: Mapped[StatutTemoignage] = mapped_column(
        String(20), default=StatutTemoignage.BROUILLON
    )
    langue: Mapped[str] = mapped_column(String(5), default="fr")

    contributeur: Mapped["Contributeur"] = relationship(back_populates="temoignages")
    maladie: Mapped["Maladie"] = relationship(back_populates="temoignages")
    obstacles: Mapped[list["ObstacleSignale"]] = relationship(
        back_populates="temoignage", cascade="all, delete-orphan"
    )
    consentement: Mapped["Consentement"] = relationship(
        back_populates="temoignage", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Temoignage {self.id} ({self.statut})>"


class ObstacleSignale(Base):
    """Association entre un témoignage et un type d'obstacle rencontré."""

    __tablename__ = "obstacle_signale"

    id: Mapped[int] = mapped_column(primary_key=True)
    temoignage_id: Mapped[int] = mapped_column(ForeignKey("temoignage.id"))
    type_obstacle_id: Mapped[int] = mapped_column(ForeignKey("type_obstacle.id"))
    severite: Mapped[int] = mapped_column(default=3)
    duree_jours: Mapped[int | None] = mapped_column()
    commentaire: Mapped[str | None] = mapped_column(Text)

    temoignage: Mapped["Temoignage"] = relationship(back_populates="obstacles")
    type_obstacle: Mapped["TypeObstacle"] = relationship(
        back_populates="signalements"
    )

    def __repr__(self) -> str:
        return f"<ObstacleSignale {self.id} (severite {self.severite})>"


class Consentement(Base):
    """Consentement recueilli lors du dépôt d'un témoignage."""

    __tablename__ = "consentement"

    id: Mapped[int] = mapped_column(primary_key=True)
    temoignage_id: Mapped[int] = mapped_column(
        ForeignKey("temoignage.id"), unique=True
    )
    version_texte: Mapped[str] = mapped_column(String(10))
    niveau_anonymisation: Mapped[NiveauAnonymisation] = mapped_column(String(20))
    autorise_publication: Mapped[bool] = mapped_column(default=False)
    autorise_plaidoyer: Mapped[bool] = mapped_column(default=False)
    date_consentement: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    temoignage: Mapped["Temoignage"] = relationship(back_populates="consentement")

    def __repr__(self) -> str:
        return f"<Consentement {self.id} ({self.niveau_anonymisation})>"


class TraductionCategorie(Base):
    """Traduction d'une catégorie d'obstacle dans une langue donnée.

    Le recours à une table de traduction plutôt qu'à des colonnes dédiées
    permet d'ajouter une langue sans modifier le schéma de la base.
    """

    __tablename__ = "traduction_categorie"
    __table_args__ = (
        UniqueConstraint("categorie_id", "langue", name="uq_traduction_categorie"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    categorie_id: Mapped[int] = mapped_column(ForeignKey("categorie_obstacle.id"))
    langue: Mapped[str] = mapped_column(String(5))
    libelle: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)

    categorie: Mapped["CategorieObstacle"] = relationship(
        back_populates="traductions"
    )

    def __repr__(self) -> str:
        return f"<TraductionCategorie {self.langue}>"


class TraductionType(Base):
    """Traduction d'un type d'obstacle dans une langue donnée."""

    __tablename__ = "traduction_type"
    __table_args__ = (
        UniqueConstraint("type_obstacle_id", "langue", name="uq_traduction_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    type_obstacle_id: Mapped[int] = mapped_column(ForeignKey("type_obstacle.id"))
    langue: Mapped[str] = mapped_column(String(5))
    libelle: Mapped[str] = mapped_column(String(200))

    type_obstacle: Mapped["TypeObstacle"] = relationship(
        back_populates="traductions"
    )

    def __repr__(self) -> str:
        return f"<TraductionType {self.langue}>"
