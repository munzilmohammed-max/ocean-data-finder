import streamlit as st
import pandas as pd
from pathlib import Path

# --- Page Config ---
st.set_page_config(page_title="Search Data", layout="wide")

# --- Data location -----------------------------------------------------------
# Path built relative to the repo, so it works locally AND on Streamlit Cloud.
# pages/ is one level below the repo root, so go up one (.parent.parent).
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "Ocean_Open_Data_Finder.xlsx"
GLOBAL_SHEET = "GLOBAL_DATASETS"
INDIAN_OCEAN_SHEET = "INDIAN_OCEAN_DATASETS"


@st.cache_data
def load_data(scope: str = "Global"):
    sheet = INDIAN_OCEAN_SHEET if scope == "Indian Ocean" else GLOBAL_SHEET
    df = pd.read_excel(DATA_FILE, sheet_name=sheet)
    df.columns = [c.strip() for c in df.columns]
    return df


st.title("🔍 Search Ocean Data")

# --- Coverage toggle (Global vs Indian Ocean) ---
scope = st.sidebar.radio(
    "🌐 Coverage",
    ["Global", "Indian Ocean"],
    help="Global = all datasets. Indian Ocean = regional subset only.",
)
df = load_data(scope)

# --- Quick search ---
search_text = st.text_input("🔎 Quick search (e.g. oxygen, ssh, chlorophyll, monsoon)")

# --- Sidebar Filters ---
st.sidebar.header("Filters")

variable = st.sidebar.selectbox("Variable", ["All"] + sorted(df["Variable"].dropna().unique()))
region = st.sidebar.selectbox("Region", ["All"] + sorted(df["Region"].dropna().unique()))
platform = st.sidebar.selectbox("Platform", ["All"] + sorted(df["Platform"].dropna().unique()))


def optional_filter(label, column):
    if column in df.columns:
        return st.sidebar.selectbox(label, ["All"] + sorted(df[column].dropna().unique()))
    return "All"


skill = optional_filter("Skill Level", "Skill_Level")
latency = optional_filter("Latency", "Latency")
login = optional_filter("Login Required", "Login_Required")

# --- Comparison Feature ---
st.sidebar.markdown("---")
st.sidebar.subheader("⚖️ Compare Datasets")
compare_list = st.sidebar.multiselect("Select datasets", df["Dataset_Name"].unique())

# --- Filtering ---
filtered = df.copy()

if search_text:
    search_cols = [c for c in ["Dataset_Name", "Variable", "Tags", "Use_Case"] if c in df.columns]
    mask = pd.Series(False, index=filtered.index)
    for c in search_cols:
        mask |= filtered[c].astype(str).str.contains(search_text, case=False, na=False)
    filtered = filtered[mask]

if variable != "All":
    filtered = filtered[filtered["Variable"] == variable]
if region != "All":
    filtered = filtered[filtered["Region"] == region]
if platform != "All":
    filtered = filtered[filtered["Platform"] == platform]
if skill != "All" and "Skill_Level" in df.columns:
    filtered = filtered[filtered["Skill_Level"] == skill]
if latency != "All" and "Latency" in df.columns:
    filtered = filtered[filtered["Latency"] == latency]
if login != "All" and "Login_Required" in df.columns:
    filtered = filtered[filtered["Login_Required"] == login]

filtered = filtered.sort_values(by="Dataset_Name")

# --- Results count ---
st.info(f"{len(filtered)} datasets found  ·  Coverage: {scope}")


# --- Icon Function ---
def get_icon(variable):
    var = str(variable).lower()
    if "temp" in var or "sst" in var:
        return "🌡️"
    elif "sal" in var or "sss" in var:
        return "🧂"
    elif "chl" in var or "phyto" in var:
        return "🌿"
    elif "oxygen" in var:
        return "🫧"
    elif "nitr" in var or "nutri" in var:
        return "🧪"
    elif "current" in var or "ssh" in var or "wave" in var:
        return "🌊"
    elif "ice" in var:
        return "❄️"
    elif "carbon" in var or "co2" in var:
        return "♻️"
    elif "bio" in var or "plankton" in var or "fish" in var:
        return "🐟"
    else:
        return "📊"


def field(row, col):
    return col in row.index and pd.notna(row[col]) and str(row[col]).strip() != ""


# --- GRID LAYOUT (2 columns) ---
cols = st.columns(2)

for i, (_, row) in enumerate(filtered.iterrows()):
    col = cols[i % 2]
    with col:
        with st.container(border=True):
            icon = get_icon(row["Variable"])
            st.markdown(f"### {icon} {row['Dataset_Name']}")

            badges = []
            if field(row, "Skill_Level"):
                badges.append(f"🎓 {row['Skill_Level']}")
            if field(row, "Latency"):
                badges.append(f"⏱️ {row['Latency']}")
            if field(row, "Login_Required") and str(row["Login_Required"]).lower() == "yes":
                badges.append("🔑 Login")
            if badges:
                st.caption("  ·  ".join(badges))

            st.write(f"**Source:** {row['Source']}")
            st.write(f"**Resolution:** {row['Spatial_Resolution']}")
            st.write(f"**Time:** {row['Time_Coverage']}")
            st.write(f"**Region:** {row['Region']}")
            st.write(f"**Platform:** {row['Platform']}")
            st.write(f"**Format:** {row['Format']}")

            with st.expander("📊 More Details"):
                if field(row, "Use_Case"):
                    st.write(f"**Use Case:** {row['Use_Case']}")
                if field(row, "Depth"):
                    st.write(f"**Depth:** {row['Depth']}")
                if field(row, "Temporal_Resolution"):
                    st.write(f"**Temporal Res:** {row['Temporal_Resolution']}")
                if field(row, "Update_Frequency"):
                    st.write(f"**Update Frequency:** {row['Update_Frequency']}")
                if field(row, "Tools"):
                    st.write(f"**Suggested tools:** {row['Tools']}")
                if field(row, "License"):
                    st.write(f"**License:** {row['License']}")
                if field(row, "DOI"):
                    st.write(f"**DOI:** {row['DOI']}")
                if field(row, "Citation"):
                    st.write(f"**Citation:** {row['Citation']}")
                if field(row, "Link_Checked"):
                    st.write(f"**Link last recorded:** {row['Link_Checked']}")
                if field(row, "Notes"):
                    st.write(f"**Notes:** {row['Notes']}")

            if field(row, "Link"):
                st.markdown(f"[🔗 Open Dataset]({row['Link']})")

# --- Comparison Output ---
if len(compare_list) >= 2:
    st.markdown("## ⚖️ Dataset Comparison")
    compare_cols = [c for c in [
        "Dataset_Name", "Variable", "Source", "Spatial_Resolution",
        "Temporal_Resolution", "Region", "Platform", "Skill_Level",
        "Latency", "Login_Required", "License"
    ] if c in df.columns]
    compare_df = df[df["Dataset_Name"].isin(compare_list)]
    st.dataframe(compare_df[compare_cols], use_container_width=True)

# --- Empty ---
if len(filtered) == 0:
    st.warning("No datasets found. Try clearing a filter or the search box.")
