from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import models, schemas

router = APIRouter()

@router.post("/drivers/")
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    db_driver = models.Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver
