"""
utils/styles.py
Shared CSS injected into every page for glassmorphism dark-mode theme.
"""

MAIN_CSS = """
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root Variables ─────────────────────────────────────────────────────── */
:root {
    --bg-dark:      #0d0f1a;
    --bg-card:      rgba(255,255,255,0.05);
    --border:       rgba(255,255,255,0.08);
    --accent:       #6c63ff;
    --accent2:      #00d4ff;
    --accent3:      #ff6584;
    --text-primary: #f0f0f8;
    --text-muted:   #8888aa;
    --success:      #00e676;
    --warning:      #ffab40;
    --error:        #ff5252;
    --glass-blur:   blur(16px);
}

/* ── Base ────────────────────────────────────────────────────────────────── */
html, body, .stApp {
    background: var(--bg-dark) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -20%, rgba(108,99,255,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0,212,255,0.10) 0%, transparent 60%) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-primary) !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: rgba(13,15,26,0.95) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: var(--glass-blur);
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;
    background: transparent !important;
    border: none !important;
    color: var(--text-muted) !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    transition: all 0.2s ease;
    font-size: 0.9rem !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

/* ── Headings ────────────────────────────────────────────────────────────── */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text-primary) !important;
}

/* ── Cards / Containers ──────────────────────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    margin-bottom: 16px;
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

.metric-card .label {
    font-size: 0.78rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.metric-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(108,99,255,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(108,99,255,0.45) !important;
}

/* ── Inputs ──────────────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.2) !important;
}

/* ── Selectbox labels ────────────────────────────────────────────────────── */
label[data-testid="stWidgetLabel"] p {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

/* ── File uploader ───────────────────────────────────────────────────────── */
[data-testid="stFileUploadDropzone"] {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-muted) !important;
}

/* ── Progress bar ────────────────────────────────────────────────────────── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 999px !important;
}

/* ── Info / Warning / Success boxes ─────────────────────────────────────── */
.stAlert {
    border-radius: 10px !important;
    border: none !important;
}

/* ── Divider ─────────────────────────────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
    margin: 24px 0 !important;
}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
}

/* ── Score ring helper ───────────────────────────────────────────────────── */
.score-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
}
.score-high   { background: rgba(0,230,118,0.15); color: #00e676; border: 1px solid rgba(0,230,118,0.3); }
.score-mid    { background: rgba(255,171,64,0.15); color: #ffab40; border: 1px solid rgba(255,171,64,0.3); }
.score-low    { background: rgba(255,82,82,0.15);  color: #ff5252; border: 1px solid rgba(255,82,82,0.3); }

/* ── Page title gradient ─────────────────────────────────────────────────── */
.gradient-title {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
}

/* ── Expander ────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
}

/* ── Plotly chart backgrounds ────────────────────────────────────────────── */
.js-plotly-plot .plotly .bg {
    fill: transparent !important;
}
</style>
"""


def inject_css():
    """Call this at the top of every page."""
    import streamlit as st
    st.markdown(MAIN_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    import streamlit as st
    st.markdown(f'<h1 class="gradient-title">{title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p style="color:var(--text-muted);margin-top:-12px;margin-bottom:24px;">{subtitle}</p>',
                    unsafe_allow_html=True)
