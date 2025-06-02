#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour :
  - supprimer tous les mots commençant par une majuscule (word[0].isupper())
  - exclure tous les mots de plus de 15 caractères
  - exclure tous les mots contenant un espace
  - trier les mots restants par longueur croissante (bucket sort linéaire)
  - préfixer le fichier de sortie par un dictionnaire Python {longueur: ligne_début},
    où 'ligne_début' est le numéro de ligne (1-based) correspondant au premier mot
    de cette longueur DANS LE FICHIER (donc en tenant compte de la première ligne d’en-tête).

Usage :
    python3 tri_par_longueur.py input.txt output.txt

Après exécution, `output.txt` commencera par une ligne du type :
    {1: 2, 2: 524, 3: 1421, ...}
qui indique que, dans le fichier final :
  - le premier mot de longueur 1 se trouve à la ligne 2 (puisque la ligne 1 est l’en-tête),
  - le premier mot de longueur 2 se trouve à la ligne 524, etc.
"""

import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Supprime les mots commençant par une majuscule, "
                    "exclut ceux >15 caractères ou contenant des espaces, "
                    "trie par longueur, et génère un en-tête avec les offsets (y compris l’en-tête)."
    )
    parser.add_argument('input', help='Fichier texte d’entrée (un mot par ligne)')
    parser.add_argument('output', help='Fichier texte de sortie généré')
    args = parser.parse_args()

    # 1) Lecture et filtrage des mots
    mots = []
    with open(args.input, 'r', encoding='utf-8') as f_in:
        for ligne in f_in:
            w = ligne.strip()
            if not w:
                continue
            # Exclure si le premier caractère est une majuscule
            if w[0].isupper():
                continue
            # Exclure si longueur > 15
            if len(w) > 15:
                continue
            # Exclure si contient un espace
            if ' ' in w:
                continue
            mots.append(w)

    # 2) Regroupement par longueur (bucket sort)
    buckets = {}
    for w in mots:
        L = len(w)
        buckets.setdefault(L, []).append(w)

    # 3) On récupère la liste triée des longueurs existantes
    longueurs = sorted(buckets.keys())

    # 4) Calcul des offsets en tenant compte de l’en-tête
    #    - Pour chaque longueur L, on calcule la ligne (1-based) dans le fichier où commence
    #      le premier mot de cette longueur. La ligne 1 est réservée à l’en-tête.
    offsets = {}
    index_courant = 0
    for L in longueurs:
        # index_courant correspond à l’index 0-based dans la liste totale des mots sans en-tête
        # Pour obtenir la ligne 1-based dans le fichier (avec l’en-tête en ligne 1), on fait +2 :
        #   - +1 pour passer de 0-based à 1-based
        #   - +1 pour décaler d’une ligne (la première ligne est l’en-tête)
        offsets[L] = index_courant + 2
        index_courant += len(buckets[L])

    # 5) Écriture du fichier de sortie
    #    - première ligne : le dictionnaire Python des offsets (lignes 1-based dans le fichier)
    #    - ensuite, tous les mots triés par longueur (dans l’ordre des buckets)
    with open(args.output, 'w', encoding='utf-8') as f_out:
        # On écrit le dict littéral Python
        f_out.write(f"{offsets}\n")
        # Puis, pour chaque longueur dans l’ordre croissant, on écrit les mots
        for L in longueurs:
            for w in buckets[L]:
                f_out.write(w + "\n")


if __name__ == "__main__":
    main()
