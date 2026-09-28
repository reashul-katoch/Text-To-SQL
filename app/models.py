from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Customer(Base):
    orders: Mapped[list["Order"]] = relationship(
    back_populates="customer"
)
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    city: Mapped[str | None] = mapped_column(
        String(100)
    )

    country: Mapped[str | None] = mapped_column(
        String(100)
    )
class Product(Base):
    
    __tablename__ = "products"
    orders: Mapped[list["Order"]] = relationship(
    back_populates="product"
)

    product_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    category: Mapped[str | None] = mapped_column(
        String(100)
    )

    price: Mapped[float] = mapped_column(
        nullable=False
    )
from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric


class Order(Base):
    __tablename__ = "orders"
    customer: Mapped["Customer"] = relationship(
        back_populates="orders")

    product: Mapped["Product"] = relationship(
        back_populates="orders")

    order_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.product_id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    order_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    total_amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )