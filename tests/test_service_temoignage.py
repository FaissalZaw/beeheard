"""Tests du service de gestion des témoignages."""

import pytest
from sqlalchemy.orm import Session

from app.modeles.enumerations import (
    NiveauAnonymisation,
    RoleContributeur,
    StatutTemoignage,
)
from app.schemas import ObstacleSaisi, TemoignageSaisi
from app.services.service_temoignage import (
    ConsentementManquantError,
    ServiceTemoignage,
    TransitionInterditeError,
)


def construire_saisie(nomenclature: dict, **surcharges) -> TemoignageSaisi:
    """Fabrique une saisie valide, modifiable par les arguments nommés."""
    donnees = {
        "role": RoleContributeur.PATIENT,
        "region": "Genève",
        "tranche_age": "30-39",
        "maladie_id": nomenclature["maladie_id"],
        "titre": "Huit mois d'attente pour un rendez-vous",
        "recit": "J'ai attendu plus de huit mois avant d'obtenir une consultation.",
        "obstacles": [ObstacleSaisi(type_obstacle_id=nomenclature["type_obstacle_id"])],
        "consentement_donne": True,
    }
    donnees.update(surcharges)
    return TemoignageSaisi(**donnees)


def test_depot_cree_un_temoignage_au_statut_soumis(
    session: Session, nomenclature: dict
) -> None:
    service = ServiceTemoignage(session)
    temoignage = service.deposer(construire_saisie(nomenclature))

    assert temoignage.id is not None
    assert temoignage.statut == StatutTemoignage.SOUMIS


def test_depot_sans_consentement_est_refuse(
    session: Session, nomenclature: dict
) -> None:
    service = ServiceTemoignage(session)
    saisie = construire_saisie(nomenclature, consentement_donne=False)

    with pytest.raises(ConsentementManquantError):
        service.deposer(saisie)


def test_depot_genere_un_pseudonyme(session: Session, nomenclature: dict) -> None:
    service = ServiceTemoignage(session)
    temoignage = service.deposer(construire_saisie(nomenclature))

    assert temoignage.contributeur.pseudonyme.startswith("BH-")


def test_anonymisation_complete_est_appliquee_au_depot(
    session: Session, nomenclature: dict
) -> None:
    service = ServiceTemoignage(session)
    temoignage = service.deposer(
        construire_saisie(
            nomenclature, niveau_anonymisation=NiveauAnonymisation.COMPLET
        )
    )

    assert temoignage.contributeur.region is None
    assert temoignage.contributeur.tranche_age is None


def test_consentement_est_trace(session: Session, nomenclature: dict) -> None:
    service = ServiceTemoignage(session)
    temoignage = service.deposer(construire_saisie(nomenclature))

    assert temoignage.consentement is not None
    assert temoignage.consentement.version_texte == "1.0"
    assert temoignage.consentement.date_consentement is not None


def test_obstacles_sont_enregistres(session: Session, nomenclature: dict) -> None:
    service = ServiceTemoignage(session)
    temoignage = service.deposer(construire_saisie(nomenclature))

    assert len(temoignage.obstacles) == 1
    assert temoignage.obstacles[0].type_obstacle_id == nomenclature["type_obstacle_id"]


def test_transition_soumis_vers_valide_est_autorisee(
    session: Session, nomenclature: dict
) -> None:
    service = ServiceTemoignage(session)
    temoignage = service.deposer(construire_saisie(nomenclature))

    service.valider(temoignage)
    assert temoignage.statut == StatutTemoignage.VALIDE


def test_transition_soumis_vers_publie_est_interdite(
    session: Session, nomenclature: dict
) -> None:
    service = ServiceTemoignage(session)
    temoignage = service.deposer(construire_saisie(nomenclature))

    with pytest.raises(TransitionInterditeError):
        service.publier(temoignage)


def test_temoignage_rejete_ne_peut_plus_evoluer(
    session: Session, nomenclature: dict
) -> None:
    service = ServiceTemoignage(session)
    temoignage = service.deposer(construire_saisie(nomenclature))
    service.rejeter(temoignage)

    with pytest.raises(TransitionInterditeError):
        service.valider(temoignage)


def test_parcours_complet_jusqu_a_publication(
    session: Session, nomenclature: dict
) -> None:
    service = ServiceTemoignage(session)
    temoignage = service.deposer(construire_saisie(nomenclature))

    service.valider(temoignage)
    service.publier(temoignage)

    assert temoignage.statut == StatutTemoignage.PUBLIE
