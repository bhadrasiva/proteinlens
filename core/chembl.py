"""
ChEMBL REST API.
Uses UniProt accession (from session state) for exact target lookup.
Gene name is only a last-resort fallback.

Bug 1 fix: mechanism.json records often have molecule_name = None.
We now fetch /molecule/{id} for any record missing a name, and also
pull max_phase from the molecule record (not the mechanism record,
which doesn't carry it reliably).
"""

import requests

CHEMBL_BASE = "https://www.ebi.ac.uk/chembl/api/data"


def _fetch_molecule(mol_chembl_id: str) -> dict:
    """Fetch a single molecule record and return name + max_phase."""
    try:
        r = requests.get(
            f"{CHEMBL_BASE}/molecule/{mol_chembl_id}.json",
            timeout=15,
        )
        r.raise_for_status()
        mol = r.json()
        name = (
            mol.get("pref_name")
            or (mol.get("molecule_synonyms") or [{}])[0].get("molecule_synonym")
            or mol_chembl_id
        )
        return {
            "name": name,
            "max_phase": mol.get("max_phase") or 0,
        }
    except Exception:
        return {"name": mol_chembl_id, "max_phase": 0}


def get_drugs_for_gene(gene_name: str, limit: int = 10) -> list[dict]:
    # Get accession from session — set by uniprot.py before this is called
    try:
        import streamlit as st
        accession = (st.session_state.get("protein_data") or {}).get("accession", "")
        canonical_gene = (st.session_state.get("protein_data") or {}).get("gene_name", gene_name)
    except Exception:
        accession = ""
        canonical_gene = gene_name

    chembl_id = _resolve_target(accession, canonical_gene)
    if not chembl_id:
        return []

    # Mechanism of action records for this target
    try:
        r = requests.get(
            f"{CHEMBL_BASE}/mechanism.json",
            params={"target_chembl_id": chembl_id, "limit": limit},
            timeout=15,
        )
        r.raise_for_status()
        mechs = r.json().get("mechanisms", [])
    except Exception:
        mechs = []

    if mechs:
        drugs = []
        seen = set()
        for m in mechs:
            mol_id = m.get("molecule_chembl_id", "")
            if not mol_id or mol_id in seen:
                continue
            seen.add(mol_id)

            # molecule_name on the mechanism record is often None — fetch if missing
            name = m.get("molecule_name")
            if not name:
                mol_data = _fetch_molecule(mol_id)
                name = mol_data["name"]
                max_phase = mol_data["max_phase"]
            else:
                # max_phase isn't reliable on mechanism records — always fetch it
                max_phase = _fetch_molecule(mol_id)["max_phase"]

            drugs.append({
                "name":      name,
                "chembl_id": mol_id,
                "mechanism": m.get("mechanism_of_action", ""),
                "max_phase": max_phase,
            })

        # Sort: approved (4) first
        drugs.sort(key=lambda d: d["max_phase"] or 0, reverse=True)
        return drugs

    # Fallback: drug indications
    try:
        r2 = requests.get(
            f"{CHEMBL_BASE}/drug_indication.json",
            params={"target_chembl_id": chembl_id, "limit": limit},
            timeout=15,
        )
        r2.raise_for_status()
        indications = r2.json().get("drug_indications", [])
    except Exception:
        indications = []

    result = []
    seen = set()
    for i in indications:
        mol_id = i.get("molecule_chembl_id", "")
        if not mol_id or mol_id in seen:
            continue
        seen.add(mol_id)

        name = i.get("molecule_name")
        if not name:
            mol_data = _fetch_molecule(mol_id)
            name = mol_data["name"]
            max_phase = mol_data["max_phase"]
        else:
            max_phase = i.get("max_phase_for_ind", 0) or 0

        result.append({
            "name":      name,
            "chembl_id": mol_id,
            "mechanism": "",
            "max_phase": max_phase,
        })

    result.sort(key=lambda d: d["max_phase"] or 0, reverse=True)
    return result


def _resolve_target(accession: str, gene_name: str) -> str:
    """Return ChEMBL target ID. Uses UniProt accession first, gene name as fallback."""

    # Strategy A: UniProt accession cross-reference — exact, no ambiguity
    if accession:
        try:
            r = requests.get(
                f"{CHEMBL_BASE}/target.json",
                params={
                    "target_components__accession": accession,
                    "organism": "Homo sapiens",
                    "target_type": "SINGLE PROTEIN",
                    "limit": 1,
                },
                timeout=15,
            )
            r.raise_for_status()
            targets = r.json().get("targets", [])
            if targets:
                return targets[0].get("target_chembl_id", "")
        except Exception:
            pass

    # Strategy B: gene name with exact match check
    try:
        r = requests.get(
            f"{CHEMBL_BASE}/target/search.json",
            params={
                "q": gene_name,
                "organism": "Homo sapiens",
                "target_type": "SINGLE PROTEIN",
                "limit": 10,
            },
            timeout=15,
        )
        r.raise_for_status()
        targets = r.json().get("targets", [])
        gene_up = gene_name.upper()
        for t in targets:
            pref = t.get("pref_name", "").upper()
            syns = []
            for c in t.get("target_components", []):
                for s in c.get("target_component_synonyms", []):
                    syns.append(s.get("component_synonym", "").upper())
            if gene_up == pref or gene_up in syns:
                return t.get("target_chembl_id", "")
        if targets:
            return targets[0].get("target_chembl_id", "")
    except Exception:
        pass

    return ""