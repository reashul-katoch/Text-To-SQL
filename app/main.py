from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.permissions import check_permission
from app.api.query import router as query_router
from app.db import get_db
from app.models import Customer
from app.api.auth import router as auth_router
from app.core.security import get_current_user


app = FastAPI(
    title="AI Text-to-SQL API",
    description="Backend API for the AI-powered Text-to-SQL system",
    version="0.1.0"
)

app.include_router(auth_router)
app.include_router(query_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "text-to-sql-api"
    }


@app.get("/customers")
def get_customers(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    statement = select(Customer)

    result = db.execute(statement)

    customers = result.scalars().all()

    return {
        "user": current_user["username"],
        "role": current_user["role"],
        "count": len(customers),
        "customers": [
            {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "email": customer.email,
                "city": customer.city,
                "country": customer.country
            }
            for customer in customers
        ]
    }


@app.post("/admin/test-write")
def test_write_permission(
    current_user: dict = Depends(get_current_user)
):
    check_permission(
        current_user["role"],
        "INSERT"
    )

    return {
        "message": "Write operation permitted",
        "user": current_user["username"],
        "role": current_user["role"]
    }