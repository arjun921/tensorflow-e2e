
from pathlib import Path
from semver import VersionInfo
import os

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