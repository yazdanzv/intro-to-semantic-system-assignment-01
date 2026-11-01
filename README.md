# Intro to Semantic System — Assignment 01

TU Wien · 188.399 Introduction to Semantic Systems · Winter semester 2026/27

Assignment 1: **Ontology Modeling** (10 points). Deadline: **2 November 2026**, via TUWEL.

The chosen application is a **travel assistant for planning city trips**. The agreed scope and eight competency questions are recorded in [the decision log](notes/plan.md). The [working ontology](ontology/travel-assistant.owl) implements 18 classes, 26 properties, and five OWL construct kinds. It loads in Protégé and passed HermiT consistency and named-class satisfiability checks. All eight competency questions are covered at schema level under the interpretations in the decision log. The three-page report is available as an [editable Word document](report/A1_ZandiyeVakili_12642780_Report.docx) and a [PDF export](submission/A1_ZandiyeVakili_12642780_Report.pdf), with two diagrams and the OWL examples. Both formats were visually checked; final student review and TUWEL upload remain pending.

## Folder structure

```text
.
├── instructions/   # Original assignment brief, kept locally
├── ontology/       # Working ontology, edited in Protégé
├── notes/          # Application idea, competency questions, modeling decisions
├── report/         # Report source and supporting figures
└── submission/     # Final files prepared for TUWEL
```

## Getting started

1. Read the original brief in `instructions/`.
2. Review the agreed travel-assistant scope in [the decision log](notes/plan.md).
3. Review the eight agreed competency questions in the decision log.
4. Open `ontology/travel-assistant.owl` in Protégé. It includes the five agreed OWL construct kinds: disjointness, inverse properties, existential restriction, exact cardinality, and a functional datatype property. The original RDF(S) model is preserved in `ontology/baseline/travel-assistant-rdfs.owl`.
5. Review `report/report.md` and the editable DOCX report. `report/build_report.py` builds the document and ontology-derived diagrams using python-docx, RDFLib, ReportLab, and Poppler.
6. Prepare and reopen the final named ontology export in Protégé, review the report PDF already in `submission/`, and upload the two required deliverables to TUWEL.

## Assignment checklist

- [x] Application idea described in two paragraphs in the report.
- [x] 5–10 competency questions (eight agreed in the decision log and included in the report).
- [x] At least 15 concepts/classes (18 implemented).
- [x] At least 20 relations/properties, including both object and datatype properties (13 object and 13 datatype properties implemented).
- [x] Labels and comments for all ontology elements (English annotations checked).
- [x] An initial RDF(S) model extended with at least 5 OWL constructs (five distinct kinds implemented).
- [x] Ontology created from scratch; instances are not required for Assignment 1.
- [x] Turtle serialization that opens successfully in Protégé (verified with Protégé 5.6.9).
- [x] A three-page report describing the idea, all questions, seven modeling steps, and five OWL features with examples; includes two diagrams and a reflection. DOCX and PDF rendered and visually checked.
- [ ] Final filenames follow the brief: `A1_<family-name>_<student-number>_Ontology.owl` and `A1_<family-name>_<student-number>_Report.pdf`.
- [ ] Final files uploaded to TUWEL by the deadline.

Use **File → Save As → Turtle Syntax** in Protégé. The brief requires Turtle syntax with the `.owl` extension.

Version 0.2 passed Turtle parsing and structural checks with RDFLib 7.6.0 (222 triples). Its names, hierarchy, domains, ranges, five OWL construct kinds, and annotations match the decision log. It also loaded in Protégé 5.6.9 and was classified successfully by HermiT 1.4.3.456: no inconsistency or unsatisfiable named domain class was found. The original baseline remains unchanged. Schema-level coverage of all eight competency questions was also verified against the required classes, properties, domains, ranges, and inheritance. No instance-level behavioral tests were performed; details, interpretations, and evidence are recorded in the decision log.

## Working with Git

Run Git commands from this repository directory:

```sh
git status
git add README.md ontology/ notes/ report/
git commit -m "Describe the modeling changes"
git push
```

The original course brief, editor backup files, temporary report renders, and submission exports are ignored by default. The completed report PDF is explicitly included in version control. Keep the editable ontology and report sources in their working folders. Add optional code, data, or query folders only if needed later.

The original brief is authoritative if this summary differs from it. Check TUWEL for any additional course or AI-assistance policies before doing the assessed work.
