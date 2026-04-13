import streamlit as st
import pandas as pd

st.set_page_config(page_title="Browse Data", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("data/Ocean_Open_Data_Master_APDRC_Added.xlsx")

df = load_data()

st.title("📊 Browse All Datasets")

# --- Filters ---
col1, col2 = st.columns(2)

variable = col1.selectbox(
    "Variable",
    ["All"] + sorted(df["Variable"].dropna().unique())
)

region = col2.selectbox(
    "Region",
    ["All"] + sorted(df["Region"].dropna().unique())
)

# --- Filtering ---
filtered = df.copy()

if variable != "All":
    filtered = filtered[filtered["Variable"] == variable]

if region != "All":
    filtered = filtered[filtered["Region"] == region]

# --- Table ---
st.dataframe(filtered, use_container_width=True)

st.info(f"{len(filtered)} datasets displayed")
