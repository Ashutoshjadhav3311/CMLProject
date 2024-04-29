import streamlit as st
import requests
import pickle5 as pickle
import os
import pandas as pd

# Step 1: Check if the Pickle File Exists and Download if Needed
file_name = "knnBest.pkl"
url = "https://picklefiles3.s3.eu-west-1.amazonaws.com/knnBest.pkl"

if not os.path.exists(file_name):
    response = requests.get(url, stream=True)
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    st.write(f"Pickle file downloaded: {file_name}")
else:
    st.write(f"Pickle file '{file_name}' already exists.")

# Step 2: Load the Model
with open(file_name, 'rb') as file:
    model = pickle.load(file)

st.write("Model loaded successfully.")

# Step 3: Create Streamlit UI for User Input
st.title("Predict with KNN Model")

# Collect user input for features
bmi = st.number_input("BMI (Body Mass Index)", value=25.0)
age = st.number_input("Age", value=30)
genhlth = st.number_input("General Health (1 to 5)", value=3)
menthlth = st.number_input("Mental Health (number of unhealthy days in the past 30)", value=3)
physhlth = st.number_input("Physical Health (number of unhealthy days in the past 30)", value=3)

highbp = st.radio("High Blood Pressure", ["No", "Yes"])
highchol = st.radio("High Cholesterol", ["No", "Yes"])
cholcheck = st.radio("Cholesterol Check", ["No", "Yes"])
smoker = st.radio("Smoker", ["No", "Yes"])
heartdiseaseorattack = st.radio("Heart Disease or Attack", ["No", "Yes"])
physactivity = st.radio("Physical Activity", ["No", "Yes"])
hvyalcoholconsump = st.radio("Heavy Alcohol Consumption", ["No", "Yes"])
anyhealthcare = st.radio("Any Healthcare Coverage", ["No", "Yes"])
sex = st.radio("Sex", ["Female", "Male"])
education = st.slider("Education (1 to 5)", min_value=1, max_value=5, value=3)
income = st.number_input("Income (in dollars)", value=40000)

# Convert to a 2D array for prediction
input_2d_array = [[
    bmi,
    age,
    genhlth,
    menthlth,
    physhlth,
    1 if highbp == "Yes" else 0,
    1 if highchol == "Yes" else 0,
    1 if cholcheck == "Yes" else 0,
    1 if smoker == "Yes" else 0,
    1 if heartdiseaseorattack == "Yes" else 0,
    1 if physactivity == "Yes" else 0,
    1 if hvyalcoholconsump == "Yes" else 0,
    1 if anyhealthcare == "Yes" else 0,
    1 if sex == "Male" else 0,
    education,
    income,
]]

# Step 4: Predict and Display Output
if st.button("Predict"):
    prediction = model.predict(input_2d_array)
    st.write(f"Prediction: {prediction[0]}")
