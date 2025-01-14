from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import List
from bson import ObjectId

# MongoDB Connection
client = MongoClient("mongodb://mongodb:27017/")
db = client['scrapit']
collection = db['item']

# FastAPI App
app = FastAPI()

# Helper Function to Convert BSON ObjectId
def to_dict(item):
    item["_id"] = str(item["_id"])
    return item

# Endpoints
@app.get("/", status_code=201)
def service_msg():
    return {"message": "CRUD root"}

@app.post("/boms", status_code=201)
def create_bom(bom: dict):
    """Create a new BoM."""
    if "bom_id" not in bom:
        raise HTTPException(status_code=400, detail="BoM must include 'bom_id'.")
    if collection.find_one({"bom_id": bom["bom_id"]}):
        raise HTTPException(status_code=400, detail="BoM with this ID already exists.")
    result = collection.insert_one(bom)
    return {"message": "BoM created successfully", "id": str(result.inserted_id)}

@app.get("/boms", response_model=List[dict])
def get_all_boms():
    """Get all BoMs."""
    return [to_dict(bom) for bom in collection.find()]

@app.get("/boms/{bom_id}", response_model=dict)
def get_bom(bom_id: str):
    """Get a BoM by ID."""
    bom = collection.find_one({"bom_id": bom_id})
    if not bom:
        raise HTTPException(status_code=404, detail="BoM not found.")
    return to_dict(bom)

@app.put("/boms/{bom_id}")
def update_bom(bom_id: str, updates: dict):
    """Update an existing BoM."""
    result = collection.update_one({"bom_id": bom_id}, {"$set": updates})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="BoM not found.")
    return {"message": "BoM updated successfully."}

@app.delete("/boms/{bom_id}")
def delete_bom(bom_id: str):
    """Delete a BoM by ID."""
    result = collection.delete_one({"bom_id": bom_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="BoM not found.")
    return {"message": "BoM deleted successfully."}

