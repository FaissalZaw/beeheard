"""Connexion à la base de données et gestion des sessions."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import URL_BASE_DONNEES


class Base(DeclarativeBase):
    """Classe de base dont héritent toutes les entités."""


moteur = create_engine(
    URL_BASE_DONNEES,
    connect_args={"check_same_thread": False},
)

FabriqueSession = sessionmaker(bind=moteur, autoflush=False, expire_on_commit=False)


def obtenir_session() -> Generator[Session, None, None]:
    """Fournit une session de base de données, fermée automatiquement."""
    session = FabriqueSession()
    try:
        yield session
    finally:
        session.close()


def creer_tables() -> None:
    """Crée l'ensemble des tables définies par les entités."""
    from app.modeles import entites  # noqa: F401

    Base.metadata.create_all(bind=moteur)
