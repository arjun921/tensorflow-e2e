# Tensorflow-E2E (WIP)

The basic workflow is outlined below
- Upload Data
- Train


# How do I run this?

## Initialize workspace and setup environment 
One time setup, only for first time users
```
make init
```

# Building a model (container)

## Upload Data
```
make upload
```
Data gets uploaded to their class folders under the folder structure shown below:
```
- workspace
  - model_name
    - version
      - data
        - class_1
        - class_2
```

Model names are `_` (underscore) seperated for sanity of traversion across operating systems.

### Versioning

Major version gets bumped automatically if the following conditions are met:
- Workspace has an old model with same name

>Idea: Add an option to include data from prior model versions or pull data from other models


## Train
Once your data has been uploaded, it will show a commmand similar to
```
make train workspace=workpace/cats_vs_dogs/1.0.0/
```
This runs the run the training script with the workspace

--- 
## Goals
More like thinking out loud
- [ ] Data `make upload` , could switch it to `make data`?
  - [x] Upload Data 
    - [x] +/- class count 
      - [x] File upload input
      - [x] class name input
    - [x] model name input
    - [x] create folder by model name in workspace
      - [x] validate folder exists/show relevant error if exists
      - [x] upload files to relevant class folder name
  - [ ] Data split
- [ ] Model Fit
  - [ ] STDOUT to Streamlit? 🤔 (THAT WOULD BE LIT!)
- [ ] Test metrics/charts
- [ ] Export deploy
- [ ] Docker push (static/dynamic port) (optional)
