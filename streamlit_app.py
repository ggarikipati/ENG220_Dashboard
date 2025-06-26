
import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

# Set wide layout and page title

# Sidebar toggle to show grouped or flat navigation
use_sections = st.sidebar.toggle("Group by Sections", value=True, key="use_sections_toggle")

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


pg.run()
