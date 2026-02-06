"""
Quick test script for multiple country predictions
"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("GDP PREDICTION TESTS - MULTIPLE COUNTRIES")
print("=" * 60)

# Test data: (Country, Population, Exports, Imports, Investment, Consumption, Govt_Spend)
test_cases = [
    ("United States", 1.1, 5.2, 4.8, 3.5, 2.8, 2.0),
    ("China", 0.5, 8.0, 7.5, 6.0, 5.5, 3.0),
    ("India", 1.2, 6.5, 5.8, 4.5, 4.0, 2.5),
    ("Germany", 0.3, 4.5, 4.2, 2.8, 2.5, 1.8),
    ("Brazil", 0.8, 3.5, 3.2, 2.0, 2.2, 1.5),
]

for country, pop, exp, imp, inv, cons, govt in test_cases:
    payload = {
        "Country": country,
        "Population": pop,
        "Exports": exp,
        "Imports": imp,
        "Investment": inv,
        "Consumption": cons,
        "Govt_Spend": govt
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n{country}:")
        print(f"  Input (T-1 growth rates):")
        print(f"    Population: {pop}%, Exports: {exp}%, Imports: {imp}%")
        print(f"    Investment: {inv}%, Consumption: {cons}%, Govt: {govt}%")
        print(f"  Predicted GDP Growth (T): {result['growth']}%")
        print(f"  Method: {result['method']}")
    else:
        print(f"\n{country}: ERROR - {response.json()['message']}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
