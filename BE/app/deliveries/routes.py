from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.auth import decode_access_token  # Import the token decoder
from . import models, schemas

security = HTTPBearer()

router = APIRouter()

@router.post("/deliveries/", response_model=schemas.Delivery)
def create_delivery(
    delivery: schemas.DeliveryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    db_delivery = models.Delivery(**delivery.dict())
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@router.get("/deliveries/{delivery_id}", response_model=schemas.Delivery)
def get_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    db_delivery = (
        db.query(models.Delivery)
        .options(joinedload(models.Delivery.shipment), joinedload(models.Delivery.driver))
        .filter(models.Delivery.id == delivery_id)
        .first()
    )
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return db_delivery

@router.get("/deliveries/", response_model=list[schemas.Delivery])
def list_deliveries(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    deliveries = (
        db.query(models.Delivery)
        .options(joinedload(models.Delivery.shipment), joinedload(models.Delivery.driver))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return deliveries

@router.put("/deliveries/{delivery_id}", response_model=schemas.Delivery)
def update_delivery(
    delivery_id: int,
    delivery_update: schemas.DeliveryBase,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    db_delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    for key, value in delivery_update.dict(exclude_unset=True).items():
        setattr(db_delivery, key, value)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@router.delete("/deliveries/{delivery_id}")
def delete_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    db_delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    db.delete(db_delivery)
    db.commit()
    return {"message": "Delivery deleted successfully"}
