from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import enum
from app.core.database import Base


class PaymentType(enum.Enum):
    cash = "cash"
    card = "card"


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    user_id = Column(Integer, ForeignKey("users.id"))
    payment_type = Column(Enum(PaymentType))
    payment_amount = Column(Numeric(12, 2))
    total = Column(Numeric(12, 2))
    rest = Column(Numeric(12, 2))

    user = relationship("User", back_populates="receipts")
    products = relationship("ReceiptProduct", back_populates="receipt", cascade="all, delete")


class ReceiptProduct(Base):
    __tablename__ = "receipt_products"

    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)

    receipt = relationship("Receipt", back_populates="products")
