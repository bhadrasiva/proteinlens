"""
Gemini API client for ProteinLens.
Only called when user asks a question — never on protein load.
Grounded strictly in fetched data.

Model: gemini-2.5-flash (free tier, up to 1000 req/day)
Context: keyword-routed — only relevant sections sent per question.
No vector DB, no embeddings — simple keyword matching cuts token use ~70%.
"""

import google.generativeai as genai

SYSTEM_PROMPT = """You are ProteinLens — an expert computational biologist and drug discovery assistant.

RULES:
1. Answer ONLY from the protein data context provided. Never use outside knowledge to fill gaps.
2. If the data doesn't cover the question, say: "The retrieved data doesn't cover this."
3. Never invent drug names, mechanisms, study results, or clinical data.
4. Cite your source inline (UniProt, ChEMBL, OpenTargets, PubMed) when making claims.
5. Be concise and scientifically precise.
6. Format responses in clean markdown. Bold key terms."""


# ── Section builders — each returns a small focused string ───────────────────

def _base(protein_data: dict) -> str:
    fn = protein_data.get("function", "")[:300]
    return "\n".join([
        f"## UniProt — {protein_data.get('gene_name','')} ({protein_data.get('accession','')})",
        f"- Protein: {protein_data.get('protein_name','N/A')}",
        f"- Length: {protein_data.get('length','N/A')} aa",
        f"- Function: {fn}",
        f"- Pathways: {'; '.join(protein_data.get('pathways', [])) or 'None listed'}",
        f"- Keywords: {', '.join(protein_data.get('keywords', [])[:10]) or 'None'}",
        f"- PDB structures available: {len(protein_data.get('pdb_ids', []))}",
    ])


def _drugs(drugs: list) -> str:
    if not drugs:
        return "## ChEMBL — Drugs\nNo drugs found for this target."
    lines = ["## ChEMBL — Drugs"]
    for d in drugs:
        phase = f"Phase {d['max_phase']}" if d.get("max_phase") else "unknown phase"
        mech = f", {d['mechanism'][:80]}" if d.get("mechanism") else ""
        lines.append(f"- {d['name']} ({d.get('chembl_id','')}) — {phase}{mech}")
    return "\n".join(lines)


def _diseases(diseases: list) -> str:
    if not diseases:
        return "## OpenTargets — Disease Associations\nNo disease associations found."
    lines = ["## OpenTargets — Disease Associations"]
    for d in diseases:
        areas = ", ".join(d.get("therapeutic_areas", [])[:2]) or "N/A"
        lines.append(f"- {d['disease_name']} (score: {d['score']}, areas: {areas})")
    return "\n".join(lines)


def _papers(papers: list) -> str:
    if not papers:
        return "## PubMed — Recent Papers\nNo papers found."
    lines = ["## PubMed — Recent Papers"]
    for p in papers:
        lines.append(
            f"- {p.get('title','')} ({p.get('year','')}) "
            f"— {p.get('author','')} — PMID {p.get('pmid','')}"
        )
    return "\n".join(lines)


# ── Keyword router — picks only sections relevant to the question ─────────────

DRUG_KEYWORDS     = {"drug", "compound", "inhibitor", "inhibition", "treatment",
                     "clinical", "phase", "approved", "molecule", "therapy",
                     "therapeutic", "chembl", "medication", "targeted"}

DISEASE_KEYWORDS  = {"disease", "cancer", "tumor", "tumour", "condition", "disorder",
                     "indication", "associated", "pathology", "syndrome", "carcinoma",
                     "opentargets", "target"}

PAPER_KEYWORDS    = {"paper", "study", "research", "published", "literature",
                     "pubmed", "journal", "article", "finding", "evidence", "trial"}

STRUCTURE_KEYWORDS = {"structure", "pdb", "3d", "fold", "domain", "binding site",
                      "active site", "residue", "crystal"}


def build_context(
    protein_data: dict,
    drugs: list,
    diseases: list,
    papers: list,
    question: str = "",
) -> str:
    """
    Route context sections based on question keywords.
    Always includes base protein info (small).
    Only adds drug/disease/paper sections if question seems to need them.
    Falls back to everything if no keywords match.
    """
    q = question.lower()
    words = set(q.split())

    want_drugs    = bool(words & DRUG_KEYWORDS)
    want_diseases = bool(words & DISEASE_KEYWORDS)
    want_papers   = bool(words & PAPER_KEYWORDS)
    want_structure = bool(words & STRUCTURE_KEYWORDS)

    # nothing matched — general question, send everything
    if not any([want_drugs, want_diseases, want_papers, want_structure]):
        want_drugs = want_diseases = want_papers = True

    sections = [_base(protein_data)]
    if want_drugs:
        sections.append(_drugs(drugs))
    if want_diseases:
        sections.append(_diseases(diseases))
    if want_papers:
        sections.append(_papers(papers))

    return "\n\n".join(sections)


def chat(api_key: str, context: str, history: list[dict], user_message: str) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )
    gemini_history = [
        {
            "role": "user",
            "parts": [f"Here is the retrieved protein data. Answer ONLY from this:\n\n{context}"]
        },
        {
            "role": "model",
            "parts": ["Understood. I will only answer from the retrieved data provided."]
        },
    ]
    for m in history:
        role = "model" if m["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [m["content"]]})

    session = model.start_chat(history=gemini_history)
    response = session.send_message(user_message)
    return response.text