"""Internationalisation de l'interface.

Les libellés de la nomenclature sont traduits en base de données. Ce module
prend en charge les chaînes fixes de l'interface, indépendantes des données.
"""

from app.modeles.enumerations import Langue

LANGUES_DISPONIBLES = [
    (Langue.FR.value, "Français"),
    (Langue.EN.value, "English"),
    (Langue.DE.value, "Deutsch"),
    (Langue.IT.value, "Italiano"),
]

TRADUCTIONS: dict[str, dict[str, str]] = {
    # Navigation
    "nav_temoigner": {
        "fr": "Témoigner", "en": "Share", "de": "Berichten", "it": "Testimoniare",
    },
    "nav_donnees": {
        "fr": "Données", "en": "Data", "de": "Daten", "it": "Dati",
    },
    "nav_synthese": {
        "fr": "Synthèse", "en": "Summary", "de": "Übersicht", "it": "Sintesi",
    },
    "nav_a_propos": {
        "fr": "À propos", "en": "About", "de": "Über", "it": "Informazioni",
    },

    # Accueil
    "accueil_titre": {
        "fr": "Rendre visibles les obstacles d'accès aux traitements",
        "en": "Making barriers to treatment access visible",
        "de": "Zugangshindernisse zu Behandlungen sichtbar machen",
        "it": "Rendere visibili gli ostacoli all'accesso alle cure",
    },
    "accueil_intro": {
        "fr": "Des traitements existent et sont autorisés, mais n'atteignent "
              "pas toujours les personnes qui en ont besoin. Les obstacles "
              "rencontrés sont rarement documentés de manière structurée, ce "
              "qui les rend invisibles pour ceux qui décident. BeeHeard "
              "recueille ces situations et les transforme en données "
              "exploitables.",
        "en": "Treatments exist and are authorised, yet they do not always "
              "reach the people who need them. The barriers encountered are "
              "rarely documented in a structured way, which makes them "
              "invisible to decision-makers. BeeHeard collects these "
              "situations and turns them into usable data.",
        "de": "Behandlungen existieren und sind zugelassen, erreichen aber "
              "nicht immer die Menschen, die sie benötigen. Die auftretenden "
              "Hindernisse werden selten strukturiert dokumentiert und "
              "bleiben für Entscheidungsträger unsichtbar. BeeHeard erfasst "
              "diese Situationen und wandelt sie in verwertbare Daten um.",
        "it": "I trattamenti esistono e sono autorizzati, ma non raggiungono "
              "sempre le persone che ne hanno bisogno. Gli ostacoli incontrati "
              "sono raramente documentati in modo strutturato, il che li rende "
              "invisibili a chi decide. BeeHeard raccoglie queste situazioni e "
              "le trasforma in dati utilizzabili.",
    },
    "accueil_bouton_temoigner": {
        "fr": "Déposer un témoignage", "en": "Submit an account",
        "de": "Bericht einreichen", "it": "Inviare una testimonianza",
    },
    "accueil_bouton_donnees": {
        "fr": "Consulter les données", "en": "View the data",
        "de": "Daten ansehen", "it": "Consultare i dati",
    },
    "accueil_comment": {
        "fr": "Comment cela fonctionne", "en": "How it works",
        "de": "So funktioniert es", "it": "Come funziona",
    },
    "etape1_titre": {
        "fr": "Vous racontez", "en": "You describe",
        "de": "Sie berichten", "it": "Racconti",
    },
    "etape1_texte": {
        "fr": "Vous décrivez librement la situation que vous avez vécue, en "
              "tant que patient, proche, professionnel de santé ou "
              "représentant d'association.",
        "en": "You freely describe the situation you experienced, as a "
              "patient, relative, healthcare professional or association "
              "representative.",
        "de": "Sie schildern frei die erlebte Situation, als Patientin oder "
              "Patient, Angehörige, Fachperson oder Vertretung eines Vereins.",
        "it": "Descrivi liberamente la situazione vissuta, come paziente, "
              "familiare, professionista sanitario o rappresentante di "
              "un'associazione.",
    },
    "etape2_titre": {
        "fr": "Vous qualifiez", "en": "You classify",
        "de": "Sie ordnen ein", "it": "Qualifichi",
    },
    "etape2_texte": {
        "fr": "Vous identifiez les obstacles rencontrés parmi une liste "
              "établie à partir de la littérature scientifique. C'est ce qui "
              "rend les témoignages comparables entre eux.",
        "en": "You identify the barriers encountered from a list derived from "
              "the scientific literature. This is what makes accounts "
              "comparable with one another.",
        "de": "Sie benennen die aufgetretenen Hindernisse anhand einer aus "
              "der Fachliteratur abgeleiteten Liste. Dies macht die Berichte "
              "untereinander vergleichbar.",
        "it": "Identifichi gli ostacoli incontrati da un elenco derivato dalla "
              "letteratura scientifica. È ciò che rende le testimonianze "
              "confrontabili tra loro.",
    },
    "etape3_titre": {
        "fr": "Nous agrégeons", "en": "We aggregate",
        "de": "Wir aggregieren", "it": "Aggreghiamo",
    },
    "etape3_texte": {
        "fr": "Les témoignages validés alimentent des indicateurs et une fiche "
              "de synthèse, utilisables par les associations et les "
              "organisations qui portent ces questions auprès des décideurs.",
        "en": "Validated accounts feed indicators and a summary sheet, usable "
              "by associations and organisations raising these issues with "
              "decision-makers.",
        "de": "Geprüfte Berichte fliessen in Indikatoren und ein "
              "Übersichtsblatt ein, nutzbar für Vereine und Organisationen, "
              "die diese Fragen bei Entscheidungsträgern einbringen.",
        "it": "Le testimonianze convalidate alimentano indicatori e una scheda "
              "di sintesi, utilizzabili dalle associazioni e organizzazioni "
              "che portano queste questioni ai decisori.",
    },
    "confiance_titre": {
        "fr": "Vos données vous appartiennent",
        "en": "Your data belongs to you",
        "de": "Ihre Daten gehören Ihnen",
        "it": "I tuoi dati ti appartengono",
    },

    # Indicateurs
    "temoignages": {
        "fr": "témoignages", "en": "accounts",
        "de": "Berichte", "it": "testimonianze",
    },
    "obstacles_signales": {
        "fr": "obstacles signalés", "en": "barriers reported",
        "de": "gemeldete Hindernisse", "it": "ostacoli segnalati",
    },
    "types_documentes": {
        "fr": "types d'obstacles documentés", "en": "documented barrier types",
        "de": "dokumentierte Hindernistypen", "it": "tipi di ostacoli documentati",
    },
    "jours_blocage": {
        "fr": "jours de blocage en moyenne", "en": "average days blocked",
        "de": "Tage Blockade im Durchschnitt", "it": "giorni di blocco in media",
    },

    # Tableau de bord
    "tdb_titre": {
        "fr": "Obstacles d'accès aux traitements",
        "en": "Barriers to treatment access",
        "de": "Hindernisse beim Zugang zu Behandlungen",
        "it": "Ostacoli all'accesso alle cure",
    },
    "tdb_intro": {
        "fr": "Indicateurs agrégés issus des témoignages validés.",
        "en": "Aggregated indicators from validated accounts.",
        "de": "Aggregierte Indikatoren aus geprüften Berichten.",
        "it": "Indicatori aggregati derivati dalle testimonianze convalidate.",
    },
    "tdb_par_categorie": {
        "fr": "Répartition par catégorie d'obstacle",
        "en": "Breakdown by barrier category",
        "de": "Verteilung nach Hinderniskategorie",
        "it": "Ripartizione per categoria di ostacolo",
    },
    "tdb_frequents": {
        "fr": "Obstacles les plus fréquemment signalés",
        "en": "Most frequently reported barriers",
        "de": "Am häufigsten gemeldete Hindernisse",
        "it": "Ostacoli segnalati più frequentemente",
    },
    "tdb_par_role": {
        "fr": "Répartition par profil de contributeur",
        "en": "Breakdown by contributor profile",
        "de": "Verteilung nach Profil der Beitragenden",
        "it": "Ripartizione per profilo del contributore",
    },
    "tdb_vide": {
        "fr": "Aucun témoignage validé pour le moment.",
        "en": "No validated account yet.",
        "de": "Noch keine geprüften Berichte.",
        "it": "Nessuna testimonianza convalidata al momento.",
    },

    # En-têtes de tableaux
    "col_obstacle": {
        "fr": "Obstacle", "en": "Barrier", "de": "Hindernis", "it": "Ostacolo",
    },
    "col_categorie": {
        "fr": "Catégorie", "en": "Category", "de": "Kategorie", "it": "Categoria",
    },
    "col_signalements": {
        "fr": "Signalements", "en": "Reports", "de": "Meldungen", "it": "Segnalazioni",
    },
    "col_gravite": {
        "fr": "Gravité moyenne", "en": "Average severity",
        "de": "Durchschnittlicher Schweregrad", "it": "Gravità media",
    },
    "col_qualite": {
        "fr": "Qualité", "en": "Capacity", "de": "Eigenschaft", "it": "Qualità",
    },

    # Formulaire
    "form_titre": {
        "fr": "Déposer un témoignage", "en": "Submit an account",
        "de": "Bericht einreichen", "it": "Inviare una testimonianza",
    },
    "form_intro": {
        "fr": "Ce formulaire permet de documenter les obstacles rencontrés "
              "dans l'accès à un traitement. Aucune donnée permettant de vous "
              "identifier n'est collectée.",
        "en": "This form documents barriers encountered in accessing "
              "treatment. No personally identifying data is collected.",
        "de": "Dieses Formular dokumentiert Hindernisse beim Zugang zu einer "
              "Behandlung. Es werden keine identifizierenden Daten erhoben.",
        "it": "Questo modulo permette di documentare gli ostacoli incontrati "
              "nell'accesso a un trattamento. Non viene raccolto alcun dato "
              "identificativo.",
    },
    "form_qui": {
        "fr": "Qui témoigne", "en": "Who is reporting",
        "de": "Wer berichtet", "it": "Chi testimonia",
    },
    "form_votre_temoignage": {
        "fr": "Votre témoignage", "en": "Your account",
        "de": "Ihr Bericht", "it": "La tua testimonianza",
    },
    "form_obstacles": {
        "fr": "Obstacles rencontrés", "en": "Barriers encountered",
        "de": "Aufgetretene Hindernisse", "it": "Ostacoli incontrati",
    },
    "form_anonymisation": {
        "fr": "Anonymisation", "en": "Anonymisation",
        "de": "Anonymisierung", "it": "Anonimizzazione",
    },
    "form_usages": {
        "fr": "Usages autorisés", "en": "Permitted uses",
        "de": "Erlaubte Verwendungen", "it": "Usi autorizzati",
    },
    "form_envoyer": {
        "fr": "Envoyer mon témoignage", "en": "Submit my account",
        "de": "Bericht absenden", "it": "Invia la mia testimonianza",
    },
    "facultatif": {
        "fr": "facultatif", "en": "optional",
        "de": "optional", "it": "facoltativo",
    },
    "dicter": {
        "fr": "Dicter", "en": "Dictate", "de": "Diktieren", "it": "Dettare",
    },
    "caracteres": {
        "fr": "caractères", "en": "characters",
        "de": "Zeichen", "it": "caratteri",
    },

    # Bandeau et pied de page
    "bandeau_demo": {
        "fr": "Jeu de données de démonstration. Les témoignages présentés sont "
              "fictifs et ne reflètent pas de situations réelles.",
        "en": "Demonstration dataset. The accounts shown are fictitious and do "
              "not reflect real situations.",
        "de": "Demonstrationsdatensatz. Die gezeigten Berichte sind fiktiv und "
              "spiegeln keine realen Situationen wider.",
        "it": "Set di dati dimostrativo. Le testimonianze presentate sono "
              "fittizie e non riflettono situazioni reali.",
    },
    "pied_projet": {
        "fr": "BeeHeard, prototype développé dans le cadre d'un Travail de "
              "Bachelor en Informatique de gestion, HEG Genève.",
        "en": "BeeHeard, a prototype developed as part of a Bachelor's thesis "
              "in Business Information Technology, HEG Geneva.",
        "de": "BeeHeard, Prototyp im Rahmen einer Bachelorarbeit in "
              "Wirtschaftsinformatik, HEG Genf.",
        "it": "BeeHeard, prototipo sviluppato nell'ambito di un lavoro di "
              "Bachelor in Informatica gestionale, HEG Ginevra.",
    },
    "pied_protection": {
        "fr": "Protection des données", "en": "Data protection",
        "de": "Datenschutz", "it": "Protezione dei dati",
    },
    "pied_mentions": {
        "fr": "Mentions légales", "en": "Legal notice",
        "de": "Impressum", "it": "Note legali",
    },
}


def traduire(cle: str, langue: str = "fr") -> str:
    """Retourne la chaîne traduite, avec repli sur le français."""
    entree = TRADUCTIONS.get(cle)
    if entree is None:
        return cle
    return entree.get(langue) or entree.get("fr", cle)


def langue_valide(valeur: str | None) -> str:
    """Normalise une langue reçue, avec repli sur la langue par défaut."""
    if valeur in {langue.value for langue in Langue}:
        return valeur
    return Langue.par_defaut().value


def contexte_langue(request) -> dict:
    """Fournit la langue courante et les libellés aux gabarits."""
    from app.dependances import obtenir_langue

    return {"langue": obtenir_langue(request)}
