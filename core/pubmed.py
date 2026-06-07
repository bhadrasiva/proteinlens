"""
NCBI PubMed E-utilities client.
Fetches recent abstracts relevant to drug discovery for a given gene.
No API key required (rate-limited; add &api_key=... for higher limits).

Bug 2 fix: gene[Title/Abstract] is case-insensitive, so "EGFR" matches
both the EGFR oncogene and eGFR (estimated glomerular filtration rate).
Fix: resolve gene symbol → NCBI Gene ID first, then anchor PubMed
query to that Gene ID — which is a controlled field, never ambiguous.
Falls back to tighter tiab query if Gene ID lookup fails.
"""

import requests
import xml.etree.ElementTree as ET

ESEARCH  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH   = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def _resolve_ncbi_gene_id(gene_name: str) -> str | None:
    """
    Resolve HGNC gene symbol → NCBI Gene ID for Homo sapiens.
    e.g. "EGFR" → "1956"
    """
    try:
        r = requests.get(
            ESEARCH,
            params={
                "db":      "gene",
                "term":    f"{gene_name}[Gene Name] AND Homo sapiens[Organism]",
                "retmode": "json",
                "retmax":  1,
            },
            timeout=10,
        )
        r.raise_for_status()
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        return ids[0] if ids else None
    except Exception:
        return None


def get_papers(gene_name: str, max_results: int = 5) -> list[dict]:
    """Return recent PubMed papers about gene + drug/therapeutic context."""

    gene_id = _resolve_ncbi_gene_id(gene_name)

    if gene_id:
        # Anchored to exact gene — never matches eGFR or other abbreviation collisions
        query = (
            f"{gene_id}[Gene ID] AND "
            "(drug OR inhibitor OR therapeutic OR cancer OR disease OR treatment)"
            "[Title/Abstract]"
        )
    else:
        # Fallback: require protein/kinase/receptor context to reduce ambiguity
        query = (
            f"{gene_name}[Title/Abstract] AND "
            "(drug OR inhibitor OR therapeutic OR cancer OR disease OR treatment)"
            "[Title/Abstract] AND "
            "(protein OR receptor OR kinase OR gene OR mutation)[Title/Abstract]"
        )

    r = requests.get(
        ESEARCH,
        params={
            "db":      "pubmed",
            "term":    query,
            "retmax":  max_results,
            "sort":    "date",
            "retmode": "json",
        },
        timeout=15,
    )
    r.raise_for_status()
    ids = r.json().get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []

    r2 = requests.get(
        EFETCH,
        params={
            "db":      "pubmed",
            "id":      ",".join(ids),
            "retmode": "xml",
            "rettype": "abstract",
        },
        timeout=15,
    )
    r2.raise_for_status()

    papers = []
    try:
        root = ET.fromstring(r2.text)
        for article in root.findall(".//PubmedArticle"):
            title_el    = article.find(".//ArticleTitle")
            abstract_el = article.find(".//AbstractText")
            year_el     = article.find(".//PubDate/Year")
            pmid_el     = article.find(".//PMID")
            journal_el  = article.find(".//Journal/Title")
            authors     = article.findall(".//Author")

            author_str = ""
            if authors:
                last = authors[0].find("LastName")
                author_str = (last.text if last is not None else "")
                if len(authors) > 1:
                    author_str += " et al."

            papers.append({
                "title":    title_el.text    if title_el    is not None else "",
                "abstract": abstract_el.text if abstract_el is not None else "",
                "year":     year_el.text     if year_el     is not None else "",
                "pmid":     pmid_el.text     if pmid_el     is not None else "",
                "journal":  journal_el.text  if journal_el  is not None else "",
                "author":   author_str,
            })
    except ET.ParseError:
        pass

    return papers