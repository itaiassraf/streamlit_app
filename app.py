
import os
import streamlit as st

# Directory to save the uploaded projects
PROJECT_DIR = "uploaded_projects"

# Ensure the directory exists
if not os.path.exists(PROJECT_DIR):
    os.makedirs(PROJECT_DIR)

st.title("Course Site - Upload and View Projects")

# File uploader widget
uploaded_file = st.file_uploader("Upload a Python project", type=["py"])

# Store uploaded file
if uploaded_file:
    # Save the file
    file_path = os.path.join(PROJECT_DIR, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# Display buttons for each uploaded project
st.write("### Uploaded Projects")

# List all uploaded projects
projects = os.listdir(PROJECT_DIR)
for project in projects:
    # Create a button for each project
    if st.button(f"Run {project}"):
        # Update the query parameters to reflect the selected project
        st.experimental_set_query_params(project=project)
