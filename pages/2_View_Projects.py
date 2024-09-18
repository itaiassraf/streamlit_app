
import streamlit as st
import os

PROJECT_DIR = "uploaded_projects"

st.title("View Uploaded Projects")

if os.path.exists(PROJECT_DIR):
    projects = os.listdir(PROJECT_DIR)
    
    if len(projects) > 0:
        st.write("Here are the uploaded projects:")
        for project in projects:
            file_path = os.path.join(PROJECT_DIR, project)
            st.write(f"- {project}")
            
            with open(file_path, 'rb') as f:
                st.download_button(label=f"Download {project}", data=f, file_name=project)
    else:
        st.write("No projects uploaded yet.")
else:
    st.write("No projects uploaded yet.")
