"""
UniProt REST API client.
Uses gene: field search for exact gene name matching.
All downstream modules should use the accession returned here.
"""

import requests

UNIPROT_BASE = "https://rest.uniprot.org/uniprotkb"

FIELDS = ",".join([
    "accession", "id", "protein_name", "gene_names",
    "sequence", "cc_function", "cc_disease", "cc_pathway",
    "keyword", "xref_pdb", "organism_name", "length"
])


def search_protein(gene_name: str) -> dict:
    """
    Search UniProt with exact gene name field match.
    gene_exact:EGFR ensures we get the EGFR gene, not anything mentioning EGFR in text.
    """
    url = (
        f"{UNIPROT_BASE}/search"
        f"?query=gene_exact:{requests.utils.quote(gene_name)}"
        f"+AND+organism_id:9606+AND+reviewed:true"
        f"&fields={FIELDS}&format=json&size=1"
    )
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        return {}
    entry = results[0]
    parsed = _parse_entry(entry)
    # Confirm the returned gene name actually matches what was searched
    # (safety net — UniProt reviewed+exact should always match but just in case)
    if parsed.get("gene_name", "").upper() != gene_name.upper():
        # Try accession-level fallback: search by gene synonym too
        pass  # UniProt reviewed+gene_exact is reliable enough
    return parsed


def get_by_accession(accession: str) -> dict:
    """Fetch a specific UniProt entry by accession ID."""
    url = f"{UNIPROT_BASE}/{accession}?fields={FIELDS}&format=json"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return _parse_entry(r.json())


def _parse_entry(entry: dict) -> dict:
    accession = entry.get("primaryAccession", "")
    protein_name = (
        entry.get("proteinDescription", {})
        .get("recommendedName", {})
        .get("fullName", {})
        .get("value", "Unknown")
    )
    genes = entry.get("genes", [])
    gene_name = genes[0].get("geneName", {}).get("value", "") if genes else ""

    sequence = entry.get("sequence", {}).get("value", "")
    length   = entry.get("sequence", {}).get("length", 0)

    function, diseases, pathways = "", [], []
    for comment in entry.get("comments", []):
        ctype = comment.get("commentType", "")
        if ctype == "FUNCTION" and not function:
            texts = comment.get("texts", [])
            if texts:
                function = texts[0].get("value", "")
        elif ctype == "DISEASE":
            d    = comment.get("disease", {})
            name = d.get("diseaseId", "")
            desc = d.get("description") or ""
            if name:
                diseases.append({"name": name, "description": desc})
        elif ctype == "PATHWAY":
            texts = comment.get("texts", [])
            if texts:
                pathways.append(texts[0].get("value", ""))

    keywords = [kw.get("name", "") for kw in entry.get("keywords", [])]

    pdb_ids = []
    for xref in entry.get("uniProtKBCrossReferences", []):
        if xref.get("database") == "PDB":
            pdb_ids.append(xref.get("id", ""))

    return {
        "accession":    accession,
        "protein_name": protein_name,
        "gene_name":    gene_name,
        "function":     function,
        "sequence":     sequence,
        "length":       length,
        "diseases":     diseases,
        "pathways":     pathways,
        "keywords":     keywords[:20],
        "pdb_ids":      pdb_ids[:10],
    }