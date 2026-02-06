"""
GDP Economic Scenario Simulator - Model Training
Uses concurrent indicators (same year) for sensitivity analysis and policy simulation

This is NOT a forecasting model - it's a scenario simulator that answers:
"If exports grow by X% and investment grows by Y%, what happens to GDP?"

Scientific Validity: Uses the GDP accounting identity relationship
GDP = Consumption + Investment + Government + (Exports - Imports)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

from config import DATASET_PATH


def prepare_features(df, encoder=None, fit_encoder=False):
    """
    Prepare features for scenario simulation
    Uses CURRENT YEAR growth rates (concurrent indicators)
    """
    # Encode country names
    if encoder is None:
        encoder = LabelEncoder()
        fit_encoder = True
    
    if fit_encoder:
        df['Country_Encoded'] = encoder.fit_transform(df['Country'])
    else:
        df['Country_Encoded'] = encoder.transform(df['Country'])
    
    # Feature columns - CURRENT YEAR (no lagging)
    feature_columns = [
        'Country_Encoded',
        'Population_Growth_Rate',
        'Exports of goods and services_Growth_Rate',
        'Imports of goods and services_Growth_Rate',
        'Gross capital formation_Growth_Rate',
        'Final consumption expenditure_Growth_Rate',
        'Government_Expenditure_Growth_Rate'
    ]
    
    X = df[feature_columns]
    y = df['GDP_Growth_Rate']
    
    return X, y, encoder, feature_columns


def evaluate_model(model, X_train, y_train, X_test, y_test):
    """
    Evaluate model performance
    """
    print("\n📈 Model Performance:")
    print("=" * 60)
    
    # Training performance
    y_train_pred = model.predict(X_train)
    train_r2 = r2_score(y_train, y_train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    
    print(f"Training Set ({len(X_train)} samples):")
    print(f"   R² Score: {train_r2:.4f} ({train_r2*100:.2f}%)")
    print(f"   RMSE: {train_rmse:.4f}")
    print(f"   MAE: {train_mae:.4f}")
    
    # Test performance
    y_test_pred = model.predict(X_test)
    test_r2 = r2_score(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    print(f"\nTest Set ({len(X_test)} samples):")
    print(f"   R² Score: {test_r2:.4f} ({test_r2*100:.2f}%)")
    print(f"   RMSE: {test_rmse:.4f}")
    print(f"   MAE: {test_mae:.4f}")
    
    print("=" * 60)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': [
            'Country',
            'Population Growth',
            'Exports Growth',
            'Imports Growth',
            'Investment Growth',
            'Consumption Growth',
            'Government Spending Growth'
        ],
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\n🔍 Feature Importance (Economic Drivers):")
    for idx, row in feature_importance.iterrows():
        print(f"   {row['Feature']}: {row['Importance']:.4f}")
    
    return {
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse
    }


def main():
    """
    Main training pipeline for GDP Scenario Simulator
    """
    print("=" * 60)
    print("GDP ECONOMIC SCENARIO SIMULATOR - Model Training")
    print("=" * 60)
    print("\n📌 Purpose: Sensitivity Analysis & Policy Simulation")
    print("   NOT forecasting - simulates economic scenarios")
    print("   Example: 'If exports grow 10%, what happens to GDP?'")
    
    # Load data
    print(f"\n📂 Loading data from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    print(f"   Loaded {len(df)} samples")
    print(f"   Countries: {df['Country'].nunique()}")
    print(f"   Years: {df['Year'].min()} - {df['Year'].max()}")
    
    # Prepare features (NO LAGGING - current year indicators)
    print("\n🔧 Preparing features (concurrent indicators)...")
    X, y, encoder, feature_columns = prepare_features(df, fit_encoder=True)
    
    print(f"   Features shape: {X.shape}")
    print(f"   Using CURRENT YEAR growth rates (no lagging)")
    
    # Standard train/test split with shuffle
    print("\n📊 Splitting data (80/20 with shuffle)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        shuffle=True
    )
    
    print(f"   Training: {len(X_train)} samples (80%)")
    print(f"   Test: {len(X_test)} samples (20%)")
    
    # Train model
    print(f"\n🤖 Training Random Forest Regressor...")
    
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print(f"   ✅ Training complete!")
    
    # Evaluate model
    results = evaluate_model(model, X_train, y_train, X_test, y_test)
    
    # Check if we achieved target accuracy
    if results['test_r2'] >= 0.85:
        print(f"\n✅ Target accuracy achieved! Test R² = {results['test_r2']:.4f} (>85%)")
    elif results['test_r2'] >= 0.80:
        print(f"\n⚠️ Close to target. Test R² = {results['test_r2']:.4f} (80-85%)")
    else:
        print(f"\n⚠️ Below target. Test R² = {results['test_r2']:.4f} (<80%)")
    
    # Save model and encoder
    model_path = "gdp_scenario_model.pkl"
    encoder_path = "country_encoder_scenario.pkl"
    
    print(f"\n💾 Saving model to: {model_path}")
    joblib.dump(model, model_path)
    
    print(f"💾 Saving encoder to: {encoder_path}")
    joblib.dump(encoder, encoder_path)
    
    # Save feature columns for API
    feature_info = {
        'feature_columns': feature_columns,
        'feature_names': [
            'Country_Encoded',
            'Population_Growth_Rate',
            'Exports_Growth_Rate',
            'Imports_Growth_Rate',
            'Investment_Growth_Rate',
            'Consumption_Growth_Rate',
            'Govt_Spend_Growth_Rate'
        ]
    }
    joblib.dump(feature_info, 'feature_info_scenario.pkl')
    print(f"💾 Saving feature info to: feature_info_scenario.pkl")
    
    print("\n✅ Training pipeline complete!")
    print("=" * 60)
    
    # Example scenario simulation
    print("\n🧪 Example Scenario Simulation:")
    print("   Scenario: Boost exports by 10%, keep others at 2%")
    
    # Get a sample country
    sample_country = "United States"
    country_code = encoder.transform([sample_country])[0]
    
    scenario_features = [
        country_code,  # Country
        1.0,          # Population: 1%
        10.0,         # Exports: 10% (boosted)
        2.0,          # Imports: 2%
        2.0,          # Investment: 2%
        2.0,          # Consumption: 2%
        2.0           # Government: 2%
    ]
    
    predicted_gdp = model.predict([scenario_features])[0]
    print(f"   Country: {sample_country}")
    print(f"   Predicted GDP Growth: {predicted_gdp:.2f}%")
    
    print("\n📌 Model Purpose:")
    print("   ✅ Sensitivity Analysis: Test impact of policy changes")
    print("   ✅ Scenario Planning: Simulate different economic conditions")
    print("   ✅ Policy Simulation: Evaluate fiscal policy effects")
    print("   ❌ NOT for forecasting future GDP")


if __name__ == "__main__":
    main()
