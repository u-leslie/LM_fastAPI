from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import models, schemas

router = APIRouter()

@router.post("/deliveries/")
def create_delivery(delivery: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    db_delivery = models.Delivery(**delivery.dict())
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery
