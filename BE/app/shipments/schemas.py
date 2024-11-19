from pydantic import BaseModel
from typing import Optional

class Driver(BaseModel):
    id: int
    name: str
    phone_number: str
    vehicle_number: str

    class Config:
        orm_mode = True

class ShipmentBase(BaseModel):
    origin: str
    destination: str
    status: Optional[str] = "pending"
    driver_id: int

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(BaseModel):
    origin: Optional[str]
    destination: Optional[str]
    status: Optional[str]
    driver_id: Optional[int]

class Shipment(ShipmentBase):
    id: int
    driver: Optional[Driver] 

    class Config:
        orm_mode = True
