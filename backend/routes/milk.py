from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..models import MilkRecord

router = APIRouter()


@router.post("/milk")
def add_milk_record(
    animal_id: int,
    milk_date: str,
    morning_milk: float,
    evening_milk: float
):
    db = SessionLocal()

    total_milk = morning_milk + evening_milk

    new_record = MilkRecord(
        animal_id=animal_id,
        milk_date=milk_date,
        morning_milk=morning_milk,
        evening_milk=evening_milk,
        total_milk=total_milk
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()

    return {
        "message": "Milk record added successfully",
        "milk_id": new_record.id,
        "total_milk": total_milk
    }


@router.get("/milk")
def get_milk_records():
    db = SessionLocal()

    records = db.query(MilkRecord).all()

    db.close()

    return records

@router.delete("/milk/{milk_id}")
def delete_milk_record(milk_id: int):
    db = SessionLocal()

    try:
        record = db.query(MilkRecord).filter(
            MilkRecord.id == milk_id
        ).first()

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Milk record not found"
            )

        db.delete(record)
        db.commit()

        return {
            "message": "Milk record deleted successfully",
            "milk_id": milk_id
        }

    finally:
        db.close()