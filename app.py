
import streamlit as st
import os
import json

# Directory to save the project information (URLs and descriptions)
PROJECTS_FILE = "projects.json"

# Ensure the project file exists
if not os.path.exists(PROJECTS_FILE):
    with open(PROJECTS_FILE, 'w') as f:
        json.dump([], f)

# Load existing projects from the file
with open(PROJECTS_FILE, 'r') as f:
    projects = json.load(f)

# Title of the app
st.title("Course Site - Upload Project URLs")

# Form to submit a project URL and description
with st.form(key="submit_project"):
    project_url = st.text_input("Enter the project URL")
    project_description = st.text_area("Enter a short description of the project")

    submit_button = st.form_submit_button("Submit Project")

    # When the form is submitted, save the project information
    if submit_button:
        if project_url and project_description:
            project_info = {
                "url": project_url,
                "description": project_description
            }

            # Save the new project to the file
            projects.append(project_info)
            with open(PROJECTS_FILE, 'w') as f:
                json.dump(projects, f)

            st.success("Project successfully submitted!")
        else:
            st.error("Please enter both a URL and a description.")

# Sidebar section to list all uploaded projects
st.sidebar.title("Project Links")
for idx, project in enumerate(projects):
    st.sidebar.write(f"### Project {idx + 1}")
    st.sidebar.write(project["description"])
    st.sidebar.markdown(f"[Visit Project]({project['url']})")
