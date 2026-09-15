"""Énumérations du domaine BeeHeard."""

from enum import Enum


class RoleContributeur(str, Enum):
    """Qualité dans laquelle une personne dépose un témoignage."""

    PATIENT = "patient"
    PROCHE = "proche"
    PROFESSIONNEL = "professionnel"
    ASSOCIATION = "association"


class StatutTemoignage(str, Enum):
    """Cycle de vie d'un témoignage."""

    BROUILLON = "brouillon"
    SOUMIS = "soumis"
    VALIDE = "valide"
    PUBLIE = "publie"
    REJETE = "rejete"


class NiveauAnonymisation(str, Enum):
    """Degré d'anonymisation choisi par le contributeur."""

    COMPLET = "complet"
    PARTIEL = "partiel"
    IDENTIFIE = "identifie"


class CodeCategorie(str, Enum):
    """Les quatre catégories d'obstacles issues de la revue de littérature."""

    ECONOMIQUE = "economique"
    ORGANISATIONNEL = "organisationnel"
    INFORMATIONNEL = "informationnel"
    SOCIAL = "social"


class Langue(str, Enum):
    """Langues prises en charge par l'interface."""

    FR = "fr"
    EN = "en"
    DE = "de"
    IT = "it"

    @classmethod
    def par_defaut(cls) -> "Langue":
        return cls.FR
