"""Price Prediction Service.

This module provides prediction logic for commodity price prediction based on
market data, temporal features, and location information.
"""

import numpy as np
from datetime import datetime
from src.services.price_predection.model import get_price_prediction_bundle
from src.schemas.price_predection_schemas import PricePredictionRequest, PricePredictionResponse


def predict_price(request: PricePredictionRequest) -> PricePredictionResponse:
    """
    Predict price (BDT) for a commodity in a given market and date.

    Args:
        request: PricePredictionRequest containing market, commodity, and temporal data

    Returns:
        PricePredictionResponse with predicted price and request metadata

    Raises:
        ValueError: If input data is invalid or model prediction fails
        KeyError: If categorical values not found in label encoders
    """

    # Load the prediction bundle
    bundle = get_price_prediction_bundle()
    model = bundle['model']
    label_encoders = bundle['label_encoders']
    features = bundle['features']

    # Create record dictionary from request
    record = {
        'date': request.date,
        'admin1': request.admin1,
        'admin2': request.admin2,
        'market': request.market,
        'latitude': request.latitude,
        'longitude': request.longitude,
        'category': request.category,
        'commodity': request.commodity,
        'unit': request.unit,
        'priceflag': request.priceflag,
        'pricetype': request.pricetype,
    }

    try:
        # Parse date string and extract temporal features
        dt = datetime.strptime(record['date'], '%Y-%m-%d')
        record['year'] = dt.year
        record['month'] = dt.month
        
        # Calculate quarter (Q1: 1-3, Q2: 4-6, Q3: 7-9, Q4: 10-12)
        record['quarter'] = (dt.month - 1) // 3 + 1
        
        # Seasonal encoding using sine and cosine
        record['month_sin'] = np.sin(2 * np.pi * dt.month / 12)
        record['month_cos'] = np.cos(2 * np.pi * dt.month / 12)

        # Encode categorical features
        categorical_cols = [
            'admin1', 'admin2', 'market', 'category',
            'commodity', 'unit', 'priceflag', 'pricetype'
        ]

        for col in categorical_cols:
            le = label_encoders[col]
            val = record[col]
            
            # Handle unseen categories by using -1
            try:
                record[col + '_enc'] = le.transform([val])[0]
            except ValueError:
                # Category not seen during training, use -1
                record[col + '_enc'] = -1

        # Prepare feature array in correct order
        feature_values = []
        for feat in features:
            feature_values.append(record.get(feat, 0))
        
        feature_array = np.array([feature_values])

        # Make prediction (model uses log transformation, so we apply inverse)
        predicted_price = float(np.expm1(model.predict(feature_array)[0]))

        # Ensure non-negative price
        predicted_price = max(predicted_price, 0.0)

        return PricePredictionResponse(
            predicted_price=round(predicted_price, 2),
            commodity=request.commodity,
            market=request.market,
            unit=request.unit,
            date=request.date
        )

    except KeyError as e:
        raise ValueError(f"Missing label encoder for feature: {str(e)}")
    
    except ValueError as e:
        raise ValueError(f"Price prediction failed: {str(e)}")

