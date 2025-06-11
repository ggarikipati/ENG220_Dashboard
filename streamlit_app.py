import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

# Set wide layout and page title
st.title("ENG220-Dashboard (Fall2024)")

# Sidebar toggle to show grouped or flat navigation
use_sections = st.sidebar.toggle("Group by Sections", value=True)

# Load navigation from the TOML file
nav = get_nav_from_toml(
    ".streamlit/pages_sections.toml" if use_sections else ".streamlit/pages.toml"
)

# Optional logo (commented out if not using one)
# st.logo("assets/logo.png")

# Create the navigation object
pg = st.navigation(nav)

# Add the title and icon from the selected page
add_page_title(pg)

# Show dashboard introduction if on the home page
if pg.title == "🏠 Dashboard Home":
    st.markdown("""
    # ENG220 Combined Project Dashboard

    Welcome to the **ENG220 Project Showcase** 🎓  
    This dashboard integrates all 21 ENG220 group projects for centralized viewing.

    ## 🔍 How to Use:
    - Use the **sidebar** to browse through the 21 ENG220 group projects.
    - Each group is listed in order (Group 001 to Group 021).
    - Some groups (like 013, 019, 020) contain multiple subpages.

    ## 📘 What You’ll Find:
    - Environmental & water data analysis
    - Regional policy evaluations
    - Interactive visual dashboards

    ---
    Select a project from the sidebar to get started!
    """)
else:
    # Run the selected project/subpage
    pg.run()
