import json
import itertools
import os
from docxtpl import DocxTemplate
from docx import Document

TEMPLATE_FILE = "fiche_modele.docx"
JSON_FILE = "monitions_livre.json"
OUTPUT_FILE = "monitions_livre.docx"

def titre_lecture(index: int) -> str:
    if index == 0:
        return "1re lecture"
    return f"{index+1}e lecture"

def group_entries(entries):
    keyfunc = lambda x: (x["solennite"], x["annee"])
    grouped = []
    for key, group in itertools.groupby(entries, keyfunc):
        grouped.append((key, list(group)))
    return grouped

def main():
    with open(JSON_FILE, encoding="utf-8") as f:
        data = json.load(f)

    groups = group_entries(data)
    final_doc = None
    tmp_name = "_tmp.docx"

    for (solennite, annee), items in groups:
        tpl = DocxTemplate(TEMPLATE_FILE)
        lectures = []
        for i, item in enumerate(items):
            lectures.append({
                "titre": titre_lecture(i),
                "ref": item["ref_bib"],
                "mon": item["monition"],
            })
        context = {
            "date": solennite,
            "nom_fete": f"{solennite} – Année {annee}",
            "lectures": lectures,
        }
        tpl.render(context)
        tpl.save(tmp_name)
        doc_part = Document(tmp_name)
        if final_doc is None:
            final_doc = doc_part
        else:
            for element in doc_part.element.body:
                final_doc.element.body.append(element)
        os.remove(tmp_name)

    if final_doc is not None:
        final_doc.save(OUTPUT_FILE)
        print(f"Document généré : {OUTPUT_FILE}")
    else:
        print("Aucune donnée à traiter.")

if __name__ == "__main__":
    main()
