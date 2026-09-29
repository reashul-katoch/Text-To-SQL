import sqlglot
from sqlglot import exp


ALLOWED_OPERATIONS = {
    "SELECT",
    "INSERT",
    "UPDATE",
    "DELETE"
}


def clean_sql(sql: str) -> str:
    """
    Remove markdown code fences if the LLM returns them.
    """

    sql = sql.strip()

    if sql.startswith("```"):
        lines = sql.splitlines()

        if lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        sql = "\n".join(lines).strip()

    return sql


def validate_sql(sql: str) -> dict:

    sql = clean_sql(sql)

    if not sql:
        return {
            "valid": False,
            "operation": None,
            "sql": None,
            "error": "Empty SQL query"
        }

    try:
        statements = sqlglot.parse(
            sql,
            dialect="mysql"
        )

    except Exception as error:
        return {
            "valid": False,
            "operation": None,
            "sql": sql,
            "error": f"Invalid SQL: {error}"
        }

    # Only one SQL statement is allowed
    if len(statements) != 1:
        return {
            "valid": False,
            "operation": None,
            "sql": sql,
            "error": "Multiple SQL statements are not allowed"
        }

    statement = statements[0]

    # Identify SQL operation
    if isinstance(statement, exp.Select):
        operation = "SELECT"

    elif isinstance(statement, exp.Insert):
        operation = "INSERT"

    elif isinstance(statement, exp.Update):
        operation = "UPDATE"

    elif isinstance(statement, exp.Delete):
        operation = "DELETE"

    else:
        return {
            "valid": False,
            "operation": None,
            "sql": sql,
            "error": "SQL operation is not allowed"
        }

    return {
        "valid": True,
        "operation": operation,
        "sql": sql,
        "error": None
    }