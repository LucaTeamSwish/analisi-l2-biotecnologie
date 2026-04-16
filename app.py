import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import os
import warnings

# ⚠️ Durante debug meglio NON silenziare tutto

# warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────

# CONFIG PAGINA (DEVE essere la prima chiamata Streamlit)

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

def load_css():
st.markdown(""" <style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

```
:root {
    --bg-primary: #0A0A0F;
    --bg-secondary: #111118;
    --bg-card: #16161E;
    --border: rgba(255,255,255,0.06);
    --text-primary: #F5F5F7;
    --text-secondary: #86868B;
    --text-tertiary: #48484A;
    --accent-blue: #3B82F6;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="block-container"] {
    padding: 2rem 3rem !important;
    max-width: 1400px !important;
}

h1 {
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
}

h2 {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}

p {
    color: var(--text-secondary) !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}

.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}

.stButton > button {
    background: var(--accent-blue) !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

/* Nascondi elementi Streamlit */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)
```

load_css()

# ─────────────────────────────────────────────

# PASSWORD (VERSIONE PIÙ SICURA)

# ─────────────────────────────────────────────

def check_password():
if "authenticated" not in st.session_state:
st.session_state.authenticated = False

```
if st.session_state.authenticated:
    return True

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-bottom: 2rem;'>
        <div style='font-size:2.3rem; font-weight:700; letter-spacing:-0.04em;'>
            Analisi Nazionale<br>L-2 Biotecnologie
        </div>
        <div style='color:#86868B; margin-top:0.75rem; font-size:0.95rem;'>
            Accesso riservato
        </div>
    </div>
    """, unsafe_allow_html=True)

    pwd = st.text_input(
        "Password",
        type="password",
        label_visibility="collapsed",
        placeholder="Inserisci il codice"
    )

    if st.button("Accedi", use_container_width=True):
        # 🔐 Usa secrets se disponibili
        correct_pwd = st.secrets.get("password", "L2")

        if pwd == correct_pwd:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Codice non valido")

return False
```

if not check_password():
st.stop()
# ─────────────────────────────────────────────

# COSTANTI GRAFICI (FIX BUG xaxis/yaxis)

# ─────────────────────────────────────────────

GEOJSON_URL = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
GRIGIO_SCURO = ["Valle d'Aosta/Vallée d'Aoste", 'Molise']

COLORI_MACRO = {
'Nord': '#3B82F6',
'Centro': '#F59E0B',
'Sud': '#34D399',
'Isole': '#818CF8'
}

BG_PLOT = '#0F172A'
BG_PAPER = '#0A0A0F'

# 🔹 BASE LAYOUT (senza xaxis/yaxis!)

BASE_LAYOUT = dict(
font=dict(family='Inter', size=12),
plot_bgcolor=BG_PLOT,
paper_bgcolor=BG_PAPER,
title_font=dict(size=18, color='white', family='Inter'),
legend=dict(font=dict(color='#D1D5DB'), bgcolor='rgba(0,0,0,0)')
)

# 🔹 DEFAULT ASSI (riutilizzabili ma separati)

X_AXIS_DEFAULT = dict(
showgrid=False,
tickfont=dict(color='#9CA3AF'),
linecolor='#374151'
)

Y_AXIS_DEFAULT = dict(
gridcolor='#1F2937',
tickfont=dict(color='#9CA3AF'),
linecolor='#374151'
)

def apply_layout(fig, **kwargs):
"""
Applica layout senza conflitti tra parametri duplicati
"""
layout = dict(BASE_LAYOUT)

```
# merge sicuro
layout.update(kwargs)

fig.update_layout(**layout)
return fig
```

def fonte_annotation(testo):
return dict(
x=0.99, y=-0.13,
xref='paper', yref='paper',
text=testo,
showarrow=False,
font=dict(size=10, color='#6B7280'),
align='right',
xanchor='right'
)

def chart_header(titolo, descrizione, istruzioni):
st.markdown(f"### {titolo}")
st.markdown(f'<p class="chart-description">{descrizione}</p>', unsafe_allow_html=True)
st.markdown(f'<div class="chart-instructions">{istruzioni}</div>', unsafe_allow_html=True)
# ─────────────────────────────────────────────

# SEZIONE: DOMANDA NAZIONALE

# ─────────────────────────────────────────────

elif sezione == "Domanda Nazionale":
st.markdown("## Domanda Nazionale")
st.markdown("---")

```
# G1 — Immatricolati
chart_header(
    "Immatricolati puri L-2 — Italia (2010–2025)",
    "Il grafico riporta il numero di studenti che si iscrivono per la prima volta a un corso L-2 "
    "Biotecnologie in Italia, per anno accademico.",
    "Passa il cursore sui punti per vedere il valore e la variazione percentuale."
)

y_2019 = imm_naz[imm_naz['anno_short'] == '2019/20']['Imm'].values[0]
y_2020 = imm_naz[imm_naz['anno_short'] == '2020/21']['Imm'].values[0]

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=imm_naz['anno_short'],
    y=imm_naz['Imm'],
    mode='none',
    fill='tozeroy',
    fillcolor='rgba(59,130,246,0.08)',
    showlegend=False
))

fig1.add_trace(go.Scatter(
    x=['2019/20', '2020/21', '2020/21', '2019/20'],
    y=[y_2019, y_2020, 0, 0],
    fill='toself',
    fillcolor='rgba(239,68,68,0.12)',
    line=dict(color='rgba(0,0,0,0)'),
    showlegend=False
))

fig1.add_trace(go.Scatter(
    x=imm_naz['anno_short'],
    y=imm_naz['Imm'],
    mode='lines+markers',
    line=dict(color='#60A5FA', width=2.5),
    marker=dict(size=7),
    customdata=imm_naz[['delta']].round(1),
    hovertemplate='<b>%{x}</b><br>Immatricolati: %{y:,}<br>Δ %{customdata[0]:+.1f}%<extra></extra>',
    showlegend=False
))

# Layout FIX
layout = dict(PLOT_LAYOUT)
layout.update({
    "title": "",
    "xaxis": dict(
        tickangle=-45,
        showgrid=False,
        tickfont=dict(color='#9CA3AF'),
        linecolor='#374151'
    ),
    "yaxis": dict(
        gridcolor='#1F2937',
        tickfont=dict(color='#9CA3AF'),
        linecolor='#374151',
        rangemode='tozero'
    )
})

fig1.update_layout(**layout)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# G2 — Laureati
chart_header(
    "Laureati L-2 — Italia (2010–2024)",
    "Numero totale di laureati per anno.",
    "Passa il cursore per vedere i valori."
)

fig2 = px.bar(
    lau_naz,
    x='AnnoS',
    y='Lau',
    color='COVID',
    color_discrete_map={True: '#EF4444', False: '#3B82F6'},
    text='Lau'
)

fig2.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

# Layout FIX
layout2 = dict(PLOT_LAYOUT)
layout2.update({
    "title": "",
    "showlegend": False,
    "xaxis": dict(
        tickangle=-45,
        showgrid=False,
        tickfont=dict(color='#9CA3AF'),
        tickmode='linear',
        dtick=1,
        linecolor='#374151'
    ),
    "yaxis": dict(
        gridcolor='#1F2937',
        tickfont=dict(color='#9CA3AF'),
        rangemode='tozero',
        linecolor='#374151'
    )
})

fig2.update_layout(**layout2)

st.plotly_chart(fig2, use_container_width=True)
```
# ─────────────────────────────────────────────

# SEZIONE: GEOGRAFIA (FIX LAYOUT STABILE)

# ─────────────────────────────────────────────

elif sezione == "Geografia":
st.markdown("## Geografia")
st.markdown("---")

```
# 🔹 FUNZIONE LAYOUT SICURO (IMPORTANTE)
def apply_layout(fig, **kwargs):
    layout = dict(PLOT_LAYOUT)
    layout.update(kwargs)
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────
# G3 — MAPPA
# ─────────────────────────────
chart_header(
    "Immatricolati puri L-2 per regione",
    "Distribuzione regionale 2020–2024 (ANVUR Cruscotto).",
    "Seleziona anno e passa sulla mappa."
)

anno1_fil = df_anvur[(df_anvur['Anno accademico'] >= 2020) & (df_anvur['regione'].notna())].copy()

df_mappa = anno1_fil.groupby(['Anno accademico', 'regione'])['imm'].sum().reset_index()
df_hover_m = anno1_fil.groupby(['Anno accademico', 'regione', 'ateneo_short', 'corso_nome'])['imm'].sum().reset_index()

def crea_hover_m(regione, anno):
    subset = df_hover_m[(df_hover_m['regione'] == regione) & (df_hover_m['Anno accademico'] == anno)]
    totale = int(subset['imm'].sum())
    txt = f"<b>{regione}</b><br>Anno: {anno}<br>Totale: <b>{totale:,}</b><br><br>"
    for _, r in subset.sort_values('imm', ascending=False).iterrows():
        txt += f"{r['ateneo_short']} — {r['corso_nome']}: {int(r['imm']):,}<br>"
    return txt

df_mappa['hover'] = df_mappa.apply(lambda r: crea_hover_m(r['regione'], r['Anno accademico']), axis=1)

anni_mappa = sorted(df_mappa['Anno accademico'].unique())
z_min, z_max = df_mappa['immatricolati'].min(), df_mappa['immatricolati'].max()

fig3 = go.Figure()

for i, anno in enumerate(anni_mappa):
    subset = df_mappa[df_mappa['Anno accademico'] == anno]

    fig3.add_trace(go.Choropleth(
        geojson=GEOJSON_URL,
        locations=subset['regione'],
        featureidkey='properties.reg_name',
        z=subset['immatricolati'],
        colorscale=[[0,'#1E3A5F'],[1,'#60A5FA']],
        zmin=z_min, zmax=z_max,
        text=subset['hover'],
        hovertemplate='%{text}<extra></extra>',
        visible=(i == 0),
        showscale=(i == 0),
        marker_line_color='#0F172A'
    ))

fig3.update_geos(fitbounds="locations", visible=False)

fig3 = apply_layout(
    fig3,
    height=650,
    margin=dict(r=20, t=110, l=0, b=40),
    geo=dict(bgcolor=BG_PAPER),
    annotations=[
        dict(
            x=0.01, y=-0.02, xref='paper', yref='paper',
            text="Grigio: regioni senza corsi L-2",
            showarrow=False,
            font=dict(size=10, color='#6B7280')
        ),
        fonte_annotation('Fonte: ANVUR Cruscotto')
    ]
)

st.plotly_chart(fig3, use_container_width=True)


# ─────────────────────────────
# G4 — TOP ATENEI
# ─────────────────────────────
chart_header(
    "Top 15 atenei L-2",
    "Ranking per immatricolati puri",
    "Seleziona anno"
)

g4_anvur = df_anvur[df_anvur['Anno accademico'] >= 2020]\
    .groupby(['Anno accademico', 'ateneo_short', 'regione'])['imm'].sum().reset_index()

g4_anvur['macro'] = g4_anvur['regione'].map({
    'Lombardia':'Nord','Veneto':'Nord','Piemonte':'Nord',
    'Lazio':'Centro','Toscana':'Centro','Marche':'Centro',
    'Campania':'Sud','Puglia':'Sud','Sicilia':'Isole'
})

anni_g4 = sorted(g4_anvur['Anno accademico'].unique())

fig4 = go.Figure()

for i, anno in enumerate(anni_g4):
    subset = g4_anvur[g4_anvur['Anno accademico'] == anno]\
        .sort_values('imm', ascending=False).head(15)

    fig4.add_trace(go.Bar(
        x=subset['imm'],
        y=subset['ateneo_short'],
        orientation='h',
        marker=dict(color=subset['macro'].map(COLORI_MACRO)),
        visible=(i == 0)
    ))

fig4 = apply_layout(
    fig4,
    height=560,
    margin=dict(t=120, l=180, r=80, b=60),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='#9CA3AF'),
        linecolor='#374151'
    ),
    yaxis=dict(
        tickfont=dict(color='#D1D5DB'),
        linecolor='#374151'
    ),
    annotations=[fonte_annotation("Fonte: ANVUR Cruscotto")]
)

st.plotly_chart(fig4, use_container_width=True)
```
# ─────────────────────────────────────────────
# SEZIONE: PROFILO STUDENTI
# ─────────────────────────────────────────────
elif sezione == "Profilo Studenti":
    st.markdown("## Profilo Studenti")
    st.markdown("---")

    alma_profilo = alma_profilo.fillna(0)

    # G5 — Gauge
    chart_header(
        "Indicatori chiave del profilo laureati L-2",
        "I tre indicatori riportano i valori del 2024 confrontati con un anno di riferimento selezionabile. "
        "La linea arancione nel gauge indica il valore dell'anno di riferimento. "
        "I dati provengono dall'indagine AlmaLaurea sul Profilo dei Laureati.",
        "Seleziona l'anno di riferimento per il confronto."
    )

    anni_ref = [2020, 2021, 2022, 2023]

    indicatori_g5 = [
        ('pct_soddisfatti', 'Soddisfatti del corso', '#3B82F6'),
        ('pct_riiscrizione', 'Si reiscriverebbero', '#34D399'),
        ('pct_magistrale', 'Prosegue magistrale', '#818CF8'),
    ]

    val_2024 = {}
    for col, _, _ in indicatori_g5:
        val_2024[col] = float(alma_profilo.loc[alma_profilo['anno'] == 2024, col].values[0])

    fig5 = go.Figure()

    for anno_ref in anni_ref:
        visible = (anno_ref == 2020)

        for col_idx, (col, titolo, colore) in enumerate(indicatori_g5):

            ref_row = alma_profilo[alma_profilo['anno'] == anno_ref]

            val_ref = float(ref_row[col].values[0]) if not ref_row.empty else 0

            fig5.add_trace(go.Indicator(
                mode='gauge+number+delta',
                value=val_2024[col],
                delta={
                    'reference': val_ref,
                    'suffix': '%',
                    'relative': False,
                    'increasing': {'color': '#34D399'},
                    'decreasing': {'color': '#F87171'}
                },
                number={'suffix': '%', 'font': {'size': 40, 'color': colore}},
                title={
                    'text': f"<b style='color:#D1D5DB'>{titolo}</b><br>"
                            f"<span style='font-size:11px;color:#6B7280'>2024 vs {anno_ref}</span>"
                },
                gauge={
                    'axis': {
                        'range': [0, 100],
                        'ticksuffix': '%',
                        'tickfont': {'color': '#6B7280'},
                        'tickcolor': '#374151'
                    },
                    'bar': {'color': colore, 'thickness': 0.25},
                    'bgcolor': '#1F2937',
                    'steps': [
                        {'range': [0, 50], 'color': '#1F2937'},
                        {'range': [50, 75], 'color': '#243547'},
                        {'range': [75, 100], 'color': '#1E3A5F'}
                    ],
                    'threshold': {
                        'line': {'color': '#F59E0B', 'width': 3},
                        'thickness': 0.75,
                        'value': val_ref
                    }
                },
                domain={
                    'x': [col_idx * 0.34, col_idx * 0.34 + 0.30],
                    'y': [0, 1]
                },
                visible=visible
            ))

    buttons_g5 = []
    for anno_ref in anni_ref:
        vis = []
        for ar in anni_ref:
            vis += [ar == anno_ref] * len(indicatori_g5)

        buttons_g5.append(dict(
            label=f'vs {anno_ref}',
            method='update',
            args=[{'visible': vis}]
        ))

    fig5.update_layout(
        title=dict(
            text='Profilo laureati L-2 — confronto anni',
            font=dict(size=18, color='white', family='Inter'),
            x=0.5
        ),
        updatemenus=[dict(
            type='buttons',
            direction='right',
            x=0.5,
            xanchor='center',
            y=1.15,
            buttons=buttons_g5,
            bgcolor='#1F2937',
            bordercolor='#3B82F6',
            font=dict(color='white')
        )],
        height=420,
        margin=dict(t=100, b=60, l=30, r=30),
        paper_bgcolor=BG_PAPER,
        annotations=[
            dict(
                x=0.5, y=-0.12,
                xref='paper', yref='paper',
                text="La linea arancione indica il valore dell'anno di riferimento",
                showarrow=False,
                font=dict(size=11, color='#6B7280')
            ),
            fonte_annotation('Fonte: AlmaLaurea — Profilo dei Laureati')
        ]
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # G6 — Magistrale
    chart_header(
        "Destinazione alla magistrale — dove proseguono gli studi",
        "Distribuzione percentuale degli studenti L-2 che proseguono la magistrale.",
        "Passa il cursore sulle barre per i dettagli."
    )

    g6 = alma_profilo[['anno',
                       'pct_stesso_ateneo_magistrale',
                       'pct_magistrale_nord',
                       'pct_magistrale_centro']].copy()

    g6['anno'] = g6['anno'].astype(str)
    g6['pct_altro'] = 100 - (
        g6['pct_stesso_ateneo_magistrale']
        + g6['pct_magistrale_nord']
        + g6['pct_magistrale_centro']
    )

    DEST = {
        'pct_stesso_ateneo_magistrale': ('Stesso ateneo', '#3B82F6'),
        'pct_magistrale_nord': ('Nord', '#818CF8'),
        'pct_magistrale_centro': ('Centro', '#F59E0B'),
        'pct_altro': ('Altro', '#374151'),
    }

    fig6 = go.Figure()

    for col, (label, color) in DEST.items():
        fig6.add_trace(go.Bar(
            x=g6['anno'],
            y=g6[col],
            name=label,
            marker_color=color,
            hovertemplate=f'<b>{label}</b><br>%{{y:.1f}}%<extra></extra>'
        ))

    fig6.update_layout(
        barmode='stack',
        **PLOT_LAYOUT,
        height=520,
        legend=dict(orientation='h', x=0.5, xanchor='center'),
        annotations=[
            fonte_annotation('Fonte: AlmaLaurea — Profilo dei Laureati')
        ]
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("---")

    # G7 — Scorecard (inalterato ma stabile)
    chart_header(
        "Scorecard — indicatori chiave",
        "",
        ""
    )

    kpi_full = [
        {'label': 'Immatricolati', 'value': '7.076', 'delta': 'stabile', 'color': '#60A5FA', 'bg': '#1E3A5F'},
        {'label': 'Laureati +54%', 'value': '+54%', 'delta': '2010–2024', 'color': '#60A5FA', 'bg': '#1E3A5F'},
        {'label': 'Soddisfatti', 'value': '80.9%', 'delta': 'alto', 'color': '#34D399', 'bg': '#064E3B'},
        {'label': 'Magistrale', 'value': '87%', 'delta': 'stabile', 'color': '#34D399', 'bg': '#064E3B'},
        {'label': 'Retribuzione', 'value': '€896', 'delta': '+31%', 'color': '#34D399', 'bg': '#064E3B'},
        {'label': 'Occupazione', 'value': '21.3%', 'delta': 'bassa', 'color': '#FCD34D', 'bg': '#78350F'},
        {'label': 'Centro Italia', 'value': '27%', 'delta': 'quota', 'color': '#FCD34D', 'bg': '#78350F'},
        {'label': 'Telematici', 'value': '0', 'delta': 'no', 'color': '#34D399', 'bg': '#064E3B'},
    ]

    fig7 = go.Figure()
    col_positions = [0.01, 0.26, 0.51, 0.76]
    row_positions = [0.52, 0.02]

    shapes = []
    annotations = []

    for idx, k in enumerate(kpi_full):
        r = idx // 4
        c = idx % 4

        x0 = col_positions[c]
        x1 = x0 + 0.23
        y0 = row_positions[r]
        y1 = y0 + 0.44

        cx = (x0 + x1) / 2

        shapes.append(dict(
            type='rect',
            xref='paper', yref='paper',
            x0=x0, x1=x1, y0=y0, y1=y1,
            fillcolor=k['bg'],
            line=dict(color=k['color'], width=1.5)
        ))

        annotations.append(dict(
            x=cx, y=(y0 + y1) / 2,
            xref='paper', yref='paper',
            text=f"<b>{k['value']}</b>",
            showarrow=False,
            font=dict(size=28, color=k['color'])
        ))

    fig7.update_layout(
        shapes=shapes,
        annotations=annotations,
        height=600,
        paper_bgcolor=BG_PAPER,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
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
        "Distribuzione tra prosecuzione, cambiamento e abbandono.",
        "Seleziona l'anno con i pulsanti."
    )

    # ── pulizia robusta indicatori ANVUR
    df_ava2['ind_float'] = (
        df_ava2['INDICATORE'].astype(str)
        .str.replace(',', '.', regex=False)
        .str.replace(' ', '', regex=False)
    )

    df_ava2['ind_float'] = pd.to_numeric(df_ava2['ind_float'], errors='coerce')

    ic14 = df_ava2[df_ava2['CODICE'] == 'iC14']
    ic21 = df_ava2[df_ava2['CODICE'] == 'iC21']

    ic14_naz = ic14.groupby('ID_ANNO_ACCADEMICO')['ind_float'].mean().reset_index()
    ic14_naz.columns = ['anno', 'ic14']

    ic21_naz = ic21.groupby('ID_ANNO_ACCADEMICO')['ind_float'].mean().reset_index()
    ic21_naz.columns = ['anno', 'ic21']

    df_destino = ic14_naz.merge(ic21_naz, on='anno', how='inner').dropna()

    # ── sicurezza valori
    df_destino['ic14'] = df_destino['ic14'].fillna(0)
    df_destino['ic21'] = df_destino['ic21'].fillna(0)

    df_destino['prosegue_stesso'] = (df_destino['ic14'] * 100).round(1)
    df_destino['cambia_corso'] = ((df_destino['ic21'] - df_destino['ic14']).clip(lower=0) * 100).round(1)
    df_destino['abbandona'] = ((1 - df_destino['ic21']).clip(lower=0) * 100).round(1)

    df_destino['anno'] = df_destino['anno'].astype(str)
    anni_g11 = sorted(df_destino['anno'].unique())

    # ─────────────────────────────
    # FIGURA
    # ─────────────────────────────
    fig11 = go.Figure()

    for i, anno in enumerate(anni_g11):
        row = df_destino[df_destino['anno'] == anno].iloc[0]

        fig11.add_trace(go.Pie(
            labels=[
                'Proseguono nello stesso corso',
                'Cambiano corso o ateneo',
                "Lasciano l'università"
            ],
            values=[
                row['prosegue_stesso'],
                row['cambia_corso'],
                row['abbandona']
            ],
            hole=0.6,
            marker=dict(
                colors=['#3B82F6', '#F59E0B', '#EF4444'],
                line=dict(color='#0F172A', width=2)
            ),
            textinfo='percent',
            hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>',
            visible=(i == 0),
            sort=False,
        ))

    # ─────────────────────────────
    # BOTTONI
    # ─────────────────────────────
    buttons_g11 = []

    for i, anno in enumerate(anni_g11):
        row = df_destino[df_destino['anno'] == anno].iloc[0]

        vis = [j == i for j in range(len(anni_g11))]

        buttons_g11.append(dict(
            label=anno,
            method='update',
            args=[{'visible': vis}, {
                'annotations': [
                    dict(
                        text=f"<b>{row['prosegue_stesso']:.1f}%</b><br>"
                             "<span style='color:#9CA3AF;font-size:11px'>resta nello stesso corso</span>",
                        x=0.5, y=0.5,
                        xref='paper', yref='paper',
                        showarrow=False,
                        font=dict(size=24, color='white'),
                        align='center'
                    ),
                    dict(
                        x=0.99, y=-0.12,
                        xref='paper', yref='paper',
                        text='Fonte: ANVUR iC14 + iC21',
                        showarrow=False,
                        font=dict(size=10, color='#6B7280'),
                        xanchor='right'
                    )
                ]
            }]
        ))

    # ─────────────────────────────
    # LAYOUT
    # ─────────────────────────────
    row0 = df_destino.iloc[0]

    fig11.update_layout(
        title=dict(
            text=f"Cosa succede dopo il primo anno — {anni_g11[0]}",
            font=dict(size=18, color='white'),
            x=0.5
        ),
        updatemenus=[dict(
            type='buttons',
            direction='right',
            x=0.5,
            xanchor='center',
            y=1.12,
            buttons=buttons_g11,
            bgcolor='#1F2937',
            bordercolor='#3B82F6',
            font=dict(color='white')
        )],
        annotations=[
            dict(
                text=f"<b>{row0['prosegue_stesso']:.1f}%</b><br>"
                     "<span style='color:#9CA3AF;font-size:11px'>resta nello stesso corso</span>",
                x=0.5, y=0.5,
                xref='paper', yref='paper',
                showarrow=False,
                font=dict(size=24, color='white'),
                align='center'
            ),
            dict(
                x=0.99, y=-0.12,
                xref='paper', yref='paper',
                text='Fonte: ANVUR iC14 + iC21',
                showarrow=False,
                font=dict(size=10, color='#6B7280'),
                xanchor='right'
            )
        ],
        height=580,
        margin=dict(t=120, b=80, l=80, r=80),
        paper_bgcolor=BG_PAPER,
        showlegend=False
    )

    st.plotly_chart(fig11, use_container_width=True)
# ─────────────────────────────────────────────
# SEZIONE: VARIANTI DEL CORSO
# ─────────────────────────────────────────────
elif sezione == "Varianti del Corso":
    st.markdown("## Varianti del Corso")
    st.markdown("---")

    # ─────────────────────────────
    # G8 — TREEMAP VARIANTI
    # ─────────────────────────────
    chart_header(
        "Distribuzione immatricolati per variante L-2",
        "Dimensione = immatricolati, colore = numero atenei",
        "Seleziona anno e passa il mouse"
    )

    df_var = df_anvur[df_anvur['Anno accademico'] >= 2019].copy()

    df_var['corso_nome'] = (
        df_var['corso_nome']
        .astype(str)
        .str.title()
        .str.strip()
    )

    anni_tree = sorted(df_var['Anno accademico'].unique())

    fig8b = go.Figure()

    for i, anno in enumerate(anni_tree):

        subset = df_var[df_var['Anno accademico'] == anno].copy()

        treemap_df = subset.groupby('corso_nome').agg(
            imm=('imm', 'sum'),
            n_atenei=('ateneo_short', 'nunique')
        ).reset_index()

        fig8b.add_trace(go.Treemap(
            labels=treemap_df['corso_nome'],
            parents=['L-2 Biotecnologie'] * len(treemap_df),
            values=treemap_df['imm'],
            textinfo='label+value',
            customdata=treemap_df[['n_atenei', 'imm']],
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Immatricolati: <b>%{customdata[1]:,.0f}</b><br>"
                "Atenei: <b>%{customdata[0]}</b><extra></extra>"
            ),
            marker=dict(
                colors=treemap_df['n_atenei'],
                colorscale='Blues',
                showscale=True,
                line=dict(color='#0F172A', width=2)
            ),
            visible=(i == 0)
        ))

    buttons_g8 = []
    for i, anno in enumerate(anni_tree):
        vis = [j == i for j in range(len(anni_tree))]
        buttons_g8.append(dict(
            label=str(anno),
            method='update',
            args=[{'visible': vis}]
        ))

    fig8b.update_layout(
        title=dict(
            text=f'Varianti L-2 — {anni_tree[0]}',
            font=dict(size=18, color='white'),
            x=0.5
        ),
        updatemenus=[dict(
            type='buttons',
            direction='right',
            x=0.5,
            xanchor='center',
            y=1.10,
            buttons=buttons_g8,
            bgcolor='#1F2937',
            bordercolor='#3B82F6',
            font=dict(color='white')
        )],
        annotations=[
            fonte_annotation('Fonte: ANVUR Cruscotto')
        ],
        height=580,
        paper_bgcolor=BG_PAPER,
        margin=dict(t=120, b=40, l=20, r=20)
    )

    st.plotly_chart(fig8b, use_container_width=True)

    st.markdown("---")

    # ─────────────────────────────
    # G12 — PROSECUZIONE VARIANTI
    # ─────────────────────────────
    chart_header(
        "Prosecuzione al II anno per variante L-2",
        "Confronto tra varianti e baseline Biotecnologie",
        "Passa il mouse per dettagli"
    )

    ic14 = df_ava2[df_ava2['CODICE'] == 'iC14'].copy()

    ic14['ind_float'] = pd.to_numeric(
        ic14['INDICATORE']
        .astype(str)
        .str.replace(',', '.', regex=False)
        .str.replace(' ', '', regex=False),
        errors='coerce'
    )

    ic14['corso_norm'] = (
        ic14['NOME_CORSO']
        .astype(str)
        .str.title()
        .str.strip()
        .str.replace(r'Biotecnologia$', 'Biotecnologie', regex=True)
    )

    ic14_var = ic14.groupby('corso_norm').agg(
        prosecuzione=('ind_float', 'mean'),
        n_atenei=('CODE_UN', 'nunique')
    ).reset_index()

    ic14_var['prosecuzione_pct'] = (ic14_var['prosecuzione'] * 100).round(1)
    ic14_var['abbandono'] = (100 - ic14_var['prosecuzione_pct']).round(1)

    # baseline sicura
    baseline_row = ic14_var[ic14_var['corso_norm'] == 'Biotecnologie']

    if baseline_row.empty:
        baseline = ic14_var['prosecuzione_pct'].mean()
    else:
        baseline = float(baseline_row['prosecuzione_pct'].values[0])

    ic14_var = ic14_var.sort_values('prosecuzione_pct')

    def color(row):
        if row['corso_norm'] == 'Biotecnologie':
            return '#6B7280'
        return '#34D399' if row['prosecuzione_pct'] > baseline else '#EF4444'

    ic14_var['colore'] = ic14_var.apply(color, axis=1)

    fig12 = go.Figure()

    fig12.add_trace(go.Bar(
        x=ic14_var['prosecuzione_pct'],
        y=ic14_var['corso_norm'],
        orientation='h',
        marker_color=ic14_var['colore'],
        text=ic14_var.apply(
            lambda r: f"{r['prosecuzione_pct']:.1f}% ({int(r['n_atenei'])})",
            axis=1
        ),
        textposition='outside',
        customdata=list(zip(ic14_var['abbandono'], ic14_var['n_atenei'])),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Prosecuzione: %{x:.1f}%<br>"
            "Abbandono: %{customdata[0]:.1f}%<br>"
            "Atenei: %{customdata[1]}<extra></extra>"
        )
    ))

    fig12.add_vline(
        x=baseline,
        line=dict(color='#6B7280', dash='dash')
    )

    fig12.update_layout(
        **PLOT_LAYOUT,
        xaxis=dict(
            title='% prosecuzione',
            ticksuffix='%',
            range=[0, 110],
            showgrid=False,
            linecolor='#374151'
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=10)
        ),
        annotations=[
            dict(
                x=baseline,
                y=1.02,
                xref='x',
                yref='paper',
                text=f'Baseline: {baseline:.1f}%',
                showarrow=False,
                font=dict(color='#9CA3AF')
            ),
            fonte_annotation('Fonte: ANVUR iC14')
        ],
        height=580,
        margin=dict(t=80, b=80, l=300, r=80),
        paper_bgcolor=BG_PAPER
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
        **PLOT_LAYOUT,
        title='',
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
