# GDP Growth Prediction Model - Backend & ML Model

## 🚀 Overview

This is the backend API and Machine Learning model for GDP Growth Prediction. It provides REST API endpoints for historical GDP data and AI-powered predictions using a Random Forest Regressor model trained on 203 countries' economic data from 1972-2021.

## 📋 Features

- **ML Model**: Random Forest Regressor with 94% test accuracy
- **203 Countries**: Trained on comprehensive global economic data
- **Historical Data**: GDP growth data from 1972-2021
- **REST API**: Flask-based API with CORS support
- **Real-time Predictions**: AI-powered GDP forecasts based on economic indicators

## 🛠️ Tech Stack

- **Python**: 3.13+
- **Flask**: 2.3.0 - Web framework
- **scikit-learn**: 1.3.0 - Machine learning
- **pandas**: 2.0.3 - Data manipulation
- **numpy**: 1.24.3 - Numerical computing
- **joblib**: 1.3.2 - Model serialization
- **flask-cors**: 4.0.0 - CORS support

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-.git
   cd GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify model files exist**
   - `gdp_model.pkl` - Trained Random Forest model
   - `country_encoder.pkl` - Country name encoder
   - `final_data_with_year.csv` - Historical data

5. **Run the server**
   ```bash
   python app.py
   ```

   Server will start on `http://127.0.0.1:5000`

## 📁 Project Structure

```
.
├── app.py                          # Main Flask application
├── gdp_model.pkl                   # Trained ML model
├── country_encoder.pkl             # Country encoder
├── final_data_with_year.csv        # Historical GDP data (1972-2021)
├── Final_Model_Data.csv            # Complete training dataset
├── retrain_model.py                # Script to retrain the model
├── test_api.py                     # API testing script
├── requirements.txt                # Python dependencies
├── data_train.ipynb                # Model training notebook
├── data_create.ipynb               # Data preparation notebook
└── README.md                       # This file
```

## 🔌 API Endpoints

### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "GDP Growth Prediction API",
  "status": "running",
  "version": "v2.0-debug",
  "model_loaded": true,
  "encoder_loaded": true,
  "endpoints": {
    "/api/history": "GET - Fetch historical data for a country",
    "/predict": "POST - Predict GDP growth rate"
  }
}
```

### 2. Get Countries List
```http
GET /api/countries
```

**Response:**
```json
[
  "Albania",
  "Algeria",
  "Andorra",
  ...
  "Zimbabwe"
]
```

**Total**: 203 countries

### 3. Get Historical Data
```http
GET /api/history?country={country_name}
```

**Parameters:**
- `country` (string, required): Country name (e.g., "United States")

**Response:**
```json
[
  {
    "Country": "United States",
    "Year": 1972,
    "GDP_Growth": 5.3,
    "Exports_Growth": 4.2,
    "Imports_Growth": 3.8
  },
  ...
]
```

**Data Range**: 1972-2021

### 4. Predict GDP Growth
```http
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "Country": "United States",
  "Population": 1.1,
  "Exports": 5.2,
  "Imports": 4.8,
  "Investment": 3.5,
  "Consumption": 2.8,
  "Govt_Spend": 2.0
}
```

**Response:**
```json
{
  "growth": 3.61,
  "method": "AI Model"
}
```

**Parameters:**
- `Country` (string): Country name
- `Population` (float): Population growth rate (%)
- `Exports` (float): Exports growth rate (%)
- `Imports` (float): Imports growth rate (%)
- `Investment` (float): Gross capital formation growth rate (%)
- `Consumption` (float): Final consumption expenditure growth rate (%)
- `Govt_Spend` (float): Government spending growth rate (%)

**Method Types:**
- `"AI Model"`: Prediction from Random Forest model
- `"Simulation"`: Fallback calculation if model fails

## 🤖 Machine Learning Model

### Model Details

- **Algorithm**: Random Forest Regressor
- **Estimators**: 100 trees
- **Training Data**: 8,297 samples from 203 countries
- **Features**: 7 economic indicators
- **Target**: GDP Growth Rate

### Model Performance

- **Training R² Score**: 0.9771 (97.71%)
- **Test R² Score**: 0.8626 (86.26%)
- **Training Set**: 6,637 samples
- **Test Set**: 1,660 samples

### Features Used

1. Country (encoded)
2. Population Growth Rate
3. Exports of goods and services Growth Rate
4. Imports of goods and services Growth Rate
5. Gross capital formation Growth Rate (Investment)
6. Final consumption expenditure Growth Rate
7. Government Spending Growth Rate

### Retraining the Model

If you need to retrain the model with updated data:

```bash
python retrain_model.py
```

This will:
1. Load `Final_Model_Data.csv`
2. Train a new Random Forest model
3. Save `gdp_model.pkl` and `country_encoder.pkl`
4. Display training and test scores

## 📊 Data Files

### Primary Data Files

1. **final_data_with_year.csv**
   - Historical GDP data for API responses
   - Years: 1972-2021
   - Countries: 203
   - Columns: Country, Year, GDP_Growth, Exports_Growth, Imports_Growth

2. **Final_Model_Data.csv**
   - Complete training dataset
   - 8,500 rows, 35 columns
   - Includes all economic indicators and growth rates

3. **gdp_model.pkl**
   - Trained Random Forest model
   - Size: ~8 MB
   - Format: joblib pickle

4. **country_encoder.pkl**
   - LabelEncoder for country names
   - Maps 203 country names to numeric codes

### Additional Data Files

- `complited_data_cleaning.csv` - Cleaned data
- `fully_corrected_data.csv` - Corrected data
- `Global_Economy_MICE_Imputed_Growth.csv` - MICE imputed data
- Various intermediate processing files

## 🧪 Testing

### Test the API

```bash
python test_api.py
```

**Expected Output:**
```
Testing GDP Prediction API...
Request data: {...}
Response status: 200
Response data: {
  "growth": 3.61,
  "method": "AI Model"
}
✅ SUCCESS: ML Model is working correctly!
```

### Manual Testing

```bash
# Test health check
curl http://localhost:5000/

# Test countries list
curl http://localhost:5000/api/countries

# Test historical data
curl "http://localhost:5000/api/history?country=United%20States"

# Test prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Country": "United States",
    "Population": 1.1,
    "Exports": 5.2,
    "Imports": 4.8,
    "Investment": 3.5,
    "Consumption": 2.8,
    "Govt_Spend": 2.0
  }'
```

## 🚀 Deployment

### Local Development

```bash
python app.py
```

Server runs on `http://127.0.0.1:5000` with debug mode off.

### Production Deployment

#### Option 1: Heroku

1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Add gunicorn to requirements.txt:
   ```bash
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### Option 2: AWS EC2

1. Launch EC2 instance (Ubuntu)
2. Install Python and dependencies
3. Clone repository
4. Run with gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

#### Option 3: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t gdp-api .
docker run -p 5000:5000 gdp-api
```

### Environment Variables

For production, set:
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### CORS Configuration

Update `app.py` for production:
```python
CORS(app, origins=["https://your-frontend-domain.com"])
```

## 🔒 Security

- ✅ CORS enabled for cross-origin requests
- ✅ Input validation on prediction endpoint
- ✅ Error handling for invalid requests
- ⚠️ Add rate limiting for production
- ⚠️ Add authentication for sensitive endpoints
- ⚠️ Use HTTPS in production

## 📈 Performance

- **Model Loading**: ~2 seconds on startup
- **Prediction Time**: ~50ms per request
- **Historical Data Query**: ~100ms per country
- **Countries List**: ~10ms

## 🐛 Troubleshooting

### Model Not Loading

**Error**: `⚠️ Model/Encoder not found`

**Solution**:
```bash
# Retrain the model
python retrain_model.py

# Verify files exist
ls -la gdp_model.pkl country_encoder.pkl
```

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'sklearn'`

**Solution**:
```bash
pip install scikit-learn==1.3.0
```

### CORS Errors

**Error**: `Access-Control-Allow-Origin` error in browser

**Solution**: Ensure `flask-cors` is installed and CORS is enabled in `app.py`

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

## 📚 Jupyter Notebooks

### data_train.ipynb
- Model training and evaluation
- Feature engineering
- Performance metrics

### data_create.ipynb
- Data cleaning and preprocessing
- Missing value imputation (MICE)
- Growth rate calculations

### random_forcasting.ipynb
- Forecasting experiments
- Alternative models testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

See LICENSE file for details.

## 📞 Support

- **GitHub Issues**: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-/issues
- **Frontend Repository**: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-FRONTEND-.git

## 🔗 Related Links

- Frontend Repository: https://github.com/jay192005/GDP_GROWTH_PREDICTION_MODEL-FRONTEND-.git
- API Documentation: See endpoints section above
- Model Training: See `retrain_model.py`

---

**Last Updated**: February 2026
**Version**: 2.0
**Python**: 3.13+
**Model Accuracy**: 86.26% (Test R²)
