import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="ASKverse Youth Tracker", layout="wide")
st.title("ASKverse Youth Skill Tracker")
st.markdown("*Find collaborators. Build the future. Powered by AppliedAncients × Grok.*")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/youth_skills.csv')
df = load_data()

# Filters
col1, col2 = st.columns([1, 3])
with col1:
    st.subheader("Filters")
    skill = st.selectbox("Skill", ["All"] + sorted(df['skill'].unique()))
    city = st.selectbox("City", ["All"] + sorted(df['city'].unique()))

filtered = df.copy()
if skill != "All": filtered = filtered[filtered['skill'] == skill]
if city != "All": filtered = filtered[filtered['city'] == city]

# Map + Table
with col2:
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    for _, row in filtered.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=10,
            popup=f"<b>{row['name']}</b><br>{row['skill']}<br>{row['city']}",
            color="#0b6d6d"
        ).add_to(m)
    st_folium(m, height=500)

st.write(f"**Found {len(filtered)} youth**")
st.dataframe(filtered[['name', 'skill', 'city']], use_container_width=True)
