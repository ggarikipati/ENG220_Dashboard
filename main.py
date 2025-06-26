# main.py
from st_pages import Page, show_pages_from_config

# Show pages from config
show_pages_from_config(".streamlit/pages_sections.toml")

# You don't need pg.run() here — the navigation will handle it.
