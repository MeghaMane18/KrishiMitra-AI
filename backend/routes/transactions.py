
from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..models import FarmTransaction

router = APIRouter()


@router.post("/transactions")
def add_transaction(
    transaction_type: str,
    category: str,
    amount: float,
    transaction_date: str,
    description: str = ""
):
    if transaction_type not in ["Income", "Expense"]:
        raise HTTPException(
            status_code=400,
            detail="Type must be Income or Expense"
        )

    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    db = SessionLocal()
    try:
        transaction = FarmTransaction(
            transaction_type=transaction_type,
            category=category,
            amount=amount,
            transaction_date=transaction_date,
            description=description
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {
            "message": "Transaction saved successfully",
            "transaction_id": transaction.id
        }
    finally:
        db.close()


@router.get("/transactions")
def get_transactions():
    db = SessionLocal()
    try:
        return (
            db.query(FarmTransaction)
            .order_by(FarmTransaction.id.desc())
            .all()
        )
    finally:
        db.close()
