from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date

from ..database import get_db
from ..models import Product, Sale

router = APIRouter(
    prefix="/shop",
    tags=["Shop Management"]
)


class SaleCreate(BaseModel):
    product_name: str
    quantity: float
    total_amount: float
    customer_name: str
    sale_date: str
    amount_paid: float = 0


@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/sales")
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).order_by(Sale.id.desc()).all()


@router.post("/sales")
def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db)
):
    if sale_data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    if sale_data.total_amount < 0 or sale_data.amount_paid < 0:
        raise HTTPException(
            status_code=400,
            detail="Amounts cannot be negative"
        )

    if sale_data.amount_paid > sale_data.total_amount:
        raise HTTPException(
            status_code=400,
            detail="Amount paid cannot exceed total amount"
        )

    remaining = sale_data.total_amount - sale_data.amount_paid

    new_sale = Sale(
        product_name=sale_data.product_name,
        quantity=sale_data.quantity,
        total_amount=sale_data.total_amount,
        customer_name=sale_data.customer_name,
        sale_date=sale_data.sale_date,
        amount_paid=sale_data.amount_paid,
        remaining_balance=remaining
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale

@router.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()

    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    db.delete(sale)
    db.commit()

    return {"message": "Sale deleted successfully"}
