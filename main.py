import streamlit as st
import os

st.set_page_config(page_title="ENG220 Dashboard Book", layout="wide")

st.title("📘 ENG220 Unified Project Launcher")

project_dirs = sorted([
    f for f in os.listdir(".")
    if f.startswith("ENG220-Group-") and os.path.isdir(f)
])

project_entry_files = {}

# Search strategy for entry points
preferred_names = ["Home.py", "main.py"]

for dir_name in project_dirs:
    py_files = [f for f in os.listdir(dir_name) if f.endswith(".py")]

    # Try preferred entry file names first
    found_entry = None
    for pref in preferred_names:
        if pref in py_files:
            found_entry = pref
            break

    # If not found, and there's only one .py file, use that
    if not found_entry and len(py_files) == 1:
        found_entry = py_files[0]

    # If still not found, fall back to the first .py file alphabetically
    if not found_entry and py_files:
        found_entry = sorted(py_files)[0]

    if found_entry:
        project_entry_files[dir_name] = os.path.join(dir_name, found_entry)

# Show dropdown only for valid projects with detected .py files
if not project_entry_files:
    st.error("No valid entry scripts found in any ENG220-Group directories.")
else:
    selected_project = st.selectbox("Select a Project", list(project_entry_files.keys()))
    selected_path = project_entry_files[selected_project]

    st.subheader(f"📂 Files in `{selected_project}`:")
    st.code("\n".join(os.listdir(selected_project)))

    st.success("🟢 Entry script detected:")
    st.code(selected_path)

    st.markdown("### 🚀 To launch the project, run this in your terminal:")
    st.code(f"streamlit run {selected_path}")
