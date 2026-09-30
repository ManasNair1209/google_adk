import os
import sqlite3
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Day4-Enterprise-MCP-Server")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "day3", "day3_tools_lab", "company.db")
API_BASE = "http://localhost:8005"
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

@mcp.tool()
def get_weather(city: str) -> dict:
    """Gets real-time weather data for a given city using OpenWeatherMap API."""
    if OPENWEATHER_API_KEY:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
            res = requests.get(url, params=params, timeout=5)
            if res.status_code == 200:
                data = res.json()
                return {
                    "source": "OpenWeatherMap API",
                    "city": data["name"],
                    "temp_celsius": data["main"]["temp"],
                    "condition": data["weather"][0]["description"].title(),
                    "humidity_percent": data["main"]["humidity"],
                }
        except Exception as e:
            return {"error": str(e)}
    return {"source": "Simulation Mode (Set OPENWEATHER_API_KEY)", "city": city, "temp_celsius": 28.5, "condition": "Partly Cloudy"}

@mcp.tool()
def get_all_products() -> dict:
    """Fetches complete product catalog from TechMart store API."""
    try:
        res = requests.get(f"{API_BASE}/products", timeout=5)
        res.raise_for_status()
        return {"products": res.json()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def find_employee_by_name(name: str) -> dict:
    """Searches company employees by name in SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT e.id, e.name, d.name AS department, e.salary, e.email FROM employees e JOIN departments d ON e.department_id = d.id WHERE LOWER(e.name) LIKE LOWER(?)", (f"%{name}%",))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return {"matches": rows}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_department_summary(department_name: str) -> dict:
    """Returns department summary analytics (headcount, manager, budget, salaries)."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        dept = cursor.execute("SELECT id, manager, location, budget FROM departments WHERE LOWER(name)=LOWER(?)", (department_name,)).fetchone()
        if not dept:
            return {"error": f"Department '{department_name}' not found."}
        stats = cursor.execute("SELECT COUNT(*) AS headcount, ROUND(AVG(salary), 2) AS avg_salary, MAX(salary) AS max_salary, MIN(salary) AS min_salary FROM employees WHERE department_id = ?", (dept["id"],)).fetchone()
        conn.close()
        return {"department": department_name, "manager": dept["manager"], "budget": dept["budget"], **dict(stats)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
