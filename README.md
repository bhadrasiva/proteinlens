# ProteinLens

AI-assisted protein intelligence platform for drug discovery research.

ProteinLens accepts a human gene/protein identifier and generates a structured drug discovery briefing by retrieving information from public biological databases and applying evidence-grounded AI analysis.

The system combines protein annotation, drug information, disease associations, structural data, and scientific literature into a single workflow.

---

## Overview

ProteinLens integrates multiple biological resources to provide a consolidated view of a protein target.

The application uses:

- UniProt for protein information and functional annotations
- ChEMBL for drug and compound information
- OpenTargets for target-disease associations
- PubMed for scientific literature retrieval
- Gemini AI for evidence-based analysis
- RCSB PDB Mol* for 3D structure visualization

---

## Features

### Protein Data Retrieval

- Protein function and description
- Gene and protein identifiers
- Functional annotations
- Protein sequence
- Available 3D structures

Source:
UniProt REST API

---

### Drug Discovery Information

- Approved drugs
- Clinical compounds
- Compound-target relationships

Source:
ChEMBL API

---

### Disease Association Analysis

- Target-disease associations
- Disease scores
- Target prioritization context

Source:
OpenTargets Platform API

---

### Literature Mining

- PubMed abstracts
- Research trends
- Drug discovery relevant studies

Source:
NCBI PubMed E-utilities

---

## Architecture

```
User Input
(Gene / Protein Name)
        |
        v
+-----------------------------+
|     Data Retrieval Layer    |
|                             |
| UniProt                     |
| ChEMBL                      |
| OpenTargets                 |
| PubMed                      |
+-----------------------------+
        |
        v
+-----------------------------+
|       AI Analysis Layer     |
|                             |
| Gemini 2.5 Flash            |
| Evidence-grounded reasoning |
+-----------------------------+
        |
        v
+-----------------------------+
|        Streamlit UI         |
|                             |
| Protein Information         |
| Drug Data                   |
| Literature                  |
| AI Analysis                 |
| 3D Structure Viewer         |
+-----------------------------+
```

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Interface | Streamlit |
| AI Model | Gemini 2.5 Flash |
| Protein Data | UniProt REST API |
| Drug Data | ChEMBL API |
| Disease Data | OpenTargets API |
| Literature | PubMed |
| Structure Viewer | RCSB PDB Mol* |

---

## Installation

Clone repository:

```bash
git clone https://github.com/bhadrasiva/proteinlens.git
cd proteinlens
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run App.py
```

---

## API Requirements

Only Gemini requires an API key.

Get API key:

https://aistudio.google.com/apikey

Free APIs:

- UniProt
- ChEMBL
- OpenTargets
- PubMed

---

## Example Targets

| Gene | Research Area |
|---|---|
| BRCA1 | Cancer biology |
| TP53 | Tumor suppression |
| EGFR | Oncology |
| KRAS | Cancer therapeutics |
| HER2 | Breast cancer |
| ACE2 | Viral entry |
| PTEN | Cancer signaling |

---

## Grounding Workflow

1. User enters gene/protein name
2. Data is retrieved from biological databases
3. Relevant context is prepared
4. Gemini analyzes only retrieved information
5. Output is generated based on available evidence

---

## Project Objectives

Explores:

- Bioinformatics API integration
- Biomedical data retrieval
- AI-assisted scientific analysis
- Drug discovery workflows
- Protein target evaluation

---

## License

MIT License
```