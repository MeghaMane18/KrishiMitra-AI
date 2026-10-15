from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..models import Crop

router = APIRouter()


@router.post("/crops")
def add_crop(
    crop_name: str,
    area_acres: float,
    sowing_date: str,
    season: str,
    farm_id: int
):
    db = SessionLocal()

    new_crop = Crop(
        crop_name=crop_name,
        area_acres=area_acres,
        sowing_date=sowing_date,
        season=season,
        farm_id=farm_id
    )

    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)
    db.close()

    return {
        "message": "Crop added successfully",
        "crop_id": new_crop.id
    }


@router.get("/crops")
def get_crops():
    db = SessionLocal()

    crops = db.query(Crop).all()

    db.close()

    return crops
@router.delete("/crops/{crop_id}")
def delete_crop(crop_id: int):
    db = SessionLocal()

    try:
        crop = db.query(Crop).filter(
            Crop.id == crop_id
        ).first()

        if crop is None:
            raise HTTPException(
                status_code=404,
                detail="Crop not found"
            )

        db.delete(crop)
        db.commit()

        return {
            "message": "Crop deleted successfully",
            "crop_id": crop_id
        }

    finally:
        db.close()