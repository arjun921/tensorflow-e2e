import os
import uuid
from pathlib import Path

import semver
import streamlit as st

from configs.config import config
from utils.helpers import get_model_dir, underscore_seperated_path

model_version = semver.VersionInfo.parse("1.0.0")

st.header("Data Uploader")
workspace_exists = os.path.exists(config.WORKSPACE)

# Check workspace exists
try:
    assert workspace_exists
except Exception as e:
    st.error(
        "Error: Local workspace not found. Did you setup enviornment with `make init`?"
    )

if (
    workspace_exists
):  # dont render UI without workspace init (helps reduce multiple folder exists checks)
    data = {}

    # Input fields
    model_name = Path(st.text_input("Enter Model Name"))
    class_count = st.number_input("How many classes?", 1, 1000, value=2)

    # Save values in URL
    st.experimental_set_query_params(class_count=class_count, model_name=model_name)

    # Retrieve app state
    app_state = st.experimental_get_query_params()
    # print(app_state)

    # Display saved result if it exist
    if "class_count" in app_state:
        class_count = app_state["class_count"][0]
        for class_x in range(int(class_count)):
            st.subheader("Upload Class")
            class_name = st.text_input("Class Name", key=class_x)
            data[class_name] = st.file_uploader(
                "Upload images", key=class_x, accept_multiple_files=True
            )
            st.text("---")
    else:
        st.write("No result to display, compute a value first.")

    save_files = st.button("Save Data")

    if save_files:
        local_model_path = underscore_seperated_path(str(model_name))
        model_path = config.WORKSPACE / local_model_path
        model_dir, model_version = get_model_dir(path=model_path, version=model_version)
        st.experimental_set_query_params(
            class_count=class_count,
            model_name=local_model_path,
            model_version=model_version,
        )

        # Create model folder in workspace
        try:
            os.makedirs(model_dir, exist_ok=True)
        except Exception as e:
            st.error(e)

        # TODO: Loop and create class subfolders
        try:
            classes = data.keys()
            for class_ in classes:
                class_path = model_dir / Path(class_)
                os.makedirs(class_path)
                for file in data[class_]:
                    if file is not None:
                        file_path = class_path / Path(file.name)
                        bytes_data = file.getvalue()
                        fopen = open(file_path, "wb")
                        fopen.write(bytes_data)
                        fopen.close()
        except Exception as e:
            st.error(e)
        # TODO: Save image files to class subfolders
        st.success(f"Data saved successfully for {model_name} v{model_version} 🎊")
        st.text("To start training, run")
        st.code("make train")
        print(data)
