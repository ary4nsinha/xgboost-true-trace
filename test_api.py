import requests
import json

# Base URL of the API
BASE_URL = "http://127.0.0.1:8000"

def test_root():
    """Test the root endpoint"""
    print("\n" + "="*50)
    print("Testing Root Endpoint")
    print("="*50)

    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_health():
    """Test the health check endpoint"""
    print("\n" + "="*50)
    print("Testing Health Check Endpoint")
    print("="*50)

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_predict():
    """Test the prediction endpoint"""
    print("\n" + "="*50)
    print("Testing Prediction Endpoint")
    print("="*50)

    # Sample input data
    test_data = {
        "Recycled Content %": 60.0,
        "Virgin Content %": 40.0,
        "Carbon Footprint (kg CO2e)": 80.0,
        "Water Consumption (L)": 400.0,
        "Power Consumption (kWh)": 30.0,
        "Packaging Recycled Content %": 50.0,
        "Expected Lifespan (yrs)": 7.0,
        "Base Material": "metal",
        "Contains Plastic": "no",
        "Biodegradable": "no",
        "Compostable": "no",
        "Recyclability Level": "high",
        "Reusability": "high",
        "Repairability": "high",
        "End-of-Life": "recyclable",
        "Coating Type": "none",
        "Mixed Materials": "no",
        "Toxicity Concerns": "none",
        "Packaging Material": "cardboard",
        "Packaging Recyclable": "yes",
        "Food Safe": "yes",
        "Chemical Leaching Risk": "none",
        "SVHC Presence": "no",
        "Plasticizer Type": "none"
    }

    print(f"\nInput Data:")
    print(json.dumps(test_data, indent=2))

    response = requests.post(
        f"{BASE_URL}/predict",
        json=test_data
    )

    print(f"\nStatus Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")

def test_low_sustainability():
    """Test with low sustainability material"""
    print("\n" + "="*50)
    print("Testing Low Sustainability Material")
    print("="*50)

    # Low sustainability material
    test_data = {
        "Recycled Content %": 5.0,
        "Virgin Content %": 95.0,
        "Carbon Footprint (kg CO2e)": 500.0,
        "Water Consumption (L)": 2000.0,
        "Power Consumption (kWh)": 200.0,
        "Packaging Recycled Content %": 0.0,
        "Expected Lifespan (yrs)": 1.0,
        "Base Material": "plastic",
        "Contains Plastic": "yes",
        "Biodegradable": "no",
        "Compostable": "no",
        "Recyclability Level": "low",
        "Reusability": "low",
        "Repairability": "low",
        "End-of-Life": "landfill",
        "Coating Type": "chemical",
        "Mixed Materials": "yes",
        "Toxicity Concerns": "high",
        "Packaging Material": "plastic",
        "Packaging Recyclable": "no",
        "Food Safe": "no",
        "Chemical Leaching Risk": "high",
        "SVHC Presence": "yes",
        "Plasticizer Type": "phthalate"
    }

    response = requests.post(
        f"{BASE_URL}/predict",
        json=test_data
    )

    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    try:
        print("\n🚀 Starting API Tests...")
        print("="*50)

        # Run all tests
        test_root()
        test_health()
        test_predict()
        test_low_sustainability()

        print("\n" + "="*50)
        print("✅ All tests completed!")
        print("="*50)

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API.")
        print("Make sure the FastAPI server is running on http://127.0.0.1:8000")
        print("\nTo start the server, run:")
        print("  python mlfastapi.py")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
