from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data import houses

app = FastAPI()

# Allow frontend (static pages) to call backend APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
