from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from app.core.database import get_db
from . import models, schemas

router = APIRouter()

# Create a shipment
@router.post("/shipments/", response_model=schemas.Shipment)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    db_shipment = models.Shipment(**shipment.dict())
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

# Read all shipments
@router.get("/shipments/", response_model=list[schemas.Shipment])
def get_all_shipments(db: Session = Depends(get_db)):
    return db.query(models.Shipment).options(joinedload(models.Shipment.driver)).all()

# Read a shipment by ID
@router.get("/shipments/{shipment_id}", response_model=schemas.Shipment)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


# Update a shipment
@router.put("/shipments/{shipment_id}", response_model=schemas.Shipment)
def update_shipment(shipment_id: int, shipment_update: schemas.ShipmentUpdate, db: Session = Depends(get_db)):
    shipment = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    for key, value in shipment_update.dict(exclude_unset=True).items():
        setattr(shipment, key, value)
    
    db.commit()
    db.refresh(shipment)
    return shipment

# Delete a shipment
@router.delete("/shipments/{shipment_id}")
def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    db.delete(shipment)
    db.commit()
    return {"detail": "Shipment deleted successfully"}
