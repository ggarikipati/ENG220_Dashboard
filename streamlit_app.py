import streamlit as st
import uuid
from st_pages import add_page_title, get_nav_from_toml

# Set layout and dashboard title
st.set_page_config(page_title="ENG220 Unified Dashboard", layout="wide")
st.title("ENG220-Dashboard (Fall2024)")

# Avoid StreamlitDuplicateElementKey by using UUID
unique_toggle_key = f"toggle_sections_{uuid.uuid4()}"
use_sections = st.sidebar.toggle("Group by Sections", value=True, key=unique_toggle_key)

# Load navigation from correct TOML
nav = get_nav_from_toml(
    ".streamlit/pages_sections.toml" if use_sections else ".streamlit/pages.toml"
)

# Navigation system
pg = st.navigation(nav)
add_page_title(pg)

# Home page content
if pg.title == "🏠 Dashboard Home":
    st.markdown("""
    # ENG220 Combined Project Dashboard

    Welcome to the **ENG220 Project Showcase** 🎓  
    This dashboard integrates all 21 ENG220 group projects for centralized viewing.

    ## How to Use:
    - Use the **sidebar** to browse through the 21 ENG220 group projects.
    - Some groups (like 013, 019, 020, 021) include multiple interactive visualizations.

    ## What You’ll Find:
    - Environmental & water data analysis
    - Regional policy evaluations
    - Interactive visual dashboards

    ---
    Select a project from the sidebar to get started!
    """)
else:
    # Run selected page
    pg.run()
