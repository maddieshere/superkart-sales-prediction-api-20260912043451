
# Import necessary libraries
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify

# Initialize the Flask Application
superkart_predictor_api = Flask("Superkart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_model_v2_0.joblib")

# Define a route for the home page (GET request)
@superkart_predictor_api.get('/')
def home():
  """
  This function handles GET requests to the root URL ('/') of the API.
  It returns a simple welcome message.
  """

  return "<h1>Welcome to the SuperKart Sales Predictor API!</h1>"


# Define an enpoint for single store sales prediction (POST request)
@superkart_predictor_api.post('/v1/predict')
def predict_sales():
  """
  This function handles POST request ot the 'v1/predict" endpoint.
  It expects a JSON payload containing property details and returns
  the predicted sales value as a JSON respnose.
  """

  # Get the JSON data from the request body
  sales_data = request.get_json()

  # Extract relevant features from the JSON data
  item = {
      'Product_Weight' : sales_data['Product_Weight'],
      'Product_Sugar_Content' : sales_data['Product_Sugar_Content'],
      'Product_Allocated_Area' : sales_data['Product_Allocated_Area'],
      'Product_MRP' : sales_data['Product_MRP'],
      'Store_Size' : sales_data['Store_Size'],
      'Store_Location_City_Type' : sales_data['Store_Location_City_Type'],
      'Store_Type' : sales_data['Store_Type'],
      'Product_Id_char' : sales_data['Product_Id_char'],
      'Store_Age_Years' : sales_data['Store_Age_Years'],
      'Product_Type_Category' : sales_data['Product_Type_Category'],
  }

  # Convert the extracted data to a Pandas DataFrame
  input_data = pd.DataFrame([item])

  # Make prediction (get sales)
  predicted_sales_price = model.predict(input_data)[0]

  return jsonify({"Predicted Total Sales Price (in dollars)": float(predicted_sales_price)})


# Define an endpoint for batch prediction (POST request)
@superkart_predictor_api.post('/v1/predictbatch')
def predict_sales_batch():
  """
  This function handles POST requests to the '/v1/predictbatch' endpoint.
  It expects a CSV file containing sales details for multiple items and
  returns a JSON response with predicted sales values for each item.
  """

  # Get the uploaded CSV file from the request
  file = request.files["file"]

  # Read the CSV file into a Pandas DataFrame
  batch_data = pd.read_csv(file)

  # Make predictions for all items in the DataFrame
  predicted_sales_prices = model.predict(batch_data).tolist()

  # Create a dictionary of predictions with item as keys
  item_ids = batch_data['Product_Id_char'].tolist()
  output_dict = dict(zip(item_ids, predicted_sales_prices))

  # Return the predictions dictionary as JSON
  return output_dict


# Run the Flask application in debug mode if this script is executed directly
if __name__ == "__main__":
  superkart_predictor_api.run(debug=True)
