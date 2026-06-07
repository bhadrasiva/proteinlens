```markdown
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

Retrieves protein-level information:

- Protein function and description
- Gene and protein identifiers
- Functional annotations
- Protein sequence
- Available 3D structures

Source:
- UniProt REST API

---

### Drug Discovery Information

Provides target-related drug information:

- Approved drugs
- Clinical compounds
- Compound-target relationships

Source:
- ChEMBL API

---

### Disease Association Analysis

Retrieves disease relevance information:

- Target-disease associations
- Disease scores
- Target prioritization context

Source:
- OpenTargets Platform API

---

### Literature Mining

Fetches recent protein-associated publications:

- PubMed abstracts
- Research trends
- Drug discovery relevant studies

Source:
- NCBI PubMed E-utilities

---

### AI-Based Scientific Analysis

Uses Gemini to generate structured analysis from retrieved biological information.

The AI system is designed to:

- Use retrieved evidence as the primary context
- Avoid unsupported claims
- Highlight missing information where data is unavailable

---

## Architecture

```

User Input
(Gene / Protein Name)
|
v
+--------------------------------+
|       Data Retrieval Layer     |
|                                |
|  UniProt                      |
|  ChEMBL                       |
|  OpenTargets                  |
|  PubMed                       |
+--------------------------------+
|
v
+--------------------------------+
|        AI Analysis Layer       |
|                                |
|  Gemini 2.5 Flash              |
|  Evidence-grounded reasoning   |
+--------------------------------+
|
v
+--------------------------------+
|        Streamlit UI             |
|                                |
|  Protein Information           |
|  Drug Data                     |
|  Literature                    |
|  AI Analysis                   |
|  3D Structure Viewer            |
+--------------------------------+

````

---

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Interface | Streamlit |
| AI Model | Gemini 2.5 Flash |
| Protein Database | UniProt REST API |
| Drug Database | ChEMBL API |
| Disease Database | OpenTargets API |
| Literature Database | PubMed E-utilities |
| Structure Viewer | RCSB PDB Mol* |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/bhadrasiva/proteinlens.git
cd proteinlens
````

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment file:

```bash
cp .env.example .env
```

Add your Gemini API key:

```bash
GEMINI_API_KEY=your_api_key
```

Run the application:

```bash
streamlit run app.py
```

---

## API Requirements

Only Gemini requires an API key.

Get your API key:

[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

The following resources are freely accessible:

* UniProt
* ChEMBL
* OpenTargets
* PubMed

---

## Example Targets

| Gene  | Research Area                           |
| ----- | --------------------------------------- |
| BRCA1 | Cancer biology                          |
| TP53  | Tumor suppression                       |
| EGFR  | Oncology                                |
| KRAS  | Cancer therapeutics                     |
| HER2  | Breast cancer                           |
| ACE2  | Viral entry and cardiovascular research |
| PTEN  | Cancer signaling                        |

---

## Grounding Workflow

ProteinLens follows a retrieval-augmented generation workflow:

1. User enters a gene or protein name
2. Biological information is retrieved from external databases
3. Relevant context is prepared
4. Gemini receives retrieved information
5. AI generates analysis based on available evidence

This approach connects AI-generated insights with biological data sources instead of relying only on model memory.

---

## Project Objectives

ProteinLens was developed as a personal project exploring:

* Bioinformatics API integration
* Biomedical knowledge retrieval
* AI-assisted scientific interpretation
* Drug discovery workflows
* Protein target analysis

---

## License

MIT License

```
```
