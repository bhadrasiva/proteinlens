"""
Chat UI · Claude aesthetic · coral accent · inline SVG · no emojis
"""

import streamlit as st
import re

# ── SVG icon helper ───────────────────────────────────────────────────────────
def _icon(path: str, size: int = 15, color: str = "#888888", style: str = "") -> str:
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:middle;flex-shrink:0;{style}">{path}</svg>'
    )

I = {
    "dna":    '<path d="M2 15c6.667-6 13.333 0 20-6"/><path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/><path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993"/>',
    "user":   '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "virus":  '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "pill":   '<path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><line x1="8.5" y1="8.5" x2="15.5" y2="15.5"/>',
    "paper":  '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    "link":   '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
    "info":   '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "flask":  '<path d="M9 3h6"/><path d="M10 3v6l-3 6h10l-3-6V3"/><path d="M6.5 15h11"/>',
}

# ── Markdown renderer ─────────────────────────────────────────────────────────
def _md(text: str) -> str:
    text = re.sub(r'\*\*(.+?)\*\*',
        r'<strong style="color:#f5f0eb;font-weight:600">\1</strong>', text)
    text = re.sub(r'`(.+?)`',
        r'<code style="background:#2a2a2a;color:#3d6b52;padding:2px 6px;border-radius:3px;'
        r'font-family:\'DM Mono\',monospace;font-size:0.82em">\1</code>', text)
    text = re.sub(r'^### (.+)$',
        r'<p style="font-family:\'DM Mono\',monospace;font-size:0.62rem;color:#3d6b52;'
        r'letter-spacing:2px;text-transform:uppercase;margin:1.1rem 0 0.35rem;font-weight:600">'
        r'\1</p>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$',
        r'<p style="font-size:0.92rem;color:#f5f0eb;font-weight:600;margin:0.9rem 0 0.35rem">'
        r'\1</p>', text, flags=re.MULTILINE)
    lines = text.split('\n')
    result, in_list = [], False
    for line in lines:
        s = line.strip()
        if s.startswith('- '):
            if not in_list:
                result.append('<ul style="margin:0.4rem 0;padding-left:1.3rem">')
                in_list = True
            result.append(f'<li style="margin:5px 0;color:#c8c0b8;line-height:1.7">{s[2:]}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if s:
                result.append(
                    f'<p style="margin:0.3rem 0;color:#c8c0b8;line-height:1.78">{line}</p>'
                )
    if in_list:
        result.append('</ul>')
    return ''.join(result)


# ── Message bubbles ───────────────────────────────────────────────────────────
def render_assistant_message(content: str):
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin:1.2rem 0;align-items:flex-start">
        <div style="width:30px;height:30px;border-radius:6px;background:#222222;
                    border:1px solid #2a2a2a;display:flex;align-items:center;
                    justify-content:center;flex-shrink:0;margin-top:2px">
            {_icon(I['dna'], 14, '#3d6b52')}
        </div>
        <div style="background:#222222;border:1px solid #2a2a2a;
                    border-radius:2px 10px 10px 10px;
                    padding:1.1rem 1.3rem;flex:1;
                    box-shadow:0 1px 4px rgba(0,0,0,0.3)">
            {_md(content)}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_user_message(content: str):
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin:1.2rem 0;align-items:flex-start;
                flex-direction:row-reverse">
        <div style="width:30px;height:30px;border-radius:6px;background:#2a2a2a;
                    border:1px solid #333333;display:flex;align-items:center;
                    justify-content:center;flex-shrink:0;margin-top:2px">
            {_icon(I['user'], 13, '#888888')}
        </div>
        <div style="background:#2a2a2a;border:1px solid #333333;
                    border-radius:10px 2px 10px 10px;
                    padding:0.85rem 1.1rem;max-width:75%;
                    color:#f5f0eb;font-size:0.88rem;line-height:1.65">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Panel section header ──────────────────────────────────────────────────────
def _section(icon_key: str, label: str, source: str):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;
                margin:2rem 0 0.8rem;padding-bottom:0.6rem;
                border-bottom:1px solid #2a2a2a">
        <div style="width:26px;height:26px;border-radius:5px;background:#222222;
                    border:1px solid #2a2a2a;display:flex;align-items:center;
                    justify-content:center">
            {_icon(I[icon_key], 13, '#3d6b52')}
        </div>
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#f5f0eb;
                     letter-spacing:1.5px;text-transform:uppercase;font-weight:500">{label}</span>
        <span style="font-size:0.65rem;color:#444444;font-family:'DM Mono',monospace">
            via {source}</span>
    </div>
    """, unsafe_allow_html=True)


def _empty(msg: str):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;padding:0.9rem 1rem;
                background:#1e1e1e;border:1px dashed #2a2a2a;border-radius:8px;
                margin-bottom:1rem">
        {_icon(I['info'], 14, '#444444')}
        <span style="font-size:0.8rem;color:#555555">{msg}</span>
    </div>
    """, unsafe_allow_html=True)


# ── Data panels ───────────────────────────────────────────────────────────────
def render_disease_panel(diseases: list):
    _section("virus", "Disease Associations", "OpenTargets")
    if not diseases:
        _empty("No disease associations found for this protein.")
        return
    cols = st.columns(2)
    for i, d in enumerate(diseases[:10]):
        score = d.get("score", 0)
        bar_w = int(score * 100)
        bar_color = "#3d6b52" if score > 0.6 else "#2d5a42" if score > 0.35 else "#333333"
        areas = ", ".join(d.get("therapeutic_areas", [])[:2]) or "—"
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:#222222;border:1px solid #2a2a2a;border-radius:8px;
                        padding:0.85rem 1rem;margin-bottom:8px">
                <div style="display:flex;align-items:flex-start;gap:7px;margin-bottom:9px">
                    {_icon(I['target'], 12, '#3d6b52', 'margin-top:2px')}
                    <p style="font-size:0.8rem;color:#f5f0eb;margin:0;font-weight:500;
                               line-height:1.4">{d['disease_name']}</p>
                </div>
                <div style="background:#1a1a1a;border-radius:2px;height:3px;margin-bottom:6px">
                    <div style="width:{bar_w}%;background:{bar_color};height:3px;border-radius:2px">
                    </div>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="font-family:'DM Mono',monospace;font-size:0.6rem;
                                 color:#3d6b52">score {score}</span>
                    <span style="font-size:0.6rem;color:#555555">{areas}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_drugs_panel(drugs: list):
    _section("pill", "Drugs & Compounds", "ChEMBL")
    if not drugs:
        _empty("No drugs or compounds found for this target.")
        return
    phase_label = {"4": "Approved", "3": "Phase III", "2": "Phase II", "1": "Phase I"}
    phase_color = {"4": "#3d6b52", "3": "#2d5a42", "2": "#7a4a38", "1": "#1b3828"}
    cols = st.columns(3)
    for i, d in enumerate(drugs[:10]):
        phase = str(d.get("max_phase", ""))
        label = phase_label.get(phase, "Preclinical")
        color = phase_color.get(phase, "#333333")
        mech = (
            f'<p style="font-size:0.65rem;color:#666666;margin:6px 0 0;line-height:1.4">'
            f'{d["mechanism"][:55]}</p>'
        ) if d.get("mechanism") else ""
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:#222222;border:1px solid #2a2a2a;
                        border-top:2px solid {color};
                        border-radius:0 0 8px 8px;padding:0.8rem 0.9rem;margin-bottom:8px">
                <div style="display:flex;align-items:flex-start;gap:6px;margin-bottom:7px">
                    {_icon(I['flask'], 12, '#3d6b52', 'margin-top:1px')}
                    <p style="font-size:0.8rem;color:#f5f0eb;margin:0;font-weight:500;
                               line-height:1.3">{d['name']}</p>
                </div>
                <span style="font-family:'DM Mono',monospace;font-size:0.6rem;
                             color:{color};background:#1a1a1a;padding:2px 8px;
                             border-radius:3px;border:1px solid {color}">{label}</span>
                {mech}
            </div>
            """, unsafe_allow_html=True)


def render_papers_panel(papers: list):
    _section("paper", "Recent Literature", "PubMed")
    if not papers:
        _empty("No recent papers found.")
        return
    for p in papers:
        url = f"https://pubmed.ncbi.nlm.nih.gov/{p['pmid']}" if p.get("pmid") else "#"
        title = p.get("title", "")
        display = title[:115] + ("…" if len(title) > 115 else "")
        meta = f"{p.get('author','')}  ·  {p.get('journal','')[:35]}  ·  {p.get('year','')}"
        st.markdown(f"""
        <div style="background:#222222;border:1px solid #2a2a2a;border-radius:8px;
                    padding:0.9rem 1rem;margin-bottom:8px">
            <div style="display:flex;align-items:flex-start;gap:8px">
                {_icon(I['link'], 12, '#555555', 'margin-top:3px;flex-shrink:0')}
                <a href="{url}" target="_blank"
                   style="font-size:0.82rem;color:#f5f0eb;text-decoration:none;
                          font-weight:500;line-height:1.5;flex:1">{display}</a>
            </div>
            <p style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#555555;
                      margin:7px 0 0;padding-left:20px">{meta}</p>
        </div>
        """, unsafe_allow_html=True)