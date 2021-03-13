# Tensorflow-E2E

## Initialize workspace and setup environment
```
make init
```

## Run Server
```
make run # Runs file upload UI for now
```


### Goals
More like thinking out loud
- [ ] Upload Data
  - [x] +/- class count 
    - [x] File upload input
    - [ ] class name input
  - [x] model name input
  - [ ] create folder by model name in workspace
    - [ ] validate folder exists/show relevant error if exists
    - [ ] upload files to relevant class folder name
- [ ] Data split
- [ ] Model Fit
- [ ] Test metrics/charts
- [ ] Export deploy
- [ ] Docker push (static/dynamic port) (optional)
