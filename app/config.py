"""Paramètres de configuration de l'application BeeHeard."""

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
