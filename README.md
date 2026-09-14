# BeeHeard

Prototype d'outil numerique destine a documenter et visualiser les obstacles
d'acces aux traitements dans les maladies rares.

Developpe dans le cadre d'un Travail de Bachelor en Informatique de gestion,
Haute Ecole de Gestion de Geneve.

## Objet

Les temoignages de patients, les observations cliniques et les analyses
economiques relatives aux obstacles d'acces existent, mais demeurent disperses
et non structures. BeeHeard propose une chaine de traitement complete :
collecter ces temoignages sous une forme structuree, les agreger en
indicateurs, et les restituer sous un format exploitable par les acteurs du
plaidoyer.

## Modules

| Module | Fonction |
|---|---|
| Collecte | Depot d'un temoignage avec qualification des obstacles, consentement explicite et anonymisation parametrable |
| Visualisation | Tableau de bord des indicateurs agreges |
| Restitution | Fiche de synthese exportable |

## Architecture

L'application adopte une architecture en couches, chaque couche n'ayant
connaissance que de la couche immediatement inferieure.

    Presentation (Jinja2)
            |
    Routes (FastAPI)          entrees HTTP, validation
            |
    Services                  logique metier, regles, transitions d'etat
            |
    Depots                    acces aux donnees
            |
    Modeles (SQLAlchemy)      entites et relations

## Pile technologique

- Python 3.13
- FastAPI pour la couche web
- SQLAlchemy pour le mappage objet-relationnel
- Pydantic pour la validation des donnees entrantes
- SQLite pour la persistance
- Jinja2 pour les gabarits
- pytest pour les tests
- Docker pour le deploiement

## Installation locale

    git clone https://github.com/FaissalZaw/beeheard.git
    cd beeheard

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    python3 scripts/initialiser_donnees.py
    python3 scripts/donnees_demonstration.py

    uvicorn main:app --reload

L'application est accessible sur http://127.0.0.1:8000

## Deploiement par conteneur

    docker compose up -d --build

Puis, pour initialiser les donnees :

    docker compose exec beeheard python3 scripts/initialiser_donnees.py
    docker compose exec beeheard python3 scripts/donnees_demonstration.py

Pour arreter :

    docker compose down

## Tests

    pytest tests -v
    pytest tests --cov=app --cov-report=term-missing

La suite comprend 31 tests : 22 tests unitaires portant sur la logique metier
et 9 tests d'integration portant sur les parcours applicatifs complets. Une
base de donnees en memoire est creee pour chaque execution, garantissant leur
independance et leur reproductibilite.

## Integration continue

Un pipeline GitHub Actions s'execute a chaque envoi de code : installation des
dependances, verification du style et execution de la suite de tests.

## Nomenclature des obstacles

La nomenclature est derivee de la revue de litterature du memoire. Elle
comprend quatre categories et vingt-et-un types d'obstacles.

| Categorie | Nombre de types |
|---|---|
| Obstacles economiques et tarifaires | 5 |
| Obstacles organisationnels et politiques | 8 |
| Obstacles informationnels | 5 |
| Determinants sociaux et discrimination | 7 |

## Protection des donnees

Conformement a la Loi federale sur la protection des donnees, quatre principes
structurent la conception :

- Consentement explicite requis avant tout enregistrement, trace avec sa
  version et sa date
- Anonymisation parametrable selon trois niveaux, appliquee au moment du depot
- Minimisation : aucune donnee identifiante directe n'est collectee, le
  pseudonyme est genere par le systeme
- Transparence sur les usages autorises, distingues entre publication et
  plaidoyer

## Donnees de demonstration

Le prototype est alimente par un jeu de donnees synthetiques construit a partir
des obstacles documentes dans la litterature. Ces temoignages sont fictifs et
ne correspondent a aucune personne reelle. L'interface le signale par un
bandeau permanent.

## Structure du depot

    beeheard/
    |-- app/
    |   |-- modeles/          entites et enumerations
    |   |-- depots/           acces aux donnees
    |   |-- services/         logique metier
    |   |-- routes/           points d'entree HTTP
    |   |-- templates/        gabarits Jinja2
    |   +-- static/           feuille de style
    |-- tests/                tests unitaires et d'integration
    |-- scripts/              initialisation et donnees de demonstration
    |-- .github/workflows/    integration continue
    |-- Dockerfile
    +-- docker-compose.yml

## Licence

Travail academique. Tous droits reserves.
