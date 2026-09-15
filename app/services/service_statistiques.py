"""Calcul des indicateurs agrégés présentés dans le tableau de bord.

Les indicateurs sont conçus pour être compréhensibles par des acteurs non
spécialistes, conformément au constat établi en section 2.7.2 : la valeur
d'un système d'information tient moins à la collecte qu'à la capacité de
restituer une information appropriable par ceux qui décident.
"""

from collections import Counter

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modeles.entites import (
    CategorieObstacle,
    Contributeur,
    ObstacleSignale,
    Temoignage,
    TraductionCategorie,
    TraductionType,
    TypeObstacle,
)
from app.modeles.enumerations import StatutTemoignage


class ServiceStatistiques:
    """Produit les indicateurs agrégés à partir des témoignages publiés."""

    STATUTS_RETENUS = (StatutTemoignage.VALIDE, StatutTemoignage.PUBLIE)

    def __init__(self, session: Session, langue: str = "fr") -> None:
        self.session = session
        self.langue = langue

    def _filtre_statut(self):
        """Restreint l'analyse aux témoignages validés ou publiés."""
        return Temoignage.statut.in_([s.value for s in self.STATUTS_RETENUS])

    def compter_temoignages(self) -> int:
        """Nombre de témoignages retenus pour l'analyse."""
        requete = select(func.count(Temoignage.id)).where(self._filtre_statut())
        return self.session.execute(requete).scalar_one()

    def compter_obstacles(self) -> int:
        """Nombre total d'obstacles signalés."""
        requete = (
            select(func.count(ObstacleSignale.id))
            .join(Temoignage)
            .where(self._filtre_statut())
        )
        return self.session.execute(requete).scalar_one()

    def repartition_par_categorie(self) -> list[dict]:
        """Nombre de signalements par catégorie d'obstacle.

        Le libellé retourné est celui de la langue courante lorsqu'une
        traduction existe, et le libellé source sinon.
        """
        requete = (
            select(
                func.coalesce(
                    TraductionCategorie.libelle, CategorieObstacle.libelle
                ).label("libelle"),
                func.count(ObstacleSignale.id).label("effectif"),
            )
            .select_from(ObstacleSignale)
            .join(TypeObstacle, ObstacleSignale.type_obstacle_id == TypeObstacle.id)
            .join(CategorieObstacle, TypeObstacle.categorie_id == CategorieObstacle.id)
            .join(Temoignage, ObstacleSignale.temoignage_id == Temoignage.id)
            .outerjoin(
                TraductionCategorie,
                (TraductionCategorie.categorie_id == CategorieObstacle.id)
                & (TraductionCategorie.langue == self.langue),
            )
            .where(self._filtre_statut())
            .group_by(
                func.coalesce(
                    TraductionCategorie.libelle, CategorieObstacle.libelle
                )
            )
            .order_by(func.count(ObstacleSignale.id).desc())
        )
        resultats = self.session.execute(requete).all()
        total = sum(effectif for _, effectif in resultats) or 1

        return [
            {
                "libelle": libelle,
                "effectif": effectif,
                "pourcentage": round(effectif / total * 100, 1),
            }
            for libelle, effectif in resultats
        ]

    def obstacles_les_plus_signales(self, limite: int = 10) -> list[dict]:
        """Types d'obstacles les plus fréquemment signalés."""
        requete = (
            select(
                func.coalesce(
                    TraductionType.libelle, TypeObstacle.libelle
                ).label("libelle"),
                func.coalesce(
                    TraductionCategorie.libelle, CategorieObstacle.libelle
                ).label("categorie"),
                func.count(ObstacleSignale.id).label("effectif"),
                func.avg(ObstacleSignale.severite).label("severite_moyenne"),
            )
            .select_from(ObstacleSignale)
            .join(TypeObstacle, ObstacleSignale.type_obstacle_id == TypeObstacle.id)
            .join(CategorieObstacle, TypeObstacle.categorie_id == CategorieObstacle.id)
            .join(Temoignage, ObstacleSignale.temoignage_id == Temoignage.id)
            .outerjoin(
                TraductionType,
                (TraductionType.type_obstacle_id == TypeObstacle.id)
                & (TraductionType.langue == self.langue),
            )
            .outerjoin(
                TraductionCategorie,
                (TraductionCategorie.categorie_id == CategorieObstacle.id)
                & (TraductionCategorie.langue == self.langue),
            )
            .where(self._filtre_statut())
            .group_by(
                func.coalesce(TraductionType.libelle, TypeObstacle.libelle),
                func.coalesce(
                    TraductionCategorie.libelle, CategorieObstacle.libelle
                ),
            )
            .order_by(func.count(ObstacleSignale.id).desc())
            .limit(limite)
        )

        return [
            {
                "libelle": libelle,
                "categorie": categorie,
                "effectif": effectif,
                "severite_moyenne": round(severite or 0, 1),
            }
            for libelle, categorie, effectif, severite in self.session.execute(
                requete
            ).all()
        ]

    def repartition_par_role(self) -> list[dict]:
        """Répartition des témoignages selon la qualité du contributeur."""
        requete = (
            select(Contributeur.role, func.count(Temoignage.id))
            .select_from(Temoignage)
            .join(Contributeur, Temoignage.contributeur_id == Contributeur.id)
            .where(self._filtre_statut())
            .group_by(Contributeur.role)
            .order_by(func.count(Temoignage.id).desc())
        )
        return [
            {"role": role, "effectif": effectif}
            for role, effectif in self.session.execute(requete).all()
        ]

    def duree_moyenne_blocage(self) -> float | None:
        """Durée moyenne, en jours, des blocages renseignés."""
        requete = (
            select(func.avg(ObstacleSignale.duree_jours))
            .join(Temoignage)
            .where(self._filtre_statut())
            .where(ObstacleSignale.duree_jours.isnot(None))
        )
        moyenne = self.session.execute(requete).scalar_one_or_none()
        return round(moyenne, 1) if moyenne is not None else None

    def synthese(self) -> dict:
        """Regroupe l'ensemble des indicateurs pour le tableau de bord."""
        return {
            "nombre_temoignages": self.compter_temoignages(),
            "nombre_obstacles": self.compter_obstacles(),
            "par_categorie": self.repartition_par_categorie(),
            "obstacles_frequents": self.obstacles_les_plus_signales(),
            "par_role": self.repartition_par_role(),
            "duree_moyenne_blocage": self.duree_moyenne_blocage(),
        }
