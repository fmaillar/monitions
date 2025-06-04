# Monitions

Ce dépôt regroupe des fichiers JSON contenant des "monitions" liturgiques.

## Contenu

- **monitions.json** : monitions quotidiennes pour l'année 2025. Chaque entrée associe une date en français à la référence biblique et au texte correspondant.
- **monitions_livre.json** : ensemble de monitions pour les solennités et fêtes, classées par année liturgique (A, B ou C). Les entrées sont listées avec la solennité, la référence biblique et le texte de la monition.

## Structure des données

### monitions.json
```json
{
  "Mardi 1er avril 2025": {
    "lecture": "Ézékiel 47, 1-9.12",
    "monition": "Ézékiel décrit l'eau jaillissant du Temple, apportant vie et fertilité partout où elle s'écoule."
  },
  ...
}
```

### monitions_livre.json
```json
[
  {
    "solennite": "1er dimanche de l’Avent",
    "annee": "A",
    "ref_bib": "Isaïe 2, 1-5",
    "monition": "Isaïe invite à marcher dans la lumière du Seigneur pour accueillir la paix entre les nations."
  },
  ...
]
```

Ces fichiers peuvent être consultés tels quels ou importés dans un outil capable de traiter du JSON afin de générer des documents ou sites web.


## Génération de fiches proclamateur

Un fichier Excel **monitions.xlsm** se trouve à la racine du dépôt. Il sert de source de données pour le script `fiche_proclamateur.py` qui génère un document Word à partir du modèle `fiche_modele.docx`.

### Packages Python requis

- `pandas`
- `docxtpl`

### Exemple

```bash
python fiche_proclamateur.py JJ/MM/AAAA
```

## Générer un livre Word

Le script `generer_livre.py` parcourt `monitions_livre.json` et assemble toutes les fiches dans un seul document Word. Il nécessite `docxtpl` et `python-docx`.

### Installation des dépendances

```bash
pip install docxtpl python-docx
```

### Utilisation

```bash
python generer_livre.py
```

Le fichier `monitions_livre.docx` sera créé à la racine du projet, contenant les fiches pour toutes les solennités classées par ordre liturgique.

