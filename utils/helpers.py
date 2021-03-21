
from pathlib import Path
from semver import VersionInfo
import os
import streamlit as st


def underscore_seperated_path(path: str):
    path = path.replace(' ','_')
    path = path.replace('-','_')
    return Path(path)

def get_model_dir(path: Path, version: VersionInfo ):
    versioned_path = path / Path(str(version))
    while os.path.exists(versioned_path):
        version = version.bump_major()
        versioned_path = path / Path(str(version))
    return versioned_path,version


def create_dir(path: Path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        st.error(e)

    
def data_uploader(data: dict, model_dir: Path):
    try:
        classes = data.keys()
        for class_ in classes:
            class_path = model_dir / Path ('data') / Path(class_)
            create_dir(class_path)
            for file in data[class_]:
                if file is not None:
                    file_path = class_path / Path(file.name)
                    bytes_data = file.getvalue()
                    fopen = open(file_path, "wb")
                    fopen.write(bytes_data)
                    fopen.close()
    except Exception as e:
        st.error(e)