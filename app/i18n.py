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
        "fr": "Tableau de bord", "en": "Dashboard",
        "de": "Übersicht", "it": "Cruscotto",
    },
    "nav_synthese": {
        "fr": "Synthèse", "en": "Summary", "de": "Übersicht", "it": "Sintesi",
    },
    "nav_a_propos": {
        "fr": "À propos", "en": "About", "de": "Über", "it": "Informazioni",
    },

    # Accueil
    "accueil_titre_avant": {
        "fr": "Rendre", "en": "Making barriers to care and treatment",
        "de": "Hindernisse beim Zugang zu Versorgung und Behandlung",
        "it": "Rendere",
    },
    "accueil_titre_accent": {
        "fr": "visibles", "en": "visible",
        "de": "sichtbar", "it": "visibili",
    },
    "accueil_titre_apres": {
        "fr": "les obstacles d'accès aux soins et aux traitements",
        "en": "", "de": " machen",
        "it": "gli ostacoli all'accesso alle cure e ai trattamenti",
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
              "invisible to those who decide. BeeHeard collects these "
              "situations and turns them into usable data.",
        "de": "Behandlungen existieren und sind zugelassen, erreichen aber "
              "nicht immer die Menschen, die sie benötigen. Die auftretenden "
              "Hindernisse werden selten strukturiert dokumentiert und bleiben "
              "für Entscheidungsträger unsichtbar. BeeHeard erfasst diese "
              "Situationen und wandelt sie in verwertbare Daten um.",
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
        "fr": "Obstacles d'accès aux soins et aux traitements",
        "en": "Barriers to care and treatment access",
        "de": "Hindernisse beim Zugang zu Versorgung und Behandlung",
        "it": "Ostacoli all'accesso alle cure e ai trattamenti",
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
              "dans l'accès aux soins ou à un traitement. Aucune donnée "
              "permettant de vous identifier n'est collectée.",
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

TRADUCTIONS.update({
    "champ_role": {
        "fr": "En quelle qualité témoignez-vous ?",
        "en": "In what capacity are you reporting?",
        "de": "In welcher Eigenschaft berichten Sie?",
        "it": "In quale qualità testimoni?",
    },
    "champ_canton": {
        "fr": "Canton", "en": "Canton", "de": "Kanton", "it": "Cantone",
    },
    "champ_age": {
        "fr": "Tranche d'âge", "en": "Age range",
        "de": "Altersgruppe", "it": "Fascia d'età",
    },
    "non_renseigne": {
        "fr": "Non renseigné", "en": "Not specified",
        "de": "Nicht angegeben", "it": "Non indicato",
    },
    "age_moins18": {
        "fr": "Moins de 18 ans", "en": "Under 18",
        "de": "Unter 18 Jahren", "it": "Meno di 18 anni",
    },
    "age_plus60": {
        "fr": "60 ans et plus", "en": "60 and over",
        "de": "60 Jahre und älter", "it": "60 anni e oltre",
    },
    "aide_anonymisation": {
        "fr": "Ces deux informations ne sont conservées que si vous choisissez "
              "un niveau d'anonymisation qui le permet, à la dernière étape.",
        "en": "These two details are kept only if you choose an anonymisation "
              "level that allows it, at the final step.",
        "de": "Diese beiden Angaben werden nur gespeichert, wenn Sie im letzten "
              "Schritt eine entsprechende Anonymisierungsstufe wählen.",
        "it": "Queste due informazioni sono conservate solo se scegli un "
              "livello di anonimizzazione che lo permette, all'ultimo passaggio.",
    },
    "champ_pathologie": {
        "fr": "Pathologie concernée", "en": "Condition concerned",
        "de": "Betroffene Erkrankung", "it": "Patologia interessata",
    },
    "champ_recit": {
        "fr": "Décrivez la situation que vous avez vécue",
        "en": "Describe the situation you experienced",
        "de": "Beschreiben Sie die erlebte Situation",
        "it": "Descrivi la situazione che hai vissuto",
    },
    "placeholder_recit": {
        "fr": "Racontez librement : ce qui s'est passé, les démarches "
              "entreprises, les réponses obtenues, les conséquences.",
        "en": "Describe freely: what happened, the steps taken, the responses "
              "received, the consequences.",
        "de": "Schildern Sie frei: was geschehen ist, welche Schritte "
              "unternommen wurden, welche Antworten kamen, welche Folgen.",
        "it": "Racconta liberamente: cosa è successo, le azioni intraprese, "
              "le risposte ottenute, le conseguenze.",
    },
    "champ_titre": {
        "fr": "Titre", "en": "Title", "de": "Titel", "it": "Titolo",
    },
    "placeholder_titre": {
        "fr": "Laissez vide : un titre sera proposé à partir de votre récit",
        "en": "Leave blank: a title will be derived from your account",
        "de": "Leer lassen: ein Titel wird aus Ihrem Bericht abgeleitet",
        "it": "Lascia vuoto: un titolo sarà proposto dal tuo racconto",
    },
    "aide_titre": {
        "fr": "Si vous ne renseignez rien, un intitulé sera généré "
              "automatiquement en reprenant le début de votre récit.",
        "en": "If left empty, a title will be generated automatically from the "
              "beginning of your account.",
        "de": "Wenn leer, wird ein Titel automatisch aus dem Anfang Ihres "
              "Berichts erzeugt.",
        "it": "Se lasci vuoto, un titolo sarà generato automaticamente "
              "dall'inizio del tuo racconto.",
    },
    "champ_date": {
        "fr": "Date de l'événement", "en": "Date of the event",
        "de": "Datum des Ereignisses", "it": "Data dell'evento",
    },
    "aide_obstacles": {
        "fr": "Sélectionnez les obstacles qui correspondent à votre situation. "
              "Cette qualification permet de rendre les témoignages "
              "comparables. Plusieurs choix sont possibles.",
        "en": "Select the barriers matching your situation. This "
              "classification makes accounts comparable. Multiple choices are "
              "possible.",
        "de": "Wählen Sie die Hindernisse, die auf Ihre Situation zutreffen. "
              "Diese Einordnung macht Berichte vergleichbar. Mehrfachauswahl "
              "ist möglich.",
        "it": "Seleziona gli ostacoli che corrispondono alla tua situazione. "
              "Questa qualificazione rende le testimonianze confrontabili. "
              "Sono possibili più scelte.",
    },
    "champ_gravite": {
        "fr": "Gravité ressentie de la situation",
        "en": "Perceived severity of the situation",
        "de": "Empfundener Schweregrad der Situation",
        "it": "Gravità percepita della situazione",
    },
    "champ_duree": {
        "fr": "Durée du blocage en jours", "en": "Duration of the blockage in days",
        "de": "Dauer der Blockade in Tagen", "it": "Durata del blocco in giorni",
    },
    "placeholder_duree": {
        "fr": "Par exemple 240 pour huit mois d'attente",
        "en": "For example 240 for eight months of waiting",
        "de": "Zum Beispiel 240 für acht Monate Wartezeit",
        "it": "Ad esempio 240 per otto mesi di attesa",
    },
    "aide_niveau": {
        "fr": "Ce choix est appliqué au moment de l'enregistrement et ne peut "
              "pas être modifié ensuite.",
        "en": "This choice is applied on submission and cannot be changed "
              "afterwards.",
        "de": "Diese Wahl wird beim Speichern angewendet und kann danach nicht "
              "mehr geändert werden.",
        "it": "Questa scelta è applicata al momento della registrazione e non "
              "può essere modificata in seguito.",
    },
    "anon_complet_titre": {
        "fr": "Anonymisation complète", "en": "Full anonymisation",
        "de": "Vollständige Anonymisierung", "it": "Anonimizzazione completa",
    },
    "anon_complet_desc": {
        "fr": "Ni canton ni tranche d'âge ne sont conservés. Recommandé.",
        "en": "Neither canton nor age range is kept. Recommended.",
        "de": "Weder Kanton noch Altersgruppe werden gespeichert. Empfohlen.",
        "it": "Né cantone né fascia d'età sono conservati. Consigliato.",
    },
    "anon_partiel_titre": {
        "fr": "Anonymisation partielle", "en": "Partial anonymisation",
        "de": "Teilweise Anonymisierung", "it": "Anonimizzazione parziale",
    },
    "anon_partiel_desc": {
        "fr": "Le canton est conservé, la tranche d'âge est supprimée.",
        "en": "The canton is kept, the age range is removed.",
        "de": "Der Kanton wird gespeichert, die Altersgruppe entfernt.",
        "it": "Il cantone è conservato, la fascia d'età è eliminata.",
    },
    "anon_etendu_titre": {
        "fr": "Anonymisation étendue", "en": "Extended anonymisation",
        "de": "Erweiterte Anonymisierung", "it": "Anonimizzazione estesa",
    },
    "anon_etendu_desc": {
        "fr": "Canton et tranche d'âge sont conservés, permettant des analyses "
              "plus fines.",
        "en": "Canton and age range are kept, allowing finer analysis.",
        "de": "Kanton und Altersgruppe werden gespeichert, was feinere "
              "Auswertungen ermöglicht.",
        "it": "Cantone e fascia d'età sono conservati, permettendo analisi più "
              "dettagliate.",
    },
    "aide_usages": {
        "fr": "Chaque usage fait l'objet d'un accord distinct. Aucun n'est "
              "activé par défaut, à l'exception du comptage statistique.",
        "en": "Each use requires separate consent. None is enabled by default, "
              "except statistical counting.",
        "de": "Jede Verwendung erfordert eine eigene Zustimmung. Keine ist "
              "standardmässig aktiviert, ausser der statistischen Zählung.",
        "it": "Ogni uso richiede un consenso distinto. Nessuno è attivo per "
              "impostazione predefinita, tranne il conteggio statistico.",
    },
    "usage_stats_titre": {
        "fr": "Statistiques agrégées", "en": "Aggregated statistics",
        "de": "Aggregierte Statistiken", "it": "Statistiche aggregate",
    },
    "usage_stats_desc": {
        "fr": "Votre témoignage alimente des comptages et des répartitions. "
              "Le récit lui-même n'est pas affiché.",
        "en": "Your account feeds counts and breakdowns. The narrative itself "
              "is not displayed.",
        "de": "Ihr Bericht fliesst in Zählungen und Verteilungen ein. Der Text "
              "selbst wird nicht angezeigt.",
        "it": "La tua testimonianza alimenta conteggi e ripartizioni. Il "
              "racconto stesso non è visualizzato.",
    },
    "usage_publication_titre": {
        "fr": "Publication anonymisée", "en": "Anonymised publication",
        "de": "Anonymisierte Veröffentlichung", "it": "Pubblicazione anonimizzata",
    },
    "usage_publication_desc": {
        "fr": "Votre récit peut être affiché dans l'espace de consultation, "
              "sous pseudonyme.",
        "en": "Your account may be displayed in the consultation area, under a "
              "pseudonym.",
        "de": "Ihr Bericht kann im Konsultationsbereich unter einem Pseudonym "
              "angezeigt werden.",
        "it": "Il tuo racconto può essere visualizzato nello spazio di "
              "consultazione, sotto pseudonimo.",
    },
    "usage_plaidoyer_titre": {
        "fr": "Supports de plaidoyer", "en": "Advocacy materials",
        "de": "Advocacy-Material", "it": "Materiali di advocacy",
    },
    "usage_plaidoyer_desc": {
        "fr": "Votre récit peut être repris dans des documents destinés aux "
              "associations, aux organisations de santé ou aux décideurs.",
        "en": "Your account may be used in documents intended for "
              "associations, health organisations or decision-makers.",
        "de": "Ihr Bericht kann in Dokumenten für Vereine, "
              "Gesundheitsorganisationen oder Entscheidungsträger verwendet "
              "werden.",
        "it": "Il tuo racconto può essere ripreso in documenti destinati alle "
              "associazioni, alle organizzazioni sanitarie o ai decisori.",
    },
    "consentement_texte": {
        "fr": "Je consens au traitement des informations que je transmets, "
              "conformément à la Loi fédérale sur la protection des données. "
              "J'ai pris connaissance de la",
        "en": "I consent to the processing of the information I provide, in "
              "accordance with the Federal Act on Data Protection. I have read "
              "the",
        "de": "Ich willige in die Bearbeitung der übermittelten Informationen "
              "gemäss dem Bundesgesetz über den Datenschutz ein. Ich habe die "
              "Kenntnis genommen von der",
        "it": "Acconsento al trattamento delle informazioni che trasmetto, "
              "conformemente alla Legge federale sulla protezione dei dati. Ho "
              "preso conoscenza della",
    },
    "minimum": {
        "fr": "minimum", "en": "minimum", "de": "Minimum", "it": "minimo",
    },
})

TRADUCTIONS.update({
    # Fiche de synthèse
    "synth_titre": {
        "fr": "Obstacles d'accès aux soins et aux traitements",
        "en": "Barriers to care and treatment access",
        "de": "Hindernisse beim Zugang zu Versorgung und Behandlung",
        "it": "Ostacoli all'accesso alle cure e ai trattamenti",
    },
    "synth_generee": {
        "fr": "Fiche de synthèse générée le",
        "en": "Summary sheet generated on",
        "de": "Übersichtsblatt erstellt am",
        "it": "Scheda di sintesi generata il",
    },
    "synth_ce_que_montrent": {
        "fr": "Ce que montrent les données",
        "en": "What the data shows",
        "de": "Was die Daten zeigen",
        "it": "Cosa mostrano i dati",
    },
    "synth_sur": {
        "fr": "Sur", "en": "Out of", "de": "Von", "it": "Su",
    },
    "synth_recueillis": {
        "fr": "témoignages recueillis,",
        "en": "accounts collected,",
        "de": "erfassten Berichten wurden",
        "it": "testimonianze raccolte,",
    },
    "synth_ont_ete_signales": {
        "fr": "obstacles ont été signalés.",
        "en": "barriers were reported.",
        "de": "Hindernisse gemeldet.",
        "it": "ostacoli sono stati segnalati.",
    },
    "synth_duree_moyenne": {
        "fr": "La durée moyenne des blocages renseignés s'établit à",
        "en": "The average duration of reported blockages is",
        "de": "Die durchschnittliche Dauer der gemeldeten Blockaden beträgt",
        "it": "La durata media dei blocchi segnalati è di",
    },
    "synth_jours": {
        "fr": "jours.", "en": "days.", "de": "Tage.", "it": "giorni.",
    },
    "synth_des_signalements": {
        "fr": "des signalements relèvent des",
        "en": "of reports fall under",
        "de": "der Meldungen betreffen",
        "it": "delle segnalazioni riguardano",
    },
    "synth_plus_signales": {
        "fr": "Obstacles les plus signalés",
        "en": "Most reported barriers",
        "de": "Am häufigsten gemeldete Hindernisse",
        "it": "Ostacoli più segnalati",
    },
    "synth_signalements": {
        "fr": "signalements, gravité moyenne",
        "en": "reports, average severity",
        "de": "Meldungen, durchschnittlicher Schweregrad",
        "it": "segnalazioni, gravità media",
    },
    "synth_sur_cinq": {
        "fr": "sur 5", "en": "out of 5", "de": "von 5", "it": "su 5",
    },
    "synth_illustratifs": {
        "fr": "Témoignages illustratifs",
        "en": "Illustrative accounts",
        "de": "Beispielhafte Berichte",
        "it": "Testimonianze illustrative",
    },
    "synth_pied": {
        "fr": "Document produit par BeeHeard à partir de témoignages recueillis "
              "avec consentement explicite et anonymisés.",
        "en": "Document produced by BeeHeard from accounts collected with "
              "explicit consent and anonymised.",
        "de": "Dokument von BeeHeard aus Berichten erstellt, die mit "
              "ausdrücklicher Zustimmung erfasst und anonymisiert wurden.",
        "it": "Documento prodotto da BeeHeard a partire da testimonianze "
              "raccolte con consenso esplicito e anonimizzate.",
    },
    "synth_imprimer": {
        "fr": "Imprimer ou exporter en PDF",
        "en": "Print or export as PDF",
        "de": "Drucken oder als PDF exportieren",
        "it": "Stampare o esportare in PDF",
    },

    # Confirmation
    "conf_titre": {
        "fr": "Votre témoignage a été enregistré",
        "en": "Your account has been recorded",
        "de": "Ihr Bericht wurde erfasst",
        "it": "La tua testimonianza è stata registrata",
    },
    "conf_reference": {
        "fr": "Référence", "en": "Reference",
        "de": "Referenz", "it": "Riferimento",
    },
    "conf_texte": {
        "fr": "Il sera examiné avant d'être intégré aux données agrégées. Les "
              "informations que vous avez transmises ont été anonymisées selon "
              "le niveau que vous avez choisi, et votre consentement a été "
              "enregistré avec sa date.",
        "en": "It will be reviewed before being included in the aggregated "
              "data. The information you provided has been anonymised "
              "according to the level you chose, and your consent has been "
              "recorded with its date.",
        "de": "Er wird geprüft, bevor er in die aggregierten Daten aufgenommen "
              "wird. Ihre Angaben wurden gemäss der gewählten Stufe "
              "anonymisiert, und Ihre Zustimmung wurde mit Datum erfasst.",
        "it": "Sarà esaminata prima di essere integrata nei dati aggregati. Le "
              "informazioni trasmesse sono state anonimizzate secondo il "
              "livello scelto, e il tuo consenso è stato registrato con la "
              "relativa data.",
    },
    "conf_aucune_donnee": {
        "fr": "Aucune donnée permettant de vous identifier n'a été conservée.",
        "en": "No data allowing you to be identified has been kept.",
        "de": "Es wurden keine Daten gespeichert, die Sie identifizieren "
              "könnten.",
        "it": "Nessun dato che permetta di identificarti è stato conservato.",
    },
    "conf_retour_accueil": {
        "fr": "Retour à l'accueil", "en": "Back to home",
        "de": "Zurück zur Startseite", "it": "Torna alla pagina iniziale",
    },

    # Avertissement de langue
    "page_francais_uniquement": {
        "fr": "",
        "en": "This page is currently available in French only.",
        "de": "Diese Seite ist derzeit nur auf Französisch verfügbar.",
        "it": "Questa pagina è attualmente disponibile solo in francese.",
    },
})

TRADUCTIONS.update({
    "filtre_categorie": {
        "fr": "Catégorie d'obstacle", "en": "Barrier category",
        "de": "Hinderniskategorie", "it": "Categoria di ostacolo",
    },
    "filtre_region": {
        "fr": "Canton", "en": "Canton", "de": "Kanton", "it": "Cantone",
    },
    "filtre_toutes": {
        "fr": "Toutes les catégories", "en": "All categories",
        "de": "Alle Kategorien", "it": "Tutte le categorie",
    },
    "filtre_toutes_regions": {
        "fr": "Tous les cantons", "en": "All cantons",
        "de": "Alle Kantone", "it": "Tutti i cantoni",
    },
    "filtre_reinitialiser": {
        "fr": "Réinitialiser", "en": "Reset",
        "de": "Zurücksetzen", "it": "Reimposta",
    },
})

TRADUCTIONS.update({
    "nav_mon_temoignage": {
        "fr": "Mon témoignage", "en": "My account",
        "de": "Mein Bericht", "it": "La mia testimonianza",
    },
    "acces_titre": {
        "fr": "Retrouver mon témoignage", "en": "Retrieve my account",
        "de": "Meinen Bericht abrufen", "it": "Ritrovare la mia testimonianza",
    },
    "acces_intro": {
        "fr": "Saisissez la référence et le code personnel qui vous ont été "
              "remis lors du dépôt. Ils vous permettent de consulter votre "
              "témoignage, de modifier les usages autorisés ou de le retirer.",
        "en": "Enter the reference and personal code provided when you "
              "submitted your account. They allow you to view it, change the "
              "permitted uses or withdraw it.",
        "de": "Geben Sie die Referenz und den persönlichen Code ein, die Sie "
              "beim Einreichen erhalten haben. Damit können Sie Ihren Bericht "
              "einsehen, die erlaubten Verwendungen ändern oder ihn "
              "zurückziehen.",
        "it": "Inserisci il riferimento e il codice personale ricevuti al "
              "momento dell'invio. Ti permettono di consultare la tua "
              "testimonianza, modificare gli usi autorizzati o ritirarla.",
    },
    "acces_champ_reference": {
        "fr": "Référence", "en": "Reference",
        "de": "Referenz", "it": "Riferimento",
    },
    "acces_champ_code": {
        "fr": "Code personnel", "en": "Personal code",
        "de": "Persönlicher Code", "it": "Codice personale",
    },
    "acces_bouton": {
        "fr": "Accéder à mon témoignage", "en": "Access my account",
        "de": "Bericht aufrufen", "it": "Accedi alla mia testimonianza",
    },
    "acces_erreur": {
        "fr": "Aucun témoignage ne correspond à ces références. Vérifiez la "
              "référence et le code saisis.",
        "en": "No account matches these details. Please check the reference "
              "and code entered.",
        "de": "Kein Bericht entspricht diesen Angaben. Bitte prüfen Sie "
              "Referenz und Code.",
        "it": "Nessuna testimonianza corrisponde a questi riferimenti. "
              "Verifica il riferimento e il codice inseriti.",
    },
    "acces_note": {
        "fr": "Le code personnel n'est conservé sous aucune forme lisible. En "
              "cas de perte, il n'est pas possible de le retrouver ni de "
              "récupérer l'accès au témoignage.",
        "en": "The personal code is not stored in any readable form. If lost, "
              "it cannot be recovered and access to the account cannot be "
              "restored.",
        "de": "Der persönliche Code wird in keiner lesbaren Form gespeichert. "
              "Bei Verlust kann er nicht wiederhergestellt und der Zugang "
              "nicht wiedererlangt werden.",
        "it": "Il codice personale non è conservato in alcuna forma leggibile. "
              "In caso di smarrimento, non è possibile recuperarlo né "
              "riottenere l'accesso alla testimonianza.",
    },
    "acces_mon_titre": {
        "fr": "Mon témoignage", "en": "My account",
        "de": "Mein Bericht", "it": "La mia testimonianza",
    },
    "acces_depose_le": {
        "fr": "Déposé le", "en": "Submitted on",
        "de": "Eingereicht am", "it": "Inviata il",
    },
    "acces_statut": {
        "fr": "Statut", "en": "Status", "de": "Status", "it": "Stato",
    },
    "statut_soumis": {
        "fr": "En attente de validation", "en": "Awaiting review",
        "de": "Wartet auf Prüfung", "it": "In attesa di convalida",
    },
    "statut_valide": {
        "fr": "Validé", "en": "Validated", "de": "Geprüft", "it": "Convalidata",
    },
    "statut_publie": {
        "fr": "Publié", "en": "Published",
        "de": "Veröffentlicht", "it": "Pubblicata",
    },
    "statut_rejete": {
        "fr": "Non retenu", "en": "Not retained",
        "de": "Nicht berücksichtigt", "it": "Non accolta",
    },
    "statut_brouillon": {
        "fr": "Brouillon", "en": "Draft", "de": "Entwurf", "it": "Bozza",
    },
    "acces_obstacles": {
        "fr": "Obstacles signalés", "en": "Reported barriers",
        "de": "Gemeldete Hindernisse", "it": "Ostacoli segnalati",
    },
    "acces_modifier_usages": {
        "fr": "Modifier les usages autorisés", "en": "Change permitted uses",
        "de": "Erlaubte Verwendungen ändern", "it": "Modificare gli usi autorizzati",
    },
    "acces_usages_note": {
        "fr": "Le niveau d'anonymisation choisi lors du dépôt n'est pas "
              "modifiable : appliqué dès la collecte, il a supprimé des "
              "données qui ne peuvent être restaurées.",
        "en": "The anonymisation level chosen at submission cannot be "
              "changed: applied on collection, it removed data that cannot be "
              "restored.",
        "de": "Die bei der Einreichung gewählte Anonymisierungsstufe kann "
              "nicht geändert werden: Sie wurde sofort angewendet und hat "
              "Daten entfernt, die nicht wiederherstellbar sind.",
        "it": "Il livello di anonimizzazione scelto al momento dell'invio non "
              "è modificabile: applicato dalla raccolta, ha eliminato dati "
              "che non possono essere ripristinati.",
    },
    "acces_enregistrer": {
        "fr": "Enregistrer les modifications", "en": "Save changes",
        "de": "Änderungen speichern", "it": "Salvare le modifiche",
    },
    "acces_modifie": {
        "fr": "Vos préférences ont été enregistrées.",
        "en": "Your preferences have been saved.",
        "de": "Ihre Einstellungen wurden gespeichert.",
        "it": "Le tue preferenze sono state salvate.",
    },
    "acces_retirer_titre": {
        "fr": "Retirer mon témoignage", "en": "Withdraw my account",
        "de": "Bericht zurückziehen", "it": "Ritirare la mia testimonianza",
    },
    "acces_retirer_texte": {
        "fr": "Vous pouvez demander la suppression définitive de votre "
              "témoignage. Cette action est irréversible et retire la "
              "contribution de l'ensemble des données agrégées.",
        "en": "You may request the permanent deletion of your account. This "
              "action is irreversible and removes the contribution from all "
              "aggregated data.",
        "de": "Sie können die endgültige Löschung Ihres Berichts verlangen. "
              "Dieser Schritt ist unwiderruflich und entfernt den Beitrag aus "
              "allen aggregierten Daten.",
        "it": "Puoi richiedere la cancellazione definitiva della tua "
              "testimonianza. Questa azione è irreversibile e rimuove il "
              "contributo da tutti i dati aggregati.",
    },
    "acces_retirer_bouton": {
        "fr": "Supprimer définitivement", "en": "Delete permanently",
        "de": "Endgültig löschen", "it": "Eliminare definitivamente",
    },
    "acces_retirer_confirmation": {
        "fr": "Cette suppression est définitive. Confirmer ?",
        "en": "This deletion is permanent. Confirm?",
        "de": "Diese Löschung ist endgültig. Bestätigen?",
        "it": "Questa eliminazione è definitiva. Confermare?",
    },
    "retrait_titre": {
        "fr": "Témoignage supprimé", "en": "Account deleted",
        "de": "Bericht gelöscht", "it": "Testimonianza eliminata",
    },
    "retrait_texte": {
        "fr": "Votre témoignage a été définitivement supprimé. Il ne figure "
              "plus dans les données agrégées.",
        "en": "Your account has been permanently deleted. It no longer "
              "appears in the aggregated data.",
        "de": "Ihr Bericht wurde endgültig gelöscht. Er erscheint nicht mehr "
              "in den aggregierten Daten.",
        "it": "La tua testimonianza è stata definitivamente eliminata. Non "
              "figura più nei dati aggregati.",
    },
    "conf_code": {
        "fr": "Code personnel", "en": "Personal code",
        "de": "Persönlicher Code", "it": "Codice personale",
    },
    "conf_conserver": {
        "fr": "Conservez ces deux éléments. Ils vous permettront de retrouver "
              "votre témoignage, de modifier les usages autorisés ou de le "
              "retirer. Le code n'est affiché qu'une seule fois et ne peut pas "
              "être régénéré.",
        "en": "Keep both of these. They will let you retrieve your account, "
              "change the permitted uses or withdraw it. The code is shown "
              "only once and cannot be regenerated.",
        "de": "Bewahren Sie beide Angaben auf. Damit können Sie Ihren Bericht "
              "abrufen, die erlaubten Verwendungen ändern oder ihn "
              "zurückziehen. Der Code wird nur einmal angezeigt und kann nicht "
              "neu erzeugt werden.",
        "it": "Conserva entrambi gli elementi. Ti permetteranno di ritrovare "
              "la tua testimonianza, modificare gli usi autorizzati o "
              "ritirarla. Il codice è mostrato una sola volta e non può essere "
              "rigenerato.",
    },
})

TRADUCTIONS.update({
    "conf_copier": {
        "fr": "Copier mes accès", "en": "Copy my details",
        "de": "Zugangsdaten kopieren", "it": "Copia i miei accessi",
    },
    "conf_copie": {
        "fr": "Copié", "en": "Copied", "de": "Kopiert", "it": "Copiato",
    },
    "conf_imprimer": {
        "fr": "Imprimer ou enregistrer en PDF",
        "en": "Print or save as PDF",
        "de": "Drucken oder als PDF speichern",
        "it": "Stampa o salva in PDF",
    },
})

TRADUCTIONS.update({
    "pathologie_choisir": {
        "fr": "Sélectionnez une pathologie", "en": "Select a condition",
        "de": "Erkrankung auswählen", "it": "Seleziona una patologia",
    },
    "pathologie_autre": {
        "fr": "Autre pathologie", "en": "Other condition",
        "de": "Andere Erkrankung", "it": "Altra patologia",
    },
    "pathologie_preciser": {
        "fr": "Précisez la pathologie", "en": "Specify the condition",
        "de": "Erkrankung angeben", "it": "Specifica la patologia",
    },
    "pathologie_placeholder": {
        "fr": "Commencez à saisir le nom de la pathologie",
        "en": "Start typing the name of the condition",
        "de": "Beginnen Sie, den Namen der Erkrankung einzugeben",
        "it": "Inizia a digitare il nome della patologia",
    },
    "pathologie_aide": {
        "fr": "Si la pathologie n'apparaît pas dans la liste, saisissez son "
              "nom. Elle sera ajoutée et disponible pour les témoignages "
              "suivants.",
        "en": "If the condition is not listed, enter its name. It will be "
              "added and available for subsequent accounts.",
        "de": "Erscheint die Erkrankung nicht in der Liste, geben Sie ihren "
              "Namen ein. Sie wird hinzugefügt und steht für weitere Berichte "
              "zur Verfügung.",
        "it": "Se la patologia non compare nell'elenco, inserisci il suo nome. "
              "Sarà aggiunta e disponibile per le testimonianze successive.",
    },
})

TRADUCTIONS.update({
    "nav_donnees_ouvertes": {
        "fr": "Données ouvertes", "en": "Open data",
        "de": "Offene Daten", "it": "Dati aperti",
    },
    "donnees_titre": {
        "fr": "Données ouvertes", "en": "Open data",
        "de": "Offene Daten", "it": "Dati aperti",
    },
    "donnees_intro": {
        "fr": "Les obstacles signalés sont mis à disposition sous forme de "
              "jeu de données structuré, réutilisable à des fins de recherche, "
              "de sensibilisation ou de plaidoyer.",
        "en": "Reported barriers are made available as a structured dataset, "
              "reusable for research, awareness-raising or advocacy purposes.",
        "de": "Die gemeldeten Hindernisse werden als strukturierter Datensatz "
              "bereitgestellt, nutzbar für Forschung, Sensibilisierung oder "
              "Advocacy.",
        "it": "Gli ostacoli segnalati sono messi a disposizione come set di "
              "dati strutturato, riutilizzabile per ricerca, sensibilizzazione "
              "o advocacy.",
    },
    "donnees_variables": {
        "fr": "variables décrites", "en": "documented variables",
        "de": "beschriebene Variablen", "it": "variabili descritte",
    },
    "donnees_telecharger": {
        "fr": "Télécharger le jeu de données", "en": "Download the dataset",
        "de": "Datensatz herunterladen", "it": "Scaricare il set di dati",
    },
    "donnees_metadonnees": {
        "fr": "Métadonnées seules", "en": "Metadata only",
        "de": "Nur Metadaten", "it": "Solo metadati",
    },
    "donnees_licence": {
        "fr": "Licence", "en": "Licence", "de": "Lizenz", "it": "Licenza",
    },
    "donnees_version": {
        "fr": "schéma version", "en": "schema version",
        "de": "Schemaversion", "it": "versione schema",
    },
    "donnees_ce_qui_figure": {
        "fr": "Ce que contient le jeu de données",
        "en": "What the dataset contains",
        "de": "Inhalt des Datensatzes",
        "it": "Cosa contiene il set di dati",
    },
    "donnees_col_variable": {
        "fr": "Variable", "en": "Variable", "de": "Variable", "it": "Variabile",
    },
    "donnees_col_type": {
        "fr": "Type", "en": "Type", "de": "Typ", "it": "Tipo",
    },
    "donnees_col_description": {
        "fr": "Description", "en": "Description",
        "de": "Beschreibung", "it": "Descrizione",
    },
    "donnees_restrictions": {
        "fr": "Ce qui ne figure pas dans le jeu de données",
        "en": "What the dataset does not contain",
        "de": "Was der Datensatz nicht enthält",
        "it": "Cosa non contiene il set di dati",
    },
    "donnees_r1_titre": {
        "fr": "Aucun récit intégral.", "en": "No full narrative.",
        "de": "Keine vollständigen Berichte.", "it": "Nessun racconto integrale.",
    },
    "donnees_r1": {
        "fr": "Seule la qualification structurée est exportée, accompagnée de "
              "la longueur du récit comme indicateur de richesse.",
        "en": "Only the structured classification is exported, along with the "
              "narrative length as an indicator of richness.",
        "de": "Nur die strukturierte Einordnung wird exportiert, ergänzt um "
              "die Textlänge als Hinweis auf den Detailgrad.",
        "it": "Solo la qualificazione strutturata è esportata, con la lunghezza "
              "del racconto come indicatore di ricchezza.",
    },
    "donnees_r2_titre": {
        "fr": "Aucune date précise.", "en": "No precise dates.",
        "de": "Keine genauen Daten.", "it": "Nessuna data precisa.",
    },
    "donnees_r2": {
        "fr": "L'année seule est conservée, le jour et le mois étant retirés "
              "pour limiter le risque de réidentification.",
        "en": "Only the year is kept, day and month being removed to limit "
              "the risk of reidentification.",
        "de": "Nur das Jahr bleibt erhalten, Tag und Monat werden entfernt, um "
              "das Risiko einer Reidentifikation zu verringern.",
        "it": "È conservato solo l'anno, giorno e mese sono rimossi per "
              "limitare il rischio di reidentificazione.",
    },
    "donnees_r3_titre": {
        "fr": "Aucun identifiant de personne.", "en": "No personal identifier.",
        "de": "Keine Personenkennung.", "it": "Nessun identificativo personale.",
    },
    "donnees_r3": {
        "fr": "Les identifiants sont propres au jeu de données et ne "
              "permettent aucun rapprochement avec une personne.",
        "en": "Identifiers are specific to the dataset and allow no link to "
              "an individual.",
        "de": "Die Kennungen gelten nur innerhalb des Datensatzes und lassen "
              "keinen Rückschluss auf Personen zu.",
        "it": "Gli identificativi sono propri del set di dati e non permettono "
              "alcun collegamento con una persona.",
    },
    "donnees_r4_titre": {
        "fr": "Consentement requis.", "en": "Consent required.",
        "de": "Zustimmung erforderlich.", "it": "Consenso richiesto.",
    },
    "donnees_r4": {
        "fr": "Seuls les témoignages dont le contributeur a explicitement "
              "autorisé un usage externe figurent dans l'export.",
        "en": "Only accounts whose contributor explicitly authorised external "
              "use appear in the export.",
        "de": "Nur Berichte, deren Verfasser einer externen Nutzung "
              "ausdrücklich zugestimmt hat, erscheinen im Export.",
        "it": "Solo le testimonianze il cui contributore ha esplicitamente "
              "autorizzato un uso esterno figurano nell'export.",
    },
    "donnees_fair": {
        "fr": "Alignement sur les principes FAIR",
        "en": "Alignment with FAIR principles",
        "de": "Ausrichtung an den FAIR-Prinzipien",
        "it": "Allineamento ai principi FAIR",
    },
    "donnees_fair_intro": {
        "fr": "Les principes FAIR visent à rendre les données de recherche "
              "repérables, accessibles, interopérables et réutilisables. Le "
              "prototype s'y aligne dans les limites suivantes.",
        "en": "The FAIR principles aim to make research data findable, "
              "accessible, interoperable and reusable. The prototype aligns "
              "with them within the following limits.",
        "de": "Die FAIR-Prinzipien sollen Forschungsdaten auffindbar, "
              "zugänglich, interoperabel und wiederverwendbar machen. Der "
              "Prototyp folgt ihnen im nachstehenden Rahmen.",
        "it": "I principi FAIR mirano a rendere i dati di ricerca "
              "reperibili, accessibili, interoperabili e riutilizzabili. Il "
              "prototipo vi si allinea entro i limiti seguenti.",
    },
    "donnees_findable": {
        "fr": "chaque signalement porte un identifiant stable et les "
              "métadonnées sont exposées séparément, sans identifiant pérenne "
              "de type DOI à ce stade",
        "en": "each report carries a stable identifier and metadata is exposed "
              "separately, without a persistent identifier such as a DOI at "
              "this stage",
        "de": "jede Meldung trägt eine stabile Kennung und die Metadaten sind "
              "separat abrufbar, ohne persistenten Bezeichner wie DOI in "
              "diesem Stadium",
        "it": "ogni segnalazione porta un identificativo stabile e i metadati "
              "sono esposti separatamente, senza identificativo persistente "
              "di tipo DOI in questa fase",
    },
    "donnees_accessible": {
        "fr": "les données agrégées sont téléchargeables librement par un "
              "protocole standard, sans authentification",
        "en": "aggregated data is freely downloadable through a standard "
              "protocol, without authentication",
        "de": "aggregierte Daten sind über ein Standardprotokoll frei "
              "herunterladbar, ohne Authentifizierung",
        "it": "i dati aggregati sono liberamente scaricabili tramite un "
              "protocollo standard, senza autenticazione",
    },
    "donnees_interoperable": {
        "fr": "les formats CSV et JSON sont ouverts, la nomenclature repose "
              "sur des codes stables et les pathologies portent leur "
              "identifiant Orphanet",
        "en": "the CSV and JSON formats are open, the classification relies on "
              "stable codes and conditions carry their Orphanet identifier",
        "de": "die Formate CSV und JSON sind offen, die Systematik beruht auf "
              "stabilen Codes und Erkrankungen tragen ihre Orphanet-Kennung",
        "it": "i formati CSV e JSON sono aperti, la nomenclatura si basa su "
              "codici stabili e le patologie portano il loro identificativo "
              "Orphanet",
    },
    "donnees_reusable": {
        "fr": "chaque variable est documentée, la licence est explicite et les "
              "conditions de consentement sont respectées",
        "en": "each variable is documented, the licence is explicit and "
              "consent conditions are respected",
        "de": "jede Variable ist dokumentiert, die Lizenz ist explizit und die "
              "Zustimmungsbedingungen werden eingehalten",
        "it": "ogni variabile è documentata, la licenza è esplicita e le "
              "condizioni di consenso sono rispettate",
    },
})


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
