"""Génération d'un jeu de témoignages de démonstration.

Les situations décrites sont fictives. Elles sont construites à partir des
obstacles documentés dans la littérature, en particulier Phillips et al.
(2022) pour les barrières perçues par les patients, Kanter et al. (2020)
pour les facteurs organisationnels et Wehrli et al. (2024) pour le contexte
suisse. Aucune ne correspond à une personne réelle.
"""

import random
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.base_donnees import FabriqueSession, creer_tables
from app.depots.depot_obstacle import DepotObstacle
from app.modeles.entites import Maladie, Temoignage, TypeObstacle
from app.modeles.enumerations import (
    NiveauAnonymisation,
    RoleContributeur,
    StatutTemoignage,
)
from app.schemas import ObstacleSaisi, TemoignageSaisi
from app.services.service_temoignage import ServiceTemoignage

REGIONS = [
    "Genève", "Vaud", "Zurich", "Berne", "Bâle-Ville",
    "Tessin", "Valais", "Fribourg", "Neuchâtel",
]

TRANCHES_AGE = ["18-29", "30-39", "40-49", "50-59", "60 et plus"]

SITUATIONS = [
    {
        "titre": "Huit mois d'attente pour une consultation spécialisée",
        "recit": (
            "Après l'orientation par mon médecin traitant, il a fallu attendre "
            "plus de huit mois pour obtenir un rendez-vous dans un service "
            "d'hématologie. Entre-temps, j'ai eu deux crises qui ont nécessité "
            "un passage aux urgences, où personne ne connaissait mon dossier. "
            "Chaque fois, j'ai dû tout réexpliquer depuis le début."
        ),
        "obstacles": ["delai_rendez_vous", "coordination_defaillante"],
        "role": RoleContributeur.PATIENT,
        "severite": 4,
        "duree": 240,
    },
    {
        "titre": "Demande de prise en charge refusée par l'assurance",
        "recit": (
            "La demande de remboursement a été refusée au motif que le "
            "traitement ne figure pas sur la liste des prestations couvertes. "
            "Le médecin-conseil a demandé des pièces complémentaires que le "
            "service hospitalier avait pourtant déjà transmises. Six mois plus "
            "tard, la situation n'a pas avancé."
        ),
        "obstacles": ["refus_remboursement", "delai_administratif", "procedure_opaque"],
        "role": RoleContributeur.PATIENT,
        "severite": 5,
        "duree": 180,
    },
    {
        "titre": "Aucun centre de référence identifiable en Suisse",
        "recit": (
            "En tant qu'infirmière, j'ai cherché à orienter un patient vers un "
            "centre spécialisé dans les hémoglobinopathies. Je n'ai trouvé "
            "aucune structure officiellement désignée. Chaque hôpital renvoyait "
            "vers un autre, sans qu'aucun ne se déclare compétent."
        ),
        "obstacles": [
            "absence_centre_reference",
            "information_indisponible",
            "coordination_defaillante",
        ],
        "role": RoleContributeur.PROFESSIONNEL,
        "severite": 4,
        "duree": None,
    },
    {
        "titre": "Méconnaissance de la maladie aux urgences",
        "recit": (
            "Lors d'une crise vaso-occlusive, le personnel des urgences a mis "
            "plusieurs heures à administrer un traitement antalgique adapté. "
            "La douleur a été mise en doute. Ce n'est pas la première fois que "
            "cela arrive, et cela nous décourage d'aller consulter."
        ),
        "obstacles": [
            "meconnaissance_soignants",
            "stigmatisation",
            "delai_rendez_vous",
        ],
        "role": RoleContributeur.PROCHE,
        "severite": 5,
        "duree": None,
    },
    {
        "titre": "Trois ans avant d'obtenir un diagnostic",
        "recit": (
            "Les premiers symptômes sont apparus dans l'enfance. Il a fallu "
            "consulter cinq praticiens différents et attendre près de trois ans "
            "avant qu'un diagnostic soit posé. Aucun ne semblait avoir rencontré "
            "cette pathologie auparavant."
        ),
        "obstacles": ["errance_diagnostique", "meconnaissance_soignants"],
        "role": RoleContributeur.PATIENT,
        "severite": 4,
        "duree": 1095,
    },
    {
        "titre": "Trajets hebdomadaires de deux heures pour les transfusions",
        "recit": (
            "Le centre le plus proche capable d'assurer les transfusions se "
            "trouve à deux heures de trajet. Les frais de déplacement ne sont "
            "pas remboursés et les absences répétées ont fini par poser un "
            "problème avec mon employeur."
        ),
        "obstacles": [
            "transport_limite",
            "cout_deplacement",
            "impact_professionnel",
        ],
        "role": RoleContributeur.PATIENT,
        "severite": 3,
        "duree": None,
    },
    {
        "titre": "Informations contradictoires sur la procédure de demande",
        "recit": (
            "L'assurance indiquait que la demande devait être déposée par "
            "l'hôpital, l'hôpital renvoyait vers le médecin traitant, qui "
            "lui-même renvoyait vers l'assurance. Personne n'a su indiquer "
            "la procédure exacte à suivre."
        ),
        "obstacles": [
            "information_contradictoire",
            "procedure_opaque",
            "delai_administratif",
        ],
        "role": RoleContributeur.ASSOCIATION,
        "severite": 4,
        "duree": 90,
    },
    {
        "titre": "Barrière linguistique lors des consultations",
        "recit": (
            "Ma mère ne parle pas suffisamment le français pour suivre des "
            "explications médicales complexes. Aucun service d'interprétariat "
            "n'était disponible, et je devais traduire moi-même des informations "
            "que je ne comprenais pas toujours."
        ),
        "obstacles": ["barriere_linguistique", "meconnaissance_soignants"],
        "role": RoleContributeur.PROCHE,
        "severite": 3,
        "duree": None,
    },
    {
        "titre": "Absence de données sur la population concernée",
        "recit": (
            "En tant qu'association, nous ne disposons d'aucune estimation "
            "fiable du nombre de personnes concernées en Suisse. Cela nous "
            "empêche de documenter nos demandes auprès des autorités et des "
            "assureurs, qui nous réclament précisément ces chiffres."
        ),
        "obstacles": ["absence_donnees", "absence_voie_tarifaire"],
        "role": RoleContributeur.ASSOCIATION,
        "severite": 5,
        "duree": None,
    },
    {
        "titre": "Reste à charge important malgré la couverture",
        "recit": (
            "Même avec une prise en charge partielle, le reste à charge annuel "
            "représente une part importante du budget familial. Les frais "
            "annexes, déplacements, traitements de confort et absences "
            "professionnelles, ne sont pas couverts."
        ),
        "obstacles": ["reste_a_charge", "cout_deplacement", "perte_revenu"],
        "role": RoleContributeur.PATIENT,
        "severite": 4,
        "duree": None,
    },
    {
        "titre": "Refus de prise en charge par un service hospitalier",
        "recit": (
            "Un service a refusé de suivre le patient au motif qu'il ne "
            "disposait pas de l'expertise nécessaire. Aucune alternative n'a "
            "été proposée, et la famille a dû chercher elle-même une autre "
            "structure."
        ),
        "obstacles": ["refus_prise_en_charge", "absence_centre_reference"],
        "role": RoleContributeur.PROFESSIONNEL,
        "severite": 5,
        "duree": 60,
    },
    {
        "titre": "Isolement après le diagnostic",
        "recit": (
            "Après l'annonce du diagnostic, aucune orientation vers un soutien "
            "psychologique ou une association de patients n'a été proposée. "
            "Il a fallu chercher seul, et plusieurs mois ont passé avant de "
            "trouver un interlocuteur."
        ),
        "obstacles": ["isolement", "information_indisponible"],
        "role": RoleContributeur.PATIENT,
        "severite": 3,
        "duree": 150,
    },
    {
        "titre": "Procédure de remboursement d'exception peu lisible",
        "recit": (
            "La procédure de remboursement au cas par cas existe, mais ses "
            "critères ne sont pas publiés. Impossible de savoir à l'avance si "
            "un dossier a des chances d'aboutir, ni sur quels éléments il sera "
            "évalué."
        ),
        "obstacles": ["procedure_opaque", "absence_voie_tarifaire"],
        "role": RoleContributeur.ASSOCIATION,
        "severite": 4,
        "duree": None,
    },
    {
        "titre": "Coordination absente entre les intervenants",
        "recit": (
            "Le suivi implique un hématologue, un médecin traitant, un service "
            "de transfusion et parfois les urgences. Aucun d'eux n'a accès aux "
            "informations des autres. Le patient sert lui-même de lien entre "
            "les intervenants."
        ),
        "obstacles": ["coordination_defaillante", "meconnaissance_soignants"],
        "role": RoleContributeur.PROFESSIONNEL,
        "severite": 4,
        "duree": None,
    },
    {
        "titre": "Répercussions professionnelles des absences répétées",
        "recit": (
            "Les hospitalisations imprévisibles ont conduit à un changement de "
            "poste, puis à une réduction du taux d'activité. L'employeur s'est "
            "montré compréhensif au début, mais la situation est devenue "
            "difficile à tenir sur la durée."
        ),
        "obstacles": ["impact_professionnel", "perte_revenu"],
        "role": RoleContributeur.PATIENT,
        "severite": 4,
        "duree": None,
    },
]


def generer(nombre_supplementaires: int = 15) -> None:
    """Insère les témoignages de démonstration et les valide."""
    creer_tables()
    session = FabriqueSession()

    try:
        if session.query(Temoignage).count() > 0:
            print("Des témoignages existent déjà. Aucune insertion.")
            return

        depot = DepotObstacle(session)
        types_par_code = {t.code: t.id for t in depot.lister_types()}
        maladies = session.query(Maladie).all()

        if not types_par_code:
            print("Nomenclature absente. Exécutez d'abord initialiser_donnees.py.")
            return

        service = ServiceTemoignage(session)
        random.seed(42)
        total = 0

        situations = SITUATIONS + random.choices(
            SITUATIONS, k=nombre_supplementaires
        )

        for index, situation in enumerate(situations):
            identifiants = [
                types_par_code[code]
                for code in situation["obstacles"]
                if code in types_par_code
            ]
            if not identifiants:
                continue

            saisie = TemoignageSaisi(
                role=situation["role"],
                region=random.choice(REGIONS),
                tranche_age=random.choice(TRANCHES_AGE),
                maladie_id=random.choice(maladies).id,
                titre=situation["titre"],
                recit=situation["recit"],
                date_evenement=date.today()
                - timedelta(days=random.randint(30, 900)),
                obstacles=[
                    ObstacleSaisi(
                        type_obstacle_id=identifiant,
                        severite=max(
                            1, min(5, situation["severite"] + random.randint(-1, 1))
                        ),
                        duree_jours=situation["duree"],
                    )
                    for identifiant in identifiants
                ],
                niveau_anonymisation=random.choice(list(NiveauAnonymisation)),
                autorise_publication=True,
                autorise_plaidoyer=index % 3 != 0,
                consentement_donne=True,
            )

            temoignage = service.deposer(saisie)

            # Quelques témoignages restent en attente de validation
            if index % 7 != 0:
                service.valider(temoignage)
            total += 1

        valides = (
            session.query(Temoignage)
            .filter(Temoignage.statut == StatutTemoignage.VALIDE.value)
            .count()
        )
        print(f"{total} témoignages insérés, dont {valides} validés.")

    finally:
        session.close()


if __name__ == "__main__":
    generer()
