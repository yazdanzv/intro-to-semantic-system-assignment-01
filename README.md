# Intro to Semantic System — Assignment 01

TU Wien · 188.399 Introduction to Semantic Systems · Winter semester 2026/27

Assignment 1: **Ontology Modeling** (10 points). Deadline: **2 November 2026**, via TUWEL.

This repository starts with a planning outline and a report outline. The domain, application idea, and ontology have not yet been developed.

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
2. Choose a domain and describe an application idea in `notes/plan.md`.
3. Write 5–10 competency questions that guide the ontology's scope.
4. Build the ontology from scratch in Protégé, starting with RDF(S) and then adding OWL constructs. Save the working file under `ontology/`.
5. Complete `report/report.md` as you work, recording the actual modeling steps and OWL examples.
6. Check the ontology in Protégé, export the report to PDF, and place the two final deliverables in `submission/`.

## Assignment checklist

- [ ] Application idea described in 2–3 paragraphs.
- [ ] 5–10 competency questions.
- [ ] At least 15 concepts/classes.
- [ ] At least 20 relations/properties, including both object and datatype properties.
- [ ] Labels and comments for all ontology elements.
- [ ] An initial RDF(S) model extended with at least 5 OWL constructs.
- [ ] Ontology created from scratch; instances are not required for Assignment 1.
- [ ] Turtle serialization that opens successfully in Protégé.
- [ ] A 2–3 page report describing the idea, questions, modeling steps, and OWL features with examples.
- [ ] Final filenames follow the brief: `A1_<family-name>_<student-number>_Ontology.owl` and `A1_<family-name>_<student-number>_Report.pdf`.
- [ ] Final files uploaded to TUWEL by the deadline.

Use **File → Save As → Turtle Syntax** in Protégé. The brief requires Turtle syntax with the `.owl` extension.

## Working with Git

Run Git commands from this repository directory:

```sh
git status
git add README.md ontology/ notes/ report/
git commit -m "Describe the modeling changes"
git push
```

The original course brief, editor backup files, and submission exports are ignored by default. Keep the editable ontology and report sources in their working folders. Add optional code, data, or query folders only if needed later.

The original brief is authoritative if this summary differs from it. Check TUWEL for any additional course or AI-assistance policies before doing the assessed work.
