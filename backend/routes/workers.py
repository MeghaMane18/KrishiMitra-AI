from fastapi import APIRouter, HTTPException
from ..database import SessionLocal
from ..models import Worker

router = APIRouter()


@router.post("/workers")
def add_worker(
    worker_name: str,
    phone: str,
    work_type: str,
    work_date: str,
    days_worked: float,
    rate_per_day: float,
    payment_status: str,
    advance_payment: float = 0
):
    db = SessionLocal()

    total_payment = days_worked * rate_per_day
    remaining_payment = total_payment - advance_payment

    new_worker = Worker(
        worker_name=worker_name,
        phone=phone,
        work_type=work_type,
        work_date=work_date,
        days_worked=days_worked,
        rate_per_day=rate_per_day,
        total_payment=total_payment,
        payment_status=payment_status,
        advance_payment=advance_payment,
        remaining_payment=remaining_payment
    )

    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    db.close()

    return {
        "message": "Worker added successfully",
        "worker_id": new_worker.id,
        "total_payment": total_payment,
        "advance_payment": advance_payment,
        "remaining_payment": remaining_payment
    }


@router.get("/workers")
def get_workers():
    db = SessionLocal()

    workers = db.query(Worker).all()

    db.close()

    return workers
@router.delete("/workers/{worker_id}")
def delete_worker(worker_id: int):
    db = SessionLocal()

    try:
        worker = db.query(Worker).filter(
            Worker.id == worker_id
        ).first()

        if worker is None:
            raise HTTPException(
                status_code=404,
                detail="Worker not found"
            )

        db.delete(worker)
        db.commit()

        return {
            "message": "Worker deleted successfully",
            "worker_id": worker_id
        }

    finally:
        db.close()