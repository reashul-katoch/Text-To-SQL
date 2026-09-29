from google import genai
from google.genai import types

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL


def get_gemini_client():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured"
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )

DATABASE_SCHEMA = """
Database: text_to_sql_db

Table: customers
- customer_id INT PRIMARY KEY
- name VARCHAR(100)
- email VARCHAR(150)
- city VARCHAR(100)
- country VARCHAR(100)

Table: products
- product_id INT PRIMARY KEY
- product_name VARCHAR(150)
- category VARCHAR(100)
- price DECIMAL(10,2)

Table: orders
- order_id INT PRIMARY KEY
- customer_id INT FOREIGN KEY -> customers.customer_id
- product_id INT FOREIGN KEY -> products.product_id
- quantity INT
- order_date DATE
- total_amount DECIMAL(10,2)
"""


SYSTEM_PROMPT = f"""
You are a Text-to-SQL system.

Convert the user's natural language question into
a valid MySQL SQL query.

Use ONLY the tables and columns provided below.

{DATABASE_SCHEMA}

Rules:
1. Return ONLY SQL.
2. Do not use markdown.
3. Do not explain the SQL.
4. Use MySQL syntax.
5. Never invent tables or columns.
"""


def generate_sql(question: str) -> str:

    client = get_gemini_client()

    models_to_try = [
        GEMINI_MODEL,
        "gemini-3.7-flash",
        "gemini-3.6-flash",
    ]

    last_error = None

    # rest of your existing code...