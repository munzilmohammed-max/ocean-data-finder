import streamlit as st

st.set_page_config(page_title="About", layout="wide")

st.title("ℹ️ About This Tool")

st.markdown("""
### 🌊 Ocean Data Finder

This platform helps researchers quickly discover open ocean datasets by variable,
region, and skill level, reducing the time required to locate relevant data sources.

---

### 🎯 Purpose
- Reduce time spent searching for ocean datasets
- Provide centralized access to multiple global data sources
- Support early career researchers in ocean science

---

### 🧭 How to use
- **Search** — type a keyword or filter by variable, region, platform, skill level,
  latency, and login requirement.
- **Browse** — view the full table, pick columns, and download your filtered view as CSV.
- **Coverage toggle** (in the sidebar) — switch between *Global* (all datasets) and
  *Indian Ocean* (regional subset only).

---

### 🌍 Data Sources
Datasets span physics, biogeochemistry, biology/ecology, and cryosphere, from providers
including:

- NASA (PO.DAAC, Earthdata, PACE)
- NOAA (NCEI, PMEL, CoastWatch)
- Copernicus Marine Service (CMEMS) & ECMWF
- Argo & BGC-Argo
- ESA (Sentinel missions, CryoSat-2)
- Asia-Pacific Data Research Center (APDRC)
- INCOIS (TropFlux, regional products)
- Community archives: GLODAP, SOCAT, OBIS, EMODnet, IMOS, IOOS, OceanSITES

---

### 👨‍🔬 Developed By

**Munzil Mohammed**
Senior Research Fellow

Developed as part of efforts under the Early Career Ocean Professionals (ECOP)
initiative to improve accessibility and usability of open ocean data.

---

### 🌐 Affiliation
- ECOP India
- UN Ocean Decade (Ocean Decade Framework)

---

### 📌 Note
This platform is a data **discovery** tool. The `Link_Checked` dates indicate when a
link was last recorded, not an automated live-check — always refer to the original data
providers for current documentation, versioning, DOIs, and appropriate usage.
""")
