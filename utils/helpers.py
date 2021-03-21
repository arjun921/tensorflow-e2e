import os
from pathlib import Path

from sklearn.model_selection import train_test_split as sksplit

import pandas as pd
import streamlit as st
from configs import config
from semver import VersionInfo



def underscore_seperated_path(path: str):
    path = path.replace(" ", "_")
    path = path.replace("-", "_")
    return Path(path)


def get_model_dir(path: Path, version: VersionInfo):
    versioned_path = path / Path(str(version))
    while os.path.exists(versioned_path):
        version = version.bump_major()
        versioned_path = path / Path(str(version))
    return versioned_path, version


def create_dir(path: Path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        st.error(e)


def data_uploader(data: dict, model_dir: Path):
    df = pd.DataFrame(columns=["path", "class"])
    try:
        classes = data.keys()
        for class_ in classes:
            class_path = model_dir / Path("data") / Path(class_)
            create_dir(class_path)
            for file in data[class_]:
                if file is not None:
                    file_path = class_path / Path(file.name)
                    bytes_data = file.getvalue()
                    fopen = open(file_path, "wb")
                    fopen.write(bytes_data)
                    fopen.close()
                    df = df.append(
                        {"path": file_path.absolute(), "class": class_},
                        ignore_index=True,
                    )
    except Exception as e:
        st.error(e)

    # write DF as CSV
    csv_path = model_dir / Path("csv") / Path("source.csv")
    create_dir(csv_path.parent)
    df.to_csv(csv_path, index=False)
    return df, csv_path.parent

def train_test_split(df: pd.DataFrame, csv_path: Path,  train_percentage: float = 0.8):
    train_df, test_df = sksplit(df, train_size=train_percentage)

    
    # Create dir (Sanity Check)
    create_dir(csv_path)
    
    # Save Train
    train_df.to_csv(csv_path / Path('train.csv'),index=False)

    # Save Test
    test_df.to_csv(csv_path / Path('test.csv'),index=False)
    return train_df, test_df
