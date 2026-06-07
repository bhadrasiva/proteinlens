"""
ProteinLens — Dark theme styles.
Drop-in replacement for the st.markdown CSS block in app.py.
Dark #0d1f17 base · #2d6a4f accent · Claude-like interface.
"""

STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600&display=swap');

/* ── CSS Variables ── */
:root {
    --bg:        #0d1f17;
    --bg-2:      #111f18;
    --bg-3:      #162a1f;
    --surface:   #1a2e22;
    --surface-2: #1f3528;
    --border:    #243d2c;
    --border-2:  #2d6a4f;
    --accent:    #2d6a4f;
    --accent-2:  #3d8a66;
    --accent-3:  #52b788;
    --text:      #d4e8dc;
    --text-2:    #8ab49a;
    --text-3:    #527a60;
    --mono:      'JetBrains Mono', monospace;
    --sans:      'Inter', sans-serif;
}

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: var(--sans) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.main,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--bg) !important;
}
.block-container {
    padding: 1.5rem 2rem 4rem !important;
    max-width: 100% !important;
    background: var(--bg) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-2) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.2rem 1rem !important;
}

/* ── Text inputs ── */
.stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    border-radius: 6px !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput input::placeholder {
    color: var(--text-3) !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(45,106,79,0.18) !important;
    outline: none !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    border-radius: 6px !important;
    transition: all 0.15s !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: var(--surface-2) !important;
    border-color: var(--accent) !important;
    color: var(--accent-3) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: var(--surface) !important;
    color: var(--accent-3) !important;
    border: 1px solid var(--border) !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    border-radius: 6px !important;
}
.stDownloadButton > button:hover {
    background: var(--surface-2) !important;
    border-color: var(--accent) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.5rem 0.7rem !important;
}
[data-testid="metric-container"] label {
    color: var(--text-3) !important;
    font-size: 0.62rem !important;
    font-family: var(--mono) !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--accent-3) !important;
    font-size: 1.1rem !important;
    font-family: var(--mono) !important;
    font-weight: 600 !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    border-radius: 6px !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-2) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-3) !important;
    font-family: var(--mono) !important;
    font-size: 0.73rem !important;
    border: none !important;
    padding: 0.65rem 1.4rem !important;
    letter-spacing: 0.3px !important;
    transition: color 0.15s !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-2) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-3) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: transparent !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--bg) !important;
    padding-top: 1.2rem !important;
}

/* ── Chat input ── */
.stChatInput textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    transition: border-color 0.15s !important;
}
.stChatInput textarea::placeholder {
    color: var(--text-3) !important;
}
.stChatInput textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(45,106,79,0.15) !important;
}
.stChatInput button {
    background: var(--accent) !important;
    border-radius: 8px !important;
}
.stChatInput button:hover {
    background: var(--accent-2) !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}

/* ── Alerts / info boxes ── */
.stAlert {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
}
.streamlit-expanderContent {
    background: var(--bg-3) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}

/* ── Dividers ── */
hr {
    border-color: var(--border) !important;
    opacity: 1 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-3); }

/* ── Always show sidebar collapse arrow ── */
[data-testid="collapsedControl"] { display: flex !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Code blocks ── */
code, pre {
    background: var(--surface) !important;
    color: var(--accent-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    font-family: var(--mono) !important;
}
</style>
"""