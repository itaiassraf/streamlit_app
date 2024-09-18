
import streamlit as st
import os
import sys
import io

# Directory where projects are stored
PROJECT_DIR = "uploaded_projects"

# Get the project from the URL query parameters
query_params = st.experimental_get_query_params()
selected_project = query_params.get('project', [None])[0]

if selected_project:
    st.title(f"Running Project: {selected_project}")
    project_path = os.path.join(PROJECT_DIR, selected_project)

    if os.path.exists(project_path):
        # Capture the standard output to display results of execution
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        try:
            # Execute the uploaded Python file
            with open(project_path) as f:
                code = f.read()
                exec(code)
            output = new_stdout.getvalue()

            # Display the output of the script
            if output:
                st.code(output)
            else:
                st.write("The script ran successfully but did not produce any output.")
        except Exception as e:
            st.error(f"Error running the script: {e}")
        finally:
            sys.stdout = old_stdout
    else:
        st.error(f"The selected project {selected_project} does not exist.")
else:
    st.warning("No project selected. Please go back to the main page and choose a project.")
