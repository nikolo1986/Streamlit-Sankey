# Sankey.py - CDAO Use Case -> SOCOM CDR Priorities

# Streamlit + Plotly Sankey | Dark Military Aesthetic

# Run: streamlit run Sankey.py

# Deps: pip install streamlit plotly pandas

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
page_title=“CDAO -> SOCOM CDR Priorities | Sankey”,
layout=“wide”,
)

st.markdown(”””

<style>
  @import url("https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap");
  html, body, [class*="css"] { background-color: #0a0e14; color: #c8d6e5; font-family: Rajdhani, sans-serif; }
  .top-banner { background: #0d1b2a; border-top: 2px solid #1f8a4c; border-bottom: 1px solid #1a3a5c; padding: 14px 28px; margin-bottom: 24px; }
  .top-banner h1 { font-family: "Share Tech Mono", monospace; font-size: 1.2rem; color: #4fc3f7; letter-spacing: 0.18em; margin: 0; text-transform: uppercase; }
  .top-banner p { font-size: 0.85rem; color: #8aabb8; letter-spacing: 0.08em; margin: 4px 0 0 0; }
  .class-banner { background-color: #1f5c2e; text-align: center; padding: 4px 0; font-family: "Share Tech Mono", monospace; font-size: 0.72rem; letter-spacing: 0.22em; color: #d4f4d4; border: 1px solid #2e8b47; }
  .section-label { font-family: "Share Tech Mono", monospace; font-size: 0.75rem; letter-spacing: 0.2em; color: #4fc3f7; text-transform: uppercase; border-left: 3px solid #1f8a4c; padding-left: 10px; margin-bottom: 12px; }
  .metric-card { background: #0d1b2a; border: 1px solid #1a3a5c; border-top: 3px solid #4fc3f7; padding: 14px 18px; }
  .metric-val { font-family: "Share Tech Mono", monospace; font-size: 2rem; color: #4fc3f7; line-height: 1; }
  .metric-lbl { font-size: 0.78rem; letter-spacing: 0.12em; color: #8aabb8; text-transform: uppercase; margin-top: 4px; }
  [data-testid="stSidebar"] { background-color: #080d13; border-right: 1px solid #1a3a5c; }
  .block-container { padding-top: 1rem; }
  footer { visibility: hidden; }
  #MainMenu { visibility: hidden; }
</style>

“””, unsafe_allow_html=True)

st.markdown(’<div class="class-banner">UNCLASSIFIED // FOR OFFICIAL USE ONLY</div>’, unsafe_allow_html=True)

st.markdown(”””

<div class="top-banner">
  <h1>CDAO USE CASE -&gt; SOCOM CDR PRIORITIES // FLOW ANALYSIS</h1>
  <p>USSOCOM J6 / CDAO | Data and Analytics Division | AY2025 | UNCLASSIFIED // FOUO</p>
</div>
""", unsafe_allow_html=True)

# — NODE DEFINITIONS —

USE_CASES = [
“Predictive Maintenance (AI-PM)”,
“ISR Data Fusion (ISRDF)”,
“Personnel Readiness (PR-Analytics)”,
“Logistics Optimization (LOG-OPT)”,
“Threat Pattern Analysis (TPA)”,
“OSINT Aggregation (OSINT-AI)”,
“Force Allocation Modeling (FAM)”,
“Cyber Anomaly Detection (CAD)”,
]

CAPABILITIES = [
“Machine Learning Pipelines”,
“Geospatial Intelligence”,
“Predictive Analytics”,
“Real-Time Data Fusion”,
“NLP / Text Analytics”,
“Decision Support Dashboards”,
]

LOE = [
“Warfighter Readiness”,
“Global SOF Network”,
“Information Advantage”,
“Integrated Deterrence”,
]

CDR_PRIORITIES = [
“Prepare SOF for Great Power Competition”,
“Sustain Lethality and Readiness”,
“Strengthen Alliances and Partnerships”,
“Modernize the Force”,
]

all_nodes = USE_CASES + CAPABILITIES + LOE + CDR_PRIORITIES

uc_idx  = {n: i for i, n in enumerate(USE_CASES)}
cap_idx = {n: i + len(USE_CASES) for i, n in enumerate(CAPABILITIES)}
loe_idx = {n: i + len(USE_CASES) + len(CAPABILITIES) for i, n in enumerate(LOE)}
pri_idx = {n: i + len(USE_CASES) + len(CAPABILITIES) + len(LOE) for i, n in enumerate(CDR_PRIORITIES)}

# — FLOW DATA —

uc_to_cap = [
(“Predictive Maintenance (AI-PM)”,      “Machine Learning Pipelines”,    18),
(“Predictive Maintenance (AI-PM)”,      “Predictive Analytics”,          14),
(“ISR Data Fusion (ISRDF)”,             “Geospatial Intelligence”,       20),
(“ISR Data Fusion (ISRDF)”,             “Real-Time Data Fusion”,         16),
(“Personnel Readiness (PR-Analytics)”,  “Predictive Analytics”,          12),
(“Personnel Readiness (PR-Analytics)”,  “Decision Support Dashboards”,   10),
(“Logistics Optimization (LOG-OPT)”,    “Machine Learning Pipelines”,    11),
(“Logistics Optimization (LOG-OPT)”,    “Decision Support Dashboards”,    9),
(“Threat Pattern Analysis (TPA)”,       “Geospatial Intelligence”,       15),
(“Threat Pattern Analysis (TPA)”,       “Real-Time Data Fusion”,         13),
(“Threat Pattern Analysis (TPA)”,       “NLP / Text Analytics”,           8),
(“OSINT Aggregation (OSINT-AI)”,        “NLP / Text Analytics”,          17),
(“OSINT Aggregation (OSINT-AI)”,        “Geospatial Intelligence”,        9),
(“Force Allocation Modeling (FAM)”,     “Decision Support Dashboards”,   14),
(“Force Allocation Modeling (FAM)”,     “Machine Learning Pipelines”,     8),
(“Cyber Anomaly Detection (CAD)”,       “Machine Learning Pipelines”,    13),
(“Cyber Anomaly Detection (CAD)”,       “Real-Time Data Fusion”,         11),
]

cap_to_loe = [
(“Machine Learning Pipelines”,   “Warfighter Readiness”,   22),
(“Geospatial Intelligence”,      “Information Advantage”,  26),
(“Geospatial Intelligence”,      “Global SOF Network”,     18),
(“Predictive Analytics”,         “Warfighter Readiness”,   16),
(“Predictive Analytics”,         “Integrated Deterrence”,  10),
(“Real-Time Data Fusion”,        “Information Advantage”,  20),
(“Real-Time Data Fusion”,        “Integrated Deterrence”,  20),
(“NLP / Text Analytics”,         “Information Advantage”,  15),
(“NLP / Text Analytics”,         “Global SOF Network”,     10),
(“Decision Support Dashboards”,  “Warfighter Readiness”,   14),
(“Decision Support Dashboards”,  “Global SOF Network”,     19),
]

loe_to_pri = [
(“Warfighter Readiness”,   “Sustain Lethality and Readiness”,          30),
(“Warfighter Readiness”,   “Prepare SOF for Great Power Competition”,  22),
(“Global SOF Network”,     “Strengthen Alliances and Partnerships”,    28),
(“Global SOF Network”,     “Prepare SOF for Great Power Competition”,  19),
(“Information Advantage”,  “Prepare SOF for Great Power Competition”,  25),
(“Information Advantage”,  “Modernize the Force”,                      36),
(“Integrated Deterrence”,  “Prepare SOF for Great Power Competition”,  18),
(“Integrated Deterrence”,  “Sustain Lethality and Readiness”,          12),
]

# — BUILD SANKEY ARRAYS —

sources, targets, values, link_labels = [], [], [], []

for uc, cap, val in uc_to_cap:
sources.append(uc_idx[uc])
targets.append(cap_idx[cap])
values.append(val)
link_labels.append(uc + “ -> “ + cap + “: “ + str(val) + “ units”)

for cap, loe, val in cap_to_loe:
sources.append(cap_idx[cap])
targets.append(loe_idx[loe])
values.append(val)
link_labels.append(cap + “ -> “ + loe + “: “ + str(val) + “ units”)

for loe, pri, val in loe_to_pri:
sources.append(loe_idx[loe])
targets.append(pri_idx[pri])
values.append(val)
link_labels.append(loe + “ -> “ + pri + “: “ + str(val) + “ units”)

# — NODE COLORS —

uc_color  = “rgba(79, 195, 247, 0.85)”
cap_color = “rgba(31, 138, 76, 0.85)”
loe_color = “rgba(255, 167, 38, 0.85)”
pri_color = “rgba(239, 83, 80, 0.85)”

node_colors = [uc_color] * len(USE_CASES) + [cap_color] * len(CAPABILITIES) + [loe_color] * len(LOE) + [pri_color] * len(CDR_PRIORITIES)

link_colors = []
for s in sources:
if s < len(USE_CASES):
link_colors.append(“rgba(79, 195, 247, 0.25)”)
elif s < len(USE_CASES) + len(CAPABILITIES):
link_colors.append(“rgba(31, 138, 76, 0.25)”)
else:
link_colors.append(“rgba(255, 167, 38, 0.25)”)

# — SIDEBAR —

with st.sidebar:
st.markdown(’<div class="section-label">// Display Options</div>’, unsafe_allow_html=True)
node_pad   = st.slider(“Node Padding”, 10, 40, 20)
node_thick = st.slider(“Node Thickness”, 10, 40, 22)
chart_h    = st.slider(“Chart Height (px)”, 500, 1000, 720)
show_table = st.checkbox(“Show Flow Data Table”, value=False)
st.markdown(”—”)
st.markdown(’<div class="section-label">// Legend</div>’, unsafe_allow_html=True)
st.markdown(”””
<div style="font-family: Rajdhani; font-size:0.82rem; line-height:1.8;">
<span style="color:#4fc3f7">[UC]</span> CDAO Use Cases<br>
<span style="color:#1f8a4c">[CA]</span> Data and Analytics Capabilities<br>
<span style="color:#ffa726">[LO]</span> Lines of Effort<br>
<span style="color:#ef5350">[PR]</span> CDR Strategic Priorities
</div>
“””, unsafe_allow_html=True)

# — METRICS —

total_flow = sum(v for _, _, v in loe_to_pri)
col1, col2, col3, col4 = st.columns(4)
with col1:
st.markdown(f’<div class="metric-card"><div class="metric-val">{len(USE_CASES)}</div><div class="metric-lbl">CDAO Use Cases</div></div>’, unsafe_allow_html=True)
with col2:
st.markdown(f’<div class="metric-card"><div class="metric-val">{len(CAPABILITIES)}</div><div class="metric-lbl">Analytics Capabilities</div></div>’, unsafe_allow_html=True)
with col3:
st.markdown(f’<div class="metric-card"><div class="metric-val">{len(LOE)}</div><div class="metric-lbl">Lines of Effort</div></div>’, unsafe_allow_html=True)
with col4:
st.markdown(f’<div class="metric-card"><div class="metric-val">{total_flow}</div><div class="metric-lbl">Total Effort Units</div></div>’, unsafe_allow_html=True)

# — SANKEY FIGURE —

fig = go.Figure(go.Sankey(
arrangement=“snap”,
node=dict(
pad=node_pad,
thickness=node_thick,
line=dict(color=”#0a0e14”, width=0.8),
label=all_nodes,
color=node_colors,
hovertemplate=”<b>%{label}</b><br>Flow: %{value} units<extra></extra>”,
),
link=dict(
source=sources,
target=targets,
value=values,
color=link_colors,
label=link_labels,
hovertemplate=”<b>%{label}</b><extra></extra>”,
),
))

fig.update_layout(
font=dict(family=“Rajdhani, sans-serif”, size=12, color=”#c8d6e5”),
paper_bgcolor=”#0a0e14”,
plot_bgcolor=”#0a0e14”,
height=chart_h,
margin=dict(l=20, r=20, t=60, b=20),
title=dict(
text=”<b>CDAO USE CASE FLOW -> SOCOM CDR STRATEGIC PRIORITIES</b><br><sup>Resource/Effort Units | AY2025 Mock Data | UNCLASSIFIED // FOUO</sup>”,
font=dict(family=“Share Tech Mono, monospace”, size=14, color=”#4fc3f7”),
x=0.02,
xanchor=“left”,
),
)

st.plotly_chart(fig, use_container_width=True)

# — OPTIONAL TABLE —

if show_table:
st.markdown(’<div class="section-label" style="margin-top:24px;">// Raw Flow Data</div>’, unsafe_allow_html=True)
rows = []
for uc, cap, val in uc_to_cap:
rows.append({“Layer”: “Use Case -> Capability”, “Source”: uc, “Target”: cap, “Effort Units”: val})
for cap, loe, val in cap_to_loe:
rows.append({“Layer”: “Capability -> LOE”, “Source”: cap, “Target”: loe, “Effort Units”: val})
for loe, pri, val in loe_to_pri:
rows.append({“Layer”: “LOE -> CDR Priority”, “Source”: loe, “Target”: pri, “Effort Units”: val})
df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)

# — FOOTER —

st.markdown(”—”)
st.markdown(’<div style="font-family: monospace; font-size:0.65rem; color:#4a6a7a; text-align:center; padding:8px 0;">UNCLASSIFIED // FOR OFFICIAL USE ONLY | USSOCOM J6 / CDAO Data and Analytics | NOT FOR PUBLIC RELEASE</div>’, unsafe_allow_html=True)