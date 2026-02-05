import requests
import json

# Test the prediction endpoint
url = "http://localhost:5000/predict"

test_data = {
    "Country": "United States",
    "Population": 1.1,
    "Exports": 5.2,
    "Imports": 4.8,
    "Investment": 3.5,
    "Consumption": 2.8,
    "Govt_Spend": 2.0
}

print("Testing GDP Prediction API...")
print(f"Request data: {json.dumps(test_data, indent=2)}")

response = requests.post(url, json=test_data)

print(f"\nResponse status: {response.status_code}")
print(f"Response data: {json.dumps(response.json(), indent=2)}")

if response.json().get('method') == 'AI Model':
    print("\n✅ SUCCESS: ML Model is working correctly!")
else:
    print("\n⚠️ WARNING: Using fallback simulation")
