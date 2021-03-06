import os
import uuid
from pathlib import Path

import semver
import streamlit as st

from configs.config import config
from utils.helpers import (create_dir, data_uploader, get_model_dir,
                           train_test_split, underscore_seperated_path)

import numpy as np

np.random.seed(43)

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

    # Render file uploaders for each class
    if "class_count" in app_state:
        class_count = app_state["class_count"][0]
        for class_x in range(int(class_count)):
            st.markdown("---")
            st.subheader("Upload Class")
            class_name = st.text_input("Class Name", key=class_x)
            data[class_name] = st.file_uploader(
                "Upload images", key=class_x, accept_multiple_files=True
            )
    else:
        st.write("No result to display, compute a value first.")
    st.markdown("---")

    # Train test split ratio
    st.title("Train test split")
    train_split_percentage = st.slider(
        "Train data %", min_value=0, max_value=100, value=config.TRAIN_PERCENT, step=5
    )
    test_split_percentage = st.slider(
        "Test data %", min_value=0, max_value=100, value=100 - train_split_percentage
    )

    # Validate Split
    total_data_coverage = train_split_percentage + test_split_percentage
    st.write("Data coverage:", total_data_coverage, "%")
    if total_data_coverage != 100:
        st.error("Split error, adjust train to cover 100%")

    train_split_percentage /= 100

    # Save dataset
    if st.button("Save Data"):
        local_model_path = underscore_seperated_path(str(model_name))
        model_path = config.WORKSPACE / local_model_path
        model_dir, model_version = get_model_dir(path=model_path, version=model_version)

        st.experimental_set_query_params(
            class_count=class_count,
            model_name=local_model_path,
            model_version=model_version,
        )

        # Create model folder in workspace
        create_dir(model_dir)

        # Create class folders with uploaded data
        df, csv_dir = data_uploader(data, model_dir)

        train_df, test_df = train_test_split(
            df, csv_path=csv_dir, train_percentage=train_split_percentage
        )

        st.success(f"Data saved successfully for {model_name} v{model_version} ????")
        st.markdown("---")
        # st.subheader('Add more data')
        # st.subheader("To append data, push new images to:")
        # st.write(model_dir.absolute())
        # st.markdown("---")
        st.title("Train")
        st.text("To start training, run")
        st.code(f"make train")
        st.text(f"And select from following in the dropdown")
        st.write("Model Name:", model_name)
        st.write("Model Version:", model_version)
