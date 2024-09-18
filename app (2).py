
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

# --- Home Page ---
def home_page():
    st.title("Welcome to the Visualization Course")
    st.header("Ben Gurion University")
    st.write("""
        This course is designed to help students build and visualize data-driven applications.
        Throughout the course, students will learn:
        - How to handle data efficiently
        - Visualize complex data using various tools
        - Build interactive applications using Streamlit
    
        Below, you'll find links to student projects that demonstrate their understanding of the topics covered in the course.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/5/52/Ben-Gurion_University_of_the_Negev_logo.svg/1200px-Ben-Gurion_University_of_the_Negev_logo.svg.png", width=300)

# --- Display Individual Project Page ---
def project_page(project):
    st.title(f"Project: {project['description']}")
    st.write(f"URL: [Visit Project]({project['url']})")
    st.write(f"Description: {project['description']}")

# --- Sidebar to Display Projects ---
def sidebar():
    st.sidebar.title("Course Navigation")

    # Home link
    if st.sidebar.button("Home"):
        st.experimental_set_query_params(page="home")
    
    # Project Links
    st.sidebar.write("### Student Projects")
    for idx, project in enumerate(projects):
        if st.sidebar.button(f"Project {idx + 1}"):
            st.experimental_set_query_params(page=f"project_{idx}")

# --- Main Section: Handle Page Navigation ---
def main():
    # Parse the page parameter from URL
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["home"])[0]

    if page == "home":
        home_page()
    elif page.startswith("project_"):
        project_idx = int(page.split("_")[1])
        project = projects[project_idx]
        project_page(project)
    else:
        st.error("Page not found")

# --- Main Application Logic ---
def run_app():
    # Sidebar for navigation
    sidebar()

    # Main content area
    main()

# --- Form to Submit New Project ---
def submit_project_form():
    st.header("Submit Your Project URL")

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

# --- Application Execution ---
if __name__ == "__main__":
    run_app()
    submit_project_form()
