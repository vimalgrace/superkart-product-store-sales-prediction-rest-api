
import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify
import datetime

superkart_api = Flask("SuperKart Product Revenue Predictor")

model = joblib.load("superkart_model.joblib")

@superkart_api.get("/")
def home():
  """
  This function handles GET requests to the root URL ("/")
  It returns a welcome message.
  """

  return "Welcome to the SuperKart Product Revenue Predictor API!"

@superkart_api.post("/v1/predict")
def predict_product_revenue():
  product_data = request.get_json()

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


  input_data = pd.DataFrame([sample])

  predicted_product_revenue = model.predict(input_data)[0]

  predicted_product_revenue = round(float(predicted_product_revenue), 2)

  return jsonify({"Predicted Product Store Sales Total (in dollars)": predicted_product_revenue})




@superkart_api.post("/v1/predictbatch")
def predict_batch_product_revenue():

  file = request.files["file"]

  input_data = pd.read_csv(file)

  predicted_product_revenue = model.predict(input_data).tolist()

  output_dict = dict(zip(list(input_data.index), predicted_product_revenue))

  return output_dict



if __name__ == "__main__":
  superkart_api.run(debug = True)

