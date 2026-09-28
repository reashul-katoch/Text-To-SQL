from app.services.clarification import check_clarification


def test_best_customers_requires_clarification():

    result = check_clarification(
        "Show me the best customers"
    )

    assert result["needs_clarification"] is True


def test_recent_orders_requires_clarification():

    result = check_clarification(
        "Show me recent orders"
    )

    assert result["needs_clarification"] is True


def test_sales_requires_clarification():

    result = check_clarification(
        "Give me sales"
    )

    assert result["needs_clarification"] is True


def test_clear_question_does_not_require_clarification():

    result = check_clarification(
        "Show me all customers from Chandigarh"
    )

    assert result["needs_clarification"] is False