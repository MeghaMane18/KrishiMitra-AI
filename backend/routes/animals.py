from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..models import Animal

router = APIRouter()


@router.post("/animals")
def add_animal(
    animal_name: str,
    animal_type: str,
    breed: str,
    age: float,
    farm_id: int
):
    db = SessionLocal()

    new_animal = Animal(
        animal_name=animal_name,
        animal_type=animal_type,
        breed=breed,
        age=age,
        farm_id=farm_id
    )

    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    db.close()

    return {
        "message": "Animal added successfully",
        "animal_id": new_animal.id
    }


@router.get("/animals")
def get_animals():
    db = SessionLocal()

    animals = db.query(Animal).all()

    db.close()

    return animals
@router.delete("/animals/{animal_id}")
def delete_animal(animal_id: int):
    db = SessionLocal()

    try:
        animal = db.query(Animal).filter(
            Animal.id == animal_id
        ).first()

        if animal is None:
            raise HTTPException(
                status_code=404,
                detail="Animal not found"
            )

        db.delete(animal)
        db.commit()

        return {
            "message": "Animal deleted successfully",
            "animal_id": animal_id
        }

    finally:
        db.close()