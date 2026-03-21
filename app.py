import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="AI Breakout Terminal", page_icon="💻", layout="wide")

# -----------------------
# 🔥 HACKER UI STYLE
# -----------------------
st.markdown("""
<style>
.stApp { background-color: #05070d; }
html, body, [class*="css"] {
    font-family: 'Courier New', monospace;
    color: #00ff9f;
}
h1, h2, h3 {
    color: #00ff9f;
    text-shadow: 0 0 12px #00ff9f;
}
[data-testid="stMetric"] {
    background-color: #0a0f1c;
    border: 1px solid #00ff9f;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 0 10px #00ff9f33;
}
section[data-testid="stSidebar"] {
    background-color: #04060a;
    border-right: 1px solid #00ff9f;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown("""
# 💻 AI BREAKOUT TERMINAL  
### YC STARTUP SIGNAL INTERCEPTION SYSTEM  
`STATUS: SCANNING FOR NEXT BILLION DOLLAR COMPANY...`
---
""")

# -----------------------
# DATA
# -----------------------
data = [
    {"name": "Perplexity AI", "sector": "Search", "batch": "W22", "growth": 90, "execution": 85, "capital": 80},
    {"name": "Scale AI", "sector": "Infra", "batch": "S16", "growth": 75, "execution": 95, "capital": 100},
    {"name": "Runway ML", "sector": "GenAI", "batch": "S18", "growth": 95, "execution": 90, "capital": 85},
    {"name": "Replit", "sector": "DevTools", "batch": "W18", "growth": 70, "execution": 75, "capital": 65},
    {"name": "LangChain", "sector": "Infra", "batch": "S23", "growth": 100, "execution": 80, "capital": 60},
    {"name": "Adept AI", "sector": "Agents", "batch": "Alumni", "growth": 85, "execution": 78, "capital": 90},
    {"name": "Cognition", "sector": "Coding", "batch": "S23", "growth": 100, "execution": 95, "capital": 70},
    {"name": "Pika Labs", "sector": "GenAI", "batch": "W24", "growth": 92, "execution": 82, "capital": 65},
]

df = pd.DataFrame(data)

# -----------------------
# SIMPLE + CLEAN SCORE
# -----------------------
df["momentum"] = (
    df["growth"] * 0.4 +
    df["execution"] * 0.4 +
    df["capital"] * 0.2
)

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.markdown("## ⚙️ FILTER SYSTEM")

sector = st.sidebar.selectbox("Sector", ["All"] + list(df["sector"].unique()))

filtered = df.copy()

if sector != "All":
    filtered = filtered[filtered["sector"] == sector]

# -----------------------
# METRICS (CLEAN)
# -----------------------
c1, c2, c3 = st.columns(3)

c1.metric("📡 STARTUPS", len(filtered))
c2.metric("⚡ TOP SIGNAL", int(filtered["momentum"].max()))
c3.metric("🧠 AVG SIGNAL", int(filtered["momentum"].mean()))

# -----------------------
# COLOR SYSTEM
# -----------------------
colors = ["#00ff9f", "#00eaff", "#ff00ff", "#ffaa00"]

# -----------------------
# MAIN VISUAL (EASY TO READ)
# -----------------------
st.markdown("## 📊 SIGNAL MAP")

bubble = px.scatter(
    filtered,
    x="growth",
    y="execution",
    size="momentum",
    color="sector",
    text="name",
    color_discrete_sequence=colors
)

bubble.update_traces(
    marker=dict(line=dict(width=1, color="#00ff9f"))
)

bubble.update_layout(
    template="plotly_dark",
    paper_bgcolor="#05070d",
    plot_bgcolor="#05070d",
    font=dict(color="#00ff9f"),
    height=550,
)

st.plotly_chart(bubble, use_container_width=True)

# -----------------------
# HYPE VS REALITY
# -----------------------
st.markdown("## ⚠️ HYPE VS EXECUTION")

hype = px.scatter(
    filtered,
    x="capital",
    y="execution",
    size="momentum",
    text="name",
    color="sector",
    color_discrete_sequence=colors
)

hype.update_layout(
    template="plotly_dark",
    paper_bgcolor="#05070d",
    plot_bgcolor="#05070d",
    font=dict(color="#00ff9f"),
)

st.plotly_chart(hype, use_container_width=True)

# -----------------------
# LEADERBOARD (SUPER CLEAN)
# -----------------------
st.markdown("## 🏆 LEADERBOARD")

leader = px.bar(
    filtered.sort_values("momentum"),
    x="momentum",
    y="name",
    orientation="h",
    color="sector",
    color_discrete_sequence=colors
)

leader.update_layout(
    template="plotly_dark",
    paper_bgcolor="#05070d",
    plot_bgcolor="#05070d",
    font=dict(color="#00ff9f"),
)

st.plotly_chart(leader, use_container_width=True)

# -----------------------
# INSIGHT ENGINE (🔥)
# -----------------------
st.markdown("## 🧠 SIGNAL ANALYSIS")

top = filtered.sort_values("momentum", ascending=False).iloc[0]
weak = filtered.sort_values("momentum").iloc[0]

st.markdown(f"""
🚀 **TARGET LOCKED:** {top['name']}  
- High growth + execution  
- Strong breakout potential  

⚠️ **WEAK SIGNAL:** {weak['name']}  
- Low momentum detected  
- Monitor or avoid  

🧬 **SYSTEM NOTE:**  
Momentum spikes often happen BEFORE funding rounds.
""")

# -----------------------
# DATA TABLE (CLEAN)
# -----------------------
st.markdown("## 📡 DATABASE")

st.dataframe(filtered.sort_values("momentum", ascending=False), use_container_width=True)
