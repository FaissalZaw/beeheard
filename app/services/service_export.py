"""Export des données agrégées à des fins de recherche.

Ce module met en oeuvre les principes FAIR (Wilkinson et al. 2016) dans les
limites que permet un prototype. Les données exportées sont dérivées des
témoignages ayant fait l'objet d'un consentement explicite à la recherche.

Le récit intégral n'est jamais exporté : seule la qualification structurée
l'est, accompagnée d'attributs contextuels grossiers. Cette restriction
répond au risque de réidentification, particulièrement élevé dans le champ
des maladies rares où un petit nombre d'attributs peut suffire à identifier
une personne.
"""

import csv
import io
import json
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config import VERSION
from app.modeles.entites import ObstacleSignale, Temoignage
from app.modeles.enumerations import StatutTemoignage

VERSION_SCHEMA = "1.0"
LICENCE = "CC BY 4.0"

COLONNES = [
    "identifiant_signalement",
    "identifiant_temoignage",
    "role_contributeur",
    "region",
    "tranche_age",
    "pathologie",
    "code_orpha",
    "categorie_obstacle",
    "type_obstacle",
    "severite",
    "duree_jours",
    "annee_evenement",
    "langue_saisie",
    "longueur_recit",
]


class ServiceExport:
    """Produit des jeux de données réutilisables à partir des témoignages."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def _temoignages_exportables(self) -> list[Temoignage]:
        """Retourne les témoignages dont l'export est autorisé.

        Seuls entrent dans l'export les témoignages validés ou publiés dont
        le contributeur a consenti à un usage de recherche ou de plaidoyer.
        """
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
            .where(
                Temoignage.statut.in_(
                    [StatutTemoignage.VALIDE.value, StatutTemoignage.PUBLIE.value]
                )
            )
        )

        return [
            t
            for t in self.session.execute(requete).scalars().all()
            if t.consentement is not None and t.consentement.autorise_plaidoyer
        ]

    def lignes(self, langue: str = "fr") -> list[dict]:
        """Produit une ligne par obstacle signalé.

        Le grain retenu est le signalement et non le témoignage, ce qui
        permet une analyse directe des fréquences et des cooccurrences.
        """
        lignes = []

        for temoignage in self._temoignages_exportables():
            for obstacle in temoignage.obstacles:
                type_obstacle = obstacle.type_obstacle
                lignes.append(
                    {
                        "identifiant_signalement": f"OBS-{obstacle.id:05d}",
                        "identifiant_temoignage": f"TEM-{temoignage.id:05d}",
                        "role_contributeur": temoignage.contributeur.role,
                        "region": temoignage.contributeur.region or "",
                        "tranche_age": temoignage.contributeur.tranche_age or "",
                        "pathologie": temoignage.maladie.nom,
                        "code_orpha": temoignage.maladie.code_orpha or "",
                        "categorie_obstacle": type_obstacle.categorie.code,
                        "type_obstacle": type_obstacle.code,
                        "severite": obstacle.severite,
                        "duree_jours": obstacle.duree_jours
                        if obstacle.duree_jours is not None
                        else "",
                        "annee_evenement": temoignage.date_evenement.year
                        if temoignage.date_evenement
                        else "",
                        "langue_saisie": temoignage.langue,
                        "longueur_recit": len(temoignage.recit),
                    }
                )

        return lignes

    def metadonnees(self) -> dict:
        """Décrit le jeu de données, condition de sa réutilisabilité."""
        lignes = self.lignes()

        return {
            "titre": "BeeHeard, obstacles d'accès aux soins et aux traitements",
            "description": (
                "Qualification structurée des obstacles d'accès rapportés par "
                "des patients, des proches, des professionnels de santé et des "
                "représentants d'associations. Une ligne par obstacle signalé."
            ),
            "version_schema": VERSION_SCHEMA,
            "version_application": VERSION,
            "date_generation": datetime.now().isoformat(timespec="seconds"),
            "licence": LICENCE,
            "nombre_signalements": len(lignes),
            "nombre_temoignages": len({l["identifiant_temoignage"] for l in lignes}),
            "avertissement": (
                "Jeu de données de démonstration. Les témoignages sources sont "
                "fictifs et ne reflètent pas de situations réelles."
            ),
            "restrictions": (
                "Le récit intégral n'est pas exporté. Seuls figurent les "
                "attributs structurés et des variables contextuelles "
                "grossières, afin de prévenir toute réidentification."
            ),
            "nomenclature": (
                "Les codes de catégories et de types d'obstacles sont dérivés "
                "de la littérature scientifique sur l'accès aux soins. Leur "
                "définition est consultable sur la page À propos."
            ),
            "colonnes": [
                {"nom": "identifiant_signalement", "type": "chaîne",
                 "description": "Identifiant du signalement, stable dans le jeu"},
                {"nom": "identifiant_temoignage", "type": "chaîne",
                 "description": "Identifiant du témoignage d'origine, permet "
                                "le regroupement des obstacles cooccurrents"},
                {"nom": "role_contributeur", "type": "catégoriel",
                 "description": "patient, proche, professionnel, association"},
                {"nom": "region", "type": "catégoriel",
                 "description": "Canton, vide si anonymisation complète"},
                {"nom": "tranche_age", "type": "catégoriel",
                 "description": "Vide sauf anonymisation étendue"},
                {"nom": "pathologie", "type": "chaîne",
                 "description": "Nom de la pathologie concernée"},
                {"nom": "code_orpha", "type": "chaîne",
                 "description": "Identifiant Orphanet, permet l'alignement "
                                "sur une nomenclature internationale"},
                {"nom": "categorie_obstacle", "type": "catégoriel",
                 "description": "economique, organisationnel, informationnel, "
                                "social"},
                {"nom": "type_obstacle", "type": "catégoriel",
                 "description": "Code du type d'obstacle signalé"},
                {"nom": "severite", "type": "entier",
                 "description": "Gravité ressentie, de 1 à 5"},
                {"nom": "duree_jours", "type": "entier",
                 "description": "Durée du blocage, vide si non renseignée"},
                {"nom": "annee_evenement", "type": "entier",
                 "description": "Année seule, le jour et le mois étant "
                                "retirés pour limiter la réidentification"},
                {"nom": "langue_saisie", "type": "catégoriel",
                 "description": "Langue dans laquelle le témoignage a été "
                                "déposé"},
                {"nom": "longueur_recit", "type": "entier",
                 "description": "Nombre de caractères du récit, indicateur "
                                "de richesse sans exposer le contenu"},
            ],
        }

    def vers_csv(self) -> str:
        """Sérialise le jeu de données au format CSV."""
        tampon = io.StringIO()
        redacteur = csv.DictWriter(tampon, fieldnames=COLONNES, delimiter=";")
        redacteur.writeheader()
        redacteur.writerows(self.lignes())
        return tampon.getvalue()

    def vers_json(self) -> dict:
        """Sérialise le jeu de données au format JSON, métadonnées incluses."""
        return {
            "metadonnees": self.metadonnees(),
            "donnees": self.lignes(),
        }

    def nom_fichier(self, extension: str) -> str:
        """Compose un nom de fichier horodaté."""
        return f"beeheard-obstacles-{date.today().isoformat()}.{extension}"
