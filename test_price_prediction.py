#!/usr/bin/env python
"""Test script for price prediction module."""

import sys
sys.path.insert(0, '/home/kawser-miah/Documents/flutter_project/farmer_assistance_backend')

from src.schemas.price_predection_schemas import PricePredictionRequest, PricePredictionResponse
from src.services.price_predection.predict import predict_price

# Example prediction request
sample_request = PricePredictionRequest(
    date='2025-09-15',
    admin1='Dhaka',
    admin2='Dhaka',
    market='Dhaka (Karwan Bazar)',
    latitude=23.81,
    longitude=90.41,
    category='cereals and tubers',
    commodity='Rice (coarse)',
    unit='KG',
    priceflag='actual',
    pricetype='Retail',
)

try:
    print("Testing price prediction...")
    result = predict_price(sample_request)
    
    print("✅ Prediction successful!")
    print(f"\n📊 Price Prediction Results:")
    print(f"  Commodity  : {result.commodity}")
    print(f"  Market     : {result.market}")
    print(f"  Date       : {result.date}")
    print(f"  Unit       : {result.unit}")
    print(f"  💰 Price   : {result.predicted_price} BDT")
    
    # Verify response model
    if isinstance(result, PricePredictionResponse):
        print("\n✅ Response model validation passed!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
