from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Customer


app = FastAPI(
    title="AI Text-to-SQL API",
    description="Backend API for the AI-powered Text-to-SQL system",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "text-to-sql-api"
    }


@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    statement = select(Customer)

    result = db.execute(statement)

    customers = result.scalars().all()

    return {
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