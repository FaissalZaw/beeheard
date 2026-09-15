/**
 * Comportements du formulaire de dépôt.
 *
 * Deux fonctions assistent la saisie : un compteur de caractères sur le
 * récit, et une dictée vocale lorsque le navigateur la prend en charge.
 */

(function () {
  "use strict";

  const LONGUEUR_MINIMALE = 30;
  const LONGUEUR_MAXIMALE = 3000;

  const recit = document.getElementById("recit");
  const compteur = document.getElementById("compteur-recit");

  /* ── Compteur de caractères ─────────────────────── */

  function actualiserCompteur() {
    const longueur = recit.value.length;
    compteur.textContent = longueur + " / " + LONGUEUR_MAXIMALE + " caractères";

    compteur.classList.remove("compteur-insuffisant", "compteur-limite");

    if (longueur > 0 && longueur < LONGUEUR_MINIMALE) {
      compteur.classList.add("compteur-insuffisant");
      compteur.textContent =
        longueur + " / " + LONGUEUR_MAXIMALE +
        " caractères (minimum " + LONGUEUR_MINIMALE + ")";
    } else if (longueur > LONGUEUR_MAXIMALE - 200) {
      compteur.classList.add("compteur-limite");
    }
  }

  if (recit && compteur) {
    recit.addEventListener("input", actualiserCompteur);
    actualiserCompteur();
  }

  /* ── Dictée vocale ──────────────────────────────── */

  const Reconnaissance =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  const bouton = document.getElementById("bouton-dictee");
  const libelle = document.getElementById("libelle-dictee");

  if (!Reconnaissance || !bouton) {
    return;
  }

  bouton.hidden = false;

  const reconnaissance = new Reconnaissance();
  reconnaissance.lang = "fr-CH";
  reconnaissance.continuous = true;
  reconnaissance.interimResults = false;

  let enEcoute = false;

  function demarrer() {
    try {
      reconnaissance.start();
    } catch (erreur) {
      console.warn("Dictée indisponible :", erreur);
    }
  }

  function arreter() {
    reconnaissance.stop();
  }

  bouton.addEventListener("click", function () {
    if (enEcoute) {
      arreter();
    } else {
      demarrer();
    }
  });

  reconnaissance.addEventListener("start", function () {
    enEcoute = true;
    bouton.classList.add("dictee-active");
    libelle.textContent = "Arrêter la dictée";
    recit.setAttribute("aria-busy", "true");
  });

  reconnaissance.addEventListener("end", function () {
    enEcoute = false;
    bouton.classList.remove("dictee-active");
    libelle.textContent = "Dicter";
    recit.removeAttribute("aria-busy");
  });

  reconnaissance.addEventListener("result", function (evenement) {
    let transcription = "";

    for (let i = evenement.resultIndex; i < evenement.results.length; i++) {
      if (evenement.results[i].isFinal) {
        transcription += evenement.results[i][0].transcript;
      }
    }

    if (!transcription) {
      return;
    }

    const separateur = recit.value.trim().length > 0 ? " " : "";
    const ajout = transcription.trim();
    const disponible = LONGUEUR_MAXIMALE - recit.value.length;

    recit.value += separateur + ajout.slice(0, Math.max(0, disponible));
    actualiserCompteur();
  });

  reconnaissance.addEventListener("error", function (evenement) {
    if (evenement.error === "not-allowed") {
      libelle.textContent = "Micro refusé";
    } else if (evenement.error === "no-speech") {
      return;
    } else {
      libelle.textContent = "Dictée indisponible";
    }
    bouton.disabled = true;
  });
})();
