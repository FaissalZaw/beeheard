"""Configuration commune aux tests.

Une base de données en mémoire est créée pour chaque test, garantissant
l'indépendance et la reproductibilité des exécutions.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.base_donnees import Base
from app.modeles.entites import CategorieObstacle, Maladie, TypeObstacle


@pytest.fixture
def session() -> Session:
    """Fournit une session sur une base de données en mémoire."""
    moteur = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=moteur)
    fabrique = sessionmaker(bind=moteur, expire_on_commit=False)
    session = fabrique()
    yield session
    session.close()


@pytest.fixture
def nomenclature(session: Session) -> dict:
    """Insère une nomenclature minimale et retourne les identifiants utiles."""
    categorie = CategorieObstacle(
        code="organisationnel",
        libelle="Obstacles organisationnels",
    )
    session.add(categorie)
    session.flush()

    type_obstacle = TypeObstacle(
        categorie_id=categorie.id,
        code="delai_rendez_vous",
        libelle="Délai d'obtention d'un rendez-vous",
    )
    maladie = Maladie(nom="Drépanocytose", code_orpha="232")
    session.add_all([type_obstacle, maladie])
    session.commit()

    return {
        "categorie_id": categorie.id,
        "type_obstacle_id": type_obstacle.id,
        "maladie_id": maladie.id,
    }
