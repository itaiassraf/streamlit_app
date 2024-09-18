
import streamlit as st
import os

PROJECT_DIR = "uploaded_projects"

if not os.path.exists(PROJECT_DIR):
    os.makedirs(PROJECT_DIR)

st.title("Upload Your Project")

uploaded_file = st.file_uploader("Choose a file", type=["py", "zip", "ipynb"])

if uploaded_file:
    file_path = os.path.join(PROJECT_DIR, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
