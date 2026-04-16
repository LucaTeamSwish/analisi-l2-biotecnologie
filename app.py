import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# CONFIG PAGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Analisi Nazionale L-2 Biotecnologie",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS STILE APPLE DARK
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* Root */
:root {
    --bg-primary: #0A0A0F;
    --bg-secondary: #111118;
    --bg-card: #16161E;
    --bg-card-hover: #1C1C26;
    --border: rgba(255,255,255,0.06);
    --border-accent: rgba(59,130,246,0.3);
    --text-primary: #F5F5F7;
    --text-secondary: #86868B;
    --text-tertiary: #48484A;
    --accent-blue: #3B82F6;
    --accent-amber: #F59E0B;
    --accent-green: #34D399;
    --accent-red: #EF4444;
    --font-display: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Base */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div {
    background-color: var(--bg-secondary) !important;
}

/* Header */
[data-testid="stHeader"] {
    background-color: var(--bg-primary) !important;
    border-bottom: 1px solid var(--border) !important;
}

/* Main content */
[data-testid="block-container"] {
    padding: 2rem 3rem !important;
    max-width: 1400px !important;
}

/* Titles */
h1 {
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.04em !important;
    color: var(--text-primary) !important;
    line-height: 1.1 !important;
}

h2 {
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
}

h3 {
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* Paragrafi */
p {
    color: var(--text-secondary) !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    font-weight: 300 !important;
}

/* Card sezione */
.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}

/* Divider */
hr {
    border-color: var(--border) !important;
    margin: 2rem 0 !important;
}

/* Sidebar navigation */
[data-testid="stSidebarNav"] {
    padding-top: 1rem !important;
}

.sidebar-title {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-tertiary);
    padding: 1rem 1rem 0.5rem;
}

/* Streamlit radio sidebar */
[data-testid="stSidebar"] .stRadio > label {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
}

[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
}

/* Bottone password */
.stButton > button {
    background: var(--accent-blue) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #2563EB !important;
    transform: translateY(-1px) !important;
}

/* Input password */
.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}

/* Plotly charts background */
.js-plotly-plot {
    background: transparent !important;
}

/* Metric */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

[data-testid="stMetricValue"] {
    color: var(--accent-blue) !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
}

/* Tag fonte */
.fonte-tag {
    font-size: 0.75rem;
    color: var(--text-tertiary);
    text-align: right;
    margin-top: 0.5rem;
    letter-spacing: 0.02em;
}

/* Istruzioni grafico */
.chart-instructions {
    background: rgba(59,130,246,0.06);
    border: 1px solid rgba(59,130,246,0.15);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    font-size: 0.82rem;
    color: #60A5FA;
    letter-spacing: 0.01em;
}

/* Descrizione grafico */
.chart-description {
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.65;
    margin-bottom: 1rem;
    font-weight: 300;
}

/* Badge */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.badge-blue { background: rgba(59,130,246,0.15); color: #60A5FA; }
.badge-amber { background: rgba(245,158,11,0.15); color: #FCD34D; }
.badge-green { background: rgba(52,211,153,0.15); color: #34D399; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* Nasconde elementi Streamlit non necessari */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PASSWORD
# ─────────────────────────────────────────────
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:center; margin-bottom: 2rem;'>
            <div style='font-size:2.5rem; font-weight:700; letter-spacing:-0.04em; color:#F5F5F7;'>
                Analisi Nazionale<br>L-2 Biotecnologie
            </div>
            <div style='color:#86868B; margin-top:0.75rem; font-size:0.95rem; font-weight:300;'>
                Accesso riservato
            </div>
        </div>
        """, unsafe_allow_html=True)

        pwd = st.text_input("Codice di accesso", type="password", label_visibility="collapsed",
                           placeholder="Inserisci il codice di accesso")
        if st.button("Accedi", use_container_width=True):
            if pwd == "L2":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Codice non valido")
    return False

if not check_password():
    st.stop()

# ─────────────────────────────────────────────
# CARICAMENTO DATI (cached)
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__)) + "/"

    def load(f):
        for enc in ['utf-8', 'latin-1']:
            try:
                return pd.read_csv(BASE + f, sep=None, engine='python', encoding=enc)
            except:
                continue

    # MUR
    df_imm   = load('MURimmatricolatixclasse.csv')
    df_lau   = load('MUR_laureatixclasse.csv')
    df_corso = load('MURiscrittixcorsodistudi.csv')

    # Filtra L-2
    imm_l2   = df_imm[df_imm['ClasseNUMERO'].astype(str).str.strip() == 'L-2'].copy()
    anno1_l2 = pd.DataFrame()
    lau_l2   = df_lau[df_lau['ClasseNUMERO'].astype(str).str.strip() == 'L-2'].copy()
    corso_l2 = df_corso[df_corso['ClasseNUMERO'].astype(str).str.strip() == 'L-2'].copy()

    # Macro area
    MACRO = {
        'Torino': 'Nord', 'Piemonte Orientale': 'Nord', 'Milano': 'Nord',
        'Milano Bicocca': 'Nord', 'Milano Cattolica': 'Nord', 'Milano San Raffaele': 'Nord',
        'Vita-Salute': 'Nord', 'Pavia': 'Nord', 'Brescia': 'Nord', 'Bergamo': 'Nord',
        'Insubria': 'Nord', 'Trento': 'Nord', 'Bolzano': 'Nord',
        'Padova': 'Nord', 'Venezia': 'Nord', 'Verona': 'Nord',
        'Trieste': 'Nord', 'Udine': 'Nord', 'Genova': 'Nord',
        'Bologna': 'Nord', 'Ferrara': 'Nord', 'Modena': 'Nord',
        'Parma': 'Nord', 'Reggio Emilia': 'Nord',
        'Firenze': 'Centro', 'Pisa': 'Centro', 'Siena': 'Centro',
        'Perugia': 'Centro', 'Camerino': 'Centro', 'Urbino': 'Centro',
        'Ancona': 'Centro', 'Macerata': 'Centro', 'Politecnica delle Marche': 'Centro',
        'Sapienza': 'Centro', 'Tor Vergata': 'Centro', 'Roma Tre': 'Centro',
        'Tuscia': 'Centro', 'Lumsa': 'Centro', 'Unicampus': 'Centro',
        'Campus Bio': 'Centro', 'Roma': 'Centro',
        "L'Aquila": 'Centro', 'Chieti': 'Centro', 'Teramo': 'Centro',
        'Napoli': 'Sud', 'Salerno': 'Sud', 'Sannio': 'Sud',
        'Bari': 'Sud', 'Lecce': 'Sud', 'Foggia': 'Sud', 'LUM': 'Sud',
        'Salento': 'Sud', 'Basilicata': 'Sud', 'Calabria': 'Sud',
        'Catanzaro': 'Sud', 'Magna Graecia': 'Sud', 'Molise': 'Sud',
        'Palermo': 'Isole', 'Catania': 'Isole', 'Messina': 'Isole',
        'Enna': 'Isole', 'Cagliari': 'Isole', 'Sassari': 'Isole',
    }

    def get_macro(nome):
        for key, area in MACRO.items():
            if key.lower() in str(nome).lower():
                return area
        return 'Non classificato'

    corso_l2['macro'] = corso_l2['AteneoNOME'].apply(get_macro)

    # AlmaLaurea
    def parse_almalaurea_csv(filepath):
        data = {}
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                for line in f:
                    line = line.strip().strip('"')
                    parts = line.split(';')
                    if len(parts) >= 2:
                        chiave = parts[0].strip().strip('"')
                        valore = parts[1].strip().strip('"')
                        if chiave and valore:
                            try:
                                data[chiave] = float(valore.replace('.', '').replace(',', '.'))
                            except:
                                data[chiave] = valore
        except:
            pass
        return data

    anni = [2020, 2021, 2022, 2023, 2024]
    profili     = {a: parse_almalaurea_csv(BASE + f'datialmalaureaPROFILO{a}.csv') for a in anni}
    occupazioni = {a: parse_almalaurea_csv(BASE + f'datialmalaureaOCCUPAZIONE{a}.csv') for a in anni}

    CHIAVE_ERASMUS = 'Hanno svolto periodi di studio all\xe2\x80\x99estero durante il corso di studio (%)'

    alma_profilo = pd.DataFrame({
        'anno': anni,
        'pct_magistrale':              [profili[a].get('Laurea magistrale biennale') for a in anni],
        'pct_stesso_ateneo_magistrale':[profili[a].get('Stesso Ateneo della laurea di primo livello') for a in anni],
        'pct_magistrale_nord':         [profili[a].get('Altro Ateneo del Nord') for a in anni],
        'pct_magistrale_centro':       [profili[a].get('Altro Ateneo del Centro') for a in anni],
        'pct_soddisfatti':             [round((profili[a].get('Decisamente s\xc3\xac', 0) or 0) + (profili[a].get('Pi\xc3\xb9 s\xc3\xac che no', 0) or 0), 1) for a in anni],
        'pct_riiscrizione':            [profili[a].get('S\xc3\xac, allo stesso corso dell\'Ateneo') for a in anni],
    })

    # Laureati
    lau_naz = lau_l2.groupby('AnnoS')['Lau'].sum().reset_index()
    lau_naz['AnnoS'] = lau_naz['AnnoS'].astype(int)
    lau_naz = lau_naz[lau_naz['AnnoS'] >= 2010].reset_index(drop=True)
    lau_naz['COVID'] = lau_naz['AnnoS'].isin([2020, 2021])

    # Immatricolati
    imm_naz = imm_l2.groupby('AnnoA')['Imm'].sum().reset_index()
    imm_naz = imm_naz[imm_naz['AnnoA'].str[:4].astype(int) >= 2010].copy()
    imm_naz['anno_short'] = imm_naz['AnnoA'].str[:4] + '/' + imm_naz['AnnoA'].str[7:9]
    imm_naz['delta'] = imm_naz['Imm'].pct_change() * 100

    # ANVUR PENTAHO
    df_anvur = pd.read_csv(BASE + 'PENTAHO(L2).csv', sep=None, engine='python', encoding='latin-1')
    df_anvur['imm'] = df_anvur['Numeratore'].str.replace(',', '').str.replace('.000', '').astype(float)
    df_anvur['corso_nome'] = df_anvur['Nome Corso'].str.split(' - ', n=1).str[1].str.strip()
    df_anvur['ateneo_clean'] = (
        df_anvur['Ateneo']
        .str.encode('latin-1').str.decode('utf-8', errors='replace')
        .str.strip()
    )
    df_anvur['ateneo_short'] = (
        df_anvur['ateneo_clean']
        .str.replace("Università di ", "", regex=False)
        .str.replace("Università della ", "", regex=False)
        .str.replace("Università del ", "", regex=False)
        .str.replace("Università degli Studi di ", "", regex=False)
        .str.replace("Università", "", regex=False)
        .str.strip()
    )

    ATENEO_REG_ANVUR = {
        'Torino': 'Piemonte', 'Piemonte Orientale': 'Piemonte',
        'Milano': 'Lombardia', 'Bicocca': 'Lombardia',
        'San Raffaele': 'Lombardia', 'Pavia': 'Lombardia',
        'Brescia': 'Lombardia', "dell'Insubria": 'Lombardia',
        'Trento': 'Trentino-Alto Adige/Südtirol',
        'Padova': 'Veneto', 'Verona': 'Veneto',
        'Trieste': 'Friuli-Venezia Giulia', 'Udine': 'Friuli-Venezia Giulia',
        'Genova': 'Liguria',
        'Bologna': 'Emilia-Romagna', 'Ferrara': 'Emilia-Romagna',
        'Modena e Reggio Emilia': 'Emilia-Romagna', 'Parma': 'Emilia-Romagna',
        'Firenze': 'Toscana', 'Pisa': 'Toscana', 'Siena': 'Toscana',
        'Perugia': 'Umbria',
        'Camerino': 'Marche', 'Carlo Bo': 'Marche',
        'La Sapienza': 'Lazio', 'Tor Vergata': 'Lazio',
        'Tuscia': 'Lazio', 'Teramo': 'Abruzzo', "de L'Aquila": 'Abruzzo',
        'Federico II': 'Campania', 'Vanvitelli': 'Campania', 'Sannio': 'Campania',
        'Bari': 'Puglia', 'Foggia': 'Puglia', 'SALENTO': 'Puglia',
        'Basilicata': 'Basilicata',
        'Calabria': 'Calabria', 'Magna Graecia': 'Calabria',
        'Catania': 'Sicilia', 'Palermo': 'Sicilia', 'Messina': 'Sicilia',
        'Cagliari': 'Sardegna', 'Sassari': 'Sardegna',
    }

    def get_regione(nome):
        for key, reg in ATENEO_REG_ANVUR.items():
            if key.lower() in str(nome).lower():
                return reg
        return None

    df_anvur['regione'] = df_anvur['ateneo_short'].apply(get_regione)
    df_anvur['macro'] = df_anvur['regione'].map({
        'Piemonte': 'Nord', 'Lombardia': 'Nord', 'Veneto': 'Nord',
        'Friuli-Venezia Giulia': 'Nord', 'Liguria': 'Nord',
        'Emilia-Romagna': 'Nord', 'Trentino-Alto Adige/Südtirol': 'Nord',
        'Toscana': 'Centro', 'Umbria': 'Centro', 'Marche': 'Centro',
        'Lazio': 'Centro', 'Abruzzo': 'Centro',
        'Campania': 'Sud', 'Puglia': 'Sud', 'Basilicata': 'Sud',
        'Calabria': 'Sud', 'Molise': 'Sud',
        'Sicilia': 'Isole', 'Sardegna': 'Isole',
    })

    # AVA2
    df_ava2 = pd.read_csv(BASE + 'L2_datadest.csv', sep=';', encoding='latin-1')
    df_ava2['ind_float'] = (
        df_ava2['INDICATORE'].astype(str).str.strip()
        .str.replace(',', '.').str.replace(' ', '')
        .apply(lambda x: float(x) if x not in ['', 'nan', 'None'] else None)
    )

    return (imm_l2, anno1_l2, lau_l2, corso_l2, lau_naz, imm_naz,
            alma_profilo, df_anvur, df_ava2)

# Carica dati
with st.spinner("Caricamento dati in corso..."):
    (imm_l2, anno1_l2, lau_l2, corso_l2, lau_naz, imm_naz,
     alma_profilo, df_anvur, df_ava2) = load_data()

# Costanti
GEOJSON_URL = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
GRIGIO_SCURO = ["Valle d'Aosta/Vallée d'Aoste", 'Molise']
COLORI_MACRO = {'Nord': '#3B82F6', 'Centro': '#F59E0B', 'Sud': '#34D399', 'Isole': '#818CF8'}
BG_PLOT = '#0F172A'
BG_PAPER = '#0A0A0F'

# parametri base condivisi - solo quelli che non conflittano mai
_BASE = dict(
    font=dict(family='Inter', size=12),
    plot_bgcolor=BG_PLOT,
    paper_bgcolor=BG_PAPER,
    title_font=dict(size=18, color='white', family='Inter'),
)
# PLOT_LAYOUT è vuoto - ogni grafico specifica i propri parametri
PLOT_LAYOUT = _BASE

def fonte_annotation(testo):
    return dict(
        x=0.99, y=-0.13, xref='paper', yref='paper',
        text=testo, showarrow=False,
        font=dict(size=10, color='#6B7280'),
        align='right', xanchor='right'
    )

def chart_header(titolo, descrizione, istruzioni):
    st.markdown(f"### {titolo}")
    st.markdown(f'<p class="chart-description">{descrizione}</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-instructions">{istruzioni}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem 0;'>
        <div style='font-size:1.1rem; font-weight:600; color:#F5F5F7; letter-spacing:-0.02em;'>
            L-2 Biotecnologie
        </div>
        <div style='font-size:0.75rem; color:#48484A; margin-top:0.25rem; font-weight:400;'>
            Analisi Nazionale
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-title">Sezioni</div>', unsafe_allow_html=True)

    sezione = st.radio(
        label="",
        options=[
            "Panoramica",
            "Domanda Nazionale",
            "Geografia",
            "Profilo Studenti",
            "Percorso Accademico",
            "Varianti del Corso",
            "Analisi Avanzata",
            "Sintesi",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#48484A; line-height:1.6;'>
        Fonti: MUR-USTAT, ANVUR,<br>AlmaLaurea · Dati 2010–2025
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEZIONE: PANORAMICA
# ─────────────────────────────────────────────
if sezione == "Panoramica":
    st.markdown("# Analisi Nazionale\nL-2 Biotecnologie")
    st.markdown("---")

    st.markdown("""
    <p>
    Questa analisi documenta il panorama nazionale del Corso di Laurea in Biotecnologie (Classe L-2)
    attraverso dati ufficiali MUR-USTAT, ANVUR e AlmaLaurea. I dati coprono il periodo 2010–2025
    e includono immatricolati, laureati, distribuzione geografica, profilo degli studenti e indicatori
    di qualità della didattica.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("### Indicatori chiave")

    # KPI
    kpi = [
        {'label': 'Immatricolati puri 2024/25', 'value': '7.076', 'delta': '↑ stabile', 'color': '#3B82F6'},
        {'label': 'Atenei attivi L-2', 'value': '43', 'delta': 'nessun telematico', 'color': '#34D399'},
        {'label': 'Soddisfatti del corso', 'value': '80.9%', 'delta': 'media 2020–2024', 'color': '#F59E0B'},
        {'label': 'Prosegue magistrale', 'value': '87%', 'delta': 'stabile 2020–2024', 'color': '#818CF8'},
    ]

    cols = st.columns(4)
    for col, k in zip(cols, kpi):
        with col:
            st.markdown(f"""
            <div class="section-card" style="border-top: 3px solid {k['color']}; padding: 1.25rem;">
                <div style="font-size:0.75rem; color:#86868B; text-transform:uppercase;
                            letter-spacing:0.08em; margin-bottom:0.5rem;">{k['label']}</div>
                <div style="font-size:2rem; font-weight:700; color:{k['color']};
                            letter-spacing:-0.03em;">{k['value']}</div>
                <div style="font-size:0.78rem; color:#48484A; margin-top:0.25rem;">{k['delta']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Struttura dell'analisi")

    sezioni_info = [
        ("Domanda Nazionale", "Trend immatricolati e laureati dal 2010 al 2025. Impatto COVID e tasso di completamento.", "#3B82F6"),
        ("Geografia", "Distribuzione regionale degli immatricolati e posizionamento degli atenei per macro area.", "#F59E0B"),
        ("Profilo Studenti", "Soddisfazione, riiscrizione e destinazione alla magistrale secondo AlmaLaurea.", "#34D399"),
        ("Percorso Accademico", "Tasso di prosecuzione al II anno e abbandoni secondo indicatori ANVUR iC14 e iC21.", "#EF4444"),
        ("Varianti del Corso", "Distribuzione delle 16 varianti di denominazione L-2 per immatricolati e prosecuzione.", "#818CF8"),
        ("Analisi Avanzata", "Correlazione tra dimensione del corso e tasso di prosecuzione. Analisi statistica originale.", "#60A5FA"),
    ]

    for nome, desc, col in sezioni_info:
        st.markdown(f"""
        <div class="section-card" style="display:flex; align-items:flex-start; gap:1rem; padding:1.25rem;">
            <div style="width:3px; background:{col}; border-radius:2px; min-height:40px; flex-shrink:0;"></div>
            <div>
                <div style="font-size:0.9rem; font-weight:600; color:#F5F5F7; margin-bottom:0.25rem;">{nome}</div>
                <div style="font-size:0.82rem; color:#86868B; font-weight:300;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEZIONE: DOMANDA NAZIONALE
# ─────────────────────────────────────────────
elif sezione == "Domanda Nazionale":
    st.markdown("## Domanda Nazionale")
    st.markdown("---")

    # G1 — Immatricolati
    chart_header(
        "Immatricolati puri L-2 — Italia (2010–2025)",
        "Il grafico riporta il numero di studenti che si iscrivono per la prima volta a un corso L-2 "
        "Biotecnologie in Italia, per anno accademico. Gli immatricolati puri escludono i trasferimenti "
        "e i passaggi di corso. Nessun ateneo telematico offre L-2, trattandosi di un corso che richiede "
        "attività laboratoriali obbligatorie.",
        "Passa il cursore sui punti per vedere il valore e la variazione percentuale rispetto all'anno precedente."
    )

    y_2019 = imm_naz[imm_naz['anno_short'] == '2019/20']['Imm'].values[0]
    y_2020 = imm_naz[imm_naz['anno_short'] == '2020/21']['Imm'].values[0]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=imm_naz['anno_short'], y=imm_naz['Imm'],
        mode='none', fill='tozeroy',
        fillcolor='rgba(59,130,246,0.08)',
        showlegend=False, hoverinfo='skip'
    ))
    fig1.add_trace(go.Scatter(
        x=['2019/20', '2020/21', '2020/21', '2019/20'],
        y=[y_2019, y_2020, 0, 0],
        fill='toself', fillcolor='rgba(239,68,68,0.12)',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False, hoverinfo='skip'
    ))
    fig1.add_trace(go.Scatter(
        x=imm_naz['anno_short'], y=imm_naz['Imm'],
        mode='lines+markers',
        line=dict(color='#60A5FA', width=2.5),
        marker=dict(size=7, color='#60A5FA', line=dict(color='#1E3A5F', width=1.5)),
        customdata=imm_naz[['delta']].round(1),
        hovertemplate='<b>%{x}</b><br>Immatricolati: <b>%{y:,}</b><br>Variazione: %{customdata[0]:+.1f}%<extra></extra>',
        showlegend=False
    ))
    idx_max = imm_naz['Imm'].idxmax()
    fig1.add_annotation(
        x=imm_naz.loc[idx_max, 'anno_short'], y=imm_naz.loc[idx_max, 'Imm'],
        text=f"Picco: {imm_naz.loc[idx_max, 'Imm']:,}",
        showarrow=True, arrowhead=2, arrowcolor='#60A5FA',
        font=dict(size=11, color='#60A5FA'), bgcolor='#1E3A5F',
        bordercolor='#60A5FA', borderwidth=1, ay=-40
    )
    fig1.add_annotation(fonte_annotation('Fonte: MUR-USTAT · Immatricolati puri L-2'))
    fig1.add_annotation(
        x='2019/20', y=400, text='Periodo COVID',
        showarrow=False, font=dict(size=10, color='#F87171'),
        xanchor='left', xshift=6
    )
    fig1.update_layout(
        **PLOT_LAYOUT, title='',
        margin=dict(t=80, b=60, l=60, r=30), height=500,
        xaxis=dict(tickangle=-45, showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#374151'),
        yaxis=dict(gridcolor='#1F2937', tickfont=dict(color='#9CA3AF'), linecolor='#374151', rangemode='tozero'),
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # G2 — Laureati
    chart_header(
        "Laureati L-2 Biotecnologie — Italia (2010–2024)",
        "Numero totale di laureati per anno solare. Le barre rosse corrispondono agli anni 2020 e 2021, "
        "durante i quali le sessioni di laurea hanno subito variazioni legate all'emergenza sanitaria. "
        "Il tasso di completamento medio, calcolato confrontando immatricolati e laureati a distanza di "
        "tre anni, si attesta intorno al 45.9%.",
        "Passa il cursore sulle barre per vedere il valore esatto. Le barre rosse indicano il periodo COVID."
    )

    fig2 = px.bar(
        lau_naz, x='AnnoS', y='Lau',
        color='COVID',
        color_discrete_map={True: '#EF4444', False: '#3B82F6'},
        labels={'Lau': 'N° Laureati', 'AnnoS': 'Anno'},
        text='Lau'
    )
    fig2.update_traces(
        texttemplate='%{text:,}', textposition='outside',
        textfont=dict(size=9, color='#9CA3AF'),
        marker_line_width=0, opacity=0.9
    )
    idx_max2 = lau_naz['Lau'].idxmax()
    fig2.add_annotation(
        x=lau_naz.loc[idx_max2, 'AnnoS'], y=lau_naz.loc[idx_max2, 'Lau'],
        text=f"Picco: {lau_naz.loc[idx_max2, 'Lau']:,}",
        showarrow=True, arrowhead=2, arrowcolor='#60A5FA',
        font=dict(size=11, color='#60A5FA'), bgcolor='#1E3A5F',
        bordercolor='#60A5FA', borderwidth=1, ay=-40
    )
    fig2.add_annotation(fonte_annotation('Fonte: MUR-USTAT · Tasso completamento medio: 45.9%'))
    fig2.update_layout(
        **PLOT_LAYOUT, title='', showlegend=False,
        margin=dict(t=80, b=60, l=60, r=30), height=500,
        xaxis=dict(tickangle=-45, showgrid=False, tickfont=dict(color='#9CA3AF'), tickmode='linear', dtick=1, linecolor='#374151'),
        yaxis=dict(gridcolor='#1F2937', tickfont=dict(color='#9CA3AF'), rangemode='tozero', linecolor='#374151'),
    )
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# SEZIONE: GEOGRAFIA
# ─────────────────────────────────────────────
elif sezione == "Geografia":
    st.markdown("## Geografia")
    st.markdown("---")

    # G3 — Mappa
    chart_header(
        "Immatricolati puri L-2 per regione",
        "La mappa mostra la distribuzione degli immatricolati puri per regione, dal 2020 al 2024. "
        "Le regioni in grigio scuro (Molise e Valle d'Aosta) non ospitano atenei con corsi L-2 attivi. "
        "I dati provengono dal Cruscotto ANVUR e coprono 43 atenei.",
        "Seleziona l'anno con i pulsanti. Passa il cursore sulla regione per vedere il dettaglio per ateneo e corso."
    )

    anno1_fil = df_anvur[(df_anvur['Anno accademico'] >= 2020) & (df_anvur['regione'].notna())].copy()
    df_mappa = anno1_fil.groupby(['Anno accademico', 'regione'])['imm'].sum().reset_index().rename(columns={'imm': 'immatricolati'})
    df_hover_m = anno1_fil.groupby(['Anno accademico', 'regione', 'ateneo_short', 'corso_nome'])['imm'].sum().reset_index()

    def crea_hover_m(regione, anno):
        subset = df_hover_m[(df_hover_m['regione'] == regione) & (df_hover_m['Anno accademico'] == anno)].sort_values('imm', ascending=False)
        totale = int(subset['imm'].sum())
        testo = f"<b>{regione}</b><br>Anno: {anno}<br>Immatricolati puri: <b>{totale:,}</b><br><br>"
        for _, row in subset.iterrows():
            testo += f"<b>{row['ateneo_short']}</b><br>&nbsp;&nbsp;{row['corso_nome']}: {int(row['imm']):,}<br>"
        return testo

    df_mappa['hover'] = df_mappa.apply(lambda r: crea_hover_m(r['regione'], r['Anno accademico']), axis=1)
    anni_mappa = sorted(df_mappa['Anno accademico'].unique())
    z_min = df_mappa['immatricolati'].min()
    z_max = df_mappa['immatricolati'].max()

    fig3 = go.Figure()
    for i, anno in enumerate(anni_mappa):
        subset = df_mappa[df_mappa['Anno accademico'] == anno]
        fig3.add_trace(go.Choropleth(
            geojson=GEOJSON_URL, locations=subset['regione'],
            featureidkey='properties.reg_name', z=subset['immatricolati'],
            colorscale=[[0.0,'#1E3A5F'],[0.3,'#2563EB'],[0.6,'#60A5FA'],[1.0,'#BAE6FD']],
            zmin=z_min, zmax=z_max,
            colorbar=dict(title=dict(text='Immatricolati<br>puri', font=dict(color='#9CA3AF')), tickfont=dict(color='#9CA3AF'), x=1.0, thickness=15),
            marker_line_color='#0F172A', marker_line_width=1.5,
            text=subset['hover'], hovertemplate='%{text}<extra></extra>',
            name=str(anno), visible=(i == 0),
        ))
        fig3.add_trace(go.Choropleth(
            geojson=GEOJSON_URL, locations=GRIGIO_SCURO,
            featureidkey='properties.reg_name', z=[0, 0],
            colorscale=[[0,'#374151'],[1,'#374151']], showscale=False,
            marker_line_color='#0F172A', marker_line_width=1.5,
            hovertemplate='<b>%{location}</b><br>Nessun corso L-2 attivo<extra></extra>',
            visible=(i == 0), showlegend=False,
        ))

    n_layers = len(fig3.data) // len(anni_mappa)
    buttons_m = []
    for i, anno in enumerate(anni_mappa):
        vis = []
        for j in range(len(anni_mappa)):
            for _ in range(n_layers):
                vis.append(j == i)
        buttons_m.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Immatricolati puri L-2 per Regione — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))

    fig3.update_layout(
        title=dict(text=f'Immatricolati puri L-2 per Regione — {anni_mappa[0]}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.08, yanchor='top',
            buttons=buttons_m, bgcolor='#1F2937', bordercolor='#3B82F6', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[
            dict(x=0.01, y=-0.02, xref='paper', yref='paper',
                 text="Grigio scuro: Molise e Valle d'Aosta — nessun corso L-2 attivo",
                 showarrow=False, font=dict(size=10, color='#6B7280'), align='left'),
            fonte_annotation('Fonte: ANVUR Cruscotto')
        ],
        margin=dict(r=20, t=110, l=0, b=40), height=650,
        font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER, geo=dict(bgcolor=BG_PAPER),
    )
    fig3.update_geos(fitbounds='locations', visible=False)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # G4 — Top atenei
    chart_header(
        "Top 15 atenei per immatricolati puri",
        "I 15 atenei con il maggior numero di immatricolati puri L-2 per anno accademico. "
        "Il colore identifica la macro area geografica dell'ateneo. Il grafico consente di confrontare "
        "il posizionamento competitivo degli atenei nazionali e il peso relativo di ciascuna area geografica.",
        "Seleziona l'anno con i pulsanti. Passa il cursore sulle barre per vedere il numero di corsi L-2 offerti e il dettaglio per corso."
    )

    g4_anvur = df_anvur[df_anvur['Anno accademico'] >= 2020].groupby(['Anno accademico', 'ateneo_short', 'regione'])['imm'].sum().reset_index()
    g4_anvur['macro'] = g4_anvur['regione'].map({
        'Piemonte': 'Nord', 'Lombardia': 'Nord', 'Veneto': 'Nord',
        'Friuli-Venezia Giulia': 'Nord', 'Liguria': 'Nord',
        'Emilia-Romagna': 'Nord', 'Trentino-Alto Adige/Südtirol': 'Nord',
        'Toscana': 'Centro', 'Umbria': 'Centro', 'Marche': 'Centro',
        'Lazio': 'Centro', 'Abruzzo': 'Centro',
        'Campania': 'Sud', 'Puglia': 'Sud', 'Basilicata': 'Sud',
        'Calabria': 'Sud', 'Molise': 'Sud',
        'Sicilia': 'Isole', 'Sardegna': 'Isole',
    })
    g4_corsi = df_anvur[df_anvur['Anno accademico'] >= 2020].groupby(['Anno accademico', 'ateneo_short'])['corso_nome'].nunique().reset_index().rename(columns={'corso_nome': 'n_corsi'})
    g4_nomi = df_anvur[df_anvur['Anno accademico'] >= 2020].groupby(['Anno accademico', 'ateneo_short', 'corso_nome'])['imm'].sum().reset_index().groupby(['Anno accademico', 'ateneo_short']).apply(
        lambda x: '<br>'.join([f"&nbsp;&nbsp;• {row['corso_nome']}: <b>{int(row['imm']):,}</b>" for _, row in x.sort_values('imm', ascending=False).iterrows()])
    ).reset_index().rename(columns={0: 'lista_corsi'})
    g4_anvur = g4_anvur.merge(g4_corsi, on=['Anno accademico', 'ateneo_short'], how='left')
    g4_anvur = g4_anvur.merge(g4_nomi, on=['Anno accademico', 'ateneo_short'], how='left')

    anni_g4 = sorted(g4_anvur['Anno accademico'].unique())
    fig4 = go.Figure()
    for i, anno in enumerate(anni_g4):
        subset = g4_anvur[g4_anvur['Anno accademico'] == anno].sort_values('imm', ascending=False).head(15).sort_values('imm', ascending=True).reset_index(drop=True)
        fig4.add_trace(go.Bar(
            x=subset['imm'], y=subset['ateneo_short'],
            orientation='h',
            marker=dict(color=[COLORI_MACRO.get(m, '#6B7280') for m in subset['macro']], line=dict(width=0), opacity=0.9),
            text=subset['imm'].astype(int).apply(lambda x: f'{x:,}'),
            textposition='outside', textfont=dict(size=11, color='#9CA3AF'),
            customdata=subset[['macro', 'n_corsi', 'lista_corsi']],
            hovertemplate='<b>%{y}</b><br>Immatricolati puri: <b>%{x:,}</b><br>Macro area: %{customdata[0]}<br>N° corsi L-2: <b>%{customdata[1]}</b><br>%{customdata[2]}<extra></extra>',
            visible=(i == 0), showlegend=False,
        ))
    for macro, colore in COLORI_MACRO.items():
        fig4.add_trace(go.Bar(x=[None], y=[None], orientation='h', marker_color=colore, name=macro, visible=True))

    n_dati = len(anni_g4)
    n_leg = len(COLORI_MACRO)
    buttons_g4 = []
    for i, anno in enumerate(anni_g4):
        vis = [j == i for j in range(n_dati)] + [True] * n_leg
        buttons_g4.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Top 15 atenei L-2 — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))

    fig4.update_layout(
        **PLOT_LAYOUT, title='',
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.10, yanchor='top',
            buttons=buttons_g4, bgcolor='#1F2937', bordercolor='#3B82F6', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=len(anni_g4)-1, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto — Immatricolati puri per ateneo')],
        xaxis=dict(title=dict(text='N° immatricolati puri', font=dict(color='#9CA3AF')), showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#374151'),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#D1D5DB'), linecolor='#374151'),
        legend=dict(title=dict(text='Macro area', font=dict(color='#9CA3AF')), font=dict(color='#D1D5DB'), bgcolor='rgba(0,0,0,0)', x=0.75, y=0.05),
        margin=dict(t=120, b=60, l=180, r=80), height=560, barmode='overlay'
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # G10 — Bubble quota macro area
    chart_header(
        "Quota immatricolati per macro area — trend 2019–2024",
        "Ogni bolla rappresenta la quota percentuale di immatricolati di una macro area rispetto al totale "
        "nazionale. La dimensione della bolla è proporzionale al numero assoluto di immatricolati. "
        "Il Nord mantiene una quota dominante ma in lieve calo dal 2020.",
        "Passa il cursore sulle bolle per vedere la quota e il numero assoluto di immatricolati."
    )

    macro_trend = df_anvur[df_anvur['Anno accademico'] >= 2019].groupby(['Anno accademico', 'macro'])['imm'].sum().reset_index().dropna(subset=['macro'])
    totale_anno = macro_trend.groupby('Anno accademico')['imm'].sum().reset_index()
    totale_anno.columns = ['Anno accademico', 'totale']
    macro_pct = macro_trend.merge(totale_anno, on='Anno accademico')
    macro_pct['pct'] = (macro_pct['imm'] / macro_pct['totale'] * 100).round(1)

    OFFSET = {'Nord': 2, 'Centro': 1, 'Sud': -1, 'Isole': -2}
    fig10 = go.Figure()
    for macro in ['Nord', 'Centro', 'Sud', 'Isole']:
        subset = macro_pct[macro_pct['macro'] == macro].sort_values('Anno accademico').copy()
        subset['pct_offset'] = subset['pct'] + OFFSET.get(macro, 0)
        fig10.add_trace(go.Scatter(
            x=subset['Anno accademico'].astype(str), y=subset['pct_offset'],
            mode='markers+text', name=macro,
            marker=dict(size=subset['imm'] / macro_pct['imm'].max() * 80 + 20,
                        color=COLORI_MACRO[macro], opacity=0.85, line=dict(color='#0F172A', width=2)),
            text=subset['pct'].apply(lambda x: f'{x:.1f}%'),
            textposition='middle center', textfont=dict(size=10, color='white', family='Inter'),
            hovertemplate=f'<b>{macro}</b><br>Anno: %{{x}}<br>Quota: <b>%{{customdata[0]:.1f}}%</b><br>Immatricolati: <b>%{{customdata[1]:,}}</b><extra></extra>',
            customdata=list(zip(subset['pct'], subset['imm'].astype(int))),
        ))

    fig10.update_layout(
        **PLOT_LAYOUT, title='',
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto — Dimensione bolla = immatricolati assoluti')],
        xaxis=dict(title=dict(text='Anno accademico', font=dict(color='#9CA3AF')), showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#374151'),
        yaxis=dict(title=dict(text='Quota (%)', font=dict(color='#9CA3AF')), gridcolor='#1F2937', ticksuffix='%', tickfont=dict(color='#9CA3AF'), linecolor='#374151', range=[0, 70]),
        legend=dict(font=dict(color='#D1D5DB'), bgcolor='rgba(0,0,0,0)', x=0.01, y=0.99),
        height=520, margin=dict(t=80, b=80, l=60, r=30),
    )
    st.plotly_chart(fig10, use_container_width=True)

    st.markdown("---")

    # G9 — Lazio
    chart_header(
        "Immatricolati puri L-2 nel Lazio — per ateneo e corso",
        "Andamento degli immatricolati puri nei tre atenei laziali che offrono corsi L-2: "
        "La Sapienza (3 corsi), Tor Vergata e Tuscia. Le linee tratteggiate indicano i corsi "
        "secondari de La Sapienza. Il grafico permette di valutare il posizionamento competitivo "
        "nel territorio laziale.",
        "Passa il cursore sulle linee per vedere i valori anno per anno per ciascun corso."
    )

    lazio_detail = df_anvur[(df_anvur['regione'] == 'Lazio') & (df_anvur['Anno accademico'] >= 2019)].groupby(['Anno accademico', 'ateneo_short', 'corso_nome'])['imm'].sum().reset_index().sort_values('Anno accademico')
    lazio_detail['label'] = lazio_detail.apply(lambda r: f"{r['ateneo_short']} — {r['corso_nome']}", axis=1)
    ordine = lazio_detail.groupby('label')['imm'].sum().sort_values(ascending=False).index.tolist()
    palette = {'La Sapienza': ['#F59E0B', '#FCD34D', '#F97316'], 'Tor Vergata': ['#3B82F6'], 'Tuscia': ['#34D399']}
    colori_label = {}
    contatori = {k: 0 for k in palette}
    for label in ordine:
        ateneo = label.split(' — ')[0]
        idx = contatori.get(ateneo, 0)
        colori_label[label] = palette.get(ateneo, ['#818CF8'])[idx % len(palette.get(ateneo, ['#818CF8']))]
        contatori[ateneo] = idx + 1

    fig9 = go.Figure()
    for label in ordine:
        df_lab = lazio_detail[lazio_detail['label'] == label].sort_values('Anno accademico')
        colore = colori_label[label]
        ateneo = label.split(' — ')[0]
        corso = label.split(' — ')[1]
        dash = 'dot' if ateneo == 'La Sapienza' and corso != 'Biotecnologie' else 'solid'
        fig9.add_trace(go.Scatter(
            x=df_lab['Anno accademico'].astype(str), y=df_lab['imm'],
            mode='lines+markers', name=label,
            line=dict(color=colore, width=2.5, dash=dash),
            marker=dict(size=8, color=colore, line=dict(color='#0F172A', width=1.5)),
            hovertemplate=f'<b>{label}</b><br>Anno: %{{x}}<br>Immatricolati puri: <b>%{{y:,.0f}}</b><extra></extra>'
        ))
        ultimo = df_lab.iloc[-1]
        fig9.add_annotation(
            x=str(int(ultimo['Anno accademico'])), y=ultimo['imm'],
            text=f"<b>{int(ultimo['imm'])}</b>",
            showarrow=False, font=dict(size=10, color=colore),
            xanchor='left', xshift=8
        )

    fig9.update_layout(
        **PLOT_LAYOUT, title='',
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto · Linee tratteggiate = corsi secondari La Sapienza')],
        xaxis=dict(title=dict(text='Anno accademico', font=dict(color='#9CA3AF')), showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#374151'),
        yaxis=dict(title=dict(text='N° immatricolati puri', font=dict(color='#9CA3AF')), gridcolor='#1F2937', tickfont=dict(color='#9CA3AF'), linecolor='#374151', rangemode='tozero'),
        legend=dict(font=dict(color='#D1D5DB'), bgcolor='rgba(0,0,0,0)', x=0.01, y=0.99),
        height=500, margin=dict(t=80, b=80, l=60, r=180),
    )
    st.plotly_chart(fig9, use_container_width=True)

# ─────────────────────────────────────────────
# SEZIONE: PROFILO STUDENTI
# ─────────────────────────────────────────────
elif sezione == "Profilo Studenti":
    st.markdown("## Profilo Studenti")
    st.markdown("---")

    # G5 — Gauge
    chart_header(
        "Indicatori chiave del profilo laureati L-2",
        "I tre indicatori riportano i valori del 2024 confrontati con un anno di riferimento selezionabile. "
        "La linea arancione nel gauge indica il valore dell'anno di riferimento. "
        "I dati provengono dall'indagine AlmaLaurea sul Profilo dei Laureati.",
        "Seleziona l'anno di riferimento per il confronto con i pulsanti in alto."
    )

    anni_disp = alma_profilo['anno'].tolist()
    anni_ref = [2020, 2021, 2022, 2023]
    indicatori_g5 = [
        ('pct_soddisfatti', 'Soddisfatti del corso', '#3B82F6'),
        ('pct_riiscrizione', 'Si reiscriverebbero', '#34D399'),
        ('pct_magistrale', 'Prosegue magistrale', '#818CF8'),
    ]
    val_2024 = {col: float(alma_profilo[alma_profilo['anno']==2024][col].values[0]) for col, _, _ in indicatori_g5}

    fig5 = go.Figure()
    for anno_ref in anni_ref:
        visible = (anno_ref == 2020)
        for col_idx, (col, titolo, colore) in enumerate(indicatori_g5):
            val_ref = float(alma_profilo[alma_profilo['anno']==anno_ref][col].values[0])
            fig5.add_trace(go.Indicator(
                mode='gauge+number+delta',
                value=val_2024[col],
                delta={'reference': val_ref, 'suffix': '%', 'relative': False,
                       'increasing': {'color': '#34D399'}, 'decreasing': {'color': '#F87171'}},
                number={'suffix': '%', 'font': {'size': 40, 'color': colore}},
                title={'text': f"<b style='color:#D1D5DB'>{titolo}</b><br><span style='font-size:11px;color:#6B7280'>2024 vs {anno_ref}</span>"},
                gauge={
                    'axis': {'range': [0, 100], 'ticksuffix': '%', 'tickfont': {'color': '#6B7280'}, 'tickcolor': '#374151'},
                    'bar': {'color': colore, 'thickness': 0.25},
                    'bgcolor': '#1F2937', 'borderwidth': 0,
                    'steps': [{'range': [0, 50], 'color': '#1F2937'}, {'range': [50, 75], 'color': '#243547'}, {'range': [75, 100], 'color': '#1E3A5F'}],
                    'threshold': {'line': {'color': '#F59E0B', 'width': 3}, 'thickness': 0.75, 'value': val_ref}
                },
                domain={'x': [col_idx * 0.34, col_idx * 0.34 + 0.30], 'y': [0, 1]},
                visible=visible,
            ))

    buttons_g5 = []
    for anno_ref in anni_ref:
        n_per_anno = len(indicatori_g5)
        vis = []
        for ar in anni_ref:
            vis += [ar == anno_ref] * n_per_anno
        buttons_g5.append(dict(label=f'vs {anno_ref}', method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Profilo laureati L-2 — 2024 vs {anno_ref}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))

    fig5.update_layout(
        title=dict(text='Profilo laureati L-2 — 2024 vs 2020', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.15, yanchor='top',
            buttons=buttons_g5, bgcolor='#1F2937', bordercolor='#3B82F6', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        height=420, margin=dict(t=100, b=60, l=30, r=30),
        font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER,
        annotations=[
            dict(x=0.5, y=-0.12, xref='paper', yref='paper',
                 text='La linea arancione indica il valore dell\'anno di riferimento selezionato',
                 showarrow=False, font=dict(size=11, color='#6B7280'), align='center'),
            fonte_annotation('Fonte: AlmaLaurea — Profilo dei Laureati')
        ]
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # G6 — Magistrale
    chart_header(
        "Destinazione alla magistrale — dove proseguono gli studi",
        "Distribuzione percentuale degli studenti L-2 che si iscrivono alla laurea magistrale, "
        "per destinazione geografica. La quota che sceglie un ateneo del Centro Italia risulta "
        "storicamente contenuta rispetto alla quota che si orienta verso atenei del Nord.",
        "Passa il cursore sulle barre per vedere la percentuale esatta di ciascun segmento. "
        "Le percentuali sono visibili direttamente all'interno delle barre colorate."
    )

    g6 = alma_profilo[['anno','pct_stesso_ateneo_magistrale','pct_magistrale_nord','pct_magistrale_centro']].copy()
    g6['anno'] = g6['anno'].astype(str)
    g6['pct_altro'] = 100 - g6['pct_stesso_ateneo_magistrale'] - g6['pct_magistrale_nord'] - g6['pct_magistrale_centro']

    DEST = {
        'pct_stesso_ateneo_magistrale': ('Stesso ateneo', '#3B82F6'),
        'pct_magistrale_nord':          ('Altro Nord', '#818CF8'),
        'pct_magistrale_centro':        ('Centro Italia', '#F59E0B'),
        'pct_altro':                    ('Estero / Altro', '#374151'),
    }

    fig6 = go.Figure()
    for col, (label, color) in DEST.items():
        fig6.add_trace(go.Bar(x=g6['anno'], y=g6[col], name=label,
            marker=dict(color=color, line=dict(width=0), opacity=0.92),
            hovertemplate=f'<b>{label}</b><br>Anno %{{x}}<br><b>%{{y:.1f}}%</b><extra></extra>'))

    for col, (label, color) in DEST.items():
        if col == 'pct_stesso_ateneo_magistrale':
            y_pos = g6[col] / 2; font_size = 13; font_color = 'white'
        elif col == 'pct_magistrale_nord':
            y_pos = g6['pct_stesso_ateneo_magistrale'] + g6[col] / 2; font_size = 11; font_color = 'white'
        elif col == 'pct_magistrale_centro':
            y_pos = g6['pct_stesso_ateneo_magistrale'] + g6['pct_magistrale_nord'] + g6[col] / 2; font_size = 10; font_color = '#FCD34D'
        else:
            y_pos = g6['pct_stesso_ateneo_magistrale'] + g6['pct_magistrale_nord'] + g6['pct_magistrale_centro'] + g6[col] / 2; font_size = 10; font_color = '#9CA3AF'
        testo = [f"{v:.0f}%" if v > 3 else "" for v in g6[col]]
        fig6.add_trace(go.Scatter(x=g6['anno'], y=y_pos, mode='text', text=testo,
            textfont=dict(size=font_size, color=font_color, family='Inter'), showlegend=False, hoverinfo='skip'))

    media_stesso = g6['pct_stesso_ateneo_magistrale'].mean()
    media_centro = g6['pct_magistrale_centro'].mean()

    fig6.update_layout(
        barmode='stack', **PLOT_LAYOUT, title='',
        xaxis=dict(title=dict(text='Anno di laurea', font=dict(color='#9CA3AF')), showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#374151'),
        yaxis=dict(title=dict(text='%', font=dict(color='#9CA3AF')), range=[0, 100], ticksuffix='%', gridcolor='#1F2937', tickfont=dict(color='#9CA3AF'), linecolor='#374151'),
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center', bgcolor='rgba(0,0,0,0)', font=dict(color='#D1D5DB', size=11)),
        annotations=[
            dict(x=0.5, y=-0.18, xref='paper', yref='paper',
                 text=f"<b style='color:white'>{media_stesso:.1f}%</b><span style='color:#9CA3AF'> resta nello stesso ateneo · </span><b style='color:#F59E0B'>{media_centro:.1f}%</b><span style='color:#9CA3AF'> sceglie un ateneo del Centro Italia</span>",
                 showarrow=False, font=dict(size=12, family='Inter'), align='center'),
            fonte_annotation('Fonte: AlmaLaurea — Profilo dei Laureati')
        ],
        height=540, margin=dict(t=80, b=100, l=60, r=30),
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("---")

    # G7 — Scorecard
    chart_header(
        "Scorecard — indicatori chiave per il sistema L-2",
        "Sintesi degli indicatori principali derivati dall'analisi dei dataset MUR, ANVUR e AlmaLaurea. "
        "Le card in verde indicano indicatori positivi, quelle in arancione segnalano dati da contestualizzare.",
        ""
    )

    kpi_full = [
        {'label': 'Immatricolati puri/anno', 'value': '7.076', 'delta': 'stabile dopo COVID', 'color': '#60A5FA', 'bg': '#1E3A5F'},
        {'label': 'Crescita laureati', 'value': '+54%', 'delta': '2010 → 2024', 'color': '#60A5FA', 'bg': '#1E3A5F'},
        {'label': 'Soddisfatti del corso', 'value': '80.9%', 'delta': '71.5% si reiscriverebbe', 'color': '#34D399', 'bg': '#064E3B'},
        {'label': 'Prosegue magistrale', 'value': '87%', 'delta': 'stabile 2020–2024', 'color': '#34D399', 'bg': '#064E3B'},
        {'label': 'Retribuzione media 2024', 'value': '€896', 'delta': '+31% vs 2020', 'color': '#34D399', 'bg': '#064E3B'},
        {'label': 'Occupazione a 1 anno', 'value': '21.3%', 'delta': '88% fa magistrale', 'color': '#FCD34D', 'bg': '#78350F'},
        {'label': 'Quota Centro Italia', 'value': '27%', 'delta': '11 atenei attivi', 'color': '#FCD34D', 'bg': '#78350F'},
        {'label': 'Atenei telematici L-2', 'value': '0', 'delta': 'corso laboratoriale', 'color': '#34D399', 'bg': '#064E3B'},
    ]

    fig7 = go.Figure()
    col_positions = [0.01, 0.26, 0.51, 0.76]
    row_positions = [0.52, 0.02]
    cell_w = 0.23
    cell_h = 0.44
    shapes = []
    annotations = []

    for idx, k in enumerate(kpi_full):
        r = idx // 4
        c = idx % 4
        x0 = col_positions[c]; x1 = x0 + cell_w
        y0 = row_positions[r]; y1 = y0 + cell_h
        cx = (x0 + x1) / 2

        shapes.append(dict(type='rect', xref='paper', yref='paper',
            x0=x0, x1=x1, y0=y0, y1=y1, fillcolor=k['bg'],
            line=dict(color=k['color'], width=1.5), layer='below'))
        shapes.append(dict(type='rect', xref='paper', yref='paper',
            x0=x0, x1=x1, y0=y1-0.025, y1=y1, fillcolor=k['color'],
            line=dict(width=0), layer='above'))
        annotations.append(dict(x=cx, y=y1-0.048, xref='paper', yref='paper',
            text=f"<b>{k['label']}</b>", showarrow=False,
            font=dict(size=11, color='white', family='Inter'), align='center', xanchor='center'))
        annotations.append(dict(x=cx, y=(y0+y1)/2+0.04, xref='paper', yref='paper',
            text=f"<b>{k['value']}</b>", showarrow=False,
            font=dict(size=30, color=k['color'], family='Inter'), align='center', xanchor='center'))
        annotations.append(dict(x=cx, y=y0+0.055, xref='paper', yref='paper',
            text=k['delta'], showarrow=False,
            font=dict(size=10, color='#9CA3AF', family='Inter'), align='center', xanchor='center'))

    fig7.update_layout(
        title=dict(text='Scorecard L-2 Biotecnologie', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        shapes=shapes, annotations=annotations, height=600,
        margin=dict(t=80, b=40, l=20, r=20),
        paper_bgcolor=BG_PAPER, plot_bgcolor=BG_PAPER,
        xaxis=dict(visible=False, range=[0,1]), yaxis=dict(visible=False, range=[0,1]),
    )
    st.plotly_chart(fig7, use_container_width=True)

# ─────────────────────────────────────────────
# SEZIONE: PERCORSO ACCADEMICO
# ─────────────────────────────────────────────
elif sezione == "Percorso Accademico":
    st.markdown("## Percorso Accademico")
    st.markdown("---")

    # G11 — Donut destino studenti
    chart_header(
        "Cosa succede dopo il primo anno — L-2 Biotecnologie",
        "Il grafico mostra la distribuzione degli immatricolati puri L-2 al termine del primo anno, "
        "suddivisi in tre categorie: chi prosegue nello stesso corso (iC14 ANVUR), chi cambia corso "
        "o ateneo ma resta nel sistema universitario (differenza iC21-iC14), e chi lascia l'università "
        "(complemento a 1 di iC21). La distinzione è importante: la maggior parte di chi non prosegue "
        "nello stesso corso non abbandona l'università, ma si trasferisce altrove.",
        "Seleziona l'anno con i pulsanti per vedere l'evoluzione nel tempo. "
        "Passa il cursore sui segmenti per vedere le percentuali esatte."
    )

    ic14 = df_ava2[df_ava2['CODICE'] == 'iC14'].copy()
    ic21 = df_ava2[df_ava2['CODICE'] == 'iC21'].copy()
    for df_ind in [ic14, ic21]:
        df_ind['ind_float'] = (df_ind['INDICATORE'].astype(str).str.strip()
            .str.replace(',', '.').str.replace(' ', '')
            .apply(lambda x: float(x) if x not in ['', 'nan', 'None'] else None))

    ic14_naz = ic14.groupby('ID_ANNO_ACCADEMICO')['ind_float'].mean().reset_index()
    ic14_naz.columns = ['anno', 'ic14']
    ic21_naz = ic21.groupby('ID_ANNO_ACCADEMICO')['ind_float'].mean().reset_index()
    ic21_naz.columns = ['anno', 'ic21']

    df_destino = ic14_naz.merge(ic21_naz, on='anno')
    df_destino['prosegue_stesso'] = (df_destino['ic14'] * 100).round(1)
    df_destino['cambia_corso']    = ((df_destino['ic21'] - df_destino['ic14']) * 100).round(1)
    df_destino['abbandona']       = ((1 - df_destino['ic21']) * 100).round(1)
    df_destino['anno'] = df_destino['anno'].astype(str)
    anni_g11 = sorted(df_destino['anno'].unique())

    fig11 = go.Figure()
    for i, anno in enumerate(anni_g11):
        row = df_destino[df_destino['anno'] == anno].iloc[0]
        fig11.add_trace(go.Pie(
            labels=['Proseguono nello stesso corso', 'Cambiano corso o ateneo', "Lasciano l'università"],
            values=[row['prosegue_stesso'], row['cambia_corso'], row['abbandona']],
            hole=0.60,
            marker=dict(colors=['#3B82F6', '#F59E0B', '#EF4444'], line=dict(color='#0F172A', width=3)),
            textinfo='percent', textposition='outside',
            textfont=dict(size=13, color='white', family='Inter'),
            hovertemplate='<b>%{label}</b><br><b>%{value:.1f}%</b> degli immatricolati<extra></extra>',
            visible=(i == 0), sort=False, pull=[0.03, 0.03, 0.03],
        ))

    buttons_g11 = []
    for i, anno in enumerate(anni_g11):
        row = df_destino[df_destino['anno'] == anno].iloc[0]
        vis = [j == i for j in range(len(anni_g11))]
        buttons_g11.append(dict(label=anno, method='update',
            args=[{'visible': vis}, {
                'title': dict(text=f"Cosa succede dopo il primo anno — {anno}", font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
                'annotations': [
                    dict(text=f"<b>{row['prosegue_stesso']:.1f}%</b><br><span style='color:#9CA3AF;font-size:11px'>resta nello<br>stesso corso</span>",
                         x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False,
                         font=dict(size=24, color='white', family='Inter'), align='center'),
                    dict(x=0.99, y=-0.12, xref='paper', yref='paper',
                         text='Fonte: ANVUR iC14 + iC21 · Media nazionale corsi L-2',
                         showarrow=False, font=dict(size=10, color='#6B7280'), align='right', xanchor='right')
                ]
            }]))

    row0 = df_destino[df_destino['anno'] == anni_g11[0]].iloc[0]
    fig11.update_layout(
        title=dict(text=f"Cosa succede dopo il primo anno — {anni_g11[0]}", font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.12, yanchor='top',
            buttons=buttons_g11, bgcolor='#1F2937', bordercolor='#3B82F6', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[
            dict(text=f"<b>{row0['prosegue_stesso']:.1f}%</b><br><span style='color:#9CA3AF;font-size:11px'>resta nello<br>stesso corso</span>",
                 x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False,
                 font=dict(size=24, color='white', family='Inter'), align='center'),
            dict(x=0.99, y=-0.12, xref='paper', yref='paper',
                 text='Fonte: ANVUR iC14 + iC21 · Media nazionale corsi L-2',
                 showarrow=False, font=dict(size=10, color='#6B7280'), align='right', xanchor='right')
        ],
        height=580, margin=dict(t=120, b=80, l=80, r=80),
        font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER,
        showlegend=True,
        legend=dict(font=dict(color='#D1D5DB', size=12), bgcolor='rgba(0,0,0,0)',
                    orientation='h', x=0.5, xanchor='center', y=-0.08)
    )
    st.plotly_chart(fig11, use_container_width=True)

# ─────────────────────────────────────────────
# SEZIONE: VARIANTI DEL CORSO
# ─────────────────────────────────────────────
elif sezione == "Varianti del Corso":
    st.markdown("## Varianti del Corso")
    st.markdown("---")

    # G8 — Treemap
    chart_header(
        "Distribuzione immatricolati per variante di denominazione L-2",
        "Il treemap mostra le 16 varianti di denominazione dei corsi L-2 in Italia, con dimensione "
        "proporzionale al numero di immatricolati e colore che indica il numero di atenei che "
        "offrono ciascuna variante. La denominazione 'Biotecnologie' è di gran lunga la più diffusa.",
        "Seleziona l'anno con i pulsanti. Passa il cursore sui rettangoli per vedere immatricolati e numero di atenei."
    )

    df_var = df_anvur[df_anvur['Anno accademico'] >= 2019].copy()
    df_var['corso_nome'] = df_var['corso_nome'].str.title().str.strip()
    anni_tree = sorted(df_var['Anno accademico'].unique())

    fig8b = go.Figure()
    for i, anno in enumerate(anni_tree):
        subset = df_var[df_var['Anno accademico'] == anno].groupby('corso_nome').agg(
            imm=('imm', 'sum'), n_atenei=('ateneo_short', 'nunique')).reset_index()
        fig8b.add_trace(go.Treemap(
            labels=subset['corso_nome'], parents=['L-2 Biotecnologie'] * len(subset),
            values=subset['imm'], customdata=subset[['n_atenei', 'imm']],
            hovertemplate='<b>%{label}</b><br>Immatricolati: <b>%{customdata[1]:,.0f}</b><br>N° atenei: <b>%{customdata[0]}</b><extra></extra>',
            marker=dict(
                colorscale=[[0.0,'#1E3A5F'],[0.4,'#2563EB'],[0.7,'#60A5FA'],[1.0,'#BAE6FD']],
                colors=subset['n_atenei'],
                colorbar=dict(title=dict(text='N° atenei', font=dict(color='#9CA3AF')), tickfont=dict(color='#9CA3AF')),
                showscale=True, line=dict(color='#0F172A', width=2),
            ),
            textfont=dict(size=13, color='white', family='Inter'),
            visible=(i == 0),
        ))

    buttons_g8 = []
    for i, anno in enumerate(anni_tree):
        vis = [j == i for j in range(len(anni_tree))]
        buttons_g8.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Varianti L-2 per immatricolati — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))

    fig8b.update_layout(
        title=dict(text=f'Varianti L-2 per immatricolati — {anni_tree[0]}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.10, yanchor='top',
            buttons=buttons_g8, bgcolor='#1F2937', bordercolor='#3B82F6', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto · Colore = n° atenei che offrono la variante')],
        height=580, margin=dict(t=120, b=60, l=20, r=20),
        font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER,
    )
    st.plotly_chart(fig8b, use_container_width=True)

    st.markdown("---")

    # G12 — Barchart varianti prosecuzione
    chart_header(
        "Tasso di prosecuzione al II anno per variante — confronto con Biotecnologie",
        "Il grafico confronta il tasso medio di prosecuzione al II anno (indicatore ANVUR iC14) "
        "per ciascuna variante di denominazione L-2, usando 'Biotecnologie' come baseline (linea tratteggiata). "
        "Le barre verdi indicano varianti con prosecuzione superiore alla baseline, quelle rosse inferiore. "
        "Il numero tra parentesi indica quanti atenei offrono quella variante: le varianti con 1-2 atenei "
        "sono meno rappresentative statisticamente.",
        "Passa il cursore sulle barre per vedere il tasso di abbandono e il numero di atenei."
    )

    ic14_g12 = df_ava2[df_ava2['CODICE'] == 'iC14'].copy()
    ic14_g12['ind_float'] = (ic14_g12['INDICATORE'].astype(str).str.strip()
        .str.replace(',', '.').str.replace(' ', '')
        .apply(lambda x: float(x) if x not in ['', 'nan', 'None'] else None))
    ic14_g12['corso_norm'] = ic14_g12['NOME_CORSO'].str.title().str.strip()
    ic14_g12['corso_norm'] = ic14_g12['corso_norm'].str.replace('Biotecnologia$', 'Biotecnologie', regex=True)

    ic14_var = ic14_g12.groupby('corso_norm')['ind_float'].mean().reset_index()
    ic14_var.columns = ['corso', 'prosecuzione']
    ic14_var['prosecuzione_pct'] = (ic14_var['prosecuzione'] * 100).round(1)
    ic14_var['abbandono'] = (100 - ic14_var['prosecuzione_pct']).round(1)
    ic14_atenei = ic14_g12.groupby('corso_norm')['CODE_UN'].nunique().reset_index()
    ic14_atenei.columns = ['corso', 'n_atenei']
    ic14_var = ic14_var.merge(ic14_atenei, on='corso')
    baseline = ic14_var[ic14_var['corso'] == 'Biotecnologie']['prosecuzione_pct'].values[0]
    ic14_var_sorted = ic14_var.sort_values('prosecuzione_pct', ascending=True).reset_index(drop=True)

    def get_colore_g12(row):
        if row['corso'] == 'Biotecnologie': return '#6B7280'
        elif row['prosecuzione_pct'] > baseline: return '#34D399'
        else: return '#EF4444'

    ic14_var_sorted['colore'] = ic14_var_sorted.apply(get_colore_g12, axis=1)

    fig12 = go.Figure()
    fig12.add_trace(go.Bar(
        x=ic14_var_sorted['prosecuzione_pct'], y=ic14_var_sorted['corso'],
        orientation='h',
        marker=dict(color=ic14_var_sorted['colore'], line=dict(width=0), opacity=0.9),
        text=ic14_var_sorted.apply(lambda r: f"{r['prosecuzione_pct']:.1f}%  ({r['n_atenei']} aten{'eo' if r['n_atenei']==1 else 'ei'})", axis=1),
        textposition='outside', textfont=dict(size=10, color='#D1D5DB'),
        hovertemplate='<b>%{y}</b><br>Prosecuzione: <b>%{x:.1f}%</b><br>Abbandono: <b>%{customdata[0]:.1f}%</b><br>N° atenei: <b>%{customdata[1]}</b><extra></extra>',
        customdata=list(zip(ic14_var_sorted['abbandono'], ic14_var_sorted['n_atenei'])),
    ))
    fig12.add_vline(x=baseline, line=dict(color='#6B7280', width=2, dash='dash'))
    fig12.update_layout(
        **PLOT_LAYOUT, title='',
        annotations=[
            dict(x=baseline, y=1.02, xref='x', yref='paper',
                 text=f'Baseline: {baseline:.1f}%', showarrow=False,
                 font=dict(size=10, color='#9CA3AF'), align='center'),
            fonte_annotation('Fonte: ANVUR iC14 · Verde = prosecuzione maggiore · Rosso = minore')
        ],
        xaxis=dict(title=dict(text='% prosecuzione al II anno', font=dict(color='#9CA3AF')),
                   showgrid=False, ticksuffix='%', tickfont=dict(color='#9CA3AF'), linecolor='#374151', range=[0, 110]),
        yaxis=dict(showgrid=False, tickfont=dict(size=10, color='#D1D5DB'), linecolor='#374151'),
        height=580, margin=dict(t=80, b=80, l=300, r=120),
    )
    st.plotly_chart(fig12, use_container_width=True)

# ─────────────────────────────────────────────
# SEZIONE: ANALISI AVANZATA
# ─────────────────────────────────────────────
elif sezione == "Analisi Avanzata":
    st.markdown("## Analisi Avanzata")
    st.markdown("---")

    chart_header(
        "Correlazione tra dimensione del corso e tasso di prosecuzione",
        "L'analisi mette in relazione il numero medio di immatricolati puri per corso (2020–2023) "
        "con il tasso di prosecuzione al II anno (iC14 ANVUR). Ogni punto rappresenta un singolo "
        "corso presso un ateneo. La linea tratteggiata mostra il trend di regressione lineare. "
        "Una correlazione negativa (r = -0.32) indica che i corsi più grandi tendono ad avere "
        "tassi di prosecuzione più bassi, con una relazione statisticamente significativa (p = 0.025).",
        "Passa il cursore sui punti per vedere il nome del corso e dell'ateneo. "
        "Il colore identifica la macro area geografica."
    )

    # Preparazione dati
    df_anvur_c = df_anvur.copy()
    df_anvur_c['CODICIONE'] = df_anvur_c['Nome Corso'].str.split(' - ').str[0].str.strip()
    lookup_c = df_anvur_c[['CODICIONE', 'ateneo_short']].drop_duplicates('CODICIONE')
    lookup_c['CODICIONE'] = lookup_c['CODICIONE'].astype(str)

    ic14_c = df_ava2[df_ava2['CODICE'] == 'iC14'].copy()
    ic14_c['ind_float'] = (ic14_c['INDICATORE'].astype(str).str.strip()
        .str.replace(',', '.').str.replace(' ', '')
        .apply(lambda x: float(x) if x not in ['', 'nan', 'None'] else None))

    imm_corso_c = df_ava2[(df_ava2['CODICE'] == 'iC00b') & (df_ava2['ID_ANNO_ACCADEMICO'] >= 2020)].copy()
    imm_corso_c['imm_val'] = (imm_corso_c['NUMERATORE'].astype(str).str.strip()
        .str.replace(',', '').str.replace('.000', '')
        .apply(lambda x: float(x) if x not in ['', 'nan', 'None'] else None))

    imm_media_c = imm_corso_c.groupby('CODICIONE')['imm_val'].mean().reset_index().rename(columns={'imm_val': 'imm_media'})
    imm_media_c['CODICIONE'] = imm_media_c['CODICIONE'].astype(str)

    ic14_corso_c = ic14_c.groupby('CODICIONE')['ind_float'].mean().reset_index()
    ic14_corso_c.columns = ['CODICIONE', 'prosecuzione']
    ic14_corso_c['prosecuzione_pct'] = (ic14_corso_c['prosecuzione'] * 100).round(1)
    ic14_corso_c['CODICIONE'] = ic14_corso_c['CODICIONE'].astype(str)

    df_corr_c = imm_media_c.merge(ic14_corso_c, on='CODICIONE', how='inner')
    df_ava2_meta = df_ava2[['CODICIONE', 'NOME_CORSO', 'ID_REGIONE_MACRO_ISTAT', 'COMUNE']].drop_duplicates('CODICIONE').copy()
    df_ava2_meta['CODICIONE'] = df_ava2_meta['CODICIONE'].astype(str)
    df_corr_c = df_corr_c.merge(df_ava2_meta, on='CODICIONE', how='left')
    df_corr_c = df_corr_c.merge(lookup_c, on='CODICIONE', how='left')

    df_corr_c['macro'] = df_corr_c['ID_REGIONE_MACRO_ISTAT'].map({1: 'Nord', 2: 'Nord', 3: 'Centro', 4: 'Sud e Isole'})
    df_corr_c['nome_display'] = (df_corr_c['NOME_CORSO'].str.title().str.strip() + ' — ' + df_corr_c['ateneo_short'].fillna(df_corr_c['COMUNE'].str.title()))

    df_plot_c = df_corr_c.dropna(subset=['imm_media', 'prosecuzione_pct', 'macro']).copy()

    slope, intercept, r, p, se = stats.linregress(df_plot_c['imm_media'], df_plot_c['prosecuzione_pct'])
    x_line = [df_plot_c['imm_media'].min(), df_plot_c['imm_media'].max()]
    y_line = [slope * x + intercept for x in x_line]

    COLORI_MACRO4 = {'Nord': '#3B82F6', 'Centro': '#F59E0B', 'Sud e Isole': '#34D399'}

    fig_corr = go.Figure()
    for macro, colore in COLORI_MACRO4.items():
        sub = df_plot_c[df_plot_c['macro'] == macro]
        fig_corr.add_trace(go.Scatter(
            x=sub['imm_media'], y=sub['prosecuzione_pct'],
            mode='markers', name=macro,
            marker=dict(color=colore, size=10, opacity=0.85, line=dict(color='#0F172A', width=1.5)),
            hovertemplate='<b>%{customdata}</b><br>Immatricolati medi: <b>%{x:.0f}</b><br>Prosecuzione: <b>%{y:.1f}%</b><extra></extra>',
            customdata=sub['nome_display'].values,
        ))
    fig_corr.add_trace(go.Scatter(
        x=x_line, y=y_line, mode='lines', name='Trend',
        line=dict(color='#9CA3AF', width=1.5, dash='dash'), hoverinfo='skip'
    ))

    fig_corr.update_layout(
        **PLOT_LAYOUT, title='',
        annotations=[
            dict(x=0.98, y=0.98, xref='paper', yref='paper',
                 text=f'r = {r:.3f} · p = {p:.3f} · n = {len(df_plot_c)}',
                 showarrow=False, font=dict(size=12, color='#9CA3AF'),
                 align='right', xanchor='right', bgcolor='#1F2937', bordercolor='#374151', borderwidth=1),
            fonte_annotation('Fonte: ANVUR iC00b + iC14 · Ogni punto = un corso presso un ateneo')
        ],
        xaxis=dict(title=dict(text='Immatricolati medi per anno (2020–2023)', font=dict(color='#9CA3AF')),
                   showgrid=True, gridcolor='#1F2937', tickfont=dict(color='#9CA3AF'), linecolor='#374151'),
        yaxis=dict(title=dict(text='Tasso prosecuzione al II anno (%)', font=dict(color='#9CA3AF')),
                   showgrid=True, gridcolor='#1F2937', ticksuffix='%', tickfont=dict(color='#9CA3AF'), linecolor='#374151'),
        legend=dict(font=dict(color='#D1D5DB'), bgcolor='rgba(0,0,0,0)', x=0.01, y=0.01),
        height=540, margin=dict(t=80, b=80, l=70, r=30),
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")
    st.markdown("### Nota metodologica")
    st.markdown("""
    <p>
    La correlazione di Pearson (r = -0.32, p = 0.025, n = 49) indica una relazione negativa moderata 
    e statisticamente significativa tra la dimensione del corso e il tasso di prosecuzione al II anno. 
    L'analisi è basata su dati ANVUR aggregati per corso e ateneo nel periodo 2020–2023. 
    La relazione osservata non implica causalità e può essere influenzata da fattori strutturali 
    quali la presenza di numero programmato, le caratteristiche del bacino di utenza locale 
    e le politiche di tutoraggio degli atenei.
    </p>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEZIONE: SINTESI
# ─────────────────────────────────────────────
elif sezione == "Sintesi":
    st.markdown("# Sintesi dell'Analisi")
    st.markdown("---")

    st.markdown("""
    <p>
    Questa sezione raccoglie i risultati principali dell'analisi nazionale del Corso di Laurea
    in Biotecnologie (Classe L-2), condotta su dati ufficiali MUR-USTAT, ANVUR e AlmaLaurea
    relativi al periodo 2010–2025.
    </p>
    """, unsafe_allow_html=True)

    # ── Domanda e offerta ────────────────────────────────────────────────────
    st.markdown("## 1. Domanda e offerta formativa")
    st.markdown("""
    <div class="section-card">
    <p>
    In Italia sono <b style="color:#F5F5F7">43 gli atenei</b> che offrono corsi afferenti alla classe L-2 Biotecnologie,
    distribuiti in tutte le macro aree geografiche. <b style="color:#F5F5F7">Nessun ateneo telematico</b> è presente
    nell'offerta L-2: la natura laboratoriale del corso lo rende strutturalmente incompatibile
    con la modalità a distanza.
    </p>
    <p>
    Il numero di <b style="color:#3B82F6">immatricolati puri</b> si attesta intorno alle <b style="color:#F5F5F7">7.076 unità</b>
    nell'anno accademico 2024/25, un valore sostanzialmente stabile rispetto al periodo
    pre-pandemia dopo il calo registrato negli anni 2020/21 e 2021/22. Il picco storico
    è stato raggiunto nel 2018/19.
    </p>
    <p>
    I <b style="color:#3B82F6">laureati</b> sono cresciuti del <b style="color:#F5F5F7">+54%</b> tra il 2010 e il 2024,
    con un tasso di completamento medio del <b style="color:#F5F5F7">45.9%</b> calcolato confrontando
    immatricolati e laureati a distanza di tre anni.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Geografia ────────────────────────────────────────────────────────────
    st.markdown("## 2. Distribuzione geografica")
    st.markdown("""
    <div class="section-card">
    <p>
    Il <b style="color:#3B82F6">Nord Italia</b> concentra la quota maggiore di immatricolati,
    attestandosi stabilmente attorno al <b style="color:#F5F5F7">50–55%</b> del totale nazionale.
    Il <b style="color:#F59E0B">Centro Italia</b> conta <b style="color:#F5F5F7">11 atenei attivi</b>
    e una quota di circa il <b style="color:#F5F5F7">27%</b> degli immatricolati.
    L'<b style="color:#34D399">Ateneo di Perugia</b> è il più grande del Centro con circa 400 immatricolati puri l'anno,
    seguito dagli atenei laziali (La Sapienza, Tor Vergata, Tuscia).
    </p>
    <p>
    Le regioni <b style="color:#F5F5F7">Molise</b> e <b style="color:#F5F5F7">Valle d'Aosta</b>
    non ospitano atenei con corsi L-2 attivi.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Profilo studenti ─────────────────────────────────────────────────────
    st.markdown("## 3. Profilo e soddisfazione degli studenti")
    st.markdown("""
    <div class="section-card">
    <p>
    Secondo i dati <b style="color:#F5F5F7">AlmaLaurea</b>, l'<b style="color:#34D399">80.9%</b>
    dei laureati L-2 si dichiara soddisfatto del corso di studi, con il
    <b style="color:#34D399">71.5%</b> che si reiscriverebbe allo stesso corso nello stesso ateneo.
    </p>
    <p>
    La <b style="color:#3B82F6">prosecuzione alla laurea magistrale</b> è molto elevata:
    l'<b style="color:#F5F5F7">87%</b> dei laureati L-2 si iscrive a un corso magistrale entro un anno.
    Di questi, la quota che sceglie un ateneo del <b style="color:#F59E0B">Centro Italia</b>
    per la magistrale si attesta attorno al <b style="color:#F5F5F7">8–10%</b>, significativamente
    inferiore alla quota di chi resta nello stesso ateneo (circa il <b style="color:#F5F5F7">55%</b>)
    o sceglie un ateneo del Nord.
    </p>
    <p>
    La <b style="color:#FCD34D">retribuzione media</b> a un anno dalla laurea è di
    <b style="color:#F5F5F7">€896</b> mensili (2024), con un incremento del
    <b style="color:#34D399">+31%</b> rispetto al 2020, riflettendo però il fatto che
    l'<b style="color:#F5F5F7">88%</b> dei laureati L-2 prosegue con la magistrale
    e quindi la quota occupata a breve termine è limitata (<b style="color:#F5F5F7">21.3%</b>).
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Percorso accademico ───────────────────────────────────────────────────
    st.markdown("## 4. Percorso accademico e abbandoni")
    st.markdown("""
    <div class="section-card">
    <p>
    Gli indicatori ANVUR AVA2 mostrano che, in media, il
    <b style="color:#3B82F6">54%</b> degli immatricolati puri L-2 prosegue
    <b style="color:#F5F5F7">nello stesso corso</b> al secondo anno (indicatore <b>iC14</b>).
    Un ulteriore <b style="color:#F59E0B">33%</b> si trasferisce ad altro corso o ateneo
    rimanendo nel sistema universitario (differenza <b>iC21–iC14</b>).
    Solo il <b style="color:#EF4444">13%</b> abbandona definitivamente l'università
    (complemento a 1 di <b>iC21</b>).
    </p>
    <p>
    Questo dato è metodologicamente rilevante: il tasso di abbandono
    <b style="color:#F5F5F7">reale è molto inferiore</b> a quello che si otterrebbe
    considerando solo chi non prosegue nello stesso corso.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Varianti e analisi avanzata ───────────────────────────────────────────
    st.markdown("## 5. Varianti del corso e analisi statistica")
    st.markdown("""
    <div class="section-card">
    <p>
    Il sistema L-2 presenta <b style="color:#F5F5F7">16 varianti</b> di denominazione.
    La denominazione <b style="color:#3B82F6">Biotecnologie</b> è di gran lunga la più diffusa
    (oltre il 70% degli immatricolati), seguita da <i>Biotecnologia</i>,
    <i>Biotecnologie Industriali</i> e <i>Biotecnologie Mediche</i>.
    </p>
    <p>
    L'analisi di correlazione tra dimensione del corso e tasso di prosecuzione al secondo anno
    mostra una <b style="color:#EF4444">relazione negativa moderata</b>
    (<b style="color:#F5F5F7">r = −0.32, p = 0.025, n = 49</b>):
    i corsi con più immatricolati tendono ad avere tassi di prosecuzione leggermente inferiori.
    La relazione è statisticamente significativa ma di entità contenuta,
    e non implica causalità — fattori strutturali come il numero programmato
    e le politiche di tutoraggio dei singoli atenei giocano un ruolo rilevante.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Conclusioni ───────────────────────────────────────────────────────────
    st.markdown("## 6. Considerazioni conclusive")
    st.markdown("""
    <div class="section-card" style="border-top: 3px solid #3B82F6;">
    <p>
    Il sistema L-2 Biotecnologie presenta caratteristiche di <b style="color:#34D399">solidità strutturale</b>:
    domanda stabile, elevata soddisfazione degli studenti, quasi assenza di abbandono definitivo
    e fortissima propensione alla prosecuzione magistrale. L'assenza di atenei telematici
    garantisce una qualità formativa omogenea legata alla componente laboratoriale.
    </p>
    <p>
    Le principali <b style="color:#F59E0B">aree di attenzione</b> riguardano:
    la <b style="color:#F5F5F7">quota di trasferimenti</b> verso altri corsi al primo anno (33%),
    che suggerisce un possibile disallineamento tra aspettative e contenuti del corso;
    la <b style="color:#F5F5F7">bassa quota di laureati L-2 che sceglie atenei del Centro</b>
    per la magistrale, che può limitare il bacino di reclutamento locale;
    e la <b style="color:#F5F5F7">frammentazione in 16 varianti</b> di denominazione,
    che riduce la riconoscibilità del titolo a livello nazionale.
    </p>
    <p style="color:#48484A; font-size:0.82rem; margin-top:1.5rem;">
    Analisi basata su dati MUR-USTAT, ANVUR AVA2 e AlmaLaurea · Periodo di riferimento: 2010–2025 ·
    Elaborazione: Ufficio Analisi Istituzionale
    </p>
    </div>
    """, unsafe_allow_html=True)
