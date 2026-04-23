“””
Sankey.py - CDAO Use Case -> SOCOM CDR Priorities
Streamlit app with Plotly Sankey diagram (dark military aesthetic)

Run with:
streamlit run Sankey.py

Dependencies:
pip install streamlit plotly pandas
“””

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ─────────────────────────────────────────────

# PAGE CONFIG

# ─────────────────────────────────────────────

st.set_page_config(
page_title=“CDAO → SOCOM CDR Priorities | Sankey”,
page_icon=“🎯”,
layout=“wide”,
)

# ─────────────────────────────────────────────

# CUSTOM CSS — DARK MILITARY AESTHETIC

# ─────────────────────────────────────────────

st.markdown(”””

<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

  html, body, [class*="css"] {
      background-color: #0a0e14;
      color: #c8d6e5;
      font-family: 'Rajdhani', sans-serif;
  }

  /* Header bar */
  .top-banner {
      background: linear-gradient(90deg, #0d1b2a 0%, #162032 50%, #0d1b2a 100%);
      border-top: 2px solid #1f8a4c;
      border-bottom: 1px solid #1a3a5c;
      padding: 14px 28px;
      margin-bottom: 24px;
  }
  .top-banner h1 {
      font-family: 'Share Tech Mono', monospace;
      font-size: 1.35rem;
      color: #4fc3f7;
      letter-spacing: 0.18em;
      margin: 0;
      text-transform: uppercase;
  }
  .top-banner p {
      font-family: 'Rajdhani', sans-serif;
      font-size: 0.85rem;
      color: #8aabb8;
      letter-spacing: 0.08em;
      margin: 4px 0 0 0;
  }

  /* Classification banner */
  .class-banner {
      background-color: #1f5c2e;
      text-align: center;
      padding: 4px 0;
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.72rem;
      letter-spacing: 0.22em;
      color: #d4f4d4;
      border: 1px solid #2e8b47;
  }

  /* Section headers */
  .section-label {
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.75rem;
      letter-spacing: 0.2em;
      color: #4fc3f7;
      text-transform: uppercase;
      border-left: 3px solid #1f8a4c;
      padding-left: 10px;
      margin-bottom: 12px;
  }

  /* Metric cards */
  .metric-row {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
  }
  .metric-card {
      flex: 1;
      background: #0d1b2a;
      border: 1px solid #1a3a5c;
      border-top: 3px solid #4fc3f7;
      padding: 14px 18px;
  }
  .metric-val {
      font-family: 'Share Tech Mono', monospace;
      font-size: 2rem;
      color: #4fc3f7;
      line-height: 1;
  }
  .metric-lbl {
      font-size: 0.78rem;
      letter-spacing: 0.12em;
      color: #8aabb8;
      text-transform: uppercase;
      margin-top: 4px;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background-color: #080d13;
      border-right: 1px solid #1a3a5c;
  }
  [data-testid="stSidebar"] .css-pkbazv {
      color: #c8d6e5;
  }

  /* Remove default Streamlit padding */
  .block-container { padding-top: 1rem; }
  footer { visibility: hidden; }
  #MainMenu { visibility: hidden; }
</style>

“””, unsafe_allow_html=True)

# ─────────────────────────────────────────────

# CLASSIFICATION BANNER

# ─────────────────────────────────────────────

st.markdown(’<div class="class-banner">UNCLASSIFIED // FOR OFFICIAL USE ONLY</div>’, unsafe_allow_html=True)

# ─────────────────────────────────────────────

# HEADER

# ─────────────────────────────────────────────

st.markdown(”””

<div class="top-banner">
  <h1>⬡ CDAO USE CASE → SOCOM CDR PRIORITIES // FLOW ANALYSIS</h1>
  <p>USSOCOM J6 / CDAO | Data & Analytics Division | AY2025 | UNCLASSIFIED // FOUO</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────

# MOCK DATA DEFINITIONS

# ─────────────────────────────────────────────

# Node layers (left → right):

# Layer 0: CDAO Use Cases

# Layer 1: Data & Analytics Capabilities

# Layer 2: CDR Priority Lines of Effort

# Layer 3: CDR Strategic Priorities

USE_CASES = [
“Predictive Maintenance\n(AI-PM)”,
“ISR Data Fusion\n(ISRDF)”,
“Personnel Readiness\n(PR-Analytics)”,
“Logistics Optimization\n(LOG-OPT)”,
“Threat Pattern Analysis\n(TPA)”,
“OSINT Aggregation\n(OSINT-AI)”,
“Force Allocation\nModeling (FAM)”,
“Cyber Anomaly\nDetection (CAD)”,
]

CAPABILITIES = [
“Machine Learning\nPipelines”,
“Geospatial\nIntelligence”,
“Predictive\nAnalytics”,
“Real-Time\nData Fusion”,
“NLP / Text\nAnalytics”,
“Decision Support\nDashboards”,
]

LOE = [
“Warfighter\nReadiness”,
“Global SOF\nNetwork”,
“Information\nAdvantage”,
“Integrated\nDeterrence”,
]

CDR_PRIORITIES = [
“Prepare SOF for\nGreat Power Competition”,
“Sustain Lethality &\nReadiness”,
“Strengthen Alliances\n& Partnerships”,
“Modernize the\nForce”,
]

# All nodes in order

all_nodes = USE_CASES + CAPABILITIES + LOE + CDR_PRIORITIES

# Index helpers

uc_idx  = {n: i for i, n in enumerate(USE_CASES)}
cap_idx = {n: i + len(USE_CASES) for i, n in enumerate(CAPABILITIES)}
loe_idx = {n: i + len(USE_CASES) + len(CAPABILITIES) for i, n in enumerate(LOE)}
pri_idx = {n: i + len(USE_CASES) + len(CAPABILITIES) + len(LOE) for i, n in enumerate(CDR_PRIORITIES)}

# ─────────────────────────────────────────────

# FLOW DATA (mock weights = resource/effort units)

# ─────────────────────────────────────────────

# Use Case → Capability

uc_to_cap = [
# (use_case, capability, value)
(“Predictive Maintenance\n(AI-PM)”,       “Machine Learning\nPipelines”,     18),
(“Predictive Maintenance\n(AI-PM)”,       “Predictive\nAnalytics”,           14),
(“ISR Data Fusion\n(ISRDF)”,              “Geospatial\nIntelligence”,        20),
(“ISR Data Fusion\n(ISRDF)”,              “Real-Time\nData Fusion”,          16),
(“Personnel Readiness\n(PR-Analytics)”,   “Predictive\nAnalytics”,           12),
(“Personnel Readiness\n(PR-Analytics)”,   “Decision Support\nDashboards”,    10),
(“Logistics Optimization\n(LOG-OPT)”,     “Machine Learning\nPipelines”,     11),
(“Logistics Optimization\n(LOG-OPT)”,     “Decision Support\nDashboards”,     9),
(“Threat Pattern Analysis\n(TPA)”,        “Geospatial\nIntelligence”,        15),
(“Threat Pattern Analysis\n(TPA)”,        “Real-Time\nData Fusion”,          13),
(“Threat Pattern Analysis\n(TPA)”,        “NLP / Text\nAnalytics”,            8),
(“OSINT Aggregation\n(OSINT-AI)”,         “NLP / Text\nAnalytics”,           17),
(“OSINT Aggregation\n(OSINT-AI)”,         “Geospatial\nIntelligence”,         9),
(“Force Allocation\nModeling (FAM)”,      “Decision Support\nDashboards”,    14),
(“Force Allocation\nModeling (FAM)”,      “Machine Learning\nPipelines”,      8),
(“Cyber Anomaly\nDetection (CAD)”,        “Machine Learning\nPipelines”,     13),
(“Cyber Anomaly\nDetection (CAD)”,        “Real-Time\nData Fusion”,          11),
]

# Capability → LOE

cap_to_loe = [
(“Machine Learning\nPipelines”,     “Warfighter\nReadiness”,    22),
(“Machine Learning\nPipelines”,     “Modernize the\nForce”,     0),  # placeholder, resolved at LOE→Pri
(“Geospatial\nIntelligence”,        “Information\nAdvantage”,   26),
(“Geospatial\nIntelligence”,        “Global SOF\nNetwork”,      18),
(“Predictive\nAnalytics”,           “Warfighter\nReadiness”,    16),
(“Predictive\nAnalytics”,           “Integrated\nDeterrence”,   10),
(“Real-Time\nData Fusion”,          “Information\nAdvantage”,   20),
(“Real-Time\nData Fusion”,          “Integrated\nDeterrence”,   20),
(“NLP / Text\nAnalytics”,           “Information\nAdvantage”,   15),
(“NLP / Text\nAnalytics”,           “Global SOF\nNetwork”,      10),
(“Decision Support\nDashboards”,    “Warfighter\nReadiness”,    14),
(“Decision Support\nDashboards”,    “Global SOF\nNetwork”,      19),
]

# LOE → CDR Priority

loe_to_pri = [
(“Warfighter\nReadiness”,   “Sustain Lethality &\nReadiness”,           30),
(“Warfighter\nReadiness”,   “Prepare SOF for\nGreat Power Competition”, 22),
(“Global SOF\nNetwork”,     “Strengthen Alliances\n& Partnerships”,     28),
(“Global SOF\nNetwork”,     “Prepare SOF for\nGreat Power Competition”, 19),
(“Information\nAdvantage”,  “Prepare SOF for\nGreat Power Competition”, 25),
(“Information\nAdvantage”,  “Modernize the\nForce”,                     36),
(“Integrated\nDeterrence”,  “Prepare SOF for\nGreat Power Competition”, 18),
(“Integrated\nDeterrence”,  “Sustain Lethality &\nReadiness”,           12),
]

# Remove placeholder

cap_to_loe = [(a, b, v) for a, b, v in cap_to_loe if v > 0]

# ─────────────────────────────────────────────

# BUILD SANKEY ARRAYS

# ─────────────────────────────────────────────

sources, targets, values, link_labels = [], [], [], []

for uc, cap, val in uc_to_cap:
sources.append(uc_idx[uc])
targets.append(cap_idx[cap])
values.append(val)
link_labels.append(f”{uc.split(chr(10))[0]} → {cap.split(chr(10))[0]}: {val} units”)

for cap, loe, val in cap_to_loe:
sources.append(cap_idx[cap])
targets.append(loe_idx[loe])
values.append(val)
link_labels.append(f”{cap.split(chr(10))[0]} → {loe.split(chr(10))[0]}: {val} units”)

for loe, pri, val in loe_to_pri:
sources.append(loe_idx[loe])
targets.append(pri_idx[pri])
values.append(val)
link_labels.append(f”{loe.split(chr(10))[0]} → {pri.split(chr(10))[0]}: {val} units”)

# ─────────────────────────────────────────────

# NODE COLORS BY LAYER

# ─────────────────────────────────────────────

uc_color   = “rgba(79, 195, 247, 0.85)”    # steel blue
cap_color  = “rgba(31, 138, 76, 0.85)”     # SOF green
loe_color  = “rgba(255, 167, 38, 0.85)”    # amber
pri_color  = “rgba(239, 83, 80, 0.85)”     # command red

node_colors = (
[uc_color]  * len(USE_CASES) +
[cap_color] * len(CAPABILITIES) +
[loe_color] * len(LOE) +
[pri_color] * len(CDR_PRIORITIES)
)

# Link colors follow source node layer

link_colors = []
for s in sources:
if s < len(USE_CASES):
link_colors.append(“rgba(79, 195, 247, 0.25)”)
elif s < len(USE_CASES) + len(CAPABILITIES):
link_colors.append(“rgba(31, 138, 76, 0.25)”)
else:
link_colors.append(“rgba(255, 167, 38, 0.25)”)

# ─────────────────────────────────────────────

# SIDEBAR CONTROLS

# ─────────────────────────────────────────────

with st.sidebar:
st.markdown(’<div class="section-label">// Display Options</div>’, unsafe_allow_html=True)
node_pad   = st.slider(“Node Padding”, 10, 40, 20)
node_thick = st.slider(“Node Thickness”, 10, 40, 22)
chart_h    = st.slider(“Chart Height (px)”, 500, 1000, 720)
show_table = st.checkbox(“Show Flow Data Table”, value=False)

```
st.markdown("---")
st.markdown('<div class="section-label">// Legend</div>', unsafe_allow_html=True)
st.markdown("""
<div style='font-family: Rajdhani; font-size:0.82rem; line-height:1.8;'>
  <span style='color:#4fc3f7'>■</span> CDAO Use Cases<br>
  <span style='color:#1f8a4c'>■</span> Data & Analytics Capabilities<br>
  <span style='color:#ffa726'>■</span> Lines of Effort<br>
  <span style='color:#ef5350'>■</span> CDR Strategic Priorities
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="font-family:Share Tech Mono; font-size:0.65rem; color:#4a6a7a; letter-spacing:0.12em;">UNCLASSIFIED // FOUO<br>NOT FOR PUBLIC RELEASE</div>', unsafe_allow_html=True)
```

# ─────────────────────────────────────────────

# METRICS ROW

# ─────────────────────────────────────────────

total_flow     = sum(v for _, _, v in loe_to_pri)
n_use_cases    = len(USE_CASES)
n_capabilities = len(CAPABILITIES)
n_loe          = len(LOE)
n_priorities   = len(CDR_PRIORITIES)

col1, col2, col3, col4 = st.columns(4)
with col1:
st.markdown(f’<div class="metric-card"><div class="metric-val">{n_use_cases}</div><div class="metric-lbl">CDAO Use Cases</div></div>’, unsafe_allow_html=True)
with col2:
st.markdown(f’<div class="metric-card"><div class="metric-val">{n_capabilities}</div><div class="metric-lbl">Analytics Capabilities</div></div>’, unsafe_allow_html=True)
with col3:
st.markdown(f’<div class="metric-card"><div class="metric-val">{n_loe}</div><div class="metric-lbl">Lines of Effort</div></div>’, unsafe_allow_html=True)
with col4:
st.markdown(f’<div class="metric-card"><div class="metric-val">{total_flow}</div><div class="metric-lbl">Total Effort Units Mapped</div></div>’, unsafe_allow_html=True)

# ─────────────────────────────────────────────

# SANKEY FIGURE

# ─────────────────────────────────────────────

fig = go.Figure(go.Sankey(
arrangement=“snap”,
node=dict(
pad=node_pad,
thickness=node_thick,
line=dict(color=”#0a0e14”, width=0.8),
label=[n.replace(”\n”, “ “) for n in all_nodes],
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
text=(
“<b>CDAO USE CASE FLOW → SOCOM CDR STRATEGIC PRIORITIES</b><br>”
“<sup style='color:#8aabb8'>Resource/Effort Units | AY2025 Mock Data | UNCLASSIFIED // FOUO</sup>”
),
font=dict(family=“Share Tech Mono, monospace”, size=14, color=”#4fc3f7”),
x=0.02,
xanchor=“left”,
),
)

st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────

# OPTIONAL FLOW DATA TABLE

# ─────────────────────────────────────────────

if show_table:
st.markdown(’<div class="section-label" style="margin-top:24px;">// Raw Flow Data</div>’, unsafe_allow_html=True)

```
rows = []
for uc, cap, val in uc_to_cap:
    rows.append({"Layer": "Use Case → Capability",
                 "Source": uc.replace("\n", " "),
                 "Target": cap.replace("\n", " "),
                 "Effort Units": val})
for cap, loe, val in cap_to_loe:
    rows.append({"Layer": "Capability → LOE",
                 "Source": cap.replace("\n", " "),
                 "Target": loe.replace("\n", " "),
                 "Effort Units": val})
for loe, pri, val in loe_to_pri:
    rows.append({"Layer": "LOE → CDR Priority",
                 "Source": loe.replace("\n", " "),
                 "Target": pri.replace("\n", " "),
                 "Effort Units": val})

df = pd.DataFrame(rows)
st.dataframe(
    df.style.set_properties(**{
        "background-color": "#0d1b2a",
        "color": "#c8d6e5",
        "border": "1px solid #1a3a5c",
    }),
    use_container_width=True,
    hide_index=True,
)
```

# ─────────────────────────────────────────────

# FOOTER

# ─────────────────────────────────────────────

st.markdown(”—”)
st.markdown(
‘<div style="font-family:Share Tech Mono; font-size:0.65rem; color:#4a6a7a; '
'letter-spacing:0.12em; text-align:center; padding:8px 0;">’
’UNCLASSIFIED // FOR OFFICIAL USE ONLY  |  ’
’USSOCOM J6 / CDAO Data & Analytics  |  ’
‘NOT FOR PUBLIC RELEASE’
‘</div>’,
unsafe_allow_html=True,
)