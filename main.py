import streamlit as st
import importlib.util
import os

# Configure the main page
st.set_page_config(
    page_title="ENG220 Unified Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to find .py file inside a directory
def find_python_file(directory):
    for file in os.listdir(directory):
        if file.endswith(".py"):
            return os.path.join(directory, file)
    return None

# Get list of project folders matching pattern
base_dir = os.getcwd()  # or set explicitly if needed
project_dirs = sorted([
    d for d in os.listdir(base_dir)
    if os.path.isdir(d) and d.startswith("ENG220-Group-")
])

# Sidebar navigation
selected_page = st.sidebar.selectbox("Select a Project", ["Main Page"] + project_dirs)

# Main landing page
def main_page():
    st.title("📘 ENG220 Unified Dashboard Book")
    st.markdown("""
    This is a collection of 21 Streamlit data visualization projects, each in its own directory.
    
    **Instructions:**
    - Select any project from the sidebar.
    - Each group developed its own dashboard with a unique `.py` file.
    """)

# Function to dynamically load and run selected script
def run_selected_project(project_dir):
    script_path = find_python_file(project_dir)
    if script_path:
        spec = importlib.util.spec_from_file_location("dynamic_module", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        st.error(f"No Python file found in {project_dir}")

# Routing
if selected_page == "Main Page":
    main_page()
else:
    run_selected_project(selected_page)
