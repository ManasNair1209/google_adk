import uvicorn
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="TechMart Shop API", version="1.0.0")

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics", "price": 2999, "stock": 45},
    {"id": 2, "name": "Python Crash Course", "category": "Books", "price": 599, "stock": 120},
    {"id": 3, "name": "Mechanical Keyboard", "category": "Electronics", "price": 4500, "stock": 18},
    {"id": 4, "name": "Running Shoes", "category": "Clothing", "price": 3200, "stock": 60},
    {"id": 5, "name": "USB-C Hub (7-in-1)", "category": "Electronics", "price": 1799, "stock": 33},
]

WEATHER = {
    "mumbai": {"city": "Mumbai", "temp_c": 32, "condition": "Humid & Partly Cloudy"},
    "london": {"city": "London", "temp_c": 15, "condition": "Overcast & Rainy"},
    "tokyo": {"city": "Tokyo", "temp_c": 27, "condition": "Sunny with clouds"},
}

@app.get("/products")
def list_products():
    return {"products": PRODUCTS, "total": len(PRODUCTS)}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product ID {product_id} not found.")
    return product

@app.get("/weather")
def get_weather(city: str = Query(...)):
    data = WEATHER.get(city.lower())
    if not data:
        raise HTTPException(status_code=404, detail=f"No weather data for '{city}'.")
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005, log_level="warning")



