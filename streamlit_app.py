import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

# Set page layout and title

st.title("ENG220-Dashboard (Fall2024)")

# ✅ Unique key avoids StreamlitDuplicateElementId error
use_sections = st.sidebar.toggle("Group by Sections", value=True, key="toggle_sections")

# Load navigation based on toggle state
nav = get_nav_from_toml(
    ".streamlit/pages_sections.toml" if use_sections else ".streamlit/pages.toml"
)

# Initialize navigation
pg = st.navigation(nav)

# Add dynamic page title & icon from current selection
add_page_title(pg)

# Show home dashboard content if on home
if pg.title == "🏠 Dashboard Home":
    st.markdown("""
    # ENG220 Combined Project Dashboard

    Welcome to the **ENG220 Project Showcase** 🎓  
    This dashboard integrates all 21 ENG220 group projects for centralized viewing.

    ## 🔍 How to Use:
    - Use the **sidebar** to browse through the 21 ENG220 group projects.
    - Each group is listed in order (Group 001 to Group 021).
    - Some groups (like 013, 019, 020, 021) contain multiple visualizations.

    ## 📘 What You’ll Find:
    - Environmental & water data analysis
    - Regional policy evaluations
    - Interactive visual dashboards

    ---
    👉 Select a project from the sidebar to get started!
    """)
else:
    # Run the selected project or subpage
    pg.run()
