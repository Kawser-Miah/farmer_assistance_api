"""
Quick Numpy Test - Fertilizer Prediction
Simple script for quick testing using numpy arrays
"""

import pickle
import numpy as np
from pathlib import Path

# Paths
assets = Path("assets")

# Load models
print("Loading models...")
model = pickle.load(open(assets / 'fertilizer_model.pkl', 'rb'))
le_fertilizer = pickle.load(open(assets / 'fertilizer_encoder.pkl', 'rb'))
le_crop = pickle.load(open(assets / 'crop_encoder.pkl', 'rb'))
le_soil = pickle.load(open(assets / 'soil_encoder.pkl', 'rb'))

print("✅ Models loaded!\n")

# Input data
crop = 'Wheat'
soil_color = 'Red'
temperature = 25
nitrogen = 80
potassium = 40
phosphorus = 40
rainfall = 100
ph = 6.5

print("Input Data:")
print(f"  Crop: {crop}")
print(f"  Soil Color: {soil_color}")
print(f"  Temperature: {temperature}°C")
print(f"  Nitrogen: {nitrogen}")
print(f"  Potassium: {potassium}")
print(f"  Phosphorus: {phosphorus}")
print(f"  Rainfall: {rainfall}mm")
print(f"  pH: {ph}")
print()

# Encode categorical features
crop_encoded = le_crop.transform([crop])[0]
soil_encoded = le_soil.transform([soil_color])[0]

# Create feature dictionary
features = {
    'Crop': crop_encoded,
    'Soil_color': soil_encoded,
    'Temperature': temperature,
    'Nitrogen': nitrogen,
    'Potassium': potassium,
    'Phosphorus': phosphorus,
    'Rainfall': rainfall,
    'pH': ph
}

# Build numpy array with correct feature order
model_features = model.feature_names_in_
feature_array = np.array([[features[f] for f in model_features]])

print(f"Feature array shape: {feature_array.shape}")
print(f"Feature order: {list(model_features)}")
print()

# Predict
prediction = model.predict(feature_array)
fertilizer = le_fertilizer.inverse_transform(prediction)[0]

# Get confidence
try:
    proba = model.predict_proba(feature_array)[0]
    confidence = max(proba) * 100
    print(f"🌱 Recommended Fertilizer: {fertilizer}")
    print(f"📈 Confidence: {confidence:.1f}%")
except:
    print(f"🌱 Recommended Fertilizer: {fertilizer}")
