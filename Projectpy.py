import streamlit as st
import requests
import pickle
import os
import pandas as pd

# Step 1: Check if the Pickle File Exists and Download if Needed
file_name = "knnforpickle.pkl"
url = "https://picklefiles3.s3.eu-west-1.amazonaws.com/knnforpickle.pkl"

if not os.path.exists(file_name):
    response = requests.get(url, stream=True)
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    st.write(f"Pickle file downloaded: {file_name} from s3 bucket")
else:
    st.write(f"Pickle file '{file_name}' already exists no required to download from s3 bucket.")

# Step 2: Load the Model
with open(file_name, 'rb') as file:
    model = pickle.load(file)

st.write("Model loaded successfully.")

if "inputs" not in st.session_state:
    st.session_state.inputs = {
        "BMI": 0.0,
        "Age": 0,
        "GenHlth": 0,
        "MentHlth": 0,
        "PhysHlth": 0,
        "HighBP": "No",
        "HighChol": "No",
        "CholCheck": "No",
        "Smoker": "No",
        "HeartDiseaseorAttack": "No",
        "PhysActivity": "No",
        "HvyAlcoholConsump": "No",
        "AnyHealthcare": "No",
        "Sex": "Female",
        "Education": 1,
        "Income": 0,
    }

# Create input fields with default values from session state
st.session_state.inputs["BMI"] = st.number_input("BMI (Body Mass Index)", value=st.session_state.inputs["BMI"])
st.session_state.inputs["Age"] = st.number_input("Age", value=st.session_state.inputs["Age"])
st.session_state.inputs["GenHlth"] = st.slider("General Health (1 to 5) More=bad health", min_value=1, max_value=5, value=st.session_state.inputs["GenHlth"])
st.session_state.inputs["MentHlth"] = st.number_input("Mental Health (number of unhealthy days in the past 30)", value=st.session_state.inputs["MentHlth"])
st.session_state.inputs["PhysHlth"] = st.number_input("Physical Health (number of unhealthy days in the past 30)", value=st.session_state.inputs["PhysHlth"])

st.session_state.inputs["HighBP"] = st.radio("High Blood Pressure", ["No", "Yes"], index=0)
st.session_state.inputs["HighChol"] = st.radio("High Cholesterol", ["No", "Yes"], index=0)
st.session_state.inputs["CholCheck"] = st.radio("Cholesterol Check", ["No", "Yes"], index=0)
st.session_state.inputs["Smoker"] = st.radio("Smoker", ["No", "Yes"], index=0)
st.session_state.inputs["HeartDiseaseorAttack"] = st.radio("Heart Disease or Attack", ["No", "Yes"], index=0)
st.session_state.inputs["PhysActivity"] = st.radio("Physical Activity", ["No", "Yes"], index=0)
st.session_state.inputs["HvyAlcoholConsump"] = st.radio("Heavy Alcohol Consumption", ["No", "Yes"], index=0)
st.session_state.inputs["AnyHealthcare"] = st.radio("Any Healthcare Coverage", ["No", "Yes"], index=0)
st.session_state.inputs["Sex"] = st.radio("Sex", ["Female", "Male"], index=0)
st.session_state.inputs["Education"] = st.slider("Education (1 to 5)", min_value=1, max_value=5, value=st.session_state.inputs["Education"])
st.session_state.inputs["Income"] = st.slider("Income between 1 to 7)",  min_value=1, max_value=7, value=st.session_state.inputs["Income"])

# Step 3: Add a Clear Button to Reset Inputs
if st.button("Clear"):
    # Reset session state inputs to default values
    for key in st.session_state.inputs:
        if key in ["BMI", "Age", "GenHlth", "MentHlth", "PhysHlth", "Income"]:
            st.session_state.inputs[key] = 0
        elif key in ["HighBP", "HighChol", "CholCheck", "Smoker", "HeartDiseaseorAttack", "PhysActivity", "HvyAlcoholConsump", "AnyHealthcare", "Sex"]:
            st.session_state.inputs[key] = "No"
        elif key == "Education":
            st.session_state.inputs[key] = 1

# Step 4: Predict Using the Loaded Model
if st.button("Predict"):
    input_2d_array = [[
        st.session_state.inputs["BMI"],
        st.session_state.inputs["Age"],
        st.session_state.inputs["GenHlth"],
        st.session_state.inputs["MentHlth"],
        st.session_state.inputs["PhysHlth"],
        1 if st.session_state.inputs["HighBP"] == "Yes" else 0,
        1 if st.session_state.inputs["HighChol"] == "Yes" else 0,
        1 if st.session_state.inputs["CholCheck"] == "Yes" else 0,
        1 if st.session_state.inputs["Smoker"] == "Yes" else 0,
        1 if st.session_state.inputs["HeartDiseaseorAttack"] == "Yes" else 0,
        1 if st.session_state.inputs["PhysActivity"] == "Yes" else 0,
        1 if st.session_state.inputs["HvyAlcoholConsump"] == "Yes" else 0,
        1 if st.session_state.inputs["AnyHealthcare"] == "Yes" else 0,
        1 if st.session_state.inputs["Sex"] == "Male" else 0,
        st.session_state.inputs["Education"],
        st.session_state.inputs["Income"],
    ]]

    prediction = model.predict(input_2d_array)

    st.write(f"Prediction: {prediction[0]}")
