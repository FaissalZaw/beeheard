"""Logique métier relative aux témoignages."""

from sqlalchemy.orm import Session

from app.config import VERSION_CONSENTEMENT
from app.depots.depot_obstacle import DepotObstacle
from app.depots.depot_temoignage import DepotTemoignage
from app.modeles.entites import (
    Consentement,
    Contributeur,
    ObstacleSignale,
    Temoignage,
)
from app.modeles.enumerations import StatutTemoignage
from app.schemas import TemoignageSaisi
from app.services.service_anonymisation import (
    appliquer_anonymisation,
    generer_pseudonyme,
)
from app.services.service_acces import calculer_empreinte, generer_code
from app.services.service_titre import generer_titre

TRANSITIONS_AUTORISEES: dict[StatutTemoignage, set[StatutTemoignage]] = {
    StatutTemoignage.BROUILLON: {StatutTemoignage.SOUMIS},
    StatutTemoignage.SOUMIS: {StatutTemoignage.VALIDE, StatutTemoignage.REJETE},
    StatutTemoignage.VALIDE: {StatutTemoignage.PUBLIE, StatutTemoignage.REJETE},
    StatutTemoignage.PUBLIE: set(),
    StatutTemoignage.REJETE: set(),
}


class ConsentementManquantError(Exception):
    """Levée lorsqu'un témoignage est déposé sans consentement explicite."""


class TransitionInterditeError(Exception):
    """Levée lorsqu'une transition d'état n'est pas autorisée."""


class ServiceTemoignage:
    """Orchestre le dépôt et le cycle de vie des témoignages."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.depot = DepotTemoignage(session)
        self.depot_obstacle = DepotObstacle(session)

    def deposer(self, saisie: TemoignageSaisi) -> Temoignage:
        """Enregistre un témoignage et le place au statut Soumis.

        Le consentement explicite conditionne l'enregistrement : sans lui,
        aucune donnée n'est persistée.
        """
        if not saisie.consentement_donne:
            raise ConsentementManquantError(
                "Le dépôt d'un témoignage requiert un consentement explicite."
            )

        region, tranche_age = appliquer_anonymisation(
            saisie.region, saisie.tranche_age, saisie.niveau_anonymisation
        )

        code_acces = generer_code()

        contributeur = Contributeur(
            pseudonyme=generer_pseudonyme(),
            empreinte_code=calculer_empreinte(code_acces),
            role=saisie.role,
            region=region,
            tranche_age=tranche_age,
        )
        self.depot.ajouter_contributeur(contributeur)

        titre = saisie.titre.strip() if saisie.titre else ""
        if not titre:
            titre = generer_titre(saisie.recit)

        temoignage = Temoignage(
            contributeur_id=contributeur.id,
            maladie_id=saisie.maladie_id,
            titre=titre,
            recit=saisie.recit,
            date_evenement=saisie.date_evenement,
            langue=saisie.langue,
            statut=StatutTemoignage.SOUMIS,
        )

        for obstacle in saisie.obstacles:
            temoignage.obstacles.append(
                ObstacleSignale(
                    type_obstacle_id=obstacle.type_obstacle_id,
                    severite=obstacle.severite,
                    duree_jours=obstacle.duree_jours,
                    commentaire=obstacle.commentaire,
                )
            )

        temoignage.consentement = Consentement(
            version_texte=VERSION_CONSENTEMENT,
            niveau_anonymisation=saisie.niveau_anonymisation,
            autorise_publication=saisie.autorise_publication,
            autorise_plaidoyer=saisie.autorise_plaidoyer,
        )

        temoignage = self.depot.ajouter(temoignage)
        # Le code en clair n'est disponible qu'à cet instant, pour affichage
        temoignage.code_acces_en_clair = code_acces
        return temoignage

    def changer_statut(
        self, temoignage: Temoignage, nouveau_statut: StatutTemoignage
    ) -> Temoignage:
        """Fait évoluer le statut d'un témoignage si la transition est permise."""
        statut_actuel = StatutTemoignage(temoignage.statut)

        if nouveau_statut not in TRANSITIONS_AUTORISEES[statut_actuel]:
            raise TransitionInterditeError(
                f"Transition interdite de {statut_actuel.value} "
                f"vers {nouveau_statut.value}."
            )
        return self.depot.mettre_a_jour_statut(temoignage, nouveau_statut)

    def valider(self, temoignage: Temoignage) -> Temoignage:
        """Valide un témoignage soumis."""
        return self.changer_statut(temoignage, StatutTemoignage.VALIDE)

    def rejeter(self, temoignage: Temoignage) -> Temoignage:
        """Rejette un témoignage."""
        return self.changer_statut(temoignage, StatutTemoignage.REJETE)

    def publier(self, temoignage: Temoignage) -> Temoignage:
        """Publie un témoignage validé."""
        return self.changer_statut(temoignage, StatutTemoignage.PUBLIE)
