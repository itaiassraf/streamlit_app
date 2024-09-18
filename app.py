
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

# Get query parameters to check if a project is being displayed
query_params = st.experimental_get_query_params()
project_id = query_params.get("project", [None])[0]

if project_id is not None:
    # Display specific project details
    try:
        project_id = int(project_id)
        if 0 <= project_id < len(projects):
            project = projects[project_id]
            st.title(f"Project {project_id + 1}:")
            st.write(f"**Description:** {project['description']}")
            st.markdown(f"[Visit Project]({project['url']})")
        else:
            st.error("Invalid project ID.")
    except ValueError:
        st.error("Invalid project ID.")
    st.markdown("[Back to Projects List](/?project=)")
else:
    # Main page - Form to submit a project URL and description
    st.title("Course Site - Upload Project URLs")

    with st.form(key="submit_project"):
      project_url = st.text_input("Enter the project URL", placeholder="https://example.com")
      project_description = st.text_area("Enter a short description of the project")

      submit_button = st.form_submit_button("Submit Project")

      if submit_button:
          if project_url.startswith("http://") or project_url.startswith("https://"):
              if project_url and project_description:
                  project_info = {
                      "url": project_url,
                      "description": project_description
                  }

                  projects.append(project_info)
                  with open(PROJECTS_FILE, 'w') as f:
                      json.dump(projects, f)

                  st.success("Project successfully submitted!")
              else:
                  st.error("Please enter both a URL and a description.")
          else:
              st.error("Please enter a valid URL (starting with http:// or https://).")


    # Sidebar section to list all uploaded projects
    st.sidebar.title("Project Links")
    for idx, project in enumerate(projects):
        st.sidebar.write(f"### Project {idx + 1}")
        st.sidebar.write(project["description"])
        st.sidebar.markdown(f"[Visit Project Page](/?project={idx})")

    st.markdown("### All Projects")
    for idx, project in enumerate(projects):
        st.write(f"### Project {idx + 1}: {project['description']}")
        st.markdown(f"[Visit Project]({project['url']})")
        st.markdown(f"[View Details](/?project={idx})")
