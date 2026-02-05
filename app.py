from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# 1. Load Model & Encoder
try:
    # Update paths to match where you saved your .pkl files
    model = joblib.load("gdp_model.pkl")
    encoder = joblib.load("country_encoder.pkl")
    print("✅ Model and Encoder loaded.")
except Exception as e:
    print(f"⚠️ Model/Encoder not found. Error: {e}")
    print("Predictions will use fallback simulation.")
    model = None
    encoder = None

# 2. Load Historical Data
try:
    # Load the new file that has the 'Year' column
    df_history = pd.read_csv('final_data_with_year.csv')
    
    # Select the columns we need for the frontend graph
    df_history = df_history[[
        'Country', 
        'Year', 
        'GDP_Growth_Rate', 
        'Exports of goods and services_Growth_Rate', 
        'Imports of goods and services_Growth_Rate'
    ]]
    
    # Rename columns to simpler names for the frontend
    df_history.columns = ['Country', 'Year', 'GDP_Growth', 'Exports_Growth', 'Imports_Growth']
    print("✅ Historical Data loaded.")

except Exception as e:
    print(f"⚠️ Historical Data Error: {e}")
    df_history = pd.DataFrame()

@app.route('/')
def home():
    return jsonify({
        'message': 'GDP Growth Prediction API',
        'status': 'running',
        'version': 'v2.0-debug',
        'model_loaded': model is not None,
        'encoder_loaded': encoder is not None,
        'endpoints': {
            '/api/history': 'GET - Fetch historical data for a country',
            '/predict': 'POST - Predict GDP growth rate'
        }
    })

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """Get list of all available countries"""
    if df_history.empty:
        return jsonify([])
    
    # Get unique countries and sort them
    countries = sorted(df_history['Country'].unique().tolist())
    return jsonify(countries)

@app.route('/api/history', methods=['GET'])
def get_history():
    country = request.args.get('country')
    
    if not country or df_history.empty:
        return jsonify([])
    
    # Filter for the country and sort by Year (1972, 1973...)
    country_data = df_history[df_history['Country'] == country].sort_values(by='Year')
    
    # Convert to dictionary for JSON response
    # replace({np.nan: None}) handles any missing values safely
    data_json = country_data.replace({np.nan: None}).to_dict(orient='records')
    
    return jsonify(data_json)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    import sys
    print(f"=== PREDICT CALLED ===", flush=True)
    sys.stdout.flush()
    print(f"Received data: {data}", flush=True)
    print(f"Model loaded: {model is not None}", flush=True)
    print(f"Encoder loaded: {encoder is not None}", flush=True)
    
    try:
        if model and encoder:
            # Encode country name to number
            country_code = encoder.transform([data['Country']])[0]
            
            # Prepare features in the exact order the model expects
            features = [
                country_code,
                float(data['Population']),
                float(data['Exports']),
                float(data['Imports']),
                float(data['Investment']),
                float(data['Consumption']),
                float(data['Govt_Spend'])
            ]
            
            print(f"Predicting for {data['Country']} with features: {features}", flush=True)
            prediction = model.predict([features])[0]
            print(f"Prediction: {prediction}", flush=True)
            return jsonify({'growth': round(prediction, 2), 'method': 'AI Model'})
        else:
            raise Exception("Model not loaded")

    except Exception as e:
        print(f"Prediction Error: {e}", flush=True)
        print(f"Error type: {type(e).__name__}", flush=True)
        import traceback
        traceback.print_exc()
        
        sim_growth = (float(data['Consumption']) * 0.6) + (float(data['Exports']) * 0.2) - (float(data['Imports']) * 0.1)
        return jsonify({'growth': round(sim_growth, 2), 'method': 'Simulation'})

if __name__ == '__main__':
    app.run(debug=False, port=5000)