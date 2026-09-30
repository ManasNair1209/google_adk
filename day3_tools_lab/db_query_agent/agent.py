# =============================================================================
# AGENT 3 — Database Query Tool
# =============================================================================
# KEY CONCEPT: Tools are not limited to HTTP calls — they can do ANYTHING
# a Python function can do: query databases, read files, call SDKs, etc.
#
# This agent uses sqlite3 (Python built-in) to query a local company database.
# Run setup_db.py once to create the database before using this agent.
#
# Database schema:
#   employees   (id, name, department_id, salary, hire_date, email)
#   departments (id, name, manager, location, budget)
# =============================================================================

import sqlite3
import os
from google.adk.agents import Agent

# ── Path to the database ─────────────────────────────────────────────────────
# __file__ is this agent.py file; we go one folder up (..) to reach tools lab root
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "company.db")


def _connect():
    """Helper: opens a read-only SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn


# ── Tool 1: List all departments ─────────────────────────────────────────────
def list_departments() -> dict:
    """Returns all departments in the company with their manager and location.

    Use this when the user asks about company structure, departments, or locations.
    """
    try:
        with _connect() as conn:
            rows = conn.execute(
                "SELECT id, name, manager, location, budget FROM departments"
            ).fetchall()
        return {"departments": [dict(r) for r in rows]}
    except Exception as e:
        return {"error": str(e), "tip": "Did you run setup_db.py first?"}


# ── Tool 2: List all employees ───────────────────────────────────────────────
def list_all_employees() -> dict:
    """Returns all employees with their name, department, salary, and hire date.

    Use this when the user wants to see the full employee list.
    """
    try:
        with _connect() as conn:
            rows = conn.execute("""
                SELECT e.id, e.name, d.name AS department, e.salary,
                       e.hire_date, e.email
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                ORDER BY e.name
            """).fetchall()
        return {"employees": [dict(r) for r in rows], "total": len(rows)}
    except Exception as e:
        return {"error": str(e), "tip": "Did you run setup_db.py first?"}


# ── Tool 3: Find employee by name ────────────────────────────────────────────
def find_employee_by_name(name: str) -> dict:
    """Searches for an employee by name (partial match, case-insensitive).

    Args:
        name: Full or partial name to search for (e.g. "Alice", "ali", "singh").

    Returns matching employees with their department, salary, and contact info.
    """
    try:
        with _connect() as conn:
            rows = conn.execute("""
                SELECT e.id, e.name, d.name AS department, e.salary,
                       e.hire_date, e.email
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                WHERE LOWER(e.name) LIKE LOWER(?)
            """, (f"%{name}%",)).fetchall()
        if not rows:
            return {"message": f"No employee found matching '{name}'."}
        return {"employees": [dict(r) for r in rows]}
    except Exception as e:
        return {"error": str(e)}


# ── Tool 4: Get department summary ───────────────────────────────────────────
def get_department_summary(department_name: str) -> dict:
    """Returns summary statistics for a given department.

    Args:
        department_name: Name of the department (e.g. "Engineering", "HR", "Sales").

    Returns: employee count, average salary, highest/lowest salary, and the manager.
    Use this when the user asks about a specific department's headcount or pay.
    """
    try:
        with _connect() as conn:
            dept = conn.execute(
                "SELECT id, manager, location, budget FROM departments WHERE LOWER(name)=LOWER(?)",
                (department_name,)
            ).fetchone()
            if not dept:
                return {"error": f"Department '{department_name}' not found."}

            stats = conn.execute("""
                SELECT COUNT(*) AS headcount,
                       ROUND(AVG(salary), 2) AS avg_salary,
                       MAX(salary) AS max_salary,
                       MIN(salary) AS min_salary
                FROM employees WHERE department_id = ?
            """, (dept["id"],)).fetchone()

        return {
            "department": department_name,
            "manager": dept["manager"],
            "location": dept["location"],
            "budget": dept["budget"],
            **dict(stats),
        }
    except Exception as e:
        return {"error": str(e)}


# ── Tool 5: Top earners ──────────────────────────────────────────────────────
def get_top_earners(limit: int = 5) -> dict:
    """Returns the top earning employees in the company.

    Args:
        limit: How many top earners to return (default is 5, max 20).

    Use this when the user asks who earns the most or wants a salary leaderboard.
    """
    limit = min(max(1, limit), 20)   # clamp between 1 and 20
    try:
        with _connect() as conn:
            rows = conn.execute("""
                SELECT e.name, d.name AS department, e.salary
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                ORDER BY e.salary DESC
                LIMIT ?
            """, (limit,)).fetchall()
        return {"top_earners": [dict(r) for r in rows]}
    except Exception as e:
        return {"error": str(e)}


# ── The Agent ────────────────────────────────────────────────────────────────
root_agent = Agent(
    name="DBQueryAgent",
    model="gemini-3.5-flash-lite",
    instruction="""You are an HR assistant with access to the company employee database.

You have five database query tools:
- list_departments: See all departments, managers, and locations
- list_all_employees: Full employee roster with salaries and join dates
- find_employee_by_name: Search for a specific employee by name
- get_department_summary: Headcount, average salary, and manager for one department
- get_top_earners: Salary leaderboard (specify how many to show)

Answer HR questions clearly. Format salary figures with currency (₹).
If you get a "did you run setup_db.py" error, tell the user to run:
  python setup_db.py
from the day2_tools_lab folder.""",
    tools=[
        list_departments,
        list_all_employees,
        find_employee_by_name,
        get_department_summary,
        get_top_earners,
    ],
)

# =============================================================================
# HOW TO TEST:
#   STEP 1 — Create the database (only once):
#     python setup_db.py
#
#   STEP 2 — Run the agent (from day2_tools_lab/):
#     adk web
#     → pick "db_query_agent"
#
# Try these prompts:
#   1. "List all departments"
#   2. "Who works in Engineering?"         → find_employee_by_name or list_all
#   3. "Tell me about the Sales department"
#   4. "Who are the top 3 earners?"
#   5. "Find an employee named Priya"
# =============================================================================
