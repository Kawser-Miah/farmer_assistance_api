"""
Test script for Fertilizer Tips API endpoint

This script demonstrates how to test the fertilizer prediction endpoint
with sample data matching your original example.
"""

import requests
import json

# API endpoint
BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/fertilizer-tips/predict"

# Sample request data (from your original example)
sample_data = {
    "crop": "Wheat",
    "soil_color": "Red",
    "temperature": 25.0,
    "nitrogen": 80.0,
    "potassium": 40.0,
    "phosphorus": 40.0,
    "rainfall": 100.0,
    "ph": 6.5
}

# Headers with JWT token (replace with actual token)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_SUPABASE_JWT_TOKEN_HERE"
}

def test_fertilizer_prediction():
    """Test the fertilizer prediction endpoint"""
    print("=" * 60)
    print("Testing Fertilizer Tips Prediction API")
    print("=" * 60)

    print(f"\n📡 Endpoint: {ENDPOINT}")
    print(f"\n📥 Request Data:")
    print(json.dumps(sample_data, indent=2))

    try:
        response = requests.post(
            ENDPOINT,
            json=sample_data,
            headers=headers,
            timeout=10
        )

        print(f"\n📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Success! Prediction Result:")
            print(json.dumps(result, indent=2))
            print(f"\n🌱 Recommended Fertilizer: {result['fertilizer']}")
            print(f"📈 Confidence: {result['confidence']:.2%}")
        else:
            print(f"\n❌ Error: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server")
        print("Make sure the server is running: uvicorn src.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    test_fertilizer_prediction()


# ============================================================================
# CURL Command Alternative (for terminal testing)
# ============================================================================
"""
curl -X POST "http://localhost:8000/fertilizer-tips/predict" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_SUPABASE_JWT_TOKEN" \
  -d '{
    "crop": "Wheat",
    "soil_color": "Red",
    "temperature": 25.0,
    "nitrogen": 80.0,
    "potassium": 40.0,
    "phosphorus": 40.0,
    "rainfall": 100.0,
    "ph": 6.5
  }'
"""
