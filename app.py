import streamlit as st
import os
import json

# Directory to save the project information (URLs, names, and descriptions)
PROJECTS_FILE = "projects.json"

# Ensure the project file exists
if not os.path.exists(PROJECTS_FILE):
    with open(PROJECTS_FILE, 'w') as f:
        json.dump([], f)

# Load existing projects from the file
with open(PROJECTS_FILE, 'r') as f:
    projects = json.load(f)

# Home page
def home_page():
    st.title("Welcome to the Visualization Course")
    st.subheader("Create amazing visualizations and submit your projects!")
    st.image("https://source.unsplash.com/featured/?visualization,code", caption="Visualize Your Ideas")
    if st.button("Submit Your Project"):
        st.experimental_set_query_params(page="submit_project")
        st.experimental_rerun()

# Submit project page
def submit_project_page():
    st.title("Submit Your Project")
    st.subheader("Please provide your project details below:")
    with st.form(key="submit_project"):
        student_name = st.text_input("Enter your name")
        project_url = st.text_input("Enter the project URL", placeholder="https://example.com")
        project_description = st.text_area("Enter a short description of the project")
        submit_button = st.form_submit_button("Submit Project")
        if submit_button:
            if student_name and (project_url.startswith("http://") or project_url.startswith("https://")) and project_description:
                project_info = {
                    "name": student_name,
                    "url": project_url,
                    "description": project_description
                }
                projects.append(project_info)
                with open(PROJECTS_FILE, 'w') as f:
                    json.dump(projects, f)
                st.success("Project successfully submitted!")
            else:
                st.error("Please enter all details correctly.")

# Individual project page
def project_page(project):
    st.title(f"Project by {project['name']}")
    st.subheader("Project Description")
    st.write(project['description'])
    st.markdown(f"[Visit Project]({project['url']})")
    st.image("https://source.unsplash.com/featured/?data,visualization", caption="Amazing Data Visualization")
    st.markdown("[Back to Projects List](/?page=projects)")

# List all projects
def list_projects_page():
    st.sidebar.title("Project Links")
    for idx, project in enumerate(projects):
        st.sidebar.write(f"### Project {idx + 1} by {project['name']}")
        st.sidebar.write(project["description"])
        st.sidebar.markdown(f"[Visit Project Page](/?project={idx})")
    
    st.title("All Submitted Projects")
    for idx, project in enumerate(projects):
        st.write(f"### Project {idx + 1}: {project['description']} by {project['name']}")
        st.markdown(f"[View Details](/?project={idx})")

# Main routing function
def main():
    # Get query parameters to check if a project is being displayed
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", [None])[0]
    project_id = query_params.get("project", [None])[0]

    # Check if the user wants to view a specific project
    if project_id is not None:
        try:
            project_id = int(project_id)
            if 0 <= project_id < len(projects):
                project_page(projects[project_id])
            else:
                st.error("Invalid project ID.")
        except ValueError:
            st.error("Invalid project ID.")
    elif page == "submit_project":
        submit_project_page()
    elif page == "projects":
        list_projects_page()
    else:
        home_page()

if __name__ == "__main__":
    main()


