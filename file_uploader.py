import streamlit as st
import uuid
from pathlib import Path
from configs.config import config
import os

st.header('Data Uploader')
workspace_exists = os.path.exists(config.WORKSPACE)

# Check workspace exists
try:
    assert workspace_exists
except Exception as e:
    st.error('Error: Local workspace not found. Did you setup enviornment with `make init`?')

if workspace_exists: # dont render UI without workspace init (helps reduce multiple folder exists checks)
    data = {}

    # Input fields
    model_name = st.text_input('Enter Model Name')
    classes = st.number_input("How many classes?", 1, 1000,value=2)


    # Save values in URL
    st.experimental_set_query_params(classes=classes,model_name=model_name)

    # Retrieve app state
    app_state = st.experimental_get_query_params()
    # print(app_state)

    data = {}

    # Display saved result if it exist
    if "classes" in app_state:
        classes = app_state["classes"][0]
        for class_x in range(int(classes)):
            st.subheader('Upload Class')
            class_name = st.text_input('Class Name',key=class_x)
            data[class_name] = st.file_uploader('Upload images', key=class_x, accept_multiple_files=True)
            st.text('---')
    else:
        st.write("No result to display, compute a value first.")

    save_files = st.button('Save Data')

    if save_files:
        # TODO: Create model folder in workspace
        # TODO: Loop and create class subfolders
        # TODO: Save image files to class subfolders
        print(data)
