import streamlit as st
import pandas as pd
import plotly.express as px

# Load the datasets
df_state = pd.read_csv("datasets/state_wise_jobs.csv")
df_org = pd.read_csv("datasets/organisation_wise_jobs.csv")
df_qual = pd.read_csv("datasets/qualification_wise_jobs.csv")
df_sector = pd.read_csv("datasets/sector_wise_jobs.csv")

# Mapping for easy selection
datasets = {
    "State-wise": {"data": df_state, "category_col": "State"},
    "Organisation-wise": {"data": df_org, "category_col": "Organisation Type"},
    "Qualification-wise": {"data": df_qual, "category_col": "Qualification"},
    "Sector-wise": {"data": df_sector, "category_col": "Sector"},
}

st.title("🔍 KaamRadar - Smart Job Finder")

# Step 1: Ask for basis of job search
basis = st.selectbox("On what basis do you want to find a job?", list(datasets.keys()))

if basis:
    df = datasets[basis]["data"]
    category_col = datasets[basis]["category_col"]

    # Step 2: Ask for category (State / Org / Qual / Sector)
    options = sorted(df[category_col].dropna().unique())
    selected = st.selectbox(f"Select {category_col}:", options)

    if selected:
        st.subheader(f"📍 Job Info for {selected} ({basis})")

        # Filter by selected category
        filtered = df[df[category_col] == selected]
        total_jobs = filtered.iloc[0, 1]  # Second column contains the total

        st.write(f"✅ Total jobs in **{selected}**: **{int(total_jobs):,}**")

        # Top 5 by job count
        st.markdown("---")
        st.subheader(f"Top 5 by {category_col}")
        top5 = df.sort_values(df.columns[1], ascending=False).head(5)
        st.dataframe(top5)

        # Optional: bar chart
        fig = px.bar(top5, x=category_col, y=top5.columns[1], title=f"Top 5 {category_col}s by Job Count")
        st.plotly_chart(fig)
