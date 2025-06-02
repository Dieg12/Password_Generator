#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de mot de passe au format "motXX!motXX!..." à partir d'une wordlist,
avec au moins un mot entièrement en majuscule et au moins un mot entièrement en minuscule.

Usage :
    python3 generateur.py wordlist.txt 5 4 6

Ici :
  - "wordlist.txt" est un fichier texte contenant un mot par ligne.
    Si la première ligne ressemble à un dictionnaire Python (ex. {2: 0, 3: 10, …}), 
    elle sera automatiquement ignorée.
  - Les arguments suivants (5, 4, 6, etc.) sont les longueurs des mots souhaités, 
    dans l'ordre. Il y aura autant de segments "motXX" que de longueurs spécifiées.
  - Il faut fournir au minimum deux longueurs pour garantir qu'il y ait 
    un mot en majuscule et un mot en minuscule.

Pour chaque longueur demandée :
  1) Le programme parcourt en boucle (en mémoire) des mots aléatoires de cette longueur,
     sans les afficher.
  2) L’utilisateur appuie simplement sur ENTRÉE pour stopper la sélection de ce mot ;
     le dernier mot "tiré" sera retenu.
  3) Un nombre aléatoire entre 00 et 99 (au format deux chiffres) est généré.
  4) Un caractère spécial aléatoire est choisi parmi "!@#$%&*".
  5) Au moins un segment sera forcé en majuscules et au moins un autre en minuscules.
  6) On enchaîne les segments sous la forme "motXX!" sauf pour le dernier segment,
     qui est "motXX" (sans caractère spécial final).

Exemple d’invocation :
    python3 generateur.py wordlist.txt 5 4 6

Le script affichera des consignes à l’utilisateur pour chaque mot de longueur 5, 4, puis 6,
et renverra quelque chose comme :
    KANTE73#wero09%bleu21
(ici "KANTE" est en majuscule, "wero" et "bleu" en minuscule).
"""

import sys
import threading
import random
import time

def charger_wordlist(path):
    """
    Charge tous les mots d'un fichier (un mot par ligne). 
    Si la première ligne ressemble à un dict Python (startwith "{" et contient ":"),
    on la saute.
    Retourne une liste de mots (sans nouvelle ligne ni espaces).
    """
    mots = []
    with open(path, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
    start = 0
    if lignes:
        premiere = lignes[0].strip()
        if premiere.startswith("{") and ":" in premiere and premiere.endswith("}"):
            start = 1  # on ignore la première ligne
    for ligne in lignes[start:]:
        w = ligne.strip()
        if not w:
            continue
        mots.append(w)
    return mots

def selectionner_mot_aleatoire(liste_mots, longueur):
    """
    Parcourt en boucle des mots aléatoires de 'liste_mots' (tous présumés avoir la bonne longueur),
    sans les afficher. L'utilisateur doit appuyer sur Entrée pour stopper le tirage ;
    on renvoie alors le dernier mot sélectionné.
    """
    stop_event = threading.Event()

    def attente_entree():
        # Laisser l'utilisateur appuyer sur Entrée pour stopper.
        input()
        stop_event.set()

    thread = threading.Thread(target=attente_entree, daemon=True)
    thread.start()

    mot_courant = None
    # Boucle tant que l'utilisateur n'a pas appuyé sur Entrée
    while not stop_event.is_set():
        mot_courant = random.choice(liste_mots)
        # On peut insérer un tout petit délai pour éviter une boucle CPU trop agressive
        time.sleep(0.01)

    thread.join()
    return mot_courant

def main():
    if len(sys.argv) < 4:
        print("Usage : python3 generateur.py wordlist.txt <longueur1> <longueur2> [<longueur3> ...]")
        print("Il faut au minimum deux longueurs pour garantir un mot en majuscule et un mot en minuscule.")
        sys.exit(1)

    chemin_wordlist = sys.argv[1]
    try:
        longueurs = [int(x) for x in sys.argv[2:]]
    except ValueError:
        print("Les longueurs doivent être des entiers. Exemple : 5 4 6")
        sys.exit(1)

    if len(longueurs) < 2:
        print("Erreur : veuillez fournir au moins deux longueurs,")
        print("afin d'assurer qu'un mot soit en majuscule et un autre en minuscule.")
        sys.exit(1)

    # 1) Chargement de la wordlist
    try:
        tous_mots = charger_wordlist(chemin_wordlist)
    except FileNotFoundError:
        print(f"Erreur : impossible d'ouvrir le fichier '{chemin_wordlist}'.")
        sys.exit(1)

    # 2) On pré-groupe les mots par longueur dans un dict (pour accélérer la sélection)
    buckets = {}
    for w in tous_mots:
        L = len(w)
        buckets.setdefault(L, []).append(w)

    # Vérification que pour chaque longueur souhaitée, on a au moins un mot
    for L in longueurs:
        if L not in buckets or not buckets[L]:
            print(f"Erreur : aucun mot de longueur {L} trouvé dans la wordlist.")
            sys.exit(1)

    # 3) Pour chaque longueur demandée, on sélectionne un mot aléatoire (en mode "roulette")
    segments = []
    caracteres_speciaux = "!@#$%&*"

    for idx, L in enumerate(longueurs, start=1):
        print(f"--- Sélection du mot #{idx} (longueur {L}) ---")
        print("Appuyez sur ENTRÉE quand vous voulez fixer le mot tiré au hasard.")
        mot_choisi = selectionner_mot_aleatoire(buckets[L], L)
        # num aléatoire deux chiffres (00 à 99)
        numero = f"{random.randint(0, 99):02d}"
        segments.append((mot_choisi, numero))

    # 4) On choisit un index pour forcer en majuscules, les autres resteront en minuscule
    n = len(segments)
    uppercase_index = random.randrange(n)

    # 5) Construction du mot de passe en appliquant la casse désirée
    password_parts = []
    for i, (mot, num) in enumerate(segments):
        if i == uppercase_index:
            mot_affiche = mot.upper()
        else:
            mot_affiche = mot.lower()
        if i < n - 1:
            special = random.choice(caracteres_speciaux)
            password_parts.append(f"{mot_affiche}{num}{special}")
        else:
            password_parts.append(f"{mot_affiche}{num}")

    mot_de_passe = "".join(password_parts)
    print("\n=== Mot de passe généré ===")
    print(mot_de_passe)

if __name__ == "__main__":
    main()
