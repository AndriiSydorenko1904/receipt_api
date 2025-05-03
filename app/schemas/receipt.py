from __future__ import annotations

from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    price: float
    quantity: float


class ProductResponse(ProductBase):
    total: float


class PaymentInfo(BaseModel):
    type: Literal["cash", "card"]
    amount: float


class ReceiptCreate(BaseModel):
    products: List[ProductBase]
    payment: PaymentInfo


class ReceiptResponse(BaseModel):
    id: int
    products: List[ProductResponse]
    payment: PaymentInfo
    total: float
    rest: float
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ReceiptShort(BaseModel):
    id: int
    total: float
    created_at: datetime
    payment: PaymentInfo

    model_config = {
        "from_attributes": True
    }
