import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

# Sidebar toggle rendered once
use_sections = st.sidebar.toggle("Group by Sections", value=True, key="use_sections_toggle_main")

# Load navigation only once based on toggle
nav = get_nav_from_toml(
    ".streamlit/pages_sections.toml" if use_sections else ".streamlit/pages.toml"
)

# Create navigation once
pg = st.navigation(nav)

# Add page title/icon
add_page_title(pg)

# Home page content (based on name from TOML)
if pg.title == "Dashboard Home":
    st.markdown("""
    # ENG220 Combined Project Dashboard Fall 2024

    Welcome to the **ENG220 Project Showcase** 🎓  
    This dashboard integrates all 21 ENG220 group projects for centralized viewing.

    ## How to Use:
    - Use the **sidebar** to browse through the 21 ENG220 group projects.
    - Each group is listed in order (Group 001 to Group 021).
    - Some groups contain multiple subpages.

    ## What You’ll Find:
    - Environmental & water data analysis
    - Regional policy evaluations
    - Interactive visual dashboards

    ### Professor: Dr. Ramiro Jordan
    Teaching Assistants
    - Chadi Harmouche
    - Gnanitha Garikipati
    - Rishitha Kondrolla

    ---
    Select a project from the sidebar to get started!
    """)
else:
    pg.run()
