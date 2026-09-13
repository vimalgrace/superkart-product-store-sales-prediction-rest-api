
# Import necessary libraries
import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify
import datetime

# Initialize the Flask application
superkart_api = Flask("SuperKart Product Revenue Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_model.joblib")

# Define a route for the home page (GET request)
@superkart_api.get("/")
def home():
  """
  This function handles GET requests to the root URL ("/")
  It returns a welcome message.
  """

  return "Welcome to the SuperKart Product Revenue Predictor API!"

# Define an endpoint for single revenue prediction (POST request)
@superkart_api.post("/v1/predict")
def predict_product_revenue():
  """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing product details and returns
    the predicted product revenue as a JSON response.
  """

  # Get the JSON data from the request body
  product_data = request.get_json()

  # Extract relevant features from the JSON data
  sample = {
        "Product_Weight": float(product_data["Product_Weight"]),
        "Product_Sugar_Content": str(product_data["Product_Sugar_Content"]).replace("reg", "Regular"),
        "Product_Allocated_Area": float(product_data["Product_Allocated_Area"]),
        "Product_MRP": float(product_data["Product_MRP"]),
        "Store_Size": product_data["Store_Size"],
        "Store_Location_City_Type": product_data["Store_Location_City_Type"],
        "Store_Type": product_data["Store_Type"],
        "Product_Id_char": product_data["Product_Id_char"],
        "Store_Age_Years": float(product_data["Store_Age_Years"]),
        "Product_Type_Category": product_data["Product_Type_Category"]

    }

  # Convert the extracted data into a Pandas DataFrame
  input_data = pd.DataFrame([sample])

  # Make prediction
  predicted_product_revenue = model.predict(input_data)[0]

  # Convert predicted_price to Python float
  predicted_product_revenue = round(float(predicted_product_revenue), 2)

  # Return the predicted product revenue
  return jsonify({"Predicted Product Store Sales Total (in dollars)": predicted_product_revenue})



# Define an endpoint for batch prediction (POST request)
@superkart_api.post("/v1/predictbatch")
def predict_batch_product_revenue():
  """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing product details for multiple products
    and returns the predicted product sales revenue as a dictionary in the JSON response.
  """

  # Get the uploaded CSV file from the request
  file = request.files["file"]

  # Read the CSV file into a Pandas DataFrame
  input_data = pd.read_csv(file)

  # Make predictions for all products in the DataFrame 
  predicted_product_revenue = model.predict(input_data).tolist()

  # Create a dictionary of predictions with row index as keys
  output_dict = dict(zip(list(input_data.index), predicted_product_revenue))

  # Return the predictions dictionary as a JSON response
  return output_dict


# Run the Flask application in debug mode if this script is executed directly
if __name__ == "__main__":
  superkart_api.run(debug = True)

