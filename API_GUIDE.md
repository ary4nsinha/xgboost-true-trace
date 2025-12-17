# Sustainability Score API - Quick Guide

## Quick Start

```bash
pip install -r requirements.txt
python mlfastapi.py
```

Server: `http://127.0.0.1:8000`

## Main Endpoint

**POST** `/predict` - Predicts sustainability score (0-100)

### Request
```json
{
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
```

### Response
```json
{
  "sustainability_score": 36.31,
  "message": "Low sustainability score - consider improvements"
}
```

## Other Endpoints

- **GET** `/` - API info
- **GET** `/health` - Health check
- **GET** `/docs` - Interactive docs (Swagger UI)

## Testing

```bash
python test_api.py
```

Or visit: `http://127.0.0.1:8000/docs`

## Fields (All 24 Required)

**Numeric (7):** Recycled Content %, Virgin Content %, Carbon Footprint, Water Consumption, Power Consumption, Packaging Recycled Content %, Expected Lifespan

**Categorical (17):** Base Material, Contains Plastic, Biodegradable, Compostable, Recyclability Level, Reusability, Repairability, End-of-Life, Coating Type, Mixed Materials, Toxicity Concerns, Packaging Material, Packaging Recyclable, Food Safe, Chemical Leaching Risk, SVHC Presence, Plasticizer Type

## Score Ranges

- 80-100: Excellent
- 60-79: Good
- 40-59: Moderate
- 0-39: Low
