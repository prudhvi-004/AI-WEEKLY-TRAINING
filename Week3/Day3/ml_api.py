from fastapi import FastAPI
from pydantic import BaseModel, Field
import pickle
import pandas as pd

app = FastAPI(title="House Price Prediction API 🚀")

# -----------------------------
# Load model
# -----------------------------
with open("house_price_model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
scaler = data["scaler"]
selector = data["selector"]
features = data["features"]


# -----------------------------
# Request Body (with aliases)
# -----------------------------
class HouseInput(BaseModel):
    number_of_bedrooms: float = Field(..., alias="number of bedrooms")
    number_of_bathrooms: float = Field(..., alias="number of bathrooms")
    living_area: float = Field(..., alias="living area")
    lot_area: float = Field(..., alias="lot area")
    number_of_floors: float = Field(..., alias="number of floors")
    number_of_views: float = Field(..., alias="number of views")
    condition_of_the_house: float = Field(..., alias="condition of the house")
    grade_of_the_house: float = Field(..., alias="grade of the house")
    area_of_the_house_excluding_basement: float = Field(..., alias="area of the house(excluding basement)")
    area_of_the_basement: float = Field(..., alias="area of the basement")
    built_year: float = Field(..., alias="built year")
    renovation_year: float = Field(..., alias="renovation year")
    postal_code: float = Field(..., alias="postal code")
    lattitude: float = Field(..., alias="lattitude")
    longitude: float = Field(..., alias="longitude")
    living_area_renov: float = Field(..., alias="living_area_renov")
    lot_area_renov: float = Field(..., alias="lot_area_renov")
    distance_from_the_airport: float = Field(..., alias="distance from the airport")

    class Config:
        populate_by_name = True


# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "API running 🚀"}


@app.post("/predict")
def predict(data: HouseInput):
    try:
        # Convert input → dict with ORIGINAL names
        input_dict = data.model_dump(by_alias=True)

        # Convert to DataFrame
        df = pd.DataFrame([input_dict])

        # Ensure correct order
        df = df[features]

        # Preprocessing
        df_selected = selector.transform(df)
        df_scaled = scaler.transform(df_selected)

        # Prediction
        prediction = model.predict(df_scaled)

        return {"prediction": int(round(prediction[0]))}

    except Exception as e:
        return {"error": str(e)}