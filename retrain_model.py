"""
Retrain the GDP prediction model with current scikit-learn version
Using features that match the API requirements
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

print("Loading data...")
# Load the training data
df = pd.read_csv('Final_Model_Data.csv')

print(f"Data shape: {df.shape}")
print(f"Available columns: {df.columns.tolist()}")

# Check if we have government spending data
if 'General government final consumption expenditure_Growth_Rate' in df.columns:
    govt_col = 'General government final consumption expenditure_Growth_Rate'
elif 'General government final consumption expenditure' in df.columns:
    # Calculate growth rate if we have the raw data
    df_sorted = df.sort_values(['Country', 'Year'])
    df['Govt_Spend_Growth_Rate'] = df_sorted.groupby('Country')['General government final consumption expenditure'].pct_change() * 100
    govt_col = 'Govt_Spend_Growth_Rate'
else:
    # Use Per capita GNI as proxy if government spending not available
    govt_col = 'Per capita GNI_Growth_Rate'
    print(f"⚠️ Using {govt_col} as proxy for government spending")

# Prepare features and target
# Encode country names
encoder = LabelEncoder()
df['Country_Encoded'] = encoder.fit_transform(df['Country'])

# Select features for training - matching API requirements
feature_columns = [
    'Country_Encoded',
    'Population_Growth_Rate',
    'Exports of goods and services_Growth_Rate',
    'Imports of goods and services_Growth_Rate',
    'Gross capital formation_Growth_Rate',  # Investment
    'Final consumption expenditure_Growth_Rate',  # Consumption
    govt_col  # Government Spending
]

target_column = 'GDP_Growth_Rate'

# Remove rows with missing values
df_clean = df[feature_columns + [target_column]].dropna()

print(f"Clean data shape: {df_clean.shape}")
print(f"Features used: {feature_columns}")

X = df_clean[feature_columns]
y = df_clean[target_column]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape}")
print(f"Test set size: {X_test.shape}")

# Train model
print("Training Random Forest model...")
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Training R² score: {train_score:.4f}")
print(f"Test R² score: {test_score:.4f}")

# Save model and encoder
print("Saving model and encoder...")
joblib.dump(model, 'gdp_model.pkl')
joblib.dump(encoder, 'country_encoder.pkl')

print("✅ Model and encoder saved successfully!")
print(f"Model type: {type(model).__name__}")
print(f"Encoder classes: {len(encoder.classes_)} countries")
print(f"Feature names: {model.feature_names_in_}")
