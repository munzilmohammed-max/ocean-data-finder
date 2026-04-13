import streamlit as st
import pandas as pd

st.set_page_config(page_title="Search Data", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("data/Ocean_Open_Data_Template.xlsx")

df = load_data()

st.title("🔍 Search Ocean Data")

# --- Search ---
search_text = st.text_input("🔎 Quick search (oxygen, ssh, chlorophyll)")

# --- Sidebar Filters ---
st.sidebar.header("Filters")

variable = st.sidebar.selectbox(
    "Variable",
    sorted(df["Variable"].dropna().unique())
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["Region"].dropna().unique())
)

platform = st.sidebar.selectbox(
    "Platform",
    ["All"] + sorted(df["Platform"].dropna().unique())
)

# --- Filtering ---
if search_text:
    filtered = df[df["Variable"].str.contains(search_text, case=False, na=False)]
else:
    filtered = df[df["Variable"] == variable]

if region != "All":
    filtered = filtered[filtered["Region"] == region]

if platform != "All":
    filtered = filtered[filtered["Platform"] == platform]

filtered = filtered.sort_values(by="Dataset_Name")

# --- Results ---
st.info(f"{len(filtered)} datasets found")

# --- Cards ---
for _, row in filtered.iterrows():
    with st.container():
        st.markdown(f"### 🌊 **{row['Dataset_Name']}**")

        col1, col2, col3 = st.columns(3)
        col1.write(f"**Source:** {row['Source']}")
        col2.write(f"**Resolution:** {row['Spatial_Resolution']}")
        col3.write(f"**Time:** {row['Time_Coverage']}")

        st.write(f"**Region:** {row['Region']}")
        st.write(f"**Platform:** {row['Platform']}")

        st.markdown(f"[🔗 Open Dataset]({row['Link']})")

        st.divider()

if len(filtered) == 0:
    st.warning("No datasets found.")
