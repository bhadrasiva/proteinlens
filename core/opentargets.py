"""
Open Targets GraphQL API.
Uses canonical gene symbol returned by UniProt, not raw user input.
"""

import requests

OT_GRAPHQL = "https://api.platform.opentargets.org/api/v4/graphql"


def get_disease_associations(gene_name: str, limit: int = 10) -> list[dict]:
    """
    gene_name here should be the canonical symbol from UniProt (e.g. 'EGFR'),
    which is passed by app.py after UniProt lookup.
    """
    # Step 1: search for target by approved symbol
    search_q = """
    query Search($q: String!) {
      search(queryString: $q, entityNames: ["target"], page: {index: 0, size: 5}) {
        hits {
          id
          object {
            ... on Target {
              id
              approvedSymbol
            }
          }
        }
      }
    }
    """
    try:
        r = requests.post(
            OT_GRAPHQL,
            json={"query": search_q, "variables": {"q": gene_name}},
            timeout=15,
        )
        r.raise_for_status()
        hits = r.json().get("data", {}).get("search", {}).get("hits", [])
    except Exception:
        return []

    # Pick hit whose approvedSymbol exactly matches
    ensembl_id = ""
    gene_up = gene_name.upper()
    for h in hits:
        obj = h.get("object", {})
        if obj.get("approvedSymbol", "").upper() == gene_up:
            ensembl_id = obj.get("id", "")
            break
    if not ensembl_id and hits:
        ensembl_id = hits[0].get("object", {}).get("id", "")
    if not ensembl_id:
        return []

    # Step 2: disease associations
    assoc_q = """
    query Assoc($id: String!, $size: Int!) {
      target(ensemblId: $id) {
        associatedDiseases(orderByScore: "overall", page: {index: 0, size: $size}) {
          rows {
            disease { id name therapeuticAreas { name } }
            score
          }
        }
      }
    }
    """
    try:
        r2 = requests.post(
            OT_GRAPHQL,
            json={"query": assoc_q, "variables": {"id": ensembl_id, "size": limit}},
            timeout=15,
        )
        r2.raise_for_status()
        rows = (
            r2.json().get("data", {})
            .get("target", {})
            .get("associatedDiseases", {})
            .get("rows", [])
        )
    except Exception:
        return []

    return [
        {
            "disease_name":       row["disease"]["name"],
            "disease_id":         row["disease"]["id"],
            "score":              round(row.get("score", 0), 3),
            "therapeutic_areas":  [a["name"] for a in row["disease"].get("therapeuticAreas", [])][:3],
        }
        for row in rows
    ]