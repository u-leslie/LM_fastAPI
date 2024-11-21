from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import decode_access_token
from . import models, schemas

security = HTTPBearer()

router = APIRouter()

@router.post("/drivers/", response_model=schemas.Driver)
def create_driver(
    driver: schemas.DriverCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    if db.query(models.Driver).filter(models.Driver.vehicle_number == driver.vehicle_number).first():
        raise HTTPException(status_code=400, detail="Vehicle number already exists")
    
    if db.query(models.Driver).filter(models.Driver.phone_number == driver.phone_number).first():
        raise HTTPException(status_code=400, detail="Phone number already exists")

    db_driver = models.Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


@router.get("/drivers/", response_model=list[schemas.Driver])
def get_all_drivers(
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    drivers = db.query(models.Driver).all()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    return drivers


@router.get("/drivers/{driver_id}", response_model=schemas.Driver)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.put("/drivers/{driver_id}", response_model=schemas.Driver)
def update_driver(
    driver_id: int,
    updated_driver: schemas.DriverUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    db_driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    # Update driver fields with provided data
    for key, value in updated_driver.dict(exclude_unset=True).items():
        setattr(db_driver, key, value)
    
    db.commit()
    db.refresh(db_driver)
    return db_driver


@router.delete("/drivers/{driver_id}", response_model=schemas.Driver)
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token),  
):
    db_driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    db.delete(db_driver)
    db.commit()
    return db_driver  