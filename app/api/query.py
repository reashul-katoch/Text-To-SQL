from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db
from app.core.security import get_current_user
from app.core.permissions import check_permission
from app.services.text_to_sql import generate_sql
from app.services.sql_validator import validate_sql
from app.services.clarification import check_clarification


router = APIRouter(
    prefix="/query",
    tags=["Text-to-SQL"]
)


class QueryRequest(BaseModel):
    question: str
    clarification: str | None = None
    confirm_write: bool = False


@router.post("")
def execute_query(
    request: QueryRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    # 1. Validate question
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # 2. Check clarification
    clarification = check_clarification(request.question)

    if clarification["needs_clarification"]:

        if not request.clarification:
            return {
                "status": "clarification_required",
                "question": clarification["question"]
            }

    # 3. Build final question
    final_question = request.question

    if request.clarification:
        final_question = (
            f"{request.question}. "
            f"User clarification: {request.clarification}"
        )

    # 4. Generate SQL using Gemini
    try:
        generated_sql = generate_sql(final_question)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Text-to-SQL generation failed: {error}"
        )

    # 5. Validate generated SQL
    validation = validate_sql(generated_sql)

    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Generated SQL failed validation",
                "error": validation["error"]
            }
        )

    sql = validation["sql"]
    operation = validation["operation"]

    # 6. Check RBAC permission
    check_permission(
        current_user["role"],
        operation
    )

    # 7. Require confirmation for write operations
    if operation in {"INSERT", "UPDATE", "DELETE"}:

        if not request.confirm_write:
            return {
                "status": "confirmation_required",
                "message": (
                    f"The generated query performs a "
                    f"{operation} operation. "
                    "Set confirm_write=true to execute it."
                ),
                "sql": sql,
                "operation": operation
            }

    # 8. Execute SQL
    try:

        result = db.execute(text(sql))

        # SELECT
        if operation == "SELECT":

            rows = result.mappings().all()

            return {
                "status": "success",
                "operation": operation,
                "sql": sql,
                "count": len(rows),
                "data": [dict(row) for row in rows]
            }

        # INSERT / UPDATE / DELETE
        db.commit()

        return {
            "status": "success",
            "operation": operation,
            "sql": sql,
            "rows_affected": result.rowcount
        }

    except Exception as error:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=f"Database execution failed: {error}"
        )