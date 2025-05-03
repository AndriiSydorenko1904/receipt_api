from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_
from datetime import datetime
from typing import List, Optional

from app.core.security import get_current_user
from app.core.database import get_db
from app.models import User, Receipt, ReceiptProduct
from app.schemas import (
    ReceiptCreate,
    ReceiptResponse,
    ReceiptShort,
    ProductResponse,
)

router = APIRouter()


@router.post("/", response_model=ReceiptResponse)
async def create_receipt(
    data: ReceiptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total = sum(p.price * p.quantity for p in data.products)
    rest = data.payment.amount - total

    receipt = Receipt(
        user_id=current_user.id,
        payment_type=data.payment.type,
        payment_amount=data.payment.amount,
        total=total,
        rest=rest,
    )

    db.add(receipt)
    await db.flush()

    products = []
    for p in data.products:
        product = ReceiptProduct(
            receipt_id=receipt.id,
            name=p.name,
            price=p.price,
            quantity=p.quantity,
            total_price=p.price * p.quantity,
        )
        db.add(product)
        products.append(product)

    await db.commit()
    await db.refresh(receipt)

    return ReceiptResponse(
        id=receipt.id,
        products=[
            ProductResponse(
                name=prod.name,
                price=float(prod.price),
                quantity=float(prod.quantity),
                total=float(prod.total_price),
            )
            for prod in products
        ],
        payment=data.payment,
        total=total,
        rest=rest,
        created_at=receipt.created_at,
    )


@router.get("/", response_model=List[ReceiptShort])
async def list_receipts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    min_total: Optional[float] = Query(None, ge=0),
    payment_type: Optional[str] = Query(None),
    created_after: Optional[datetime] = Query(None),
    created_before: Optional[datetime] = Query(None),
    skip: int = 0,
    limit: int = 10,
):
    filters = [Receipt.user_id == current_user.id]
    if min_total is not None:
        filters.append(Receipt.total >= min_total)
    if payment_type:
        filters.append(Receipt.payment_type == payment_type)
    if created_after:
        filters.append(Receipt.created_at >= created_after)
    if created_before:
        filters.append(Receipt.created_at <= created_before)

    result = await db.execute(
        select(Receipt)
        .where(and_(*filters))
        .order_by(Receipt.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    receipts = result.scalars().all()

    return [
        ReceiptShort(
            id=r.id,
            total=float(r.total),
            created_at=r.created_at,
            payment={
                "type": r.payment_type.value,
                "amount": float(r.payment_amount),
            },
        )
        for r in receipts
    ]


@router.get("/{receipt_id}", response_model=ReceiptResponse)
async def get_receipt(
    receipt_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Receipt)
        .options(selectinload(Receipt.products))
        .where(Receipt.id == receipt_id, Receipt.user_id == current_user.id)
    )
    receipt = result.scalar_one_or_none()
    if not receipt:
        raise HTTPException(status_code=404, detail="Check not found")

    return ReceiptResponse(
        id=receipt.id,
        products=[
            ProductResponse(
                name=p.name,
                price=float(p.price),
                quantity=float(p.quantity),
                total=float(p.total_price),
            )
            for p in receipt.products
        ],
        payment={
            "type": receipt.payment_type.value,
            "amount": float(receipt.payment_amount),
        },
        total=float(receipt.total),
        rest=float(receipt.rest),
        created_at=receipt.created_at,
    )
