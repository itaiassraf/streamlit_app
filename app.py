import streamlit as st
import os
import json
from PIL import Image

# Path to the projects file and image directory
PROJECTS_FILE = "projects.json"
IMAGES_DIR = "project_images"

# Ensure the projects file and image directory exist
if not os.path.exists(PROJECTS_FILE):
    with open(PROJECTS_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Load existing projects
with open(PROJECTS_FILE, 'r') as f:
    try:
        projects = json.load(f)
    except json.JSONDecodeError:
        projects = []

# Function to save projects
def save_projects():
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=4)

# Home Page
def home_page():
    st.set_page_config(page_title="Visualization Course Home", page_icon="📊")
    st.title("📊 Welcome to the Visualization Course!")
    st.image("Data-Visualization.jpg", use_column_width=True, caption="Visualize Your Ideas")
    st.write("""
        ### About the Course
        Welcome to the Visualization Course! This course will guide you through the fundamentals and advanced techniques of creating impactful visualizations. Showcase your projects and learn from others.
    """)
    if st.button("🚀 Submit Your Project"):
        st.experimental_set_query_params(page="submit_project")
    
    if st.button("📁 View Submitted Projects"):
        st.experimental_set_query_params(page="projects")

# Submit Project Page
def submit_project_page():
    st.set_page_config(page_title="Submit Project", page_icon="📝")
    st.title("📝 Submit Your Project")
    st.write("Please provide the following details to submit your project:")
    
    with st.form(key="submit_project_form"):
        student_name = st.text_input("🔹 Your Name")
        project_url = st.text_input("🔹 Project URL", placeholder="https://example.com")
        project_description = st.text_area("🔹 Short Description of Your Project")
        delete_code = st.text_input("🔹 Set a Delete Code (for deleting your project later)")
        project_image = st.file_uploader("🔹 Upload an Image of Your Project (optional)", type=["jpg", "png", "jpeg"])
        submit_button = st.form_submit_button("Submit Project")
    
    if submit_button:
        if not student_name.strip():
            st.error("Please enter your name.")
        elif not (project_url.startswith("http://") or project_url.startswith("https://")):
            st.error("Please enter a valid URL (starting with http:// or https://).")
        elif not project_description.strip():
            st.error("Please enter a short description of your project.")
        elif not delete_code.strip():
            st.error("Please set a delete code.")
        else:
            # Save the image if uploaded
            image_filename = None
            if project_image is not None:
                image_filename = f"{len(projects)}_{project_image.name}"
                image_path = os.path.join(IMAGES_DIR, image_filename)
                with open(image_path, "wb") as f:
                    f.write(project_image.getbuffer())
            
            project_info = {
                "name": student_name.strip(),
                "url": project_url.strip(),
                "description": project_description.strip(),
                "image": image_filename,
                "delete_code": delete_code.strip()
            }
            projects.append(project_info)
            save_projects()
            st.success("✅ Project successfully submitted!")
    
    st.markdown("---")
    
    # After submission, a button to go back to the home page
    if st.button("🏠 Back to Home"):
        st.experimental_set_query_params(page="home")

# Project Detail Page
def project_detail_page(project_id):
    st.set_page_config(page_title=f"Project {project_id + 1}", page_icon="🔍")
    try:
        project = projects[project_id]
    except IndexError:
        st.error("Invalid Project ID.")
        return

    st.title(f"🔍 Project {project_id + 1}: {project['name']}")
    
    # Increase font size for the description
    st.markdown(f"<div style='font-size: 18px;'><strong>Description:</strong> {project['description']}</div>", unsafe_allow_html=True)
    st.markdown(f"**URL:** [Visit Project]({project['url']})")
    
    # Display the uploaded image if available
    if project.get("image"):
        image_path = os.path.join(IMAGES_DIR, project["image"])
        if os.path.exists(image_path):
            st.image(image_path, caption=f"Project Image: {project['name']}", use_column_width=True)
    else:
        st.image("https://source.unsplash.com/1600x900/?data,visualization", use_column_width=True, caption="Amazing Data Visualization")
    
    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.experimental_set_query_params(page="home")
    if st.button("📄 Back to Projects List"):
        st.experimental_set_query_params(page="projects")

# Projects List Page (with Delete Option for Own Projects)
def projects_list_page():
    st.set_page_config(page_title="All Projects", page_icon="📁")
    st.title("📁 All Submitted Projects")
    
    if not projects:
        st.info("No projects have been submitted yet.")
    else:
        for idx, project in enumerate(projects):
            st.subheader(f"🔹 Project {idx + 1}: {project['name']}")
            
            # Increase font size for the description in the list
            st.markdown(f"<div style='font-size: 16px;'><strong>Description:</strong> {project['description']}</div>", unsafe_allow_html=True)
            
            st.markdown(f"**URL:** [Visit Project]({project['url']})")
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button(f"View Details 🔍", key=f"view_{idx}"):
                    st.experimental_set_query_params(page="project", id=str(idx))
            with col2:
                delete_code_input = st.text_input("Enter Delete Code", key=f"delete_code_{idx}", type="password")
                if st.button(f"Delete ❌", key=f"delete_{idx}"):
                    if delete_code_input.strip() == project.get("delete_code", ""):
                        # Remove image if exists
                        if project.get("image"):
                            image_path = os.path.join(IMAGES_DIR, project["image"])
                            if os.path.exists(image_path):
                                os.remove(image_path)
                        
                        del projects[idx]
                        save_projects()
                        st.experimental_set_query_params(page="projects")
                    else:
                        st.error("Incorrect delete code. You can only delete your own project.")
            st.markdown("---")
    
    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.experimental_set_query_params(page="home")

# Main Routing Function
def main():
    # Get query parameters
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["home"])[0]
    project_id = query_params.get("id", [None])[0]

    if page == "home":
        home_page()
    elif page == "submit_project":
        submit_project_page()
    elif page == "projects":
        projects_list_page()
    elif page == "project" and project_id is not None:
        if project_id.isdigit():
            project_detail_page(int(project_id))
        else:
            st.error("Invalid Project ID.")
    else:
        home_page()

if __name__ == "__main__":
    main()
