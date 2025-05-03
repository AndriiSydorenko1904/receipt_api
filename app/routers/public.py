from fastapi import Depends, HTTPException, Query, Response, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import Receipt
from app.schemas import ReceiptResponse, ProductResponse

from app.core.settings import get_settings

settings = get_settings()

router = APIRouter()


@router.get("/{receipt_id}")
async def get_receipt_public(
    receipt_id: int,
    format: str = Query(default="text", pattern="^(text|json)$"),
    line_width: int = Query(default=32, ge=20, le=80),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Receipt)
        .options(selectinload(Receipt.products))
        .where(Receipt.id == receipt_id)
    )
    receipt = result.scalar_one_or_none()

    if not receipt:
        raise HTTPException(status_code=404, detail="Check not found")

    if format == "json":
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

    # --- ASCII TEXT FORMAT ---
    lines = []
    append = lines.append

    def center(text: str) -> str:
        return text.center(line_width)

    def sep(char="="):
        return char * line_width

    append(center(settings.RECEIPT_HEADER_NAME))
    append(sep("="))

    for p in receipt.products:
        qty_price = f"{float(p.quantity):.2f} x {float(p.price):.2f}"
        append(qty_price)
        append(p.name[:line_width])
        append(f"{float(p.total_price):,.2f}".rjust(line_width))

    append(sep("-"))
    append(f"СУМА {float(receipt.total):,.2f}".rjust(line_width))
    append(f"{receipt.payment_type.value.title()} {float(receipt.payment_amount):,.2f}".rjust(line_width))
    append(f"Решта {float(receipt.rest):,.2f}".rjust(line_width))
    append(sep("="))
    append(receipt.created_at.strftime("%d.%m.%Y %H:%M").center(line_width))
    append(center("Дякуємо за покупку!"))

    return Response(content="\n".join(lines), media_type="text/plain")
