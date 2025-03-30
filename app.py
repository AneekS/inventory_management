import os
import pandas as pd
from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Ensure the CSV file is stored in a persistent location
df_path = "/data/retail_store_inventory.csv"  # Change from local path

# Check if the file exists before loading
if not os.path.exists(df_path):
    raise FileNotFoundError(f"Dataset not found at {df_path}")

df = pd.read_csv(df_path)

# Convert 'Date' column to datetime format if it exists
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])

# Initialize FastAPI app
app = FastAPI()
PORT = int(os.getenv("PORT", 8000))  # Use 8000 if PORT is not set
DATABASE_URL = os.getenv("DATABASE_URL", None)  # For future database integration

# Load CSV file
df_path = "/data/retail_store_inventory.csv"
if not os.path.exists(df_path):
    raise FileNotFoundError(f"Dataset not found at {df_path}")
df = pd.read_csv(df_path)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/inventory")
def get_inventory():
    """Fetch all inventory data."""
    return df.to_dict(orient="records")

@app.get("/inventory/{product_id}")
def get_product(product_id: int):
    """Fetch details of a specific product by ID."""
    product = df[df['Product ID'] == product_id]
    if product.empty:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.to_dict(orient="records")[0]

@app.post("/predict")
def predict_demand(product_id: int, current_stock: int):
    """Dummy ML prediction endpoint for demand forecasting."""
    predicted_demand = max(0, current_stock - 10)  # Replace with actual ML logic
    return {"product_id": product_id, "predicted_demand": predicted_demand}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
