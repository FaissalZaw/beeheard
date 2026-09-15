"""Traductions de la nomenclature des obstacles.

Les libellés sources sont en français. Ce module fournit leurs équivalents
en anglais, allemand et italien, les trois autres langues pertinentes pour
le contexte suisse.
"""

TRADUCTIONS_CATEGORIES = {
    "economique": {
        "en": ("Economic and pricing barriers",
               "Barriers related to treatment cost, reimbursement or the "
               "inadequacy of payment mechanisms."),
        "de": ("Wirtschaftliche und tarifliche Hindernisse",
               "Hindernisse im Zusammenhang mit Behandlungskosten, Vergütung "
               "oder unzureichenden Zahlungsmechanismen."),
        "it": ("Ostacoli economici e tariffari",
               "Ostacoli legati al costo del trattamento, al rimborso o "
               "all'inadeguatezza dei meccanismi di pagamento."),
    },
    "organisationnel": {
        "en": ("Organisational and political barriers",
               "Barriers related to care structures, administrative delays "
               "and the absence of dedicated processes."),
        "de": ("Organisatorische und politische Hindernisse",
               "Hindernisse im Zusammenhang mit Versorgungsstrukturen, "
               "administrativen Verzögerungen und fehlenden Verfahren."),
        "it": ("Ostacoli organizzativi e politici",
               "Ostacoli legati alla struttura di presa in carico, ai ritardi "
               "amministrativi e all'assenza di procedure dedicate."),
    },
    "informationnel": {
        "en": ("Informational barriers",
               "Barriers related to the absence, dispersion or opacity of the "
               "information needed to access treatment."),
        "de": ("Informationsbezogene Hindernisse",
               "Hindernisse durch fehlende, verstreute oder intransparente "
               "Informationen für den Zugang zur Behandlung."),
        "it": ("Ostacoli informativi",
               "Ostacoli legati all'assenza, alla dispersione o all'opacità "
               "delle informazioni necessarie per accedere al trattamento."),
    },
    "social": {
        "en": ("Social determinants and discrimination",
               "Barriers related to living conditions, stigma and linguistic "
               "or cultural obstacles."),
        "de": ("Soziale Determinanten und Diskriminierung",
               "Hindernisse im Zusammenhang mit Lebensbedingungen, "
               "Stigmatisierung sowie sprachlichen oder kulturellen Barrieren."),
        "it": ("Determinanti sociali e discriminazione",
               "Ostacoli legati alle condizioni di vita, alla stigmatizzazione "
               "e alle barriere linguistiche o culturali."),
    },
}

TRADUCTIONS_TYPES = {
    # Économiques
    "refus_remboursement": {
        "en": "Reimbursement refused by the insurer",
        "de": "Ablehnung der Kostenübernahme durch den Versicherer",
        "it": "Rifiuto di rimborso da parte dell'assicurazione",
    },
    "reste_a_charge": {
        "en": "Out-of-pocket costs too high",
        "de": "Zu hohe Eigenbeteiligung",
        "it": "Spese a carico troppo elevate",
    },
    "absence_voie_tarifaire": {
        "en": "No established reimbursement pathway",
        "de": "Kein etablierter Vergütungsweg",
        "it": "Assenza di una via di rimborso stabilita",
    },
    "cout_deplacement": {
        "en": "Cost of travel to the treatment centre",
        "de": "Reisekosten zum Behandlungszentrum",
        "it": "Costo degli spostamenti verso il centro di cura",
    },
    "perte_revenu": {
        "en": "Income lost through work absences",
        "de": "Einkommensverlust durch Arbeitsausfälle",
        "it": "Perdita di reddito dovuta alle assenze dal lavoro",
    },
    "refus_de_financer": {
        "en": "Refusal to fund despite recognised eligibility",
        "de": "Finanzierungsverweigerung trotz anerkannter Berechtigung",
        "it": "Rifiuto di finanziamento nonostante l'idoneità riconosciuta",
    },
    # Organisationnels
    "delai_rendez_vous": {
        "en": "Waiting time for a specialist appointment",
        "de": "Wartezeit auf einen Facharzttermin",
        "it": "Tempi di attesa per una visita specialistica",
    },
    "absence_centre_reference": {
        "en": "No reference centre for the condition",
        "de": "Kein Referenzzentrum für die Erkrankung",
        "it": "Assenza di un centro di riferimento per la patologia",
    },
    "coordination_defaillante": {
        "en": "Poor coordination between care providers",
        "de": "Mangelnde Koordination zwischen den Beteiligten",
        "it": "Cattivo coordinamento tra gli operatori",
    },
    "refus_prise_en_charge": {
        "en": "Care refused by a healthcare facility",
        "de": "Behandlungsablehnung durch eine Einrichtung",
        "it": "Rifiuto di presa in carico da parte di una struttura",
    },
    "delai_administratif": {
        "en": "Processing time for an administrative request",
        "de": "Bearbeitungsdauer eines administrativen Antrags",
        "it": "Tempi di trattamento di una domanda amministrativa",
    },
    "errance_diagnostique": {
        "en": "Time elapsed before diagnosis",
        "de": "Zeit bis zur Diagnosestellung",
        "it": "Tempo trascorso prima della diagnosi",
    },
    "non_prise_en_compte_information": {
        "en": "Information provided by the patient disregarded",
        "de": "Vom Patienten übermittelte Informationen unberücksichtigt",
        "it": "Informazioni fornite dal paziente non prese in considerazione",
    },
    "medecine_defensive": {
        "en": "Decision driven by institutional caution rather than need",
        "de": "Entscheidung aus institutioneller Vorsicht statt nach Bedarf",
        "it": "Decisione guidata dalla prudenza istituzionale anziché dal bisogno",
    },
    "deni_institutionnel": {
        "en": "Denial of the problem by the institution approached",
        "de": "Leugnung des Problems durch die angefragte Institution",
        "it": "Negazione del problema da parte dell'istituzione interpellata",
    },
    "blocage_politique": {
        "en": "Deadlock caused by disagreement between institutions or actors",
        "de": "Blockade durch Uneinigkeit zwischen Institutionen oder Akteuren",
        "it": "Blocco dovuto a disaccordo tra istituzioni o attori",
    },
    # Informationnels
    "information_indisponible": {
        "en": "No information available on treatment options",
        "de": "Keine Informationen zu Behandlungsoptionen verfügbar",
        "it": "Informazioni non disponibili sulle opzioni di trattamento",
    },
    "procedure_opaque": {
        "en": "Application procedure unclear or undocumented",
        "de": "Antragsverfahren unklar oder nicht dokumentiert",
        "it": "Procedura di domanda poco chiara o non documentata",
    },
    "absence_donnees": {
        "en": "No data on the condition or the population concerned",
        "de": "Keine Daten zur Erkrankung oder betroffenen Bevölkerung",
        "it": "Assenza di dati sulla patologia o sulla popolazione interessata",
    },
    "information_contradictoire": {
        "en": "Contradictory information between interlocutors",
        "de": "Widersprüchliche Auskünfte verschiedener Stellen",
        "it": "Informazioni contraddittorie tra gli interlocutori",
    },
    "meconnaissance_soignants": {
        "en": "Condition poorly known to healthcare staff",
        "de": "Unkenntnis der Erkrankung beim Behandlungspersonal",
        "it": "Scarsa conoscenza della patologia da parte del personale sanitario",
    },
    # Sociaux
    "transport_limite": {
        "en": "Difficulty travelling to care facilities",
        "de": "Schwierigkeiten bei der Anreise zu Behandlungsorten",
        "it": "Difficoltà di trasporto verso i luoghi di cura",
    },
    "stigmatisation": {
        "en": "Stigma associated with the condition",
        "de": "Stigmatisierung aufgrund der Erkrankung",
        "it": "Stigmatizzazione legata alla patologia",
    },
    "barriere_linguistique": {
        "en": "Language barrier in the care relationship",
        "de": "Sprachbarriere in der Behandlungsbeziehung",
        "it": "Barriera linguistica nella relazione di cura",
    },
    "impact_professionnel": {
        "en": "Consequences for working life",
        "de": "Auswirkungen auf die Erwerbstätigkeit",
        "it": "Ripercussioni sull'attività professionale",
    },
    "isolement": {
        "en": "Social isolation or lack of support",
        "de": "Soziale Isolation oder fehlende Unterstützung",
        "it": "Isolamento sociale o assenza di sostegno",
    },
    "mise_en_doute_parole": {
        "en": "Account or symptoms questioned by healthcare staff",
        "de": "Anzweiflung der Schilderung oder Symptome durch Fachpersonal",
        "it": "Parola o sintomi messi in dubbio dal personale sanitario",
    },
    "absence_ecoute": {
        "en": "Request not listened to or not taken seriously",
        "de": "Anliegen nicht angehört oder nicht ernst genommen",
        "it": "Assenza di ascolto o di presa sul serio della richiesta",
    },
    "mauvaise_foi": {
        "en": "Bad-faith response or unfounded argument opposed to the request",
        "de": "Antwort in schlechtem Glauben oder unbegründete Ablehnung",
        "it": "Risposta in malafede o argomento infondato opposto alla richiesta",
    },
}
