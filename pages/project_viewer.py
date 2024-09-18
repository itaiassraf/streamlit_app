
import streamlit as st
import os
import sys
import io

# Directory where projects are stored
PROJECT_DIR = "uploaded_projects"

# Get the project from the URL query parameters
query_params = st.query_params
selected_project = query_params.get('project', [None])[0]

if selected_project:
    st.title(f"Running Project: {selected_project}")
    project_path = os.path.join(PROJECT_DIR, selected_project)

    # Capture the standard output to display results of execution
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    try:
        # Execute the uploaded Python file safely
        exec(open(project_path).read())
        output = new_stdout.getvalue()

        # Display the output of the script
        st.code(output)
    except Exception as e:
        st.error(f"Error running the script: {e}")
    finally:
        sys.stdout = old_stdout
else:
    st.warning("No project selected.")
