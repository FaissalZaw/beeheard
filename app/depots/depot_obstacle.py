"""Accès aux données relatives à la nomenclature des obstacles."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modeles.entites import CategorieObstacle, Maladie, TypeObstacle


class DepotObstacle:
    """Encapsule la consultation de la nomenclature."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def lister_categories(self) -> list[CategorieObstacle]:
        """Retourne les catégories avec leurs types d'obstacles."""
        requete = select(CategorieObstacle).options(
            selectinload(CategorieObstacle.types)
        )
        return list(self.session.execute(requete).scalars().all())

    def lister_types(self) -> list[TypeObstacle]:
        """Retourne l'ensemble des types d'obstacles."""
        requete = select(TypeObstacle).options(
            selectinload(TypeObstacle.categorie)
        )
        return list(self.session.execute(requete).scalars().all())

    def obtenir_type_par_id(self, identifiant: int) -> TypeObstacle | None:
        """Retourne un type d'obstacle par son identifiant."""
        return self.session.get(TypeObstacle, identifiant)

    def lister_maladies(self) -> list[Maladie]:
        """Retourne les maladies enregistrées."""
        return list(self.session.execute(select(Maladie)).scalars().all())
