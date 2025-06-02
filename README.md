# Générateur de mots de passe

Ce document explique le fonctionnement du script **`password_generator.py`**, le format attendu de la **wordlist**, ainsi qu’un exemple de commande pour générer un mot de passe.

---

## 1. Présentation

Le script **`password_generator.py`** permet de construire un mot de passe sous la forme :

```
mot1XX!mot2XX!mot3XX...
```

- `motN` : un mot aléatoire choisi dans une liste (wordlist), de longueur fixée par l’utilisateur.  
- `XX`   : un nombre aléatoire de 00 à 99 (toujours sur deux chiffres, avec un zéro devant si nécessaire).  
- `!`    : un caractère spécial choisi au hasard parmi `!@#$%&*`.  
- À la fin du mot de passe, **il n’y a pas** de caractère spécial supplémentaire.  

En plus, le script garantit qu’au moins l’un des mots est **entièrement en majuscules** et qu’au moins un autre mot est **entièrement en minuscules**.

L’utilisateur choisit, via les arguments de la ligne de commande, la ou les longueurs souhaitées pour chaque segment. Le mot de passe comportera donc autant de blocs `(mot+chiffres)` que de longueurs indiquées.

---

## 2. Format de la wordlist

Le script s’appuie sur un fichier texte (wordlist) contenant **un mot par ligne**. Voici les règles à respecter :

1. **Encodage** : UTF-8  
2. **Structure** :  
   - Si la première ligne ressemble à un dictionnaire Python (par exemple `{2: 0, 3: 10, …}`), elle sera **automatiquement ignorée**.  
   - Toutes les autres lignes doivent contenir **exactement un mot**, sans espaces ni caractères parasites.  
   - Les majuscules et minuscules sont acceptées dans la liste d’entrée, car le script **ne filtre pas** sur la casse ; il se contente de sélectionner un mot et de le transformer ensuite en `upper()` ou `lower()`.

### Exemple de wordlist minimale (`wordlist.txt`)

```
{2: 0, 3: 15, 4: 45}
arbre
Chat
maison
PLUIE
soleil
ecole
porte
CHAUD
mitre
```

---

## 3. Installation et prérequis

- **Python 3.6+** requis  
- Aucune dépendance externe  
- Placez `password_generator.py` et `wordlist.txt` dans le même dossier (ou indiquez le chemin complet)

---

## 4. Utilisation

```bash
python3 password_generator.py <chemin_wordlist> <longueur1> <longueur2> [<longueur3> ...]
```

Exemple :

```bash
python3 password_generator.py wordlist.txt 5 4 6
```

---

## 5. Format final du mot de passe

Exemple :

```
plane73#PORT08%maison21
```

- `plane73#` → minuscule  
- `PORT08%`  → majuscule  
- `maison21` → minuscule (pas de caractère à la fin)

---

## 6. Conseils

- Utilisez une wordlist diversifiée  
- Le tirage des mots est non visible et stoppé manuellement pour plus d'entropie  
- Gardez la wordlist confidentielle

---

## 7. Problèmes fréquents

- **Fichier introuvable** : vérifiez le chemin  
- **Pas de mot pour une longueur donnée** : complétez la wordlist  
- **Moins de 2 longueurs** : le script exige au moins un mot en minuscule + un en majuscule  

(README généré par IA)