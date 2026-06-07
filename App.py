"""
ProteinLens — Grounded Protein Intelligence for Drug Discovery
Claude aesthetic: deep charcoal · warm white · coral/amber accent
No LLM on load · Gemini answers on demand only
"""

import streamlit as st
import streamlit.components.v1 as components

from core.uniprot import search_protein
from core.chembl import get_drugs_for_gene
from core.opentargets import get_disease_associations
from core.pubmed import get_papers
from core.llm import build_context, chat

from ui.sidebar import render_sidebar
from ui.chat import (
    render_assistant_message,
    render_user_message,
    render_disease_panel,
    render_drugs_panel,
    render_papers_panel,
)

st.set_page_config(
    page_title="ProteinLens",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject fonts + CSS inside <style> — no stray text outside ────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@300;400;500;600&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #1a1a1a !important;
        color: #f5f0eb !important;
    }
    .main, [data-testid="stAppViewContainer"] { background: #1a1a1a !important; }
    .block-container {
        padding: 2rem 2.5rem 5rem !important;
        max-width: 820px !important;
        margin: 0 auto !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #111111 !important;
        border-right: 1px solid #2a2a2a !important;
    }
    section[data-testid="stSidebar"] > div { padding: 1.4rem 1.1rem !important; }

    /* ── Text inputs ── */
    .stTextInput input {
        background: #222222 !important;
        border: 1px solid #333333 !important;
        color: #f5f0eb !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        border-radius: 8px !important;
        padding: 0.7rem 1rem !important;
        transition: border-color 0.15s !important;
    }
    .stTextInput input::placeholder { color: #555555 !important; }
    .stTextInput input:focus {
        border-color: #3d6b52 !important;
        box-shadow: 0 0 0 3px rgba(61,107,82,0.15) !important;
        outline: none !important;
    }
    div[data-testid="stTextInput"] { margin-bottom: 0 !important; }

    /* ── Primary button (Send / Search) ── */
    .stButton button {
        background: #3d6b52 !important;
        color: #ffffff !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.3rem !important;
        transition: background 0.15s !important;
        height: 42px !important;
    }
    .stButton button:hover { background: #2d5a42 !important; }

    /* ── Sidebar buttons ── */
    section[data-testid="stSidebar"] .stButton button {
        background: #222222 !important;
        color: #3d6b52 !important;
        border: 1px solid #333333 !important;
        font-size: 0.75rem !important;
        padding: 0.45rem 0.9rem !important;
        height: auto !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #3d6b52 !important;
        color: #ffffff !important;
        border-color: #3d6b52 !important;
    }

    /* ── Download button ── */
    .stDownloadButton button {
        background: #222222 !important;
        color: #3d6b52 !important;
        border: 1px solid #333333 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.72rem !important;
        border-radius: 6px !important;
        height: auto !important;
    }

    /* ── Metrics ── */
    [data-testid="metric-container"] {
        background: #222222 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.8rem !important;
    }
    [data-testid="metric-container"] label {
        color: #666666 !important;
        font-size: 0.62rem !important;
        font-family: 'DM Mono', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #f5f0eb !important;
        font-size: 1.1rem !important;
        font-family: 'DM Mono', monospace !important;
        font-weight: 600 !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background: #222222 !important;
        border-color: #333333 !important;
        color: #f5f0eb !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.78rem !important;
        border-radius: 6px !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid #2a2a2a !important;
        gap: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #555555 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.7rem !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
    }
    .stTabs [aria-selected="true"] {
        color: #f5f0eb !important;
        border-bottom: 2px solid #3d6b52 !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent !important;
        padding-top: 1.2rem !important;
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #3d6b52 !important; }

    /* ── Alert/error ── */
    .stAlert { border-radius: 8px !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #1a1a1a; }
    ::-webkit-scrollbar-thumb { background: #333333; border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: #3d6b52; }

    [data-testid="collapsedControl"] { display: flex !important; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
for key in ["protein_data", "context", "loaded_gene", "api_key"]:
    if key not in st.session_state:
        st.session_state[key] = None
for key in ["chat_history", "drugs", "diseases", "papers"]:
    if key not in st.session_state:
        st.session_state[key] = []

render_sidebar()


# ── Static protein card ───────────────────────────────────────────────────────
def _render_protein_card(p: dict):
    keywords = "".join([
        f'<span style="display:inline-block;background:#222222;border:1px solid #333333;'
        f'border-radius:4px;padding:2px 8px;font-family:\'DM Mono\',monospace;'
        f'font-size:0.63rem;color:#888888;margin:2px 3px 2px 0">{kw}</span>'
        for kw in p.get("keywords", [])[:10]
    ])
    pathways = " · ".join(p.get("pathways", [])[:2]) or "—"
    fn = p.get("function", "")
    fn_short = fn[:480] + ("…" if len(fn) > 480 else "")
    st.markdown(f"""
    <div style="background:#222222;border:1px solid #2a2a2a;
                border-top:2px solid #3d6b52;
                border-radius:0 0 10px 10px;padding:1.5rem 1.6rem;margin-bottom:1.4rem">
        <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:5px">
            <span style="font-family:'DM Mono',monospace;font-size:1.25rem;font-weight:600;
                         color:#f5f0eb">{p.get('gene_name','')}</span>
            <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#555555">
                {p.get('accession','')}</span>
            <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#555555;
                         margin-left:auto">{p.get('length',0):,} aa</span>
        </div>
        <p style="font-size:0.8rem;color:#888888;margin:0 0 12px">{p.get('protein_name','')}</p>
        <p style="font-size:0.88rem;color:#c8c0b8;line-height:1.75;margin:0 0 14px">{fn_short}</p>
        <p style="font-size:0.7rem;color:#555555;font-family:'DM Mono',monospace;margin:0 0 10px">
            {pathways}</p>
        <div>{keywords}</div>
    </div>
    <p style="font-size:0.68rem;color:#444444;font-family:'DM Mono',monospace;
              text-align:center;margin:0 0 1.5rem;letter-spacing:1.5px">
        DATA LOADED FROM UNIPROT · CHEMBL · OPENTARGETS · PUBMED
    </p>
    """, unsafe_allow_html=True)


# ── Data loader (zero LLM calls) ──────────────────────────────────────────────
def load_protein(gene: str):
    if not st.session_state.get("api_key"):
        return False, "Add your Gemini API key in the sidebar first."

    st.session_state["loaded_gene"] = gene
    st.session_state["chat_history"] = []

    with st.spinner(f"UniProt — {gene}"):
        protein = search_protein(gene)
        if not protein:
            st.session_state["loaded_gene"] = None
            return False, f"No reviewed UniProt entry found for **{gene}**."
        st.session_state["protein_data"] = protein

    canonical = protein.get("gene_name", gene)
    st.session_state["loaded_gene"] = canonical

    with st.spinner(f"OpenTargets — disease associations for {canonical}"):
        try:
            st.session_state["diseases"] = get_disease_associations(canonical)
        except Exception:
            st.session_state["diseases"] = []

    with st.spinner(f"ChEMBL — drugs & compounds for {canonical}"):
        try:
            st.session_state["drugs"] = get_drugs_for_gene(canonical)
        except Exception:
            st.session_state["drugs"] = []

    with st.spinner(f"PubMed — recent papers for {canonical}"):
        try:
            st.session_state["papers"] = get_papers(canonical)
        except Exception:
            st.session_state["papers"] = []

    # Context built fresh per question in the chat handler (keyword routing)
    return True, ""


# ── Landing ───────────────────────────────────────────────────────────────────
if not st.session_state.get("loaded_gene"):
    gene_examples = ["EGFR", "BRCA1", "TP53", "KRAS", "ACE2", "HER2", "PTEN"]
    chips = "".join([
        f'<span style="display:inline-block;background:#222222;border:1px solid #333333;'
        f'border-radius:6px;padding:5px 14px;font-family:\'DM Mono\',monospace;'
        f'font-size:0.76rem;color:#888888;margin:3px">{g}</span>'
        for g in gene_examples
    ])

    st.markdown(f"""
    <div style="text-align:center;padding:3.5rem 1rem 2.5rem">
        <p style="font-family:'DM Mono',monospace;font-size:2rem;font-weight:600;
                  color:#f5f0eb;margin:0;letter-spacing:-0.5px">ProteinLens</p>
        <p style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#555555;
                  letter-spacing:3px;text-transform:uppercase;margin:8px 0 1.6rem">
            grounded protein intelligence</p>
        <p style="font-size:0.9rem;color:#888888;margin:0 auto 2rem;
                  max-width:480px;line-height:1.8">
            Enter a gene name to fetch live data from UniProt, ChEMBL,
            OpenTargets &amp; PubMed — then ask Gemini anything, answered only from what was retrieved.
        </p>
        <div style="margin-bottom:0.5rem">{chips}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Landing search — st.form so Enter key works ───────────────────────
    with st.form("landing_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            gene_input = st.text_input(
                "gene", placeholder="Gene name — EGFR, BRCA1, TP53 ...",
                label_visibility="collapsed", key="landing_gene",
            )
        with col_btn:
            go = st.form_submit_button("↑", use_container_width=True)

    if go and gene_input:
        gene = gene_input.strip().upper().split()[0]
        ok, err = load_protein(gene)
        if not ok:
            render_assistant_message(f"**Error:** {err}")
        else:
            st.rerun()
    elif go and not gene_input:
        st.warning("Enter a gene name.")


# ── Protein loaded ────────────────────────────────────────────────────────────
else:
    gene = st.session_state["loaded_gene"]

    tab_chat, tab_data = st.tabs(["  Chat", "  Data"])

    with tab_chat:
        _render_protein_card(st.session_state["protein_data"])

        for msg in st.session_state.get("chat_history", []):
            if msg["role"] == "assistant":
                render_assistant_message(msg["content"])
            else:
                render_user_message(msg["content"])

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            col_in, col_btn = st.columns([5, 1])
            with col_in:
                user_input = st.text_input(
                    "msg", placeholder=f"Ask anything about {gene} ...",
                    label_visibility="collapsed", key="chat_input",
                )
            with col_btn:
                send = st.form_submit_button("↑", use_container_width=True)

        should_send = send and user_input
        if should_send:
            token = user_input.strip().upper().split()[0]
            is_new_gene = (
                len(user_input.strip().split()) == 1
                and user_input.strip().replace("-", "").isalpha()
                and token != gene
            )
            if is_new_gene:
                ok, err = load_protein(token)
                if not ok:
                    render_assistant_message(f"**Error:** {err}")
                else:
                    st.rerun()
            else:
                st.session_state["chat_history"].append({"role": "user", "content": user_input})
                with st.spinner(""):
                    try:
                        history = [
                            m for m in st.session_state["chat_history"][:-1]
                            if m["role"] in ("user", "assistant")
                        ]
                        # Build context fresh, routed to sections relevant to this question
                        context = build_context(
                            st.session_state["protein_data"],
                            st.session_state["drugs"],
                            st.session_state["diseases"],
                            st.session_state["papers"],
                            question=user_input,
                        )
                        response = chat(
                            st.session_state["api_key"],
                            context,
                            history,
                            user_input,
                        )
                        st.session_state["chat_history"].append(
                            {"role": "assistant", "content": response}
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gemini error: {e}")

    with tab_data:
        pdb_ids = (st.session_state.get("protein_data") or {}).get("pdb_ids", [])
        if pdb_ids:
            st.markdown("""
            <p style="font-family:'DM Mono',monospace;font-size:0.62rem;color:#555555;
                      letter-spacing:2px;text-transform:uppercase;margin:0 0 8px">
                3D Structure</p>
            """, unsafe_allow_html=True)
            selected = st.selectbox("PDB", pdb_ids[:10], key="pdb_select",
                                    label_visibility="collapsed")

            # ── py3Dmol viewer — renders in Streamlit canvas, not sandboxed iframe ──
            try:
                import py3Dmol
                from stmol import showmol

                view = py3Dmol.view(width=760, height=480)
                view.addModelsAsFrames(
                    f"https://files.rcsb.org/download/{selected}.pdb"
                )
                view.setStyle({"model": -1}, {"cartoon": {"color": "spectrum"}})
                view.setBackgroundColor("#111111")
                view.zoomTo()
                showmol(view, height=480, width=760)

            except Exception:
                # Fallback: clean link card if stmol/py3Dmol not installed or WebGL fails
                st.markdown(f"""
                <div style="background:#1e1e1e;border:1px solid #2a2a2a;border-radius:8px;
                            padding:2rem;text-align:center">
                    <p style="font-family:'DM Mono',monospace;font-size:0.72rem;
                               color:#666666;margin:0 0 10px">
                        3D viewer unavailable in this environment</p>
                    <a href="https://www.rcsb.org/structure/{selected}" target="_blank"
                       style="font-family:'DM Mono',monospace;font-size:0.75rem;
                              color:#3d6b52;text-decoration:none">
                        Open {selected} in RCSB PDB ↗</a>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <p style="font-family:monospace;font-size:0.6rem;color:#555555;margin:6px 0 1rem">
                PDB: {selected} ·
                <a href="https://www.rcsb.org/structure/{selected}" target="_blank"
                   style="color:#3d6b52;text-decoration:none">open in RCSB ↗</a>
            </p>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        render_disease_panel(st.session_state.get("diseases", []))
        render_drugs_panel(st.session_state.get("drugs", []))
        render_papers_panel(st.session_state.get("papers", []))