from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import pickle

app = FastAPI(title="Wine Quality Prediction")

# Load model
with open("quality_model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]


# Feature order (VERY IMPORTANT)
features = [
    "fixed_acidity", "volatile_acidity", "citric_acid",
    "residual_sugar", "chlorides", "free_sulfur_dioxide",
    "total_sulfur_dioxide", "density", "pH",
    "sulphates", "alcohol"
]


# Input schema
class WineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float


@app.get("/")
def home():
    return {"message": "Wine Quality Analysis"}


@app.post("/predict")
def predict(data: WineInput):
    try:
        # Convert input → dict
        input_dict = data.model_dump()

        # Convert to DataFrame
        df = pd.DataFrame([input_dict])

        # Ensure correct column order
        df = df[features]

        # Convert to numpy
        input_data = df.values

        # Prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data).tolist()

        result = "Good Quality" if prediction == 1 else "Bad Quality"

        return {
            "prediction": result,
            "class": int(prediction),
            "probability": probability
        }

    except Exception as e:
        return {
            "error": str(e)
        }