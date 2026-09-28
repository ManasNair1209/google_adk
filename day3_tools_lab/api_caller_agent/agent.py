import requests
from google.adk.agents import Agent

API_BASE = "http://localhost:8005"

def get_all_products() -> dict:
    """Fetches the complete product catalog from TechMart shop."""
    try:
        res = requests.get(f"{API_BASE}/products", timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def get_product_by_id(product_id: int) -> dict:
    """Fetches details for a single product by its integer ID.

    Args:
        product_id: Numeric product identifier (e.g. 1, 2, 5).
    """
    try:
        res = requests.get(f"{API_BASE}/products/{product_id}", timeout=5)
        if res.status_code == 404:
            return {"error": f"Product ID {product_id} not found."}
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def get_weather(city: str) -> dict:
    """Gets current weather information for a specified city.

    Args:
        city: Name of the city (e.g. "Mumbai", "London", "Tokyo").
    """
    try:
        res = requests.get(f"{API_BASE}/weather", params={"city": city}, timeout=5)
        if res.status_code == 404:
            return {"error": f"Weather data not available for '{city}'."}
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}

root_agent = Agent(
    name="APICallerAgent",
    model="gemini-3.5-flash-lite",
    instruction="Assist users with product lookup and weather queries using available tools.",
    tools=[get_all_products, get_product_by_id, get_weather],
)



