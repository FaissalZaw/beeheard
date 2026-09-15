"""Tests d'intégration des parcours applicatifs.

Ces tests exercent la chaîne complète, de la requête HTTP jusqu'à la
persistance, sur une base de données isolée créée pour chaque exécution.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.base_donnees import Base, obtenir_session
from app.modeles.entites import CategorieObstacle, Maladie, TypeObstacle
from main import app


@pytest.fixture
def client() -> TestClient:
    """Fournit un client de test connecté à une base isolée."""
    moteur = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=moteur)
    fabrique = sessionmaker(bind=moteur, expire_on_commit=False)

    session = fabrique()
    categorie = CategorieObstacle(code="organisationnel", libelle="Organisationnels")
    session.add(categorie)
    session.flush()
    session.add(
        TypeObstacle(
            categorie_id=categorie.id,
            code="delai_rendez_vous",
            libelle="Délai de rendez-vous",
        )
    )
    session.add(Maladie(nom="Drépanocytose", code_orpha="232"))
    session.commit()

    def remplacer_session():
        nouvelle = fabrique()
        try:
            yield nouvelle
        finally:
            nouvelle.close()

    app.dependency_overrides[obtenir_session] = remplacer_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    session.close()


def test_sonde_de_sante(client: TestClient) -> None:
    reponse = client.get("/sante")
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "operationnel"


def test_tableau_de_bord_est_accessible(client: TestClient) -> None:
    reponse = client.get("/tableau-de-bord")
    assert reponse.status_code == 200
    assert "Obstacles d'accès aux traitements" in reponse.text


def test_formulaire_affiche_la_nomenclature(client: TestClient) -> None:
    reponse = client.get("/temoignage")
    assert reponse.status_code == 200
    assert "Délai de rendez-vous" in reponse.text
    assert "Drépanocytose" in reponse.text


def test_depot_complet_redirige_vers_la_confirmation(client: TestClient) -> None:
    reponse = client.post(
        "/temoignage",
        data={
            "role": "patient",
            "maladie_id": 1,
            "titre": "Attente prolongée avant consultation",
            "recit": "Le délai d'obtention d'un rendez-vous a dépassé six mois.",
            "obstacles": [1],
            "severite": 4,
            "niveau_anonymisation": "complet",
            "consentement_donne": "true",
        },
        follow_redirects=False,
    )
    assert reponse.status_code == 303
    assert reponse.headers["location"].startswith("/temoignage/confirmation")
    assert "reference=Contributeur-" in reponse.headers["location"]


def test_depot_sans_consentement_est_refuse(client: TestClient) -> None:
    reponse = client.post(
        "/temoignage",
        data={
            "role": "patient",
            "maladie_id": 1,
            "titre": "Attente prolongée avant consultation",
            "recit": "Le délai d'obtention d'un rendez-vous a dépassé six mois.",
            "obstacles": [1],
            "severite": 4,
            "niveau_anonymisation": "complet",
        },
    )
    assert reponse.status_code == 400
    assert "consentement" in reponse.text.lower()


def test_depot_sans_obstacle_est_refuse(client: TestClient) -> None:
    reponse = client.post(
        "/temoignage",
        data={
            "role": "patient",
            "maladie_id": 1,
            "titre": "Attente prolongée avant consultation",
            "recit": "Le délai d'obtention d'un rendez-vous a dépassé six mois.",
            "severite": 4,
            "niveau_anonymisation": "complet",
            "consentement_donne": "true",
        },
    )
    assert reponse.status_code == 400
    assert "obstacle" in reponse.text.lower()


def test_api_statistiques_retourne_la_synthese(client: TestClient) -> None:
    reponse = client.get("/api/statistiques")
    assert reponse.status_code == 200
    donnees = reponse.json()
    assert "nombre_temoignages" in donnees
    assert "par_categorie" in donnees


def test_fiche_de_synthese_est_generee(client: TestClient) -> None:
    reponse = client.get("/synthese")
    assert reponse.status_code == 200
    assert "Fiche de synthèse" in reponse.text


def test_page_de_confirmation(client: TestClient) -> None:
    reponse = client.get("/temoignage/confirmation")
    assert reponse.status_code == 200
    assert "enregistré" in reponse.text
