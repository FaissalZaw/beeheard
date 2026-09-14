"""Tests du service d'anonymisation."""

from app.modeles.enumerations import NiveauAnonymisation
from app.services.service_anonymisation import (
    appliquer_anonymisation,
    generer_pseudonyme,
)


def test_pseudonyme_respecte_le_format() -> None:
    pseudonyme = generer_pseudonyme()
    assert pseudonyme.startswith("Contributeur-")
    assert len(pseudonyme) == len("Contributeur-") + 5


def test_pseudonymes_successifs_sont_distincts() -> None:
    pseudonymes = {generer_pseudonyme() for _ in range(100)}
    assert len(pseudonymes) == 100


def test_anonymisation_complete_supprime_tout_attribut_contextuel() -> None:
    region, tranche = appliquer_anonymisation(
        "Genève", "30-39", NiveauAnonymisation.COMPLET
    )
    assert region is None
    assert tranche is None


def test_anonymisation_partielle_conserve_la_region() -> None:
    region, tranche = appliquer_anonymisation(
        "Genève", "30-39", NiveauAnonymisation.PARTIEL
    )
    assert region == "Genève"
    assert tranche is None


def test_niveau_identifie_conserve_les_attributs() -> None:
    region, tranche = appliquer_anonymisation(
        "Genève", "30-39", NiveauAnonymisation.IDENTIFIE
    )
    assert region == "Genève"
    assert tranche == "30-39"
