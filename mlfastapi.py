from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
import joblib
import pandas as pd
import numpy as np

app = FastAPI(
    title="Sustainability Score Prediction API",
    description="API for predicting sustainability scores of materials",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained pipeline
MODEL_PATH = "best_sustainability_model.joblib"
try:
    pipeline = joblib.load(MODEL_PATH)
    print(f"✓ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    raise

# Feature lists
NUMERIC_FEATURES = [
    "Recycled Content %",
    "Virgin Content %",
    "Carbon Footprint (kg CO2e)",
    "Water Consumption (L)",
    "Power Consumption (kWh)",
    "Packaging Recycled Content %",
    "Expected Lifespan (yrs)"
]

CATEGORICAL_FEATURES = [
    "Base Material",
    "Contains Plastic",
    "Biodegradable",
    "Compostable",
    "Recyclability Level",
    "Reusability",
    "Repairability",
    "End-of-Life",
    "Coating Type",
    "Mixed Materials",
    "Toxicity Concerns",
    "Packaging Material",
    "Packaging Recyclable",
    "Food Safe",
    "Chemical Leaching Risk",
    "SVHC Presence",
    "Plasticizer Type"
]

ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

class SustainabilityInput(BaseModel):
    recycled_content: float = Field(..., alias="Recycled Content %", ge=0, le=100)
    virgin_content: float = Field(..., alias="Virgin Content %", ge=0, le=100)
    carbon_footprint: float = Field(..., alias="Carbon Footprint (kg CO2e)", ge=0)
    water_consumption: float = Field(..., alias="Water Consumption (L)", ge=0)
    power_consumption: float = Field(..., alias="Power Consumption (kWh)", ge=0)
    packaging_recycled_content: float = Field(..., alias="Packaging Recycled Content %", ge=0, le=100)
    expected_lifespan: float = Field(..., alias="Expected Lifespan (yrs)", ge=0)

    base_material: str = Field(..., alias="Base Material")
    contains_plastic: str = Field(..., alias="Contains Plastic")
    biodegradable: str = Field(..., alias="Biodegradable")
    compostable: str = Field(..., alias="Compostable")
    recyclability_level: str = Field(..., alias="Recyclability Level")
    reusability: str = Field(..., alias="Reusability")
    repairability: str = Field(..., alias="Repairability")
    end_of_life: str = Field(..., alias="End-of-Life")
    coating_type: str = Field(..., alias="Coating Type")
    mixed_materials: str = Field(..., alias="Mixed Materials")
    toxicity_concerns: str = Field(..., alias="Toxicity Concerns")
    packaging_material: str = Field(..., alias="Packaging Material")
    packaging_recyclable: str = Field(..., alias="Packaging Recyclable")
    food_safe: str = Field(..., alias="Food Safe")
    chemical_leaching_risk: str = Field(..., alias="Chemical Leaching Risk")
    svhc_presence: str = Field(..., alias="SVHC Presence")
    plasticizer_type: str = Field(..., alias="Plasticizer Type")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "Recycled Content %": 50.0,
                "Virgin Content %": 50.0,
                "Carbon Footprint (kg CO2e)": 100.0,
                "Water Consumption (L)": 500.0,
                "Power Consumption (kWh)": 50.0,
                "Packaging Recycled Content %": 30.0,
                "Expected Lifespan (yrs)": 5.0,
                "Base Material": "plastic",
                "Contains Plastic": "yes",
                "Biodegradable": "no",
                "Compostable": "no",
                "Recyclability Level": "high",
                "Reusability": "medium",
                "Repairability": "low",
                "End-of-Life": "recyclable",
                "Coating Type": "none",
                "Mixed Materials": "no",
                "Toxicity Concerns": "none",
                "Packaging Material": "cardboard",
                "Packaging Recyclable": "yes",
                "Food Safe": "yes",
                "Chemical Leaching Risk": "low",
                "SVHC Presence": "no",
                "Plasticizer Type": "none"
            }
        }


class PredictionResponse(BaseModel):
    sustainability_score: float
    message: str


def clean_text(x) -> str:
    """Clean and normalize text fields"""
    if pd.isna(x):
        return "unknown"
    return str(x).strip().lower()


def predict_sustainability_score(input_data: dict) -> float:
    """
    Predict sustainability score from input data
    """
    df = pd.DataFrame([input_data])

    for col in CATEGORICAL_FEATURES:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    df = df[ALL_FEATURES]

    print("\n=== INPUT DATA ===")
    print(df.T)

    try:
        transformed = pipeline.named_steps['preprocess'].transform(df)
        print("\n=== TRANSFORMED DATA (first 10 features) ===")
        print(transformed[0][:10])

        prediction = pipeline.predict(df)
        return float(prediction[0])
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise


@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Sustainability Score Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Predict sustainability score",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation (Swagger UI)",
            "/redoc": "GET - API documentation (ReDoc)"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": pipeline is not None
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(input_data: SustainabilityInput):
    """
    Predict sustainability score for given material properties

    Returns a score typically between 0-100 representing sustainability rating
    """
    try:
        data_dict = input_data.model_dump(by_alias=True)
        score = predict_sustainability_score(data_dict)

        if score >= 80:
            message = "Excellent sustainability score!"
        elif score >= 60:
            message = "Good sustainability score"
        elif score >= 40:
            message = "Moderate sustainability score"
        else:
            message = "Low sustainability score - consider improvements"

        return PredictionResponse(
            sustainability_score=round(score, 2),
            message=message
        )

    except Exception as e:
        print(f"Error in prediction endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "mlfastapi:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
