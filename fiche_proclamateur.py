"""Script qui écrit un fichier word pour les monitions."""

import sys
import re
import locale
from datetime import datetime, date
import pandas as pd
from docxtpl import DocxTemplate

def mois_francais(mois_num):
    mois = [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"
    ]
    return mois[mois_num - 1]

def format_date_fr_safe(d: date) -> str:
    jour = d.day
    mois = mois_francais(d.month)
    annee = d.year
    return f"{jour:02d} {mois} {annee}"


# === CONFIGURATION ===
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
EXCEL_FILE = "monitions.xlsm"  # Ton fichier source
SHEET_MONITIONS = "Feuil1"  # Onglet contenant les monitions
SHEET_META = "Feuil2"  # Onglet contenant l'année liturgique et le début de l'Avent
TEMPLATE_FILE = "fiche_modele.docx"
OUTPUT_FILE = "fiche_proclamateur_{}.docx"

# === Récupération de la date cible en argument ===
if len(sys.argv) < 2:
    print("Usage: python fiche_proclamateur.py JJ/MM/AAAA")
    sys.exit(1)
DATE_CIBLE = datetime.strptime(sys.argv[1], "%d/%m/%Y")

# === Lecture des métadonnées ===
meta = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_META, header=None, index_col=None)
CYCLE = str(meta.iloc[0, 1]).strip()
DEBUT_AVENT = pd.to_datetime(meta.iloc[1, 5], dayfirst=True)

# === Lecture des monitions ===
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_MONITIONS)

df["date"] = pd.to_datetime(df["date"], dayfirst=True)
ligne = df[df["date"] == DATE_CIBLE]
if ligne.empty:
    raise ValueError("Date non trouvée dans le fichier Excel.")
ligne = ligne.iloc[0]

# === Extraction des lectures dynamiques ===
def extraire_monition(cell):
    """Extrait la monition."""
    if pd.isna(cell):
        return ("", "")
    cell = str(cell).strip()
    # cell = re.sub(r"\s+[-–—]\s+", " — ", cell, 1)  # unifie le séparateur
    parts = str(cell).split("—", 1)
    return parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""

lectures = []
for i in range(1, 9):
    key = f"lecture{i}_{CYCLE}"
    if key not in ligne or pd.isna(ligne[key]):
        continue
    ref, mon = extraire_monition(ligne[key])
    titre = f"{i}re lecture" if i == 1 else f"{i}e lecture"
    lectures.append({
        "num": i,
        "titre": titre,
        "ref": ref,
        "mon": mon
    })

# === Remplissage du modèle ===
tpl = DocxTemplate(TEMPLATE_FILE)
context = {
    "date": format_date_fr_safe(DATE_CIBLE),
    "nom_fete": f"{ligne['nom_fête']} – Année {CYCLE}",
    "lectures": lectures
}
tpl.render(context)
# === Création du document Word ===
tpl.save(OUTPUT_FILE.format(DATE_CIBLE.strftime("%Y-%m-%d")))
print("Fiche proclamateur générée avec succès !")
