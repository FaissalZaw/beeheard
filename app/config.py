"""Paramètres de configuration de l'application BeeHeard."""

import os
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# Base de données
URL_BASE_DONNEES = f"sqlite:///{RACINE / 'data' / 'beeheard.db'}"

# Application
NOM_APPLICATION = "BeeHeard"
VERSION = "0.1.0"

# Version du texte de consentement présenté aux contributeurs
VERSION_CONSENTEMENT = "1.0"

# Jeu de données de démonstration
DONNEES_FICTIVES = True

# Administration
# Le mot de passe est lu depuis l'environnement afin de ne jamais figurer
# dans le dépôt. La valeur par défaut ne vaut que pour la démonstration.
MOT_DE_PASSE_ADMIN = os.environ.get("BEEHEARD_ADMIN", "demo-beeheard-2026")
DUREE_SESSION_HEURES = 8
