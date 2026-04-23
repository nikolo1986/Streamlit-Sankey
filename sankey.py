# Sankey.py - CDAO Use Case -> SOCOM CDR Priorities
# Run: streamlit run Sankey.py
# Requires: pip install streamlit plotly pandas

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title='CDAO SOCOM Sankey', layout='wide')

st.markdown('<style>html,body{background:#0a0e14;color:#c8d6e5;font-family:sans-serif}.top-banner{background:#0d1b2a;border-top:2px solid #1f8a4c;padding:14px 28px;margin-bottom:24px}.top-banner h1{font-size:1.1rem;color:#4fc3f7;letter-spacing:.15em;margin:0;text-transform:uppercase}.top-banner p{font-size:.85rem;color:#8aabb8;margin:4px 0 0 0}.class-banner{background:#1f5c2e;text-align:center;padding:4px 0;font-size:.72rem;color:#d4f4d4;border:1px solid #2e8b47}.metric-card{background:#0d1b2a;border:1px solid #1a3a5c;border-top:3px solid #4fc3f7;padding:14px 18px}.metric-val{font-size:2rem;color:#4fc3f7;line-height:1}.metric-lbl{font-size:.75rem;color:#8aabb8;text-transform:uppercase;margin-top:4px}.stSidebar,.css-1d391kg{background:#080d13}footer{visibility:hidden}</style>', unsafe_allow_html=True)

st.markdown('<div class="class-banner">UNCLASSIFIED // FOR OFFICIAL USE ONLY</div>', unsafe_allow_html=True)

st.markdown('<div class="top-banner"><h1>CDAO USE CASE -> SOCOM CDR PRIORITIES // FLOW ANALYSIS</h1><p>USSOCOM J6 / CDAO | Data and Analytics Division | AY2025 | UNCLASSIFIED // FOUO</p></div>', unsafe_allow_html=True)

USE_CASES = [
    'Predictive Maintenance (AI-PM)',
    'ISR Data Fusion (ISRDF)',
    'Personnel Readiness (PR-Analytics)',
    'Logistics Optimization (LOG-OPT)',
    'Threat Pattern Analysis (TPA)',
    'OSINT Aggregation (OSINT-AI)',
    'Force Allocation Modeling (FAM)',
    'Cyber Anomaly Detection (CAD)',
]

CAPABILITIES = [
    'Machine Learning Pipelines',
    'Geospatial Intelligence',
    'Predictive Analytics',
    'Real-Time Data Fusion',
    'NLP Text Analytics',
    'Decision Support Dashboards',
]

LOE = [
    'Warfighter Readiness',
    'Global SOF Network',
    'Information Advantage',
    'Integrated Deterrence',
]

CDR_PRIORITIES = [
    'Prepare SOF for Great Power Competition',
    'Sustain Lethality and Readiness',
    'Strengthen Alliances and Partnerships',
    'Modernize the Force',
]

all_nodes = USE_CASES + CAPABILITIES + LOE + CDR_PRIORITIES
uc_idx  = {n: i for i, n in enumerate(USE_CASES)}
cap_idx = {n: i + len(USE_CASES) for i, n in enumerate(CAPABILITIES)}
loe_idx = {n: i + len(USE_CASES) + len(CAPABILITIES) for i, n in enumerate(LOE)}
pri_idx = {n: i + len(USE_CASES) + len(CAPABILITIES) + len(LOE) for i, n in enumerate(CDR_PRIORITIES)}

uc_to_cap = [
    ('Predictive Maintenance (AI-PM)', 'Machine Learning Pipelines', 18),
    ('Predictive Maintenance (AI-PM)', 'Predictive Analytics', 14),
    ('ISR Data Fusion (ISRDF)', 'Geospatial Intelligence', 20),
    ('ISR Data Fusion (ISRDF)', 'Real-Time Data Fusion', 16),
    ('Personnel Readiness (PR-Analytics)', 'Predictive Analytics', 12),
    ('Personnel Readiness (PR-Analytics)', 'Decision Support Dashboards', 10),
    ('Logistics Optimization (LOG-OPT)', 'Machine Learning Pipelines', 11),
    ('Logistics Optimization (LOG-OPT)', 'Decision Support Dashboards', 9),
    ('Threat Pattern Analysis (TPA)', 'Geospatial Intelligence', 15),
    ('Threat Pattern Analysis (TPA)', 'Real-Time Data Fusion', 13),
    ('Threat Pattern Analysis (TPA)', 'NLP Text Analytics', 8),
    ('OSINT Aggregation (OSINT-AI)', 'NLP Text Analytics', 17),
    ('OSINT Aggregation (OSINT-AI)', 'Geospatial Intelligence', 9),
    ('Force Allocation Modeling (FAM)', 'Decision Support Dashboards', 14),
    ('Force Allocation Modeling (FAM)', 'Machine Learning Pipelines', 8),
    ('Cyber Anomaly Detection (CAD)', 'Machine Learning Pipelines', 13),
    ('Cyber Anomaly Detection (CAD)', 'Real-Time Data Fusion', 11),
]

cap_to_loe = [
    ('Machine Learning Pipelines', 'Warfighter Readiness', 22),
    ('Geospatial Intelligence', 'Information Advantage', 26),
    ('Geospatial Intelligence', 'Global SOF Network', 18),
    ('Predictive Analytics', 'Warfighter Readiness', 16),
    ('Predictive Analytics', 'Integrated Deterrence', 10),
    ('Real-Time Data Fusion', 'Information Advantage', 20),
    ('Real-Time Data Fusion', 'Integrated Deterrence', 20),
    ('NLP Text Analytics', 'Information Advantage', 15),
    ('NLP Text Analytics', 'Global SOF Network', 10),
    ('Decision Support Dashboards', 'Warfighter Readiness', 14),
    ('Decision Support Dashboards', 'Global SOF Network', 19),
]

loe_to_pri = [
    ('Warfighter Readiness', 'Sustain Lethality and Readiness', 30),
    ('Warfighter Readiness', 'Prepare SOF for Great Power Competition', 22),
    ('Global SOF Network', 'Strengthen Alliances and Partnerships', 28),
    ('Global SOF Network', 'Prepare SOF for Great Power Competition', 19),
    ('Information Advantage', 'Prepare SOF for Great Power Competition', 25),
    ('Information Advantage', 'Modernize the Force', 36),
    ('Integrated Deterrence', 'Prepare SOF for Great Power Competition', 18),
    ('Integrated Deterrence', 'Sustain Lethality and Readiness', 12),
]

sources, targets, values, link_labels = [], [], [], []
for src, tgt, v in uc_to_cap:
    sources.append(uc_idx[src]); targets.append(cap_idx[tgt]); values.append(v)
    link_labels.append(src + ' -> ' + tgt)
for src, tgt, v in cap_to_loe:
    sources.append(cap_idx[src]); targets.append(loe_idx[tgt]); values.append(v)
    link_labels.append(src + ' -> ' + tgt)
for src, tgt, v in loe_to_pri:
    sources.append(loe_idx[src]); targets.append(pri_idx[tgt]); values.append(v)
    link_labels.append(src + ' -> ' + tgt)

node_colors = (['rgba(79,195,247,0.85)'] * len(USE_CASES) +
               ['rgba(31,138,76,0.85)'] * len(CAPABILITIES) +
               ['rgba(255,167,38,0.85)'] * len(LOE) +
               ['rgba(239,83,80,0.85)'] * len(CDR_PRIORITIES))
link_colors = []
for src in sources:
    if src < len(USE_CASES):
        link_colors.append('rgba(79,195,247,0.2)')
    elif src < len(USE_CASES) + len(CAPABILITIES):
        link_colors.append('rgba(31,138,76,0.2)')
    else:
        link_colors.append('rgba(255,167,38,0.2)')

with st.sidebar:
    node_pad   = st.slider('Node Padding', 10, 40, 20)
    node_thick = st.slider('Node Thickness', 10, 40, 22)
    chart_h    = st.slider('Chart Height px', 500, 1000, 720)
    show_table = st.checkbox('Show Flow Data Table', value=False)

total_flow = sum(v for _, _, v in loe_to_pri)
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div class="metric-val">{len(USE_CASES)}</div><div class="metric-lbl">Use Cases</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div class="metric-val">{len(CAPABILITIES)}</div><div class="metric-lbl">Capabilities</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div class="metric-val">{len(LOE)}</div><div class="metric-lbl">Lines of Effort</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div class="metric-val">{total_flow}</div><div class="metric-lbl">Effort Units</div></div>', unsafe_allow_html=True)

fig = go.Figure(go.Sankey(
    arrangement='snap',
    node=dict(
        pad=node_pad, thickness=node_thick,
        line=dict(color='#0a0e14', width=0.8),
        label=all_nodes, color=node_colors,
        hovertemplate='<b>%{label}</b><br>Flow: %{value} units<extra></extra>',
    ),
    link=dict(
        source=sources, target=targets, value=values,
        color=link_colors, label=link_labels,
        hovertemplate='<b>%{label}</b><extra></extra>',
    ),
))

fig.update_layout(
    font=dict(family='sans-serif', size=12, color='#c8d6e5'),
    paper_bgcolor='#0a0e14', plot_bgcolor='#0a0e14',
    height=chart_h, margin=dict(l=20, r=20, t=60, b=20),
    title=dict(
        text='<b>CDAO USE CASE -> SOCOM CDR STRATEGIC PRIORITIES</b>',
        font=dict(size=13, color='#4fc3f7'),
        x=0.02, xanchor='left',
    ),
)
st.plotly_chart(fig, use_container_width=True)

if show_table:
    rows = []
    for src, tgt, v in uc_to_cap:
        rows.append({'Layer': 'UC->Cap', 'Source': src, 'Target': tgt, 'Units': v})
    for src, tgt, v in cap_to_loe:
        rows.append({'Layer': 'Cap->LOE', 'Source': src, 'Target': tgt, 'Units': v})
    for src, tgt, v in loe_to_pri:
        rows.append({'Layer': 'LOE->Pri', 'Source': src, 'Target': tgt, 'Units': v})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.markdown('---')
st.markdown('<div style="font-size:.65rem;color:#4a6a7a;text-align:center">UNCLASSIFIED // FOR OFFICIAL USE ONLY | USSOCOM J6 / CDAO | NOT FOR PUBLIC RELEASE</div>', unsafe_allow_html=True)
