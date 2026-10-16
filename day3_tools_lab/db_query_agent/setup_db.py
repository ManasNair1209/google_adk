import sqlite3
import os

# Write the database to the day3_tools_lab root so both db_query_agent and the
# day4 MCP server (which look one level up) resolve to the same file.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "company.db")

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS departments;

        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manager TEXT NOT NULL,
            location TEXT NOT NULL,
            budget INTEGER NOT NULL
        );

        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            salary INTEGER NOT NULL,
            hire_date TEXT NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );
    """)

    cursor.executemany("INSERT INTO departments VALUES (?, ?, ?, ?, ?)", [
        (1, "Engineering", "Ramesh Kumar", "Bangalore", 5000),
        (2, "HR", "Sunita Sharma", "Mumbai", 1500),
    ])

    cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", [
        (1, "Arjun Patel", 1, 95000, "2021-03-15", "arjun.patel@techcorp.in"),
        (2, "Pooja Singh", 2, 55000, "2022-07-01", "pooja.singh@techcorp.in"),
        (3, "Sneha Iyer", 1, 110000, "2020-01-20", "sneha.iyer@techcorp.in"),
    ])

    conn.commit()
    conn.close()
    print("Database company.db successfully initialized!")

if __name__ == "__main__":
    create_database()
