import streamlit as st
import os

st.set_page_config(page_title="Unified Dashboard", layout="wide")

st.title("📘 ENG220 Unified Dashboard")
st.markdown("Select a project below to launch its visualization in a new tab.")

# Define project folder base
project_base_dir = "."

# Get project folders matching ENG220-Group-XXX
project_dirs = sorted([
    f for f in os.listdir(project_base_dir)
    if f.startswith("ENG220-Group-") and os.path.isdir(os.path.join(project_base_dir, f))
])

selected_project = st.selectbox("Choose a project", project_dirs)

# Optional: show list of .py files inside the selected directory
project_path = os.path.join(project_base_dir, selected_project)
py_files = [f for f in os.listdir(project_path) if f.endswith(".py")]

st.write(f"📂 Files in `{selected_project}`:")
st.code("\n".join(py_files))

# Button to launch the selected project
if st.button("🚀 Launch Project"):
    project_launch_command = f"streamlit run {os.path.join(selected_project, 'Home.py')}"
    st.write(f"Run this command in a terminal:")
    st.code(project_launch_command)
    st.success("Copy this command and run it in a separate terminal to launch the selected app.")
