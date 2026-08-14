from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from data import houses
import requests
import os

# Load trained model
MODEL_FILENAME = os.getenv("MODEL_FILENAME", "house_price_model.joblib")

app = FastAPI()

# Allow frontend (static pages) to call backend APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_API_BASE_URL = os.getenv("MODEL_API_BASE_URL", "http://localhost:8000")

@app.get("/")
def read_root():
    return {"message": "Backend is running"}

@app.get("/api/houses")
def get_houses():
    return {"houses": houses}

@app.get("/api/houses/{house_id}")
def get_house(house_id: int):
    for house in houses:
        if house["id"] == house_id:
            return house
    return {"error": "House not found"}

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()

    # Forward request to ML model service
    response = requests.post(MODEL_API_BASE_URL+"/predict", json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get prediction from ML service"}
