"""
Fertilizer Recommendation - Numpy Array Testing & Batch Predictions

This script demonstrates how to use the fertilizer model directly with numpy arrays
for testing, batch predictions, and data analysis.
"""

import pickle
import numpy as np
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

# Load models and encoders
print("=" * 60)
print("Loading Models & Encoders...")
print("=" * 60)

le_fertilizer = pickle.load(open(ASSETS_DIR / 'fertilizer_encoder.pkl', 'rb'))
le_crop = pickle.load(open(ASSETS_DIR / 'crop_encoder.pkl', 'rb'))
le_soil = pickle.load(open(ASSETS_DIR / 'soil_encoder.pkl', 'rb'))
model = pickle.load(open(ASSETS_DIR / 'fertilizer_model.pkl', 'rb'))

print(f"✅ Model loaded: {type(model).__name__}")
print(f"✅ Fertilizer encoder classes: {len(le_fertilizer.classes_)}")
print(f"✅ Crop encoder classes: {len(le_crop.classes_)}")
print(f"✅ Soil encoder classes: {len(le_soil.classes_)}")
print(f"✅ Model features: {list(model.feature_names_in_)}")

# Get model feature order
model_features = model.feature_names_in_


print("\n" + "=" * 60)
print("Example 1: Single Prediction (Original Example)")
print("=" * 60)

# Single prediction example
crop = 'Wheat'
soil_color = 'Red'
temperature = 25
nitrogen = 80
potassium = 40
phosphorus = 40
rainfall = 100
ph = 6.5

print(f"\n📊 Input Data:")
print(f"  Crop: {crop}")
print(f"  Soil Color: {soil_color}")
print(f"  Temperature: {temperature}°C")
print(f"  Nitrogen: {nitrogen}")
print(f"  Potassium: {potassium}")
print(f"  Phosphorus: {phosphorus}")
print(f"  Rainfall: {rainfall}mm")
print(f"  pH: {ph}")

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

# Build numpy array with correct feature order (2D array for single prediction)
feature_array = np.array([[features[f] for f in model_features]])

# Make prediction
prediction_encoded = model.predict(feature_array)
predicted_fertilizer = le_fertilizer.inverse_transform(prediction_encoded)[0]

# Get confidence (if available)
try:
    probabilities = model.predict_proba(feature_array)[0]
    confidence = max(probabilities)
    print(f"\n🎯 Predicted Fertilizer: {predicted_fertilizer}")
    print(f"📈 Confidence: {confidence:.2%}")
except AttributeError:
    print(f"\n🎯 Predicted Fertilizer: {predicted_fertilizer}")
    print("📈 Confidence: N/A (model doesn't support probability)")


print("\n" + "=" * 60)
print("Example 2: Batch Predictions (Multiple Samples)")
print("=" * 60)

# Multiple samples for batch prediction
batch_data = {
    'crops': ['Wheat', 'Rice', 'Maize', 'Cotton', 'Wheat'],
    'soil_colors': ['Red', 'Black', 'Brown', 'Red', 'Black'],
    'temperatures': [25, 30, 28, 35, 22],
    'nitrogen': [80, 75, 70, 60, 85],
    'potassium': [40, 45, 50, 35, 42],
    'phosphorus': [40, 38, 45, 30, 40],
    'rainfall': [100, 150, 120, 80, 110],
    'ph': [6.5, 6.8, 6.2, 7.0, 6.4]
}

n_samples = len(batch_data['crops'])

print(f"\n📊 Batch Input Data ({n_samples} samples):")
for i in range(n_samples):
    print(f"\n  Sample {i+1}:")
    print(f"    Crop: {batch_data['crops'][i]}, Soil: {batch_data['soil_colors'][i]}")
    print(f"    Temp: {batch_data['temperatures'][i]}°C, N: {batch_data['nitrogen'][i]}, "
          f"K: {batch_data['potassium'][i]}, P: {batch_data['phosphorus'][i]}")
    print(f"    Rainfall: {batch_data['rainfall'][i]}mm, pH: {batch_data['ph'][i]}")

# Encode categorical features for batch
crops_encoded = le_crop.transform(batch_data['crops'])
soils_encoded = le_soil.transform(batch_data['soil_colors'])

# Build batch feature array
batch_features = []
for i in range(n_samples):
    feature_dict = {
        'Crop': crops_encoded[i],
        'Soil_color': soils_encoded[i],
        'Temperature': batch_data['temperatures'][i],
        'Nitrogen': batch_data['nitrogen'][i],
        'Potassium': batch_data['potassium'][i],
        'Phosphorus': batch_data['phosphorus'][i],
        'Rainfall': batch_data['rainfall'][i],
        'pH': batch_data['ph'][i]
    }
    # Maintain correct feature order
    batch_features.append([feature_dict[f] for f in model_features])

# Convert to numpy array
batch_array = np.array(batch_features)
print(f"\n📐 Batch array shape: {batch_array.shape}")

# Make batch predictions
batch_predictions = model.predict(batch_array)
batch_fertilizers = le_fertilizer.inverse_transform(batch_predictions)

# Get confidences for batch
try:
    batch_probabilities = model.predict_proba(batch_array)
    batch_confidences = [max(probs) for probs in batch_probabilities]
except AttributeError:
    batch_confidences = [1.0] * n_samples

print("\n🎯 Batch Prediction Results:")
for i in range(n_samples):
    print(f"\n  Sample {i+1}: {batch_data['crops'][i]} in {batch_data['soil_colors'][i]} soil")
    print(f"    → Fertilizer: {batch_fertilizers[i]}")
    print(f"    → Confidence: {batch_confidences[i]:.2%}")


print("\n" + "=" * 60)
print("Example 3: Available Encoder Classes")
print("=" * 60)

print(f"\n🌾 Available Crops ({len(le_crop.classes_)}):")
crops_list = ', '.join(le_crop.classes_)
print(f"   {crops_list}")

print(f"\n🟤 Available Soil Colors ({len(le_soil.classes_)}):")
soils_list = ', '.join(le_soil.classes_)
print(f"   {soils_list}")

print(f"\n💚 Available Fertilizers ({len(le_fertilizer.classes_)}):")
fertilizers_list = ', '.join(le_fertilizer.classes_)
print(f"   {fertilizers_list}")


print("\n" + "=" * 60)
print("Example 4: Load from CSV and Predict (using numpy)")
print("=" * 60)

# Example CSV data
csv_data = """Wheat,Red,25.0,80,40,40,100,6.5
Rice,Black,30.0,75,45,38,150,6.8
Maize,Brown,28.0,70,50,45,120,6.2"""

# Parse CSV manually to numpy array
lines = csv_data.strip().split('\n')
n_rows = len(lines)

crops_csv = []
soils_csv = []
numerical_data = []

for line in lines:
    parts = line.split(',')
    crops_csv.append(parts[0])
    soils_csv.append(parts[1])
    numerical_data.append([float(x) for x in parts[2:]])

print(f"\n📊 Data loaded: {n_rows} rows")

# Encode categorical
crops_encoded_csv = le_crop.transform(crops_csv)
soils_encoded_csv = le_soil.transform(soils_csv)

# Build feature array
csv_features = []
for i in range(n_rows):
    feature_dict = {
        'Crop': crops_encoded_csv[i],
        'Soil_color': soils_encoded_csv[i],
        'Temperature': numerical_data[i][0],
        'Nitrogen': numerical_data[i][1],
        'Potassium': numerical_data[i][2],
        'Phosphorus': numerical_data[i][3],
        'Rainfall': numerical_data[i][4],
        'pH': numerical_data[i][5]
    }
    csv_features.append([feature_dict[f] for f in model_features])

csv_array = np.array(csv_features)

# Predict
csv_predictions = model.predict(csv_array)
csv_fertilizers = le_fertilizer.inverse_transform(csv_predictions)

print("\n🎯 CSV Prediction Results:")
for i in range(n_rows):
    print(f"  {crops_csv[i]} → {csv_fertilizers[i]}")


print("\n" + "=" * 60)
print("Example 5: Model Information")
print("=" * 60)

print(f"\n📊 Model Type: {type(model).__name__}")
print(f"📊 Number of Features: {len(model.feature_names_in_)}")
print(f"📊 Feature Names: {list(model.feature_names_in_)}")

# Try to get more model info
try:
    if hasattr(model, 'get_params'):
        params = model.get_params()
        print(f"📊 Model Parameters: {list(params.keys())}")
except:
    pass

try:
    if hasattr(model, 'classes_'):
        print(f"📊 Number of Classes: {len(model.classes_)}")
except:
    pass


print("\n" + "=" * 60)
print("Example 6: Using Direct Numpy Arrays (No Dictionaries)")
print("=" * 60)

# Direct numpy array construction
# Order: Crop, Soil_color, Temperature, Nitrogen, Potassium, Phosphorus, Rainfall, pH
direct_input = np.array([
    [le_crop.transform(['Wheat'])[0], le_soil.transform(['Red'])[0], 25, 80, 40, 40, 100, 6.5],
    [le_crop.transform(['Rice'])[0], le_soil.transform(['Black'])[0], 30, 75, 45, 38, 150, 6.8]
])

print(f"\n📐 Direct numpy array shape: {direct_input.shape}")
print(f"   Array:\n{direct_input}")

# Predict
direct_predictions = model.predict(direct_input)
direct_fertilizers = le_fertilizer.inverse_transform(direct_predictions)

print(f"\n🎯 Direct Array Predictions:")
print(f"   Sample 1: {direct_fertilizers[0]}")
print(f"   Sample 2: {direct_fertilizers[1]}")


print("\n" + "=" * 60)
print("✅ All Numpy Array Examples Completed Successfully!")
print("=" * 60)
