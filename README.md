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
