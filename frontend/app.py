
import streamlit as st
import pandas as pd
import requests

# Base URL of the Flash backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Predictor")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for store item features
product_weight = st.number_input(
    "Product Weight", min_value=1.0, value=2.0)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"])

product_allocated_area = st.number_input(
    "Product Allocated Area", min_value=0.0, value=1.0)

product_mrp = st.number_input(
    "Product MRP", min_value=1.0, value=50.0)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"])

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"])

store_type = st.selectbox(
    "Store Type",
    ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])

product_id_char = st.selectbox(
    "Product ID Character", ["FD", "NC", "DR"])

store_age_years = st.number_input(
    "Store Age (in years)", min_value=1, value=10)

product_type_category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_mrp,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Id_char': product_id_char,
    'Store_Age_Years': store_age_years,
    'Product_Type_Category': product_type_category}])


# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
  response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data.to_dict(orient="records")[0])

  if response.status_code == 200:
    prediction = response.json()["Predicted Total Sales Price (in dollars)"]
    st.success(f"Predicted Total Sales Price (in dollars): ${prediction:.2f}")
  else:
    st.error("Unable to connect to the Prediction API.")


# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for bacth prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
  if st.button("Predict Batch", type="primary"):
    files = {"file": uploaded_file}

    # Send file to flask
    response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)

    if response.status_code == 200:
      predictions = response.json()
      st.success("Batch predictions completed!")
      st.write(predictions)
    else:
      st.error("Unable to connect to the Prediction API.")
