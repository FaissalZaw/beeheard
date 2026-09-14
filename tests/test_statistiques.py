"""Tests du service de calcul des indicateurs agrégés."""

from sqlalchemy.orm import Session

from app.modeles.enumerations import RoleContributeur
from app.schemas import ObstacleSaisi, TemoignageSaisi
from app.services.service_statistiques import ServiceStatistiques
from app.services.service_temoignage import ServiceTemoignage


def deposer_et_valider(
    session: Session, nomenclature: dict, severite: int = 3, duree: int | None = None
) -> None:
    """Dépose un témoignage puis le valide, afin qu'il entre dans les statistiques."""
    service = ServiceTemoignage(session)
    saisie = TemoignageSaisi(
        role=RoleContributeur.PATIENT,
        maladie_id=nomenclature["maladie_id"],
        titre="Témoignage de démonstration",
        recit="Récit suffisamment long pour satisfaire la validation du schéma.",
        obstacles=[
            ObstacleSaisi(
                type_obstacle_id=nomenclature["type_obstacle_id"],
                severite=severite,
                duree_jours=duree,
            )
        ],
        consentement_donne=True,
    )
    temoignage = service.deposer(saisie)
    service.valider(temoignage)


def test_aucun_temoignage_donne_des_indicateurs_nuls(
    session: Session, nomenclature: dict
) -> None:
    statistiques = ServiceStatistiques(session)
    assert statistiques.compter_temoignages() == 0
    assert statistiques.compter_obstacles() == 0
    assert statistiques.repartition_par_categorie() == []


def test_seuls_les_temoignages_valides_sont_comptes(
    session: Session, nomenclature: dict
) -> None:
    service = ServiceTemoignage(session)
    saisie = TemoignageSaisi(
        role=RoleContributeur.PATIENT,
        maladie_id=nomenclature["maladie_id"],
        titre="Témoignage soumis mais non validé",
        recit="Récit suffisamment long pour satisfaire la validation du schéma.",
        obstacles=[ObstacleSaisi(type_obstacle_id=nomenclature["type_obstacle_id"])],
        consentement_donne=True,
    )
    service.deposer(saisie)

    statistiques = ServiceStatistiques(session)
    assert statistiques.compter_temoignages() == 0


def test_comptage_des_temoignages_valides(session: Session, nomenclature: dict) -> None:
    for _ in range(3):
        deposer_et_valider(session, nomenclature)

    statistiques = ServiceStatistiques(session)
    assert statistiques.compter_temoignages() == 3
    assert statistiques.compter_obstacles() == 3


def test_repartition_par_categorie(session: Session, nomenclature: dict) -> None:
    deposer_et_valider(session, nomenclature)

    repartition = ServiceStatistiques(session).repartition_par_categorie()
    assert len(repartition) == 1
    assert repartition[0]["effectif"] == 1
    assert repartition[0]["pourcentage"] == 100.0


def test_obstacles_les_plus_signales(session: Session, nomenclature: dict) -> None:
    deposer_et_valider(session, nomenclature, severite=4)
    deposer_et_valider(session, nomenclature, severite=2)

    obstacles = ServiceStatistiques(session).obstacles_les_plus_signales()
    assert obstacles[0]["effectif"] == 2
    assert obstacles[0]["severite_moyenne"] == 3.0


def test_duree_moyenne_ignore_les_valeurs_absentes(
    session: Session, nomenclature: dict
) -> None:
    deposer_et_valider(session, nomenclature, duree=10)
    deposer_et_valider(session, nomenclature, duree=20)
    deposer_et_valider(session, nomenclature, duree=None)

    assert ServiceStatistiques(session).duree_moyenne_blocage() == 15.0


def test_synthese_contient_toutes_les_cles(
    session: Session, nomenclature: dict
) -> None:
    deposer_et_valider(session, nomenclature)

    synthese = ServiceStatistiques(session).synthese()
    for cle in (
        "nombre_temoignages",
        "nombre_obstacles",
        "par_categorie",
        "obstacles_frequents",
        "par_role",
        "duree_moyenne_blocage",
    ):
        assert cle in synthese
