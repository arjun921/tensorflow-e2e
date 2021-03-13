import streamlit as st
import uuid

st.header('Data Uploader')

data = {}

# Input fields
model_name = st.text_input('Enter some text')
classes = st.number_input("How many classes?", 1, 1000)

st.experimental_set_query_params(classes=classes,model_name=model_name)  # Save value

# Retrieve app state
app_state = st.experimental_get_query_params()  
print(app_state)

# Display saved result if it exist
if "classes" in app_state:
    classes = app_state["classes"][0]
    for x in range(int(classes)):
        st.file_uploader(f'File uploader: {x}')
else:
    st.write("No result to display, compute a value first.")

