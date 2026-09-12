import streamlit as st
import pandas as pd
import requests


BACKEND_URL = "http://backend:7860"

st.title("SuperKart Product Revenue Predictor")

st.subheader("Online Prediction")


product_weight = st.number_input("Enter Product Weight", value = 12.5)
product_sugar_content = st.selectbox("Select Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
product_allocated_area = st.number_input("Enter Product Allocated Area", value = 0.05)
product_mrp = st.number_input("Enter Product MRP", value = 150.0)
store_size = st.selectbox("Select Store Size", ['Small', 'Medium', 'High'])
store_location_city_type = st.selectbox("Select Store Location City Type", ['Tier 1', 'Tier 2', 'Tier 3'])
store_type = st.selectbox("Select Store Type", ['Supermarket Type1', 'Supermarket Type2', 'Departmental Store', 'Food Mart'])
product_id_char = st.selectbox("Select Product ID char", ["FD", "NC", "DR"])
store_age_years = st.number_input("Enter Store Age in Years", min_value = 0.0, value = 17.0)
product_type_category = st.selectbox("Select Product Type Category", ['Non Perishables', 'Perishables'])

input_data = pd.DataFrame([{
    "product_weight": product_weight,
    "product_sugar_content": product_sugar_content,
    "product_allocated_area": product_allocated_area,
    "product_mrp": product_mrp,
    "store_size": store_size,
    "store_location_city_type": store_location_city_type,
    "store_type": store_type,
    "product_id_char": product_id_char,
    "store_age_years": store_age_years,
    "product_type_category": product_type_category

}])

if st.button("Predict", type = "primary"):
  response = requests.post(f"{BACKEND_URL}/v1/predict", json = input_data.to_dict(orient = "records")[0])

  if response.status_code == 200:
    prediction = response.json()["Predicted Product Store Sales Total (in dollars)"]
    st.success(f"Predicted Product Store Sales Total (in dollars): {prediction}")

  else:
    st.error("Error occurred during prediction.")


st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload a CSV file", type = ["csv"])

if uploaded_file is not None:
  if st.button("Predict", type = "primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files = {"file": uploaded_file})
    if response.status_code == 200:
      predictions = response.json()
      st.json(predictions)
    else:
      st.error("Error occurred during batch prediction.")
