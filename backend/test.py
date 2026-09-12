import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify
import datetime

superkart_api = Flask("SuperKart Product Revenue Predictor")

saved_model = joblib.load("superkart_model.joblib")

print(saved_model)

print("hi")

payload = {
  "Product_Weight": 12.66,
  "Product_Sugar_Content": "Low Sugar",
  "Product_Allocated_Area": 0.027,
  "Product_MRP": 117.08,
  "Store_Size": "Medium",
  "Store_Location_City_Type": "Tier 2",
  "Store_Type": "Supermarket Type2",
  "Product_Id_char": "FD",
  "Store_Age_Years": 16.0,
  "Product_Type_Category": "Non Perishables"
}


print(saved_model.predict(pd.DataFrame(payload, index=[0])))


# import xgboost
# import sklearn
# import numpy
# import pandas
# import joblib

# print("xgboost:", xgboost.__version__)
# print("sklearn:", sklearn.__version__)
# print("numpy:", numpy.__version__)
# print("pandas:", pandas.__version__)
# print("joblib:", joblib.__version__)
