import sqlglot
from sqlglot import exp


ALLOWED_TABLES = {
    "customers",
    "products",
    "orders",
}


ALLOWED_COLUMNS = {
    "customers": {
        "customer_id",
        "name",
        "email",
        "city",
        "country",
    },
    "products": {
        "product_id",
        "product_name",
        "category",
        "price",
    },
    "orders": {
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "order_date",
        "total_amount",
    },
}


def clean_sql(sql: str) -> str:
    if not sql:
        return ""

    sql = sql.strip()
    if sql.startswith("```"):
        lines = sql.splitlines()

        if lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        sql = "\n".join(lines).strip()

    return sql


def get_operation(statement):
    if isinstance(statement, exp.Select):
        return "SELECT"

    if isinstance(statement, exp.Insert):
        return "INSERT"

    if isinstance(statement, exp.Update):
        return "UPDATE"

    if isinstance(statement, exp.Delete):
        return "DELETE"

    return None


def validate_tables(statement):
    tables = statement.find_all(exp.Table)

    for table in tables:

        table_name = table.name.lower()

        if table_name not in ALLOWED_TABLES:
            return False, (
                f"Table '{table_name}' is not allowed"
            )

    return True, None


def validate_columns(statement):
    tables = statement.find_all(exp.Table)

    table_names = {
        table.name.lower()
        for table in tables
    }

    for column in statement.find_all(exp.Column):

        column_name = column.name.lower()

        # If the column is qualified, use its table.
        if column.table:

            table_name = column.table.lower()

            if table_name not in ALLOWED_COLUMNS:
                return False, (
                    f"Table '{table_name}' is not allowed"
                )

            if column_name not in ALLOWED_COLUMNS[table_name]:
                return False, (
                    f"Column '{column_name}' "
                    f"is not allowed for table "
                    f"'{table_name}'"
                )

        else:

            # Check whether the unqualified column
            # exists in at least one referenced table.
            valid = any(
                column_name in ALLOWED_COLUMNS[table_name]
                for table_name in table_names
            )

            if not valid:
                return False, (
                    f"Column '{column_name}' "
                    "is not allowed"
                )

    return True, None
def apply_select_limit(sql: str, limit: int = 100) -> str:
    statement = sqlglot.parse_one(
        sql,
        dialect="mysql"
    )

    if not isinstance(statement, exp.Select):
        return sql

    if statement.args.get("limit"):
        return sql

    statement = statement.limit(limit)

    return statement.sql(dialect="mysql")


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

    if len(statements) != 1:

        return {
            "valid": False,
            "operation": None,
            "sql": sql,
            "error": (
                "Multiple SQL statements are not allowed"
            )
        }

    statement = statements[0]

    operation = get_operation(statement)

    if not operation:

        return {
            "valid": False,
            "operation": None,
            "sql": sql,
            "error": "SQL operation is not allowed"
        }

    tables_valid, table_error = validate_tables(statement)

    if not tables_valid:

        return {
            "valid": False,
            "operation": operation,
            "sql": sql,
            "error": table_error
        }

    columns_valid, column_error = validate_columns(statement)

    if not columns_valid:

        return {
            "valid": False,
            "operation": operation,
            "sql": sql,
            "error": column_error
        }

    return {
        "valid": True,
        "operation": operation,
        "sql": sql,
        "error": None
    }