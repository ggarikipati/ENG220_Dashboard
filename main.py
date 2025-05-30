import streamlit as st
import os

st.set_page_config(page_title="ENG220 Dashboard Book", layout="wide")

st.title("📘 ENG220 Unified Project Launcher")

project_dirs = sorted([
    f for f in os.listdir(".")
    if f.startswith("ENG220-Group-") and os.path.isdir(f)
])

project_entry_files = {}

# Detect the entry script in each directory
for dir_name in project_dirs:
    files = os.listdir(dir_name)
    for entry_file in ["Home.py", "main.py"]:
        if entry_file in files:
            project_entry_files[dir_name] = os.path.join(dir_name, entry_file)
            break

# Sidebar to select a project
selected_project = st.selectbox("Select a Project", list(project_entry_files.keys()))

# Show contents of selected project
st.subheader(f"📂 Files in `{selected_project}`:")
st.code("\n".join(os.listdir(selected_project)))

# Show launch instructions
entry_script = project_entry_files[selected_project]
launch_command = f"streamlit run {entry_script}"

st.markdown("---")
st.success("🟢 Entry script detected:")
st.code(entry_script)

st.markdown("### 🚀 To launch the project, run this in your terminal:")
st.code(launch_command)
