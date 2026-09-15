"""Schémas de validation des données entrantes et sortantes."""

from datetime import date

from pydantic import BaseModel, Field

from app.modeles.enumerations import NiveauAnonymisation, RoleContributeur


class ObstacleSaisi(BaseModel):
    """Obstacle qualifié lors du dépôt d'un témoignage."""

    type_obstacle_id: int
    severite: int = Field(default=3, ge=1, le=5)
    duree_jours: int | None = Field(default=None, ge=0)
    commentaire: str | None = None


class TemoignageSaisi(BaseModel):
    """Ensemble des informations recueillies lors d'un dépôt."""

    role: RoleContributeur
    region: str | None = None
    tranche_age: str | None = None

    maladie_id: int | None = None
    maladie_libre: str | None = Field(default=None, max_length=200)
    titre: str | None = Field(default=None, max_length=200)
    recit: str = Field(min_length=30, max_length=3000)
    date_evenement: date | None = None
    langue: str = Field(default="fr", max_length=5)

    obstacles: list[ObstacleSaisi] = Field(min_length=1)

    niveau_anonymisation: NiveauAnonymisation = NiveauAnonymisation.COMPLET
    autorise_statistiques: bool = True
    autorise_publication: bool = False
    autorise_plaidoyer: bool = False
    consentement_donne: bool
