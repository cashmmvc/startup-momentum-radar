import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Startup Momentum Radar", page_icon="🚀", layout="wide")

st.title("Ai Startup Momentum Radar")
st.write("A simple VC-style dashboard that tracks ai startup momentum.")

# -----------------------
# Sample startup data
# -----------------------
data = data = [
    {"name": "Perplexity AI", "sector": "AI Search", "batch": "YC W22", "website_growth": 45, "hiring_growth": 35, "social_growth": 50, "funding_millions": 25},
    {"name": "Scale AI", "sector": "AI Infrastructure", "batch": "YC S16", "website_growth": 38, "hiring_growth": 40, "social_growth": 42, "funding_millions": 100},
    {"name": "Runway ML", "sector": "Generative AI", "batch": "YC S18", "website_growth": 50, "hiring_growth": 45, "social_growth": 60, "funding_millions": 75},
    {"name": "Replit", "sector": "AI DevTools", "batch": "YC W18", "website_growth": 35, "hiring_growth": 30, "social_growth": 33, "funding_millions": 20},
    {"name": "LangChain", "sector": "AI Infrastructure", "batch": "YC S23", "website_growth": 55, "hiring_growth": 42, "social_growth": 65, "funding_millions": 10},
    {"name": "Adept AI", "sector": "AI Agents", "batch": "YC Alumni", "website_growth": 48, "hiring_growth": 38, "social_growth": 55, "funding_millions": 65},
    {"name": "Cognition Labs", "sector": "AI Coding", "batch": "YC S23", "website_growth": 60, "hiring_growth": 50, "social_growth": 70, "funding_millions": 21},
    {"name": "Pika Labs", "sector": "Generative AI", "batch": "YC W24", "website_growth": 52, "hiring_growth": 36, "social_growth": 58, "funding_millions": 12},
]

df = pd.DataFrame(data)

def norm(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-9)

df["momentum_score"] = (
    norm(df["website_growth"]) * 35 +
    norm(df["hiring_growth"]) * 30 +
    norm(df["social_growth"]) * 20 +
    norm(df["funding_millions"]) * 15
).round(1)

# -----------------------
# Fake trend data
# -----------------------
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
rng = np.random.default_rng(42)
rows = []

for _, row in df.iterrows():
    base = float(row["momentum_score"]) - 8
    slope = rng.uniform(1.5, 4.5)
    noise = rng.normal(0, 1.5, size=len(months))

    for i, month in enumerate(months):
        score = max(0, base + slope * i + noise[i])
        rows.append({
            "Month": month,
            "Startup": row["name"],
            "Sector": row["sector"],
            "Score": round(score, 1)
        })

trend_df = pd.DataFrame(rows)

# -----------------------
# Sidebar filters
# -----------------------
st.sidebar.header("Filters")
sector_choice = st.sidebar.selectbox("Sector", ["All"] + sorted(df["sector"].unique().tolist()))
min_score = st.sidebar.slider("Minimum momentum score", 0.0, float(df["momentum_score"].max()), 0.0, 1.0)

filtered = df.copy()

if sector_choice != "All":
    filtered = filtered[filtered["sector"] == sector_choice]

filtered = filtered[filtered["momentum_score"] >= min_score]

if filtered.empty:
    st.warning("No startups match your filters.")
    st.stop()

# -----------------------
# Top metrics
# -----------------------
c1, c2, c3 = st.columns(3)
c1.metric("Startups shown", len(filtered))
c2.metric("Highest score", f"{filtered['momentum_score'].max():.1f}")
c3.metric("Average score", f"{filtered['momentum_score'].mean():.1f}")

# -----------------------
# Charts
# -----------------------
bubble = px.scatter(
    filtered,
    x="website_growth",
    y="hiring_growth",
    size="momentum_score",
    color="sector",
    hover_name="name",
    text="name",
    size_max=55,
    title="Momentum Map: Website Growth vs Hiring Growth"
)
bubble.update_traces(textposition="top center")
bubble.update_layout(height=550, legend_title_text="Sector")

trend_filtered = trend_df[trend_df["Startup"].isin(filtered["name"])]

line = px.line(
    trend_filtered,
    x="Month",
    y="Score",
    color="Startup",
    markers=True,
    category_orders={"Month": months},
    title="Momentum Over Time"
)
line.update_layout(height=550)

leaderboard = px.bar(
    filtered.sort_values("momentum_score", ascending=True),
    x="momentum_score",
    y="name",
    color="sector",
    orientation="h",
    title="Leaderboard"
)
leaderboard.update_layout(height=500, yaxis_title="")

treemap = px.treemap(
    filtered,
    path=["sector", "name"],
    values="momentum_score",
    color="momentum_score",
    title="Momentum by Sector"
)
treemap.update_layout(height=500)

left, right = st.columns(2)
with left:
    st.plotly_chart(bubble, use_container_width=True)
with right:
    st.plotly_chart(line, use_container_width=True)

left2, right2 = st.columns(2)
with left2:
    st.plotly_chart(leaderboard, use_container_width=True)
with right2:
    st.plotly_chart(treemap, use_container_width=True)

st.subheader("Startup table")
st.dataframe(
    filtered.sort_values("momentum_score", ascending=False),
    use_container_width=True
)
