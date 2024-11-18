from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import models, schemas

router = APIRouter()

@router.post("/shipments/")
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    db_shipment = models.Shipment(**shipment.dict())
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment
