# GDP Growth Prediction System

An AI-powered web application to predict GDP growth rates based on economic indicators.

## Features
- 📊 Historical GDP data visualization with interactive charts
- 🤖 AI-powered predictions using Random Forest model
- ⚡ Real-time analysis of economic indicators
- 🌍 Support for 150+ countries

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: React.js
- **Charts**: Recharts
- **ML Model**: Random Forest (scikit-learn)

## Setup Instructions

### 1. Backend Setup (Flask)

```bash
# Install Python dependencies
pip install flask flask-cors joblib pandas numpy scikit-learn

# Run the Flask backend
python app.py
```

The backend will start on `http://localhost:5000`

### 2. Frontend Setup (React)

```bash
# Navigate to frontend directory
cd fronend

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will start on `http://localhost:3000`

## How to Use

1. **Start Backend**: Run `python app.py` in the root directory
2. **Start Frontend**: Run `npm start` in the `fronend` directory
3. **Access Application**: Open `http://localhost:3000` in your browser
4. **Navigate**: 
   - Home page: Landing page with features
   - Click "🚀 Detect Growth Rate" to go to the dashboard
5. **View Historical Data**: Enter a country name and click "View History"
6. **Make Predictions**: Fill in the economic indicators and click "Analyze & Predict"

## API Endpoints

### GET /api/history
Fetch historical GDP data for a country
```
Query Parameters: country (string)
Example: http://localhost:5000/api/history?country=India
```

### POST /predict
Predict GDP growth rate
```json
{
  "Country": "India",
  "Population": "2.5",
  "Exports": "5.0",
  "Imports": "4.0",
  "Investment": "6.0",
  "Consumption": "3.5",
  "Govt_Spend": "2.0"
}
```

## Input Parameters

All values should be growth rates (percentage):
- **Population**: Population growth rate
- **Exports**: Exports of goods and services growth rate
- **Imports**: Imports of goods and services growth rate
- **Investment**: Gross capital formation growth rate
- **Consumption**: Final consumption expenditure growth rate
- **Govt_Spend**: Government expenditure growth rate

## Troubleshooting

### "Not Found" Error
- Make sure you're accessing `http://localhost:3000` (React) not `http://localhost:5000` (Flask)
- Ensure both servers are running

### Backend Connection Error
- Check if Flask is running on port 5000
- Verify CORS is enabled in app.py

### Module Not Found
- Run `npm install` in the fronend directory
- Run `pip install -r requirements.txt` for Python dependencies
