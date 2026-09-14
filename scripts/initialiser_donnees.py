"""Initialisation de la nomenclature et du jeu de données de démonstration.

La nomenclature des obstacles est dérivée de la revue de littérature :
- les quatre catégories correspondent à la structure de la section 2.5
- les types d'obstacles reprennent les barrières documentées par
  Phillips et al. (2022), Kanter et al. (2020) et Wehrli et al. (2024)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.base_donnees import FabriqueSession, creer_tables
from app.modeles.entites import CategorieObstacle, Maladie, TypeObstacle

CATEGORIES = [
    {
        "code": "economique",
        "libelle": "Obstacles économiques et tarifaires",
        "description": (
            "Obstacles liés au coût du traitement, à son remboursement "
            "ou à l'inadéquation des mécanismes de paiement."
        ),
    },
    {
        "code": "organisationnel",
        "libelle": "Obstacles organisationnels et politiques",
        "description": (
            "Obstacles liés à la structure de prise en charge, aux délais "
            "administratifs et à l'absence de processus dédiés."
        ),
    },
    {
        "code": "informationnel",
        "libelle": "Obstacles informationnels",
        "description": (
            "Obstacles liés à l'absence, à la dispersion ou à l'opacité "
            "de l'information nécessaire pour accéder au traitement."
        ),
    },
    {
        "code": "social",
        "libelle": "Déterminants sociaux et discrimination",
        "description": (
            "Obstacles liés aux conditions de vie, à la stigmatisation "
            "et aux barrières linguistiques ou culturelles."
        ),
    },
]

TYPES_OBSTACLES = [
    # Économiques
    ("economique", "refus_remboursement", "Refus de remboursement par l'assurance"),
    ("economique", "reste_a_charge", "Reste à charge trop élevé"),
    ("economique", "absence_voie_tarifaire", "Absence de voie de remboursement établie"),
    ("economique", "cout_deplacement", "Coût des déplacements vers le centre de soins"),
    ("economique", "perte_revenu", "Perte de revenu liée aux absences professionnelles"),
    ("economique", "refus_de_financer", "Refus de financer malgré une éligibilité reconnue"),
    # Organisationnels
    ("organisationnel", "delai_rendez_vous", "Délai d'obtention d'un rendez-vous spécialisé"),
    ("organisationnel", "absence_centre_reference", "Absence de centre de référence pour la pathologie"),
    ("organisationnel", "coordination_defaillante", "Mauvaise coordination entre les intervenants"),
    ("organisationnel", "refus_prise_en_charge", "Refus de prise en charge par une structure de soins"),
    ("organisationnel", "delai_administratif", "Délai de traitement d'une demande administrative"),
    ("organisationnel", "errance_diagnostique", "Délai avant l'établissement du diagnostic"),
    ("organisationnel", "non_prise_en_compte_information", "Informations transmises par le patient non prises en compte"),
    ("organisationnel", "medecine_defensive", "Décision guidée par la prudence institutionnelle plutôt que par le besoin"),
    ("organisationnel", "deni_institutionnel", "Déni du problème par l'institution sollicitée"),
    ("organisationnel", "blocage_politique", "Blocage lié à un désaccord entre institutions ou acteurs"),
    # Informationnels
    ("informationnel", "information_indisponible", "Information non disponible sur les options de traitement"),
    ("informationnel", "procedure_opaque", "Procédure de demande peu claire ou non documentée"),
    ("informationnel", "absence_donnees", "Absence de données sur la pathologie ou la population concernée"),
    ("informationnel", "information_contradictoire", "Informations contradictoires entre interlocuteurs"),
    ("informationnel", "meconnaissance_soignants", "Méconnaissance de la pathologie par les soignants"),
    # Sociaux
    ("social", "transport_limite", "Difficulté de transport vers les lieux de soins"),
    ("social", "stigmatisation", "Stigmatisation liée à la pathologie"),
    ("social", "barriere_linguistique", "Barrière linguistique dans la relation de soin"),
    ("social", "impact_professionnel", "Répercussions sur l'activité professionnelle"),
    ("social", "isolement", "Isolement social ou absence de soutien"),
    ("social", "mise_en_doute_parole", "Parole ou symptômes mis en doute par les soignants"),
    ("social", "absence_ecoute", "Absence d'écoute ou de prise au sérieux de la demande"),
    ("social", "mauvaise_foi", "Réponse de mauvaise foi ou argument sans fondement opposé à la demande"),
]

MALADIES = [
    {"nom": "Drépanocytose", "code_orpha": "232", "est_rare": True},
    {"nom": "Bêta-thalassémie", "code_orpha": "848", "est_rare": True},
]


def initialiser() -> None:
    """Crée les tables puis insère la nomenclature de référence."""
    creer_tables()
    session = FabriqueSession()

    try:
        if session.query(CategorieObstacle).count() > 0:
            print("La nomenclature est déjà initialisée.")
            return

        categories = {}
        for donnees in CATEGORIES:
            categorie = CategorieObstacle(**donnees)
            session.add(categorie)
            session.flush()
            categories[categorie.code] = categorie

        for code_categorie, code, libelle in TYPES_OBSTACLES:
            session.add(
                TypeObstacle(
                    categorie_id=categories[code_categorie].id,
                    code=code,
                    libelle=libelle,
                )
            )

        for donnees in MALADIES:
            session.add(Maladie(**donnees))

        session.commit()

        print(f"{len(CATEGORIES)} catégories insérées.")
        print(f"{len(TYPES_OBSTACLES)} types d'obstacles insérés.")
        print(f"{len(MALADIES)} maladies insérées.")

    finally:
        session.close()


if __name__ == "__main__":
    initialiser()
