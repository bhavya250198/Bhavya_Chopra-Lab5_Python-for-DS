# app.py

from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__, template_folder='templates')


# Load the trained model from the pickle file
model_filename = 'random_forest_model.pkl'
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Define the predict function
def predict_price(present_price, kms_driven, fuel_type, seller_type, transmission, owner,age_of_the_car):
    # Create a DataFrame with the input data
    
    input_data = pd.DataFrame({
        'Present_Price': [float(present_price)],
    'Kms_Driven': [int(kms_driven)],
    'Fuel_Type_Diesel': [1] if fuel_type == 'Diesel' else [0],
    'Fuel_Type_Petrol': [1] if fuel_type == 'Petrol' else [0],
    # 'Seller_Type_Dealer': [1] if seller_type == 'Dealer' else [0],
    'Seller_Type_Individual': [1] if seller_type == 'Individual' else [0],
    # 'Transmission_Automatic': [1] if transmission == 'Automatic' else [0],
    'Transmission_Manual': [1] if transmission == 'Manual' else [0],
    'Owner':[int(owner)],
        'age_of_the_car':[int(age_of_the_car)]
    })

    # Make a prediction using the loaded model
    predicted_price = model.predict(input_data)

    return predicted_price[0]

# Define the route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for handling predictions
@app.route('/predict', methods=['POST'])
def make_prediction():
    if request.method == 'POST':
        present_price = request.form['present_price']
        kms_driven = request.form['kms_driven']
        fuel_type = request.form['fuel_type']
        seller_type = request.form['seller_type']
        transmission = request.form['transmission']
        owner = request.form['owner']
        age_of_the_car=request.form['age_of_the_car']
        # Call the predict_price function
        predicted_price = predict_price(present_price, kms_driven, fuel_type, seller_type, transmission, owner,age_of_the_car)

        # Display the predicted price on a new page or within the same page
        return f'Predicted Selling Price: {predicted_price} lakhs'

if __name__ == '__main__':
    app.run(debug=True)
