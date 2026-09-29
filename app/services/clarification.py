import re


def check_clarification(question: str) -> dict:

    question_lower = question.lower().strip()

    # Ambiguous "best" questions
    if "best customer" in question_lower or "best customers" in question_lower:

        return {
            "needs_clarification": True,
            "question": (
                "What do you mean by 'best customers'?"
                " You can choose highest total spending or most orders."
            )
        }

    # Ambiguous "recent" questions
    if "recent order" in question_lower or "recent orders" in question_lower:

        return {
            "needs_clarification": True,
            "question": (
                "What time period should I consider as recent?"
                " For example, the last 7 days or last 30 days."
            )
        }

    # Ambiguous sales questions
    if "sales" in question_lower and not any(
        word in question_lower
        for word in ["revenue", "orders", "quantity", "amount"]
    ):

        return {
            "needs_clarification": True,
            "question": (
                "What do you want to measure by sales?"
                " Revenue, number of orders, or quantity sold?"
            )
        }

    return {
        "needs_clarification": False,
        "question": None
    }