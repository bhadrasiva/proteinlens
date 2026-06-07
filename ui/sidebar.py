"""
Sidebar · Claude aesthetic · coral accent · inline SVG · no emojis
"""

import os
import streamlit as st
import streamlit.components.v1 as components

try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass


def _icon(path: str, size: int = 13, color: str = "#888888") -> str:
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:middle;flex-shrink:0">{path}</svg>'
    )

SVG = {
    "check":  '<polyline points="20 6 9 17 4 12"/>',
    "key":    '<path d="m21 2-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0 3 3L22 7l-3-3m-3.5 3.5L19 4"/>',
    "dna":    '<path d="M2 15c6.667-6 13.333 0 20-6"/><path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/><path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993"/>',
    "grid":   '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>',
    "cube":   '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>',
    "link":   '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "info":   '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
    "dl":     '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
}


def render_sidebar():
    with st.sidebar:

        # ── Brand ─────────────────────────────────────────────────────────
        st.markdown("""
        <div style="padding:0.2rem 0 1.2rem;margin-bottom:1.2rem;
                    border-bottom:1px solid #2a2a2a">
            <p style="font-family:'DM Mono',monospace;font-size:0.95rem;font-weight:600;
                      color:#f5f0eb;margin:0 0 3px">ProteinLens</p>
            <p style="font-family:'DM Mono',monospace;font-size:0.58rem;color:#555555;
                      margin:0;letter-spacing:2px;text-transform:uppercase">
                protein intelligence</p>
        </div>
        """, unsafe_allow_html=True)

        # ── API Key ────────────────────────────────────────────────────────
        env_key = os.environ.get("GEMINI_API_KEY", "").strip()

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:7px">
            {_icon(SVG['key'], 12, '#888888')}
            <span style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#666666;
                         letter-spacing:2px;text-transform:uppercase">API Key</span>
        </div>
        """, unsafe_allow_html=True)

        if env_key:
            st.session_state["api_key"] = env_key
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;background:#1e2a1e;
                        border:1px solid #2a3a2a;border-radius:6px;
                        padding:8px 12px;margin-bottom:14px">
                <div style="width:18px;height:18px;border-radius:50%;background:#2a3a2a;
                            display:flex;align-items:center;justify-content:center;flex-shrink:0">
                    {_icon(SVG['check'], 10, '#52b788')}
                </div>
                <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#52b788">
                    loaded from .env</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            current = st.session_state.get("api_key", "")
            typed = st.text_input(
                "api_key_field", value=current, type="password",
                placeholder="AIza...",
                label_visibility="collapsed",
                help="Get a free key at aistudio.google.com/apikey",
            )
            if typed and typed != current:
                st.session_state["api_key"] = typed
                st.rerun()

            if st.session_state.get("api_key"):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;background:#1e2a1e;
                            border:1px solid #2a3a2a;border-radius:6px;
                            padding:7px 12px;margin-top:6px;margin-bottom:10px">
                    <div style="width:16px;height:16px;border-radius:50%;background:#2a3a2a;
                                display:flex;align-items:center;justify-content:center;flex-shrink:0">
                        {_icon(SVG['check'], 9, '#52b788')}
                    </div>
                    <span style="font-family:'DM Mono',monospace;font-size:0.66rem;color:#52b788">
                        key set for this session</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex;align-items:flex-start;gap:6px;margin:5px 0 12px">
                    {_icon(SVG['info'], 12, '#555555')}
                    <p style="font-size:0.7rem;color:#666666;margin:0;line-height:1.55">
                        Free key at
                        <a href="https://aistudio.google.com/apikey" target="_blank"
                           style="color:#3d6b52;text-decoration:none">
                            aistudio.google.com/apikey</a>
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # ── Session ────────────────────────────────────────────────────────
        if st.session_state.get("loaded_gene"):
            p = st.session_state.get("protein_data") or {}

            st.markdown(f"""
            <div style="border-top:1px solid #2a2a2a;margin:1.2rem 0 1rem"></div>
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px">
                {_icon(SVG['dna'], 12, '#888888')}
                <span style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#666666;
                             letter-spacing:2px;text-transform:uppercase">Session</span>
            </div>
            <div style="background:#222222;border:1px solid #2a2a2a;border-radius:8px;
                        padding:10px 12px;margin-bottom:12px">
                <p style="font-family:'DM Mono',monospace;font-size:0.9rem;font-weight:600;
                          color:#f5f0eb;margin:0 0 2px">{st.session_state['loaded_gene']}</p>
                <p style="font-size:0.72rem;color:#888888;margin:0 0 5px;line-height:1.4">
                    {p.get('protein_name','')[:44]}</p>
                <p style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#555555;margin:0">
                    {p.get('accession','')} · {p.get('length',0):,} aa
                </p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.metric("Diseases", len(st.session_state.get("diseases") or []))
                st.metric("Papers", len(st.session_state.get("papers") or []))
            with c2:
                st.metric("Drugs", len(st.session_state.get("drugs") or []))
                st.metric("Structures", len(p.get("pdb_ids", [])))

            if p.get("sequence"):
                fasta = f">{p.get('gene_name','protein')}|{p.get('accession','')}\n"
                fasta += "\n".join(
                    p["sequence"][i:i+60] for i in range(0, len(p["sequence"]), 60)
                )
                st.download_button(
                    "Download FASTA",
                    data=fasta,
                    file_name=f"{p.get('gene_name','protein')}.fasta",
                    mime="text/plain",
                    use_container_width=True,
                )

            if st.button("Clear session", use_container_width=True):
                for k in ["protein_data", "context", "loaded_gene"]:
                    st.session_state[k] = None
                for k in ["chat_history", "drugs", "diseases", "papers"]:
                    st.session_state[k] = []
                st.rerun()

            _render_structure_viewer(p)

        # ── Footer ─────────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="border-top:1px solid #2a2a2a;margin-top:1.5rem;padding-top:0.9rem">
            <div style="display:flex;align-items:center;gap:5px;margin-bottom:4px">
                {_icon(SVG['grid'], 10, '#444444')}
                <span style="font-family:'DM Mono',monospace;font-size:0.58rem;color:#444444">
                    UniProt · ChEMBL · OpenTargets · PubMed</span>
            </div>
            <div style="display:flex;align-items:center;gap:5px">
                {_icon(SVG['link'], 10, '#444444')}
                <a href="https://github.com/bhadrasiva/proteinlens" target="_blank"
                   style="font-family:'DM Mono',monospace;font-size:0.58rem;
                          color:#3d6b52;text-decoration:none">
                    github.com/bhadrasiva/proteinlens</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_structure_viewer(p: dict):
    pdb_ids = (p or {}).get("pdb_ids", [])
    if not pdb_ids:
        return
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:6px;margin:1rem 0 6px">
        <span style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#666666;
                     letter-spacing:2px;text-transform:uppercase">3D Preview</span>
    </div>
    """, unsafe_allow_html=True)
    # just show the selectbox info; full viewer is in Data tab
    st.markdown(f"""
    <div style="background:#222222;border:1px solid #2a2a2a;border-radius:6px;
                padding:8px 12px">
        <p style="font-family:'DM Mono',monospace;font-size:0.7rem;color:#888888;margin:0">
            {len(pdb_ids)} structures available</p>
        <p style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#555555;margin:3px 0 0">
            View in Data tab ↗</p>
    </div>
    """, unsafe_allow_html=True)