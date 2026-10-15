from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..models import Farm


router = APIRouter()


@router.post("/farms")
def add_farm(
    farmer_name: str,
    farm_name: str,
    location: str,
    total_acres: float
):
    db = SessionLocal()

    new_farm = Farm(
        farmer_name=farmer_name,
        farm_name=farm_name,
        location=location,
        total_acres=total_acres
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)
    db.close()

    return {
        "message": "Farm added successfully",
        "farm_id": new_farm.id
    }


@router.get("/farms")
def get_farms():
    db = SessionLocal()

    farms = db.query(Farm).all()

    db.close()

    return farms
@router.delete("/farms/{farm_id}")
def delete_farm(farm_id: int):
    db = SessionLocal()

    try:
        farm = db.query(Farm).filter(
            Farm.id == farm_id
        ).first()

        if farm is None:
            raise HTTPException(
                status_code=404,
                detail="Farm not found"
            )

        db.delete(farm)
        db.commit()

        return {
            "message": "Farm deleted successfully",
            "farm_id": farm_id
        }

    finally:
        db.close()