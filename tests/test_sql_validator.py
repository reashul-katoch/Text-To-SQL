from app.services.sql_validator import validate_sql


def test_valid_select():

    result = validate_sql(
        "SELECT * FROM customers"
    )

    assert result["valid"] is True
    assert result["operation"] == "SELECT"


def test_valid_update():

    result = validate_sql(
        "UPDATE customers SET city = 'Delhi' "
        "WHERE customer_id = 1"
    )

    assert result["valid"] is True
    assert result["operation"] == "UPDATE"


def test_valid_delete():

    result = validate_sql(
        "DELETE FROM customers WHERE customer_id = 1"
    )

    assert result["valid"] is True
    assert result["operation"] == "DELETE"


def test_drop_is_rejected():

    result = validate_sql(
        "DROP TABLE customers"
    )

    assert result["valid"] is False


def test_multiple_statements_are_rejected():

    result = validate_sql(
        "SELECT * FROM customers; "
        "SELECT * FROM products"
    )

    assert result["valid"] is False